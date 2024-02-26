from sqlalchemy import ForeignKeyConstraint
from flaskbitirme import db

### MANY-TO-MANY RELATIONSHIP EXTRA TABLES ###
# Relationship table for CourseObjective and PerformanceIndicator (many-to-many)
courseobjective_performanceindicator = db.Table('courseobjective_performanceindicator',
                                                db.Column('course_objective_id', db.Integer,
                                                          db.ForeignKey('CourseObjective.id'), primary_key=True),
                                                db.Column('performance_indicator_id', db.String(5),
                                                          db.ForeignKey('PerformanceIndicator.id'), primary_key=True)
                                                )

# Relationship table for StudentOutcome and PerformanceIndicator (many-to-many)
studentoutcome_performanceindicator = db.Table('studentoutcome_performanceindicator',
                                               db.Column('student_outcome_id', db.Integer,
                                                         db.ForeignKey('StudentOutcome.id'), primary_key=True),
                                               db.Column('performance_indicator_id', db.String(5),
                                                         db.ForeignKey('PerformanceIndicator.id'), primary_key=True)
                                               )

# Relationship table for CourseInstance and PerformanceIndicator (many-to-many)
'''
courseinstance_performanceindicator = db.Table('courseinstance_performanceindicator',
    db.Column('course_instance_id', db.String(5), db.ForeignKey('CourseInstance.course_code'), primary_key=True),
    db.Column('performance_indicator_id', db.Integer, db.ForeignKey('PerformanceIndicator.id'), primary_key=True)
)'''


class CourseInstancePerformanceIndicator(db.Model):  # piEvaluation
    __tablename__ = 'CourseInstancePerformanceIndicator'
    course_instance_code = db.Column(db.String(5), primary_key=True)
    course_instance_year = db.Column(db.Integer, primary_key=True)
    course_instance_semester = db.Column(db.String(1), primary_key=True)
    performance_indicator_id = db.Column(db.String(5), db.ForeignKey('PerformanceIndicator.id'), primary_key=True)

    weight = db.Column(db.Float, nullable=False)
    average = db.Column(db.Float, nullable=False)
    stdDev = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    course_instance = db.relationship(
        'CourseInstance',
        foreign_keys=[course_instance_code, course_instance_year, course_instance_semester]
    )
    __table_args__ = (
        ForeignKeyConstraint(['course_instance_code', 'course_instance_year', 'course_instance_semester'],
                             ['CourseInstance.course_code', 'CourseInstance.year', 'CourseInstance.semester']),
    )


# Relationship table for AssessmentItem and PerformanceIndicator (many-to-many)
assessmentitem_performanceindicator = db.Table('assessmentitem_performanceindicator',
                                               db.Column('assessment_item_id', db.Integer,
                                                         db.ForeignKey('AssessmentItem.id'), primary_key=True),
                                               db.Column('performance_indicator_id', db.String(5),
                                                         db.ForeignKey('PerformanceIndicator.id'), primary_key=True)
                                               )


### END OF MANY-TO-MANY RELATIONSHIP EXTRA TABLES ###


class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    surname = db.Column(db.String(50), unique=True, nullable=False)
    departments = db.relationship('Department', backref='admin', lazy=True)


class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    surname = db.Column(db.String(50), unique=True, nullable=False)
    course_instances = db.relationship('CourseInstance', backref='instructor', lazy=True)


class Coordinator(db.Model):
    __tablename__ = 'Coordinator'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    surname = db.Column(db.String(50), unique=True, nullable=False)
    department_code = db.Column(db.String(5), db.ForeignKey('Department.department_code'), nullable=False)


class Department(db.Model):
    __tablename__ = 'Department'
    department_code = db.Column(db.String(5), primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('Admin.id'), nullable=False)
    courses = db.relationship('Course', backref='department', lazy=True)
    coordinators = db.relationship('Coordinator', backref='department', lazy=True)
    student_outcomes = db.relationship('StudentOutcome', backref='department', lazy=True)


