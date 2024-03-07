from flask import render_template, request, jsonify, url_for, redirect
from flaskbitirme import app, db, bcrypt
import pandas as pd
from flaskbitirme.models import *
from flask_login import login_user, current_user, logout_user

df = pd.DataFrame()  # Initialize an empty DataFrame
all_sheets = {}


@app.route('/upload', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Redirect to the login page if the user is not authenticated
    
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user is an Admin
        admin = Admin.query.filter_by(email=email).first()
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            # Set session variable or perform any other necessary actions
            return render_template('home.html')  # Redirect to admin dashboard
        
        # Check if the user is an Instructor
        instructor = Instructor.query.filter_by(email=email).first()
        #print(instructor.email)
        if instructor and bcrypt.check_password_hash(instructor.password, password):
            login_user(instructor)
            print('instructor logged in')
            # Set session variable or perform any other necessary actions
            return render_template('home.html')  # Redirect to instructor dashboard
        
        
        # Check if the user is a Coordinator
        coordinator = Coordinator.query.filter_by(email=email).first()
        if coordinator and bcrypt.check_password_hash(coordinator.password, password):
            login_user(coordinator)
            # Set session variable or perform any other necessary actions
            return render_template('home.html')  # Redirect to coordinator dashboard
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match."
            return render_template('signup.html', error=error)

        # Check if username is already taken based on the role
        if role == 'Admin':
            existing_user = Admin.query.filter_by(email=email).first()
        elif role == 'Instructor':
            existing_user = Instructor.query.filter_by(email=email).first()
        elif role == 'Coordinator':
            existing_user = Coordinator.query.filter_by(email=email).first()
        else:
            error = "Invalid role."
            return render_template('signup.html', error=error)

        if existing_user:
            error = f"{role} username already exists. Please choose a different username."
            return render_template('signup.html', error=error)
        
        # Encrypt the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user object and add it to the appropriate table in the database
        if role == 'Admin':
            new_user = Admin(name=name,surname=surname,email=email,password=hashed_password)
        elif role == 'Instructor':
            new_user = Instructor(name=name,surname=surname,email=email,password=hashed_password)
        elif role == 'Coordinator':
            new_user = Coordinator(name=name,surname=surname,email=email,password=hashed_password)
        else:
            # This should never happen due to the earlier check, but included for completeness
            error = "Invalid role."
            return render_template('signup.html', error=error)

        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')

    # If the request method is GET, simply render the signup page
    return render_template('signup.html')


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
    performance_indicators = PerformanceIndicator.query.all()

    result = db.session.query(PerformanceIndicator).join(CourseInstancePerformanceIndicator,
                                                         CourseInstancePerformanceIndicator.performance_indicator_id == PerformanceIndicator.id). \
        join(CourseInstance, ((CourseInstancePerformanceIndicator.course_instance_code == CourseInstance.course_code) &
                              (CourseInstancePerformanceIndicator.course_instance_year == CourseInstance.year) &
                              (
                                      CourseInstancePerformanceIndicator.course_instance_semester == CourseInstance.semester))). \
        filter((CourseInstance.course_code == '242') &
               (CourseInstance.year == 2023) &
               (CourseInstance.semester == 'S')).all()
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
"""


# Get StudentOutcomes
@app.route('/api/studentoutcomes', methods=['GET'])
def getStudentOutcomes():
    student_outcomes = StudentOutcome.query.all()

    # Query to fetch StudentOutcomes related to the department with code '355'

    result_so = db.session.query(StudentOutcome). \
        filter(StudentOutcome.department_code == '355').all()

    # Convert student outcomes to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in student_outcomes
    ]
    print(result_so)
    return jsonify(indicators_list)


@app.route('/')
def dashboard():
    # Render the dashboard.html template
    return render_template('dashboard.html')


@app.route('/process')
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


@app.route('/api/courseobjectives', methods=['GET'])
def getCourseObjective():
    courseObjectives = CourseObjective.query.all()

    # SQL query using SQLAlchemy
    result_co = db.session.query(CourseObjective.description, CourseObjective.id) \
        .join(CourseObjectiveScore, CourseObjective.id == CourseObjectiveScore.course_objective_id) \
        .filter(
        CourseObjectiveScore.course_code == '350',
        CourseObjectiveScore.year == 2023,
        CourseObjectiveScore.semester == 'S'
    ).all()

    # Convert course objectives to a list of dictionaries
    indicators_list = [
        {
            'id': indicator.id,
            'description': indicator.description,
        }
        for indicator in result_co
    ]
    print(result_co)
    return jsonify(indicators_list)
