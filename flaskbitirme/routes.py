from flask import render_template, request, jsonify, url_for, redirect
from flaskbitirme import app, db, bcrypt
import pandas as pd
from flaskbitirme.models import *
from flask_login import login_user, current_user, logout_user, login_required

df = pd.DataFrame()  # Initialize an empty DataFrame
all_sheets = {}


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def home():
    print("home func:", current_user.name)

    global df
    global all_sheets

    # Request method is POST
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('home.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('home.html', message='No selected file')

        all_sheets = pd.read_excel(file, sheet_name=None)
        # Access and print each sheet separately
        '''for sheet_name, sheet_df in all_sheets.items():
            print(f"Sheet name: {sheet_name}")
            print(sheet_df)'''

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file)

        # Extract table names from the first row
        table_names = df.columns.tolist()

        # Count the number of records (rows), excluding the first row
        num_records = len(df)

        excel_data_json = df.to_json(orient='records')

        return render_template('home.html', table_names=table_names, num_records=num_records, excel=excel_data_json)

    # Request method is GET
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(current_user.email)
        return redirect(url_for('course_list'))

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        # Check if the user is an Admin
        admin = Admin.query.filter_by(email=email).first()
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('course_list'))  # Redirect to admin dashboard

        # Check if the user is an Instructor
        instructor = Instructor.query.filter_by(email=email).first()
        if instructor and bcrypt.check_password_hash(instructor.password, password):
            login_user(instructor)
            return redirect(url_for('course_list'))  # Redirect to instructor dashboard

        # Check if the user is a Coordinator
        coordinator = Coordinator.query.filter_by(email=email).first()
        if coordinator and bcrypt.check_password_hash(coordinator.password, password):
            login_user(coordinator)
            return redirect(url_for('course_list'))  # Redirect to coordinator dashboard

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/coordinator_panel', methods=['GET', 'POST'])
@login_required
def coordinator_panel():
    if current_user.userType != 'Coordinator':
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        instructor_id = request.form.get('instructor')
        courseInstanceData = request.form.get('course_instance')
        courseInstanceDataList = courseInstanceData.split('-')
        course_code = courseInstanceDataList[0]
        year = courseInstanceDataList[1]
        semester = courseInstanceDataList[2]

        # Fetch the selected instructor and course instance from the database
        instructor = Instructor.query.get(instructor_id)
        course_instance = CourseInstance.query.filter_by(course_code=course_code, year=year, semester=semester).first()

        if instructor and course_instance:
            # Update the course instance with the selected instructor
            course_instance.instructor_id = instructor.id
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('coordinator_panel'))
    else:
        # Fetch all instructors
        instructors = Instructor.query.all()

        # Fetch all unassigned course instances
        unassigned_course_instances = CourseInstance.query.filter_by(instructor_id=None).all()
        available_courses = Course.query.filter_by(department_code=current_user.department_code).all()
        print(available_courses)
        return render_template('coordinator.html', instructors=instructors, courses=available_courses, unassigned_course_instances=unassigned_course_instances)
    

