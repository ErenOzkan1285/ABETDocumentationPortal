from flask import render_template, request, jsonify, url_for, redirect, flash, abort
from flaskbitirme import app, db, bcrypt
import pandas as pd
from flaskbitirme.models import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
import json

df = pd.DataFrame()  # Initialize an empty DataFrame
all_sheets = {}


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def home():
    #print("home func:", current_user.name)

    global df
    global all_sheets

    # Request method is POST
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('home.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('home.html', message='No selected file')

        try:
            all_sheets = pd.read_excel(file, sheet_name=None,engine='openpyxl')
            df = pd.read_excel(file,engine='openpyxl')
        except:
            abort(400, 'Invalid file format. Please upload an Excel file.')
        # Access and print each sheet separately
        '''for sheet_name, sheet_df in all_sheets.items():
            print(f"Sheet name: {sheet_name}")
            print(sheet_df)'''

        # Read the Excel file into a pandas DataFrame
        

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
        print(current_user.department_code)
        return render_template('coordinator.html', instructors=instructors, courses=available_courses, unassigned_course_instances=unassigned_course_instances)


###
@app.route('/assigncoordinator', methods=['GET', 'POST'])
@login_required
def assigncoordinator():
    if current_user.userType != 'Admin':
        return redirect(url_for('dashboard'))
    
    # Post request
    if request.method == 'POST':
        instructor_id = request.form['instructor_id']
        department_code = request.form['department_code']

        instructor = Instructor.query.filter_by(id=instructor_id).first()
        department = Department.query.filter_by(department_code=department_code).first()
            
        if not instructor:
            flash('Instructor not found', 'error')
            return redirect(url_for('assigncoordinator'))

        if not department:
            flash('Department not found', 'error')
            return redirect(url_for('assigncoordinator'))
        
        email = instructor.email
        name = instructor.name
        surname = instructor.surname
        # This is not a good way to implement this // SONRA BAKCAM TEKRAR
        hashed_password = bcrypt.generate_password_hash("1234").decode('utf-8')

        db.session.delete(instructor)
        db.session.commit()
        
        new_coordinator = Coordinator(
                name=name, 
                surname=surname, 
                email=email, 
                password=hashed_password,
                department_code=department_code
            )
        
        # Remove the instructor from the Instructor table
        db.session.add(new_coordinator)
        db.session.commit()

        return redirect(url_for('assigncoordinator'))
    
    # GET request: fetch coordinators without a department and departments with no coordinators
    instructors = Instructor.query.all()
    # Subquery to find departments with coordinators
    departments_with_coordinators_subquery = db.session.query(Department.department_code).join(Coordinator).distinct()
    departments_without_coordinator = Department.query.filter(~Department.department_code.in_(departments_with_coordinators_subquery)).all()
    
    return render_template('assigncoordinator.html', instructors=instructors, departments=departments_without_coordinator)
###


##
# Admin excel file upload for database
@app.route('/admin_excel_upload', methods=['GET', 'POST'])
@login_required
def admin_excel_upload():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))
    
    # POST method
    if request.method == 'POST':

        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        dep_code = request.form['department_code']
        dep = Department(department_code=dep_code)
        db.session.add(dep)
        db.session.commit()
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'
        
        if file:
            # Read the Excel file
            excel_file = pd.ExcelFile(file)
            
            # Iterate over each sheet in the Excel file
        for sheet_name in excel_file.sheet_names:
            # Read data from the current sheet
            excel_data = pd.read_excel(excel_file, sheet_name)
        
            # Iterate over each row in the DataFrame
            if sheet_name == 'Student Outcomes':
                for index, row in excel_data.iterrows():
                    id = row['ID']
                    description = row['Description']
                    
                    # Create a new StudentOutcome 
                    student_outcome_existed = StudentOutcome.query.filter_by(id=id)
                    if not student_outcome_existed:
                        student_outcome = StudentOutcome(id=id, department_code=dep_code,description=description)
                        db.session.add(student_outcome)

                    existing_relationship = StudentOutcomeDepartment.query.filter_by(
                            student_outcome_id=id,
                            department_code=dep_code
                            ).first()
                    
                    if not existing_relationship:
                        relationship = StudentOutcomeDepartment(student_outcome_id=id, department_code=dep_code, description='!')
                        db.session.add(relationship)
                    
                    # Add the object to the session 
                    
                db.session.commit()
                    

            elif sheet_name == 'Performance Indicators':
                for index, row in excel_data.iterrows():
                    id = row['ID']
                    description = row['Description']
                    std_outcomes = row['Student Outcomes'] # studentoutcome_performanceindicator
                    course_list = row['Evaluated in Courses']

                    # Creating performance indicator
                    perf_indicator = PerformanceIndicator(id=id[1:],description=description[1:])
                    db.session.add(perf_indicator)

                    individual_std_outcomes = [part.strip() for part in std_outcomes.split(',')]
                    # Filling studentoutcome_performanceindicator table
                    for std_outcome in individual_std_outcomes:
                        stmt = studentoutcome_performanceindicator.insert().values(
                            student_outcome_id=std_outcome,
                            performance_indicator_id=perf_indicator.id
                        )
                        db.session.execute(stmt)

                    individual_courses = [part.strip()[-3:] for part in course_list.split(',')]
                    for c in individual_courses:
                        cccourse = Course.query.filter_by(course_code=c).first()
                        if not cccourse:
                            course = Course(course_code=c, department_code=dep_code)
                            db.session.add(course)

                        existing_relationship = CoursePerformanceIndicator.query.filter_by(
                            course_code=c,
                            performance_indicator_id=perf_indicator.id
                            ).first()
                        if not existing_relationship:
                            relationship = CoursePerformanceIndicator(course_code=c, performance_indicator_id=perf_indicator.id)
                            db.session.add(relationship)
                    
                db.session.commit()
                        
            
    # GET method
    return render_template('adminexcel.html')

