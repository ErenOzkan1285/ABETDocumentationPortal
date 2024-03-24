from flaskbitirme import db
from flaskbitirme.models import *

def fill_database():
    # Create courses
    courses_data = [
        {"course_code": "350", "department_code": "355"},
        {"course_code": "351", "department_code": "355"},
        {"course_code": "242", "department_code": "355"},
        {"course_code": "445", "department_code": "355"},
        {"course_code": "438", "department_code": "355"},
        {"course_code": "466", "department_code": "355"},
        {"course_code": "491", "department_code": "355"},
        {"course_code": "492", "department_code": "355"},
        {"course_code": "477", "department_code": "356"},
        {"course_code": "347", "department_code": "356"},
        {"course_code": "280", "department_code": "356"},
        {"course_code": "230", "department_code": "356"}
    ]

    # Define Performance Indicators data
    performance_indicators_data = [
        {"id": "PI-a1", "description": "Analyze the computational complexity of algorithms by using discrete mathematics."},
        {"id": "PI-a2", "description": "Express facts and situations by using symbolic logic and set theory."},
        {"id": "PI-a3", "description": "Apply logical principles for sound reasoning."},
        {"id": "PI-a4", "description": "Analyze and reason about dynamic system models presented as systems of linear differential and difference equations."},
        {"id": "PI-a5", "description": "Apply linear algebra to model and solve computational problems."},
        {"id": "PI-a6", "description": "Apply probability theory and statistics to handle uncertainty."},
        {"id": "PI-a7", "description": "Analyze the power and limitations of abstract models of computation."},
        {"id": "PI-a8", "description": "Understand the fundamental concepts, laws and theories of natural sciences (such as Physics, Chemistry and Biology)."},
        {"id": "PI-b1", "description": "Infer facts and relationships from collected data."},
        {"id": "PI-b2", "description": "Design test procedures for finding defects in software and hardware."},
        {"id": "PI-b3", "description": "Design test procedures to assess the performance and other quality attributes of software."},
        {"id": "PI-c1", "description": "Design computer-based systems with realistic requirements."},
        {"id": "PI-c2", "description": "Evaluate and adapt standard algorithms algorithms (e.g. sorting, searching, string processing, language recognition, combination generation, and graph processing) for realistic tasks."},
        {"id": "PI-c3", "description": "Design and implement algorithms, heuristics and supporting data structures as packaged components."},
        {"id": "PI-c4", "description": "Design and implement components and systems to process (i.e. acquire, store, organize, manipulate, access and present) varied amounts of data."},
        {"id": "PI-c5", "description": "Interpret the needs of stakeholders in terms of system requirements."},
        {"id": "PI-c6", "description": "Understand broad economic, environmental, social, cultural, political, legal, ethical, safety, and security issues in both local and global scale."},
        {"id": "PI-d1", "description": "Understand the basic concepts of an engineering discipline other than computer engineering."},
        {"id": "PI-d2", "description": "Analyze the requirements of computational system interfaces with non-computational systems (such as electrical or mechanical)."},
        {"id": "PI-d3", "description": "Work as a member of a team."},
        {"id": "PI-e1", "description": "Construct mathematical or logical models of computational problems."},
        {"id": "PI-e2", "description": "Derive system properties from models."},
        {"id": "PI-e3", "description": "Integrate a set of available hardware and software components into a working system."},
        {"id": "PI-f1", "description": "Understand ethical codes (such as IEEE Code of Conduct, ACM Code of Ethics and Professional Conduct, and IEEE-CS ACM Software Engineering Code of Ethics and Professional Practice)."},
        {"id": "PI-f2", "description": "Understand legal issues related with engineering practice, including intellectual property rights, safety, security, and privacy."},
        {"id": "PI-g2", "description": "Use (read, write, speak, listen) English as the second language."},
        {"id": "PI-g3", "description": "Use non-verbal modes of communication, e.g. graphical."},
        {"id": "PI-i1", "description": "Self-assess one’s knowledge in a topic of interest."},
        {"id": "PI-i2", "description": "Explore topics not covered in lectures."},
        {"id": "PI-j1", "description": "Discuss newsworthy developments that arise from the use of information and communication technologies."},
        {"id": "PI-k1", "description": "Use a widely accepted high-level programming language (e.g. Java, C# and C++)."},
        {"id": "PI-k2", "description": "Use a widely accepted modeling language, such as UML."},
        {"id": "PI-k3", "description": "Use a well-known machine-oriented programming language (e.g. C and assembly languages)."},
        {"id": "PI-k4", "description": "Use a programming language in non-imperative paradigm, e.g. functional and logic."},
        {"id": "PI-k5", "description": "Use some special purpose languages and tools (such as those for mathematical programming, data manipulation and query, statistical analysis, hardware description, and simulation)."},
        {"id": "PI-k6", "description": "Use an integrated software development environment."}
    ]

    # Define Student Outcomes data
    student_outcomes_data = [
        {"id": "SO-1", "department_code": "355",
         "description": "An ability to identify, formulate, and solve complex engineering problems by applying principles of engineering, science, and mathematics."},
        {"id": "SO-2", "department_code": "355",
         "description": "An ability to apply engineering design to produce solutions that meet specified needs with consideration of public health, safety, and welfare, as well as global, cultural, social, environmental, and economic factors."},
        {"id": "SO-3", "department_code": "355",
         "description": "An ability to communicate effectively with a range of audiences."},
        {"id": "SO-4", "department_code": "355",
         "description": "An ability to recognize ethical and professional responsibilities in engineering situations and make informed judgments, which must consider the impact of engineering solutions in global, economic, environmental, and societal contexts."},
        {"id": "SO-5", "department_code": "355",
         "description": "An ability to function effectively on a team whose members together provide leadership, create a collaborative and inclusive environment, establish goals, plan tasks, and meet objectives."},
        {"id": "SO-6", "department_code": "355",
         "description": "An ability to develop and conduct appropriate experimentation, analyze and interpret data, and use engineering judgment to draw conclusions."},
        {"id": "SO-7", "department_code": "355",
         "description": "An ability to acquire and apply new knowledge as needed, using appropriate learning strategies."}
    ]

    # Define data for Student Outcome Performance Indicators
    so_pi_data = [
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a2"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a3"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a4"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a5"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a6"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a7"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-a8"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-b1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-b2"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-b3"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-c1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-c5"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-d1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-e1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-e2"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-e3"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k1"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k2"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k3"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k4"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k5"},
        {"student_outcome_id": "SO-1", "performance_indicator_id": "PI-k6"},

        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-b2"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-b3"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c1"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c2"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c3"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c4"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c5"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-c6"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-d2"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k1"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k2"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k3"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k4"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k5"},
        {"student_outcome_id": "SO-2", "performance_indicator_id": "PI-k6"},

        {"student_outcome_id": "SO-3", "performance_indicator_id": "PI-g2"},
        {"student_outcome_id": "SO-3", "performance_indicator_id": "PI-g3"},
        {"student_outcome_id": "SO-3", "performance_indicator_id": "PI-k2"},

        {"student_outcome_id": "SO-4", "performance_indicator_id": "PI-c6"},
        {"student_outcome_id": "SO-4", "performance_indicator_id": "PI-f1"},
        {"student_outcome_id": "SO-4", "performance_indicator_id": "PI-f2"},
        {"student_outcome_id": "SO-4", "performance_indicator_id": "PI-j1"},

        {"student_outcome_id": "SO-5", "performance_indicator_id": "PI-d1"},
        {"student_outcome_id": "SO-5", "performance_indicator_id": "PI-d2"},
        {"student_outcome_id": "SO-5", "performance_indicator_id": "PI-d3"},
        {"student_outcome_id": "SO-5", "performance_indicator_id": "PI-g2"},
        {"student_outcome_id": "SO-5", "performance_indicator_id": "PI-g3"},

        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-b1"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-b2"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-b3"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k1"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k2"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k3"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k4"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k5"},
        {"student_outcome_id": "SO-6", "performance_indicator_id": "PI-k6"},

        {"student_outcome_id": "SO-7", "performance_indicator_id": "PI-c5"},
        {"student_outcome_id": "SO-7", "performance_indicator_id": "PI-i1"},
        {"student_outcome_id": "SO-7", "performance_indicator_id": "PI-i2"},
        {"student_outcome_id": "SO-7", "performance_indicator_id": "PI-j1"},
    ]

    courseInstance = [
        {"course_code": "350", "year": "2023", "semester": "S", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "14.0", "overallWeight": "10.0", "outOf": "20.0" ,"instructor_id": "3"},

        {"course_code": "242", "year": "2021", "semester": "S", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "16.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "3"},

        {"course_code": "242", "year": "2022", "semester": "S", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "8.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "3"},

        {"course_code": "445", "year": "2023", "semester": "F", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "18.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "3"},

        {"course_code": "445", "year": "2022", "semester": "F", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "12.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "3"},

        {"course_code": "445", "year": "2021", "semester": "F", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "24.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "3"},

        {"course_code": "466", "year": "2020", "semester": "F", "normalizedScore": "5.0", "normalizedSTD": "10.0",
         "stdDev": "12.0", "average": "6.0", "overallWeight": "10.0", "outOf": "20.0", "instructor_id": "7"}
    ]



    courseObjective = [
        {"id": "1", "description": "Understand the domain and the basic terminology of Software Engineering",
         "course_code": "350"},
        {"id": "2", "description": "Analyse widely used software process models",
         "course_code": "350"},
        {"id": "3", "description": "Compare plan-driven and agile approaches to software development",
         "course_code": "350"},
        {"id": "4", "description": "Distinguish user requirements and system requirements",
         "course_code": "350"},
        {"id": "5", "description": "Distinguish functional requirements and different kinds of non-functional requirements",
         "course_code": "350"},
        {"id": "6", "description": "Compose a software requirement specification that is verifiable, correct, consistent, complete and unambiguous",
         "course_code": "350"},
        {"id": "7", "description": "Apply UML for modelling various aspects of computer-based systems using a state-of-art tool",
         "course_code": "350"},
        {"id": "8", "description": "Construct a requirements model for a computer-based system using UML",
         "course_code": "350"},
        {"id": "9", "description": "Construct a design model for a computer-based system using UML",
         "course_code": "350"},
        {"id": "10", "description": "Analyse system architecture from multiple viewpoints",
         "course_code": "350"},
        {"id": "11", "description": "Assess candidate architectural patterns and design patterns for a given design problem",
         "course_code": "350"},
        {"id": "12", "description": "Distinguish different levels of testing",
         "course_code": "350"},
        {"id": "13", "description": "Select testing techniques appropriate for a given test objective",
         "course_code": "350"},
        {"id": "14", "description": "Understand the fundamental concepts of quality as related to software, such as process quality and product quality, along with related standards",
         "course_code": "350"},
        {"id": "15", "description": "Understand software metrics and their relation to product quality",
         "course_code": "350"},
        {"id": "16", "description": "Discuss the processes involved in evolution of software",
         "course_code": "350"},
        {"id": "17", "description": "Identify ethical issues in a given situation, using the terminology of ACM/IEEE SECEPP",
         "course_code": "350"},
    ]


    # Attempt to commit everything to the database
    try:
        # Add courses to the session, skipping existing ones
        for course_data in courses_data:
            course_code = course_data["course_code"]
            department_code = course_data["department_code"]
            existing_course = Course.query.filter_by(course_code=course_code, department_code=department_code).first()
            if not existing_course:
                course = Course(**course_data)
                db.session.add(course)


        # Create Performance Indicator objects, skipping existing ones
        for pi_data in performance_indicators_data:
            pi_id = pi_data["id"]
            existing_pi = PerformanceIndicator.query.filter_by(id=pi_id).first()
            if not existing_pi:
                pi = PerformanceIndicator(**pi_data)
                db.session.add(pi)


        # Create Student Outcome objects, skipping existing ones
        for so_data in student_outcomes_data:
            so_id = so_data["id"]
            department_code = so_data["department_code"]
            existing_so = StudentOutcome.query.filter_by(id=so_id, department_code=department_code).first()
            if not existing_so:
                so = StudentOutcome(**so_data)
                db.session.add(so)


        for data in so_pi_data:
            so_id = data[
                "student_outcome_id"]  # Assuming these are IDs that need to be converted to integers or used as is
            pi_id = data["performance_indicator_id"]

            # Retrieve the StudentOutcome and PerformanceIndicator instances
            student_outcome = StudentOutcome.query.filter_by(id=so_id).first()
            performance_indicator = PerformanceIndicator.query.filter_by(id=pi_id).first()

            # Check if they already exist, and if not, create them (you might want to adjust this logic based on your needs)
            if not student_outcome:
                student_outcome = StudentOutcome(id=so_id)
                db.session.add(student_outcome)

            if not performance_indicator:
                performance_indicator = PerformanceIndicator(id=pi_id)
                db.session.add(performance_indicator)

            # Associate the StudentOutcome with the PerformanceIndicator if not already associated
            if performance_indicator not in student_outcome.performance_indicators:
                student_outcome.performance_indicators.append(performance_indicator)



        for instance in courseInstance:
            # Extracting information from the current dictionary
            course_code = instance['course_code']
            year = int(instance['year'])  # Converting year to integer
            semester = instance['semester']
            normalizedScore = float(instance['normalizedScore'])  # Converting to float
            normalizedSTD = float(instance['normalizedSTD'])  # Converting to float
            stdDev = float(instance['stdDev'])  # Converting to float
            average = float(instance['average'])  # Converting to float
            overallWeight = float(instance['overallWeight'])  # Converting to float
            outOf = float(instance['outOf'])  # Converting to float
            instructor_id = int(instance['instructor_id'])  # Converting instructor_id to integer

            # Check if a CourseInstance with the same primary key exists
            existing_instance = CourseInstance.query.filter_by(course_code=course_code, year=year,
                                                               semester=semester).first()

            if existing_instance:
                print(f"CourseInstance already exists: {course_code}, {year}, {semester}")
                continue  # Skip to the next iteration if this CourseInstance already exists

            # Create a new CourseInstance object if it does not exist
            new_course_instance = CourseInstance(
                course_code=course_code,
                year=year,
                semester=semester,
                normalizedScore=normalizedScore,
                normalizedSTD=normalizedSTD,
                stdDev=stdDev,
                average=average,
                overallWeight=overallWeight,
                outOf=outOf,
                instructor_id=instructor_id
            )

            # Add the new object to the session
            db.session.add(new_course_instance)

        for obj in courseObjective:
            # Extracting information from the current dictionary
            obj_id = int(obj['id'])  # Converting id to integer
            description = obj['description']
            course_code = obj['course_code']

            # Check if a CourseObjective with the same id exists
            existing_objective = CourseObjective.query.filter_by(id=obj_id).first()

            if existing_objective:
                print(f"CourseObjective already exists: ID {obj_id}")
                continue  # Skip to the next iteration if this CourseObjective already exists

            # Create a new CourseObjective object if it does not exist
            new_course_objective = CourseObjective(
                id=obj_id,
                description=description,
                course_code=course_code
            )

            # Add the new object to the session
            db.session.add(new_course_objective)





        db.session.commit()
        print("Database filled successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {e}")