@app.route('/addcourseinstance', methods=['GET', 'POST'])
@login_required
def addcourseinstance():
    if current_user.userType != 'Coordinator':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Handle form submission
        course_code = request.form['course_code']
        year = request.form['year']
        semester = request.form['semester']

        # Check if a CourseInstance with the same composite key already exists
        existing_instance = CourseInstance.query.filter_by(course_code=course_code, year=year, semester=semester).first()
        if existing_instance:
            available_courses = Course.query.all()
            error = 'Instance exists.'
            return render_template('coordinator.html', courses=available_courses, error=error)

        normalized_score = 0
        normalized_std = 0
        std_dev = 0
        average = 0
        overall_weight = 0
        out_of = 0
        instructor_id = None # Null value for now

        # Create CourseInstance object and add it to the database
        course_instance = CourseInstance(course_code=course_code, year=year, semester=semester, 
                                         normalizedScore=normalized_score, normalizedSTD=normalized_std,
                                         stdDev=std_dev, average=average, overallWeight=overall_weight,
                                         outOf=out_of, instructor_id=instructor_id)
        db.session.add(course_instance)
        db.session.commit()

        # Fetch available courses from the database
        available_courses = Course.query.all()
        return redirect(url_for('course_list'))  
    else:
        # Fetch available courses from the database
        available_courses = Course.query.all()
        return render_template('coordinator.html', courses=available_courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match."
            return render_template('register.html', error=error)
        
        existing_admin = Admin.query.filter_by(email=email).first()
        existing_instructor = Instructor.query.filter_by(email=email).first()
        existing_coordinator = Coordinator.query.filter_by(email=email).first()

        # Check if username is already taken based on the email
        if existing_admin or existing_coordinator or existing_instructor: 
            error = f"User with {email} already exists. Please choose a different username."
            return render_template('register.html', error=error)

        # Encrypt the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create the instructor 
        new_user = Instructor(name=name, surname=surname, email=email, password=hashed_password)
        
        # Add it to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    # If the request method is GET, simply render the signup page
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    # Render the dashboard.html template
    return render_template('dashboard.html')


@app.route('/course')
@login_required
def course_list():
    # Render the dashboard.html template
    return render_template('courses.html')


@app.route('/process')
@login_required
def process():
    global all_sheets

    if 'secondpage' in all_sheets:
        try:
            # Assuming 'secondpage' is the sheet in your DataFrame
            second_page_df = all_sheets['secondpage']

            # Drop rows with NaN values in the 'score' column
            second_page_df = second_page_df.dropna(subset=['score'])

            # Extract the 'score' column data as a list
            score_column_data = second_page_df['score'].tolist()

            # Render the process.html template and pass the 'score' column data
            return render_template('process.html', score_column_data=score_column_data)
        except Exception as e:
            return render_template('process.html', message=f'Error processing second page data: {str(e)}')
    else:
        return render_template('process.html', message="No page(tab) called 'secondpage'")


# API ENDPOINTS

# Get Excel Data
@app.route('/api/excel', methods=['GET'])
def get_excel_data():
    global df
    excel_data_json = df.to_json(orient='records')
    return jsonify(excel_data_json)


# Add a new API endpoint for the second page
@app.route('/api/secondpage', methods=['GET'])
def get_second_page_data():
    global all_sheets

    if 'Survey' in all_sheets:
        try:
            # Assuming 'Survey' is the second sheet in your DataFrame
            second_page_df = all_sheets['Survey']

            # Drop rows with NaN values in the 'score' column
            second_page_df = second_page_df.dropna(subset=['score'])

            # Transpose the DataFrame
            second_page_df_transposed = second_page_df.set_index('Unnamed: 0').transpose()

            # Convert transposed DataFrame to a list of dictionaries
            second_page_data = second_page_df_transposed.to_dict(orient='records')

            return jsonify(second_page_data)
        except Exception as e:
            return jsonify({'message': f'Error processing second page: {str(e)}'})
    else:
        return jsonify({"message": "No page(tab) called 'Survey'"})


"""
# Get PerformanceIndicators
@app.route('/api/performanceindicators', methods=['GET'])
def getPerformanceIndicators():
    performance_indicators = PerformanceIndicator.query.all()

    # Convert performance indicators to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in performance_indicators
    ]

    return jsonify(indicators_list)
"""


@app.route('/api/performanceindicators', methods=['GET'])
def getPerformanceIndicators():
    course_code = request.args.get('course_code')
    year = request.args.get('year')
    semester = request.args.get('semester')

    query = PerformanceIndicator.query.join(CourseInstancePerformanceIndicator,
                                            CourseInstancePerformanceIndicator.performance_indicator_id == PerformanceIndicator.id). \
        join(CourseInstance, ((CourseInstancePerformanceIndicator.course_instance_code == CourseInstance.course_code) &
                              (CourseInstancePerformanceIndicator.course_instance_year == CourseInstance.year) &
                              (CourseInstancePerformanceIndicator.course_instance_semester == CourseInstance.semester)))

    if course_code and year and semester:
        query = query.filter((CourseInstance.course_code == course_code) &
                             (CourseInstance.year == int(year)) &
                             (CourseInstance.semester == semester))

    result = query.all()

    # Convert performance indicators to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in result
    ]

    print(indicators_list)
    return jsonify(indicators_list)


