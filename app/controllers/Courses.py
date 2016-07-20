from system.core.controller import *

class Courses(Controller):
    def __init__(self, action):
        super(Courses, self).__init__(action)
        self.load_model('Course')
        self.db = self._app.db
   
    def index(self):
        courses = self.models['Course'].get_all_courses() #create a varibale courses and grab everything from model object named .get_all_courses
        print courses
        return self.load_view('/courses/index.html', courses=courses)

    def add(self):
        details = {
        'course_name': request.form['course_name'],
        'description': request.form['description']
        }

        self.models['Course'].add_details(details)
        return redirect('/')

    def delete_page(self,id):
        show_course = self.models['Course'].show_details(id)  #create a variable show_course and give it instruction to grab from model['Course'].show_details
        return self.load_view('/courses/remove.html', id=id, show_course=show_course[0])

    def remove(self,id):
        data = {
        'id' : id
        }
        self.models['Course'].delete_course(data)
        return redirect('/')





