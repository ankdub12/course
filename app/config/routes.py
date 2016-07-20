
from system.core.router import routes


routes['default_controller'] = 'Courses'
routes['/'] ='Courses#index'
routes['POST']['/add'] = 'Courses#add'
routes['/delete/<id>'] = 'Courses#delete_page'
routes['POST']['/delete_confirm/<id>'] = 'Courses#remove'