@app.route('/api/studentoutcomes', methods=['GET'])
def getStudentOutcomes():
    department_code = request.args.get('department_code')

    if department_code is None:
        student_outcomes = StudentOutcome.query.all()  # if it's not specified all studentoutcomes will come
    else:
        student_outcomes = StudentOutcome.query.filter_by(department_code=department_code).all()

    # Convert student outcomes to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in student_outcomes
    ]
    return jsonify(indicators_list)


@app.route('/soCalculation')
def soCalculation():
    return render_template('soCalculation.html')


@app.route('/api/courseobjectives', methods=['GET'])
def getCourseObjective():
    """course_code = request.args.get('course_code')
    year = request.args.get('year')
    semester = request.args.get('semester')

    result_co = db.session.query(CourseObjective.description, CourseObjective.id) \
        .join(CourseObjectiveScore, CourseObjective.id == CourseObjectiveScore.course_objective_id) \
        .filter(
        CourseObjectiveScore.course_code == course_code,
        CourseObjectiveScore.year == year,
        CourseObjectiveScore.semester == semester
    ).all()

    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in result_co
    ]

    print(result_co)
    return jsonify(indicators_list)"""

    course_code = request.args.get('course_code')

    course_objectives = CourseObjective.query.filter_by(course_code=course_code).all()
    print(course_objectives)
    print(len(course_objectives))
    results = []

    for objective in course_objectives:
        print(f"Processing CourseObjective ID: {objective.id}")
        performance_indicators = [pi.id for pi in objective.performance_indicators]
        print(f"Performance Indicators: {performance_indicators}")
        results.append({
            'course_objective_id': objective.id,
            'description': objective.description,
            'performance_indicators': performance_indicators
        })
        print(results)
    return jsonify(results)


from flask import jsonify


@app.route('/api/instructor/courses', methods=['GET'])
def get_instructor_selected_courses():
    instructor_email = current_user.email
    year = request.args.get('year')
    semester = request.args.get('semester')
    print(instructor_email)
    print(year)
    print(semester)
    instructor = Instructor.query.filter_by(email=instructor_email).first()

    if instructor:
        course_instances = CourseInstance.query.filter_by(instructor_id=instructor.id, year=year,
                                                          semester=semester).all()

        courses_info = []
        for course_instance in course_instances:
            course_info = {
                'course_code': course_instance.course_code,
                'year': course_instance.year,
                'semester': course_instance.semester
            }
            courses_info.append(course_info)

        return jsonify({'instructor_name': instructor.name, 'courses_info': courses_info})
    else:
        return jsonify({'message': f"Instructor with email {instructor_email} not found"}), 404


# all courses of a program that have been opened according to the selected year and semester
@app.route('/api/courses', methods=['GET'])
def get_courses_by_filter():
    year = request.args.get('year')
    semester = request.args.get('semester')
    department_code = request.args.get('department_code')

    courses = CourseInstance.query.filter_by(year=year, semester=semester, department_code=department_code).all()

    courses_data = []
    for course in courses:
        course_data = {
            'course_code': course.course_code,
            'instructor_id': course.instructor_id,
        }
        courses_data.append(course_data)

    return jsonify({'courses': courses_data}), 200


