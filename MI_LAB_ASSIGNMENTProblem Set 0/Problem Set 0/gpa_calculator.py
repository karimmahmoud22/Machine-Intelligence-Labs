from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    
    total_hours = 0
    total_points = 0
    # iterate through the list of courses
    for course in courses:
        # check if the student is present in the course
        if student.id in course.grades:
            # if the student is present in the course then add the hours and points
            total_hours += course.hours
            total_points += course.hours * Course.convert_grade_to_points(course.grades[student.id])
    
    if total_hours == 0:
        return 0
    # return the gpa
    return total_points / total_hours

    
    
    #utils.NotImplemented()