##

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


@app.route('/process', methods = ['POST'])
@login_required
def process():
    global all_sheets
    if 'Survey' in all_sheets:
        try:
            # Assuming 'secondpage' is the sheet in your DataFrame
            second_page_df = all_sheets['Survey']

            # Drop rows with NaN values in the 'score' column
            second_page_df = second_page_df.dropna(subset=['score'])

            # Extract the 'score' column data as a list
            score_column_data = second_page_df['score'].tolist()
            
            
            pi_weights = request.form.get('piWeights')
    
            print("PIWEIGHTS: ", pi_weights)
            # Render the process.html template and pass the 'score' column data
            return render_template('process.html', score_column_data=score_column_data, pi_weights=pi_weights)
        except Exception as e:
            return render_template('process.html', message=f'Error processing second page data: {str(e)}', pi_weights=pi_weights)
    else:
        return render_template('process.html', message="No page(tab) called 'Survey'")


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

    query = PerformanceIndicator.query.join(CoursePerformanceIndicator,
                                            CoursePerformanceIndicator.performance_indicator_id == PerformanceIndicator.id). \
        join(CourseInstance, ((CoursePerformanceIndicator.course_code == CourseInstance.course_code)))

    if course_code:
        query = query.filter((CourseInstance.course_code == course_code))

    result = query.all()

    # Convert performance indicators to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in result
    ]
    return jsonify(indicators_list)


"""@app.route('/api/studentoutcomes', methods=['GET'])
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
    return jsonify(indicators_list)"""

@app.route('/api/studentoutcomes', methods=['GET'])
def get_student_outcomes_for_department():
    department_code = request.args.get('department_code')
    if not department_code:
        return jsonify({'error': 'Department code is required'}), 400

    # Querying the database to find all entries in StudentOutcomeDepartment with the given department code
    outcomes = StudentOutcomeDepartment.query.filter_by(department_code=department_code).all()

    if not outcomes:
        return jsonify({'error': 'No student outcomes found for this department'}), 404

    # Creating a list of outcomes to return as JSON
    results = [{
        'student_outcome_id': outcome.student_outcome_id,
        'description': outcome.description
    } for outcome in outcomes]

    return jsonify(results), 200


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
    