@app.route('/calculate_student_outcomes', methods=['POST'])
def calculate_student_outcomes():
    data = request.json
    start_semester = data['start_semester']
    end_semester = data['end_semester']
    start_year = data['start_year']
    end_year = data['end_year']

    # dates btw
    filtered_courses = CourseInstancePerformanceIndicator.query.filter(
        CourseInstancePerformanceIndicator.course_instance_semester.in_([start_semester, end_semester]),
        CourseInstancePerformanceIndicator.course_instance_year.between(start_year, end_year)
    ).all()

    # avg of pi
    pi_averages = {}
    for course in filtered_courses:
        pi_id = course.performance_indicator_id
        if pi_id not in pi_averages:
            pi_averages[pi_id] = {'total': 0, 'count': 0}
        pi_averages[pi_id]['total'] += course.average  # "average" alanını kullan
        pi_averages[pi_id]['count'] += 1

    for pi_id, data in pi_averages.items():
        pi_averages[pi_id] = data['total'] / data['count'] if data['count'] else 0

    # match the pı's with the so and calculate summation of so
    student_outcomes_sums = {}
    for pi_id, pi_avg in pi_averages.items():
        related_sos = db.session.query(
            studentoutcome_performanceindicator.c.student_outcome_id
        ).filter(
            studentoutcome_performanceindicator.c.performance_indicator_id == pi_id
        ).all()

        for outcome in related_sos:
            so_id = outcome.student_outcome_id
            if so_id not in student_outcomes_sums:
                student_outcomes_sums[so_id] = {'total': 0, 'count': 0}
            student_outcomes_sums[so_id]['total'] += pi_avg
            student_outcomes_sums[so_id]['count'] += 1

    # calculate so avg
    student_outcomes_averages = {}
    for so_id, data in student_outcomes_sums.items():
        student_outcomes_averages[so_id] = data['total'] / data['count'] if data['count'] else 0

    print(start_year)
    print(end_year)
    print(start_semester)
    print(end_semester)

    # return so

    #return so

    student_outcomes_response = {f'SO-{so_id}': avg for so_id, avg in student_outcomes_averages.items()}

    return jsonify(student_outcomes_response)



@app.route('/save_course_instance_performance_indicators', methods=['POST'])
def save_course_instance_performance_indicators():
    data = request.json
    course_instance_code = data['course_instance_code']
    course_instance_year = data['course_instance_year']
    course_instance_semester = data['course_instance_semester']
    performance_indicator_id = data['performance_indicator_id']
    weight = data['weight']
    average = data['average']
    std_dev = data['std_dev']
    description = data['description']

    # Query the database for existing entry
    existing_entry = CourseInstancePerformanceIndicator.query.filter_by(
        course_instance_code=course_instance_code,
        course_instance_year=course_instance_year,
        course_instance_semester=course_instance_semester,
        performance_indicator_id=performance_indicator_id
    ).first()

    if existing_entry:
        # Update existing entry
        existing_entry.weight = weight
        existing_entry.average = average
        existing_entry.stdDev = std_dev
        existing_entry.description = description
    else:
        # If entry doesn't exist, create a new one
        new_element = CourseInstancePerformanceIndicator(
            course_instance_code=course_instance_code,
            course_instance_year=course_instance_year,
            course_instance_semester=course_instance_semester,
            performance_indicator_id=performance_indicator_id, 
            weight=weight,
            average=average, 
            stdDev=std_dev, 
            description=description
        )
        db.session.add(new_element)

    db.session.commit()
    return render_template('dashboard.html')



"""@app.route('/get_course_objectives', methods=['GET'])
def get_course_objectives():

    course_code = request.args.get('course_code')

    course_objectives = CourseObjective.query.filter_by(course_code=course_code).all()

    results = []
    for objective in course_objectives:
        performance_indicators = [pi.id for pi in objective.performance_indicators]
        results.append({
            'course_objective_id': objective.id,
            'description': objective.description,
            'performance_indicators': performance_indicators
        })

    return jsonify(results)"""
