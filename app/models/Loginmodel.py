from system.core.model import Model
import re



class Loginmodel(Model):
    def __init__(self):
        super(Loginmodel, self).__init__()
    
    def create(self,data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not data['name']:
            errors.append('Name cannot be blank')
        elif len(data['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif data['password'] != data['confirm_password']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = data['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (name, alias, email, password, date_hire) VALUES (:name, :alias, :email, :pw_hash, date_hire)"
            details = {
                'name': data['name'],
                'alias': data['alias'],
                'email': data['email'],
                'date_hire': data['date_hire'],
                'pw_hash': hashed_pw
                }
            self.db.query_db(query,details)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return {"status": True, "user": user[0]}

    
    def check_login(self,data):
        password = data['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': data['email']
                    }
        user = self.db.query_db(user_query, user_data)
        if not user:
            return False
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return {"user": user[0]}
            else:
                return False

    def add_item(self, data):
        query = "INSERT INTO Items(item, date_added, user_id) VALUES (:item, NOW(), :id)"
        added_items = self.db.query_db(query, data)
        id_query = "SELECT id as item_id from Items WHERE user_id = :id and item = :item"
        item_details = self.db.query_db(id_query, data)
        data['item_id'] = item_details[0]['item_id']
        user_query = "INSERT INTO wishlist(user_id, Item_id) Values (:id, :item_id)"
        self.db.query_db(user_query, data)
        return

    def wishlist(self,data):
        query = 'select DISTINCT items.id, item, items.id, users.name as name, date_added from wishlist join items on item_id = items.id join users on users.id = items.user_id where wishlist.user_id = :id'
        #query = "SELECT item, items.id ,users.name, date_added from wishlist join items on item_id = items.id join users on wishlist.user_id = users.id where wishlist.user_id = :id"
        wishlist_info = self.db.query_db(query, data)
        query_data = 'select DISTINCT items.id, item, users.name as name, date_added from wishlist join items on item_id = items.id join users on users.id = items.user_id where wishlist.user_id != :id'
        #query_data = "SELECT item, items.id ,users.name, date_added from wishlist join items on item_id = items.id join users on wishlist.user_id = users.id where wishlist.user_id != :id"
        others_wishlist_info = self.db.query_db(query_data, data)
        return { 'show_wishlist': wishlist_info, 'other_wishlist': others_wishlist_info}

    def show_list(self, data):
        query = "SELECT users.name, items.item from wishlist left join users on wishlist.user_id = users.id left join Items on wishlist.Item_id = Items.id where wishlist.item_id = :id"
        item_data = self.db.query_db(query, data)
        return { 'item_data' : item_data }

    def delete_from_list(self, data):
        query = "DELETE from wishlist where item_id = :item_id and user_id = :user_id"
        self.db.query_db(query, data)
        return

    def delete_from_item(self, data):
        query = "DELETE from items where id = :item_id and user_id = :user_id"
        self.db.query_db(query, data)

    def add_to_list(self, data):
        query = "INSERT INTO wishlist(user_id, item_id ) VALUES (:user_id, :item_id)"
        self.db.query_db(query, data)




    