@app.route('/api/latest_semester_year', methods=['GET'])
def get_latest_semester_year():
    # Query to get the latest course instance year and semester
    latest_course_instance = db.session.query(
        CourseInstance.year,
        CourseInstance.semester
    ).order_by(
        CourseInstance.year.desc(),
        CourseInstance.semester.desc()
    ).first()

    if latest_course_instance:
        latest_year, latest_semester = latest_course_instance
    else:
        latest_year, latest_semester = '2023', 'S'  # Default values if no data found

    return jsonify({'year': latest_year, 'semester': latest_semester})

@app.route('/save_course_objective_score', methods=['POST'])
def save_course_objective_score():
    # Get the data from the request
    data = request.json
    # Extract data from the request
    course_objective_id = data['course_objective_id']
    course_code = data['course_code']
    year = data['year']
    semester = data['semester']
    target_score = data['target_score']
    actual_score = data['actual_score']
    student_score = data['student_score']
    status = data['status']
    notes = data['notes']
    
    existing_entry = CourseObjectiveScore.query.filter_by(
        course_objective_id=course_objective_id,
        course_code=course_code,
        year=year,
        semester=semester
    ).first()

    if existing_entry:
        # Update existing entry
        existing_entry.targetScore = target_score
        existing_entry.actualScore = actual_score
        existing_entry.studentScore = student_score
        existing_entry.status = status
        existing_entry.notes = notes
    else:
        # If entry doesn't exist, create a new one
        new_element = CourseObjectiveScore(
            course_objective_id=course_objective_id,
            course_code=course_code,
            year=year,
            semester=semester, 
            targetScore=target_score,
            actualScore=actual_score, 
            studentScore=student_score, 
            status=status,
            notes = notes
        )
        db.session.add(new_element)

    db.session.commit()
    return render_template('dashboard.html')

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

#related with the CoursePerformanceIndicator table
@app.route('/course/performance-indicators', methods=['POST'])
def get_performance_indicator_ids():
    # Parse course_code from the JSON request body
    request_data = request.get_json()
    course_code = request_data.get('course_code')

    if not course_code:
        return jsonify({"error": "Course code is required"}), 400

    # Query the course_performance_indicator table for the given course code
    performance_indicator_ids = db.session.query(
        CoursePerformanceIndicator.performance_indicator_id
    ).filter(
        CoursePerformanceIndicator.course_code == course_code
    ).all()

    # Convert the query result to a list of IDs
    performance_indicator_ids = [pi[0] for pi in performance_indicator_ids]

    # Return the list of performance indicator IDs as JSON
    return jsonify(performance_indicator_ids)

# Admin panel route
@app.route('/admin_panel', methods=['GET'])
@login_required
def admin_panel():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    student_outcomes = StudentOutcomeDepartment.query.all()
    performance_indicators = PerformanceIndicator.query.all()
    return render_template('admin.html', student_outcomes=student_outcomes,
                           performance_indicators=performance_indicators)


@app.route('/add_student_outcome', methods=['POST'])
@login_required
def add_student_outcome():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    id = request.form['student_outcome_id']
    department_code = request.form['department_code']
    description = request.form['description']

    # Department code validation
    department = Department.query.filter_by(department_code=department_code).first()
    if not department:
        flash('Invalid department code.', 'error')
        return redirect(url_for('admin_panel'))

    existing_outcome = StudentOutcomeDepartment.query.filter_by(student_outcome_id=id, department_code=department_code).first()
    if existing_outcome:
        flash('Student Outcome already exists for this department.', 'error')
    else:
        new_outcome = StudentOutcomeDepartment(student_outcome_id=id, department_code=department_code, description=description)
        db.session.add(new_outcome)
        try:
            db.session.commit()
            flash('Student Outcome added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding student outcome: {}'.format(e), 'error')
    return redirect(url_for('admin_panel'))



