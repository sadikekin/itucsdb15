import psycopg2 as dbapi2
from flask import current_app
from flask_login import UserMixin

class Users(UserMixin):
    def __init__(self,Id,FirstName,LastName,Mail,Password,Birthdate,City,Gender,UserType,Avatar,Bio):
        self.Id = Id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Mail = Mail
        self.Password = Password
        self.Birthdate = Birthdate
        self.Bio = Bio
        self.City = City
        self.Gender = Gender
        self.UserType = UserType
        self.Avatar = Avatar
        self.active = True
        if UserType == 0:
            self.is_admin = True
        else:
            self.is_admin = False

    @property
    def get_gender(self):
        return self.Gender

    @property
    def get_birthdate(self):
        return self.Birthdate

    @property
    def get_bio(self):
        return self.Bio

    @property
    def get_city(self):
        return self.City

    @property
    def get_avatar(self):
        return self.Avatar

    @property
    def get_mail(self):
        return self.Mail

    @property
    def get_name(self):
        return self.FirstName

    @property
    def get_lastname(self):
        return self.LastName

    @property
    def get_type(self):
        return self.UserType
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return self.Mail

    @property
    def get_Id(self):
        return self.Id

def get_user(db_mail):
    if type(db_mail) is int:
        return None

    if db_mail in current_app.config['ADMIN_USERS']:
        user = Users(1,'admin','admin','admin@restoranlandin.com',current_app.config['PASSWORD'], '2012-10-10', '', '',0, '','')
        return user

    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE MAIL = %s"""
        cursor.execute(statement, [db_mail])
        db_user = cursor.fetchone()
        user = Users(db_user[0],db_user[1], db_user[2], db_user[3],db_user[4], db_user[5], db_user[6], db_user[7], db_user[8], db_user[9], db_user[10])


    if user is not None:
        user.is_admin = user.Mail in current_app.config['ADMIN_USERS']

    return user

def get_user_list():
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS"""
        cursor.execute(statement)
        db_users = cursor.fetchall()
    return db_users

def delete_user_by_id(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            DELETE FROM USERS WHERE ID = %s"""
        cursor.execute(query, [userID] )
        connection.commit()

def get_voted_restaurants(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT RESTAURANTS.NAME,RESTAURANTS.ADDRESS,STAR,RESTAURANTS.ID FROM RESTAURANTS,STAR_RESTAURANTS WHERE USER_ID = %s AND
        RESTAURANTS.ID =STAR_RESTAURANTS.RESTAURANT_ID """
        cursor.execute(query, [userID])
        return cursor.fetchall()

def get_restaurants(userId):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT ID,NAME,ADDRESS,SCORE FROM RESTAURANTS WHERE CREATOR_ID = %s"""
        cursor.execute(query, [userId])
        return cursor.fetchall()

def get_user_by_id(userID):
    with dbapi2.connect(current_app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """
            SELECT * FROM USERS WHERE ID = %s"""
        cursor.execute(query, [userID] )
        db_user = cursor.fetchone()
        user = Users(db_user[0],db_user[1], db_user[2], db_user[3],db_user[4], db_user[5], db_user[6], db_user[7], db_user[8], db_user[9], db_user[10])
        print(user.Avatar)
        return user
        