class StudentOutcome(db.Model):
    __tablename__ = 'StudentOutcome'
    id = db.Column(db.String(5), primary_key=True)
    department_code = db.Column(db.String(5), db.ForeignKey('Department.department_code'), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    performance_indicators = db.relationship('PerformanceIndicator', secondary=studentoutcome_performanceindicator,
                                             back_populates='student_outcomes', lazy=True)


class PerformanceIndicator(db.Model):
    __tablename__ = 'PerformanceIndicator'
    id = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(120), unique=True, nullable=False)

    assessment_items = db.relationship('AssessmentItem', secondary=assessmentitem_performanceindicator,
                                       back_populates='performance_indicators', lazy=True)
    course_instances = db.relationship('CourseInstance', secondary=CourseInstancePerformanceIndicator.__tablename__,
                                       backref='related_CIs', lazy=True)
    student_outcomes = db.relationship('StudentOutcome', secondary=studentoutcome_performanceindicator,
                                       back_populates='performance_indicators', lazy=True)
    course_objectives = db.relationship('CourseObjective', secondary=courseobjective_performanceindicator,
                                        back_populates='performance_indicators', lazy=True)


class Course(db.Model):
    __tablename__ = 'Course'
    course_code = db.Column(db.String(5), primary_key=True)
    department_code = db.Column(db.String(5), db.ForeignKey('Department.department_code'), nullable=False)
    course_instances = db.relationship('CourseInstance', backref='course', lazy=True)
    course_objectives = db.relationship('CourseObjective', backref='course', lazy=True)


class AssessmentItem(db.Model):
    __tablename__ = 'AssessmentItem'
    id = db.Column(db.Integer, primary_key=True)

    # Composite Key reference to 'CourseInstance'
    course_code = db.Column(db.String(5), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(1), nullable=False)

    weight = db.Column(db.Float, nullable=False)
    average = db.Column(db.Float, nullable=False)
    stdDev = db.Column(db.Float, nullable=False)
    outOf = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    # Define the composite foreign key relationship
    course_instance = db.relationship(
        'CourseInstance',
        lazy=True,
        primaryjoin=(
            "and_("
            "AssessmentItem.course_code == foreign(CourseInstance.course_code), "
            "AssessmentItem.year == foreign(CourseInstance.year), "
            "AssessmentItem.semester == foreign(CourseInstance.semester)"
            ")"),
        backref=db.backref('assessment_items', lazy=True)
    )

    performance_indicators = db.relationship('PerformanceIndicator', secondary=assessmentitem_performanceindicator,
                                             back_populates='assessment_items', lazy=True)


class CourseInstance(db.Model):
    __tablename__ = 'CourseInstance'
    # Composite Key: (course_code, year, semester)
    course_code = db.Column(db.String(5), db.ForeignKey('Course.course_code'), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(1), primary_key=True)
    ### end of composite key

    normalizedScore = db.Column(db.Float, nullable=False)
    normalizedSTD = db.Column(db.Float, nullable=False)
    stdDev = db.Column(db.Float, nullable=False)
    average = db.Column(db.Float, nullable=False)
    overallWeight = db.Column(db.Float, nullable=False)
    outOf = db.Column(db.Float, nullable=False)

    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'), nullable=False)

    # performance_indicators = db.relationship('PerformanceIndicator',secondary='CourseInstancePerformanceIndicator', back_populates='related_PIs', lazy=True )


class CourseObjective(db.Model):
    __tablename__ = 'CourseObjective'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), unique=True, nullable=False)
    course_code = db.Column(db.String(5), db.ForeignKey('Course.course_code'))
    course_objective_scores = db.relationship('CourseObjectiveScore', backref='courseobjective', lazy=True)

    performance_indicators = db.relationship('PerformanceIndicator', secondary=courseobjective_performanceindicator,
                                             back_populates='course_objectives', lazy=True)


class CourseObjectiveScore(db.Model):
    __tablename__ = 'CourseObjectiveScore'
    id = db.Column(db.Integer, primary_key=True)
    course_objective_id = db.Column(db.Integer, db.ForeignKey('CourseObjective.id'), nullable=False)

    # Composite Key reference to 'CourseInstance'
    course_code = db.Column(db.String(5), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(1), nullable=False)

    targetScore = db.Column(db.Float, nullable=False)
    actualScore = db.Column(db.Float, nullable=False)
    studentScore = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(1), nullable=False)

    # Define the composite foreign key relationship
    course_instance = db.relationship(
        'CourseInstance',
        lazy=True,
        primaryjoin=(
            "and_("
            "CourseObjectiveScore.course_code == foreign(CourseInstance.course_code), "
            "CourseObjectiveScore.year == foreign(CourseInstance.year), "
            "CourseObjectiveScore.semester == foreign(CourseInstance.semester)"
            ")"),
        backref=db.backref('courseobjectivescores', lazy=True)
    )

# $env:FLASK_APP = "run"
# echo $env:FLASK_APP
# flask db init
# flask db migrate
# flask db upgrade