@app.route('/update_student_outcome', methods=['POST'])
@login_required
def update_student_outcome():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    id = request.form.get('student_outcome_id')
    current_department_code = request.form.get('current_department_code')
    new_department_code = request.form.get('new_department_code')
    new_description = request.form.get('description')

    if not id or not current_department_code or not new_description:
        flash('Missing required fields.', 'error')
        return redirect(url_for('admin_panel'))

    outcome = StudentOutcomeDepartment.query.filter_by(
        student_outcome_id=id,
        department_code=current_department_code
    ).first()

    if outcome:
        if new_department_code:
            department_exists = Department.query.filter_by(department_code=new_department_code).first()
            if department_exists:
                outcome.department_code = new_department_code
            else:
                flash('New department code does not exist.', 'error')
                return redirect(url_for('admin_panel'))

        outcome.description = new_description
        try:
            db.session.commit()
            flash('Student Outcome updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating student outcome: {}'.format(e), 'error')
    else:
        flash('No Student Outcome found with this ID and department code combination.', 'error')

    return redirect(url_for('admin_panel'))



@app.route('/delete_student_outcome/<student_outcome_id>/<department_code>', methods=['POST'])
@login_required
def delete_student_outcome(student_outcome_id, department_code):
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    outcome = StudentOutcomeDepartment.query.filter_by(
        student_outcome_id=student_outcome_id,
        department_code=department_code
    ).first_or_404()

    db.session.delete(outcome)
    try:
        db.session.commit()
        flash('Student Outcome deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting student outcome: {}'.format(e), 'error')
    return redirect(url_for('admin_panel'))


@app.route('/add_performance_indicator', methods=['POST'])
@login_required
def add_performance_indicator():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    id = request.form['id']
    description = request.form['description']

    existing_indicator = PerformanceIndicator.query.filter_by(id=id).first()
    if existing_indicator:
        flash('Performance Indicator already exists.', 'error')
    else:
        new_indicator = PerformanceIndicator(id=id, description=description)
        db.session.add(new_indicator)
        try:
            db.session.commit()
            flash('Performance Indicator added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding performance indicator: {}'.format(e), 'error')
    return redirect(url_for('admin_panel'))

@app.route('/update_performance_indicator', methods=['POST'])
@login_required
def update_performance_indicator():
    if current_user.userType != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    id = request.form['id']
    description = request.form['description']

    indicator = PerformanceIndicator.query.filter_by(id=id).first()
    if indicator:
        indicator.description = description
        try:
            db.session.commit()
            flash('Performance Indicator updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating performance indicator: {}'.format(e), 'error')
    else:
        flash('No Performance Indicator found with this ID', 'error')
    return redirect(url_for('admin_panel'))

@app.route('/delete_performance_indicator/<id>', methods=['POST'])
@login_required
def delete_performance_indicator(id):
    if current_user.userType != 'Admin':
        return redirect(url_for('dashboard'))

    indicator = PerformanceIndicator.query.get_or_404(id)
    db.session.delete(indicator)
    try:
        db.session.commit()
        flash('Performance Indicator deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting performance indicator: {}'.format(e), 'error')
    return redirect(url_for('admin_panel'))



@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    student_outcome_id = request.form.get('student_outcome_id')
    performance_indicator_id = request.form.get('performance_indicator_id')

    # Check if the relationship already exists
    existing_relationship = db.session.query(studentoutcome_performanceindicator).filter(
        studentoutcome_performanceindicator.c.student_outcome_id == student_outcome_id,
        studentoutcome_performanceindicator.c.performance_indicator_id == performance_indicator_id
    ).first()

    if existing_relationship:
        return jsonify({'error': 'This relationship already exists'}), 409  # Conflict status

    try:
        # Insert new relationship if not existing
        new_relationship = studentoutcome_performanceindicator.insert().values(
            student_outcome_id=student_outcome_id,
            performance_indicator_id=performance_indicator_id
        )
        db.session.execute(new_relationship)
        db.session.commit()
        return jsonify({'message': 'Relationship added successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add relationship: ' + str(e)}), 500


