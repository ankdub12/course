
from system.core.model import Model

class Course(Model):
    def __init__(self):
        super(Course, self).__init__()
    
    def add_details(self, details):
        query = " INSERT INTO course (courses_name, Description, Date_added) VALUES (:course_name, :description, NOW())"
        data = {
            'course_name': details['course_name'],
            'description': details['description']
            }
        return self.db.query_db(query,data)

    def get_all_courses(self):
        query = "SELECT * FROM course"
        return self.db.query_db(query)

    def show_details(self,id):
        query = "SELECT * FROM course WHERE id = :id"
        data_from = {
        'id': id
        }
        return self.db.query_db(query,data_from)

    def delete_course(self,data):
        query = "DELETE FROM course WHERE id =:id"
        return self.db.query_db(query,data)
        





