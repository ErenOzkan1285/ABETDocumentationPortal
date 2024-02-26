from flask import render_template, request, jsonify
from flaskbitirme import app
import pandas as pd
from flaskbitirme.models import *

df = pd.DataFrame()  # Initialize an empty DataFrame
all_sheets = {}


@app.route('/upload', methods=['GET', 'POST'])
def home():
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