@app.route('/delete_relationship/<student_outcome_id>/<performance_indicator_id>', methods=['POST'])
def delete_relationship(student_outcome_id, performance_indicator_id):
    try:
        # Delete the specified relationship
        delete_relationship = studentoutcome_performanceindicator.delete().where(
            db.and_(
                studentoutcome_performanceindicator.c.student_outcome_id == student_outcome_id,
                studentoutcome_performanceindicator.c.performance_indicator_id == performance_indicator_id
            )
        )
        db.session.execute(delete_relationship)
        db.session.commit()
        return jsonify({'message': 'Relationship deleted successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete relationship: ' + str(e)}), 500


@app.route('/get_initial_data')
def get_initial_data():
    outcomes = StudentOutcome.query.all()
    indicators = PerformanceIndicator.query.all()
    relationships = db.session.query(
        studentoutcome_performanceindicator.c.student_outcome_id,
        studentoutcome_performanceindicator.c.performance_indicator_id
    ).all()

    return jsonify({
        'outcomes': [{ 'id': o.id, 'description': o.description } for o in outcomes],
        'indicators': [{ 'id': i.id, 'description': i.description } for i in indicators],
        'relationships': [{'student_outcome_id': r[0], 'performance_indicator_id': r[1]} for r in relationships]
    })


@app.route('/save_assessment_item_details', methods=['POST'])
def save_assessment_item_details():
    data = request.json
    
    # Ensure that 'assessmentItemsData' exists in the received JSON
    if 'assessmentItemsData' in data:
        assessment_items = data['assessmentItemsData']
        
        # Iterate over each assessment item
        for item in assessment_items:
            course_code = item['course_code']
            year = item['year']
            semester = item['semester']
            name = item['name']
            
            # Check if an assessment item with the same name already exists for the same year, semester, and course
            existing_item = AssessmentItem.query.filter_by(course_code=course_code, year=year, semester=semester, name=name).first()
            
            if existing_item:
                # If an existing item is found, update its details
                existing_item.weight = item['weight']
                existing_item.average = item['average']
                existing_item.stdDev = item['stdDev']
                existing_item.outOf = item['outOf']
                existing_item.selectedPIs = ','.join(pi['id'] for pi in item['selectedPIs'])
            else:
                # Create a new AssessmentItem instance
                new_item = AssessmentItem(
                    course_code=course_code,
                    year=year,
                    semester=semester,
                    weight=item['weight'],
                    average=item['average'],
                    stdDev=item['stdDev'],
                    outOf=item['outOf'],
                    name=name,
                    selectedPIs=','.join(pi['id'] for pi in item['selectedPIs']),
                    description=''
                )
                
                # Add the new item to the database session
                db.session.add(new_item)
        
        # Commit all changes to the database session
        db.session.commit()
    
    # Redirect to the dashboard or any other appropriate page
    return render_template('dashboard.html')

@app.route('/api/course/<string:course_code>/latest-assessment-items', methods=['GET'])
def get_latest_course_assessment_items(course_code):
    latest_course_instance = db.session.query(CourseInstance).\
        filter(CourseInstance.course_code == course_code).\
        order_by(CourseInstance.year.desc(), CourseInstance.semester.desc()).first()

    if not latest_course_instance:
        return jsonify({'message': 'No course instance found for the specified course code'}), 404

    assessment_items = db.session.query(AssessmentItem).\
        filter(AssessmentItem.course_code == course_code).\
        filter(AssessmentItem.year == latest_course_instance.year).\
        filter(AssessmentItem.semester == latest_course_instance.semester).all()

    assessment_items_list = []
    for item in assessment_items:
        assessment_items_list.append({
            'id': item.id,
            'course_code': item.course_code,
            'year': item.year,
            'semester': item.semester,
            'selectedPIs': item.selectedPIs,
            'name': item.name,
            'weight': item.weight,
            'average': item.average,
            'stdDev': item.stdDev,
            'outOf': item.outOf,
            'description': item.description
        })

    return jsonify({'assessment_items': assessment_items_list}), 200
    
    
    
    
