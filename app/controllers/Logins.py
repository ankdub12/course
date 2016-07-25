from system.core.controller import *

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Loginmodel')
        self.db = self._app.db
   
    def index(self):
        if session.has_key('id'):
            data = {
                'id': session['id']
                }
            details = self.models['Loginmodel'].wishlist(data)
            return self.load_view('mainpage.html', wishlist=details['show_wishlist'], others_wishlist=details['other_wishlist'])       
        else:
            return self.load_view('index.html')

    def logout(self):
        if session.has_key('id'):
            session.pop('id')
        if session.has_key('name'):
            session.pop('name')
        return redirect('/')


    def create(self):
        data = {
        'name': request.form['name'],
        'alias': request.form['alias'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
        'date_hire': request.form['date_hire']
        }
        create_status = self.models['Loginmodel'].create(data)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
        return redirect('/')

    def login(self):
        data = {
        'email' : request.form['email'],
        'password': request.form['password']
        }
        status = self.models['Loginmodel'].check_login(data)
        if status:
            session['id'] = status['user']['id']
            session['name'] = status['user']['name']
        else:
            flash("Email or password does not exist")
        return redirect('/')

    def add(self):
       return self.load_view('add_items.html')

    def add_items(self):
        data = {
        'item': request.form['item'],
        'id': session['id']
        }
        self.models['Loginmodel'].add_item(data)
        return redirect('/')

    def showwish(self, id):
        data = {
        'id': id
        }
        itemlist = self.models['Loginmodel'].show_list(data)
        item = itemlist['item_data'][0]['item']
        return self.load_view('wish_items.html', itemlist= itemlist['item_data'], item=item)

    def delete(self, id):
        data = {
        'item_id': id,
        'user_id': session['id']
        }
        self.models['Loginmodel'].delete_from_list(data)
        self.models['Loginmodel'].delete_from_item(data)
        return redirect('/')

    def add_wishlist(self, id):
        data = {
        'item_id': id,
        'user_id': session['id']
        }
        self.models['Loginmodel'].add_to_list(data)
        return redirect('/')

    def remove(self, id):
        data = {
        'item_id': id,
        'user_id': session['id']
        }
        self.models['Loginmodel'].delete_from_list(data)
        return redirect('/')





   





























       