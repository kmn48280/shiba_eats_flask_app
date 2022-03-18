from app import db, login
from datetime import datetime as dt, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True),
    first_name = db.Column(db.String(150)),
    last_name = db.Column(db.String(150)),
    email = db.Column(db.String(200), index=True, unique=True),
    password = db.Column(db.String(200)),
    created_on = db.Column(db.DateTime, default=dt.utcnow),
    modified_on = db.Column(db.DateTime, onupdate=dt.utcnow),
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User',
        secondary = followers,
        primaryjoin = (followers.c.follower_id == user_id),
        secondaryjoin = (followers.c.followed_id == user_id),
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )
    token = db.Column(db.String, index=True, unique=True),
    token_exp = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)


    ### TOKEN METHODS ###
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        if self.token and self.token_exp > current_time + timedelta(seconds=120):
            return self.token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=121)
    
    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        else:
            return u


    def __repr___(self):
        return f'<User: {self.user_id} | {self.email}>'
    
    def get_icon_src(self):
        return f'/static/dog_avatars/{self.icon}'
    
    ### CHECK IF USER IS FOLLOWING ANYONE (RETURN #) ###
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.user_id).count()>0
    
    
    ### METHOD TO FOLLOW USER ###
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()
    
    ### METHOD TO UNFOLLOW USER ###
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()
    
    ### METHOD TO RETRIEVE ALL THE POSTS FROM USERS I FOLLOW ###
    def followed_posts(self):
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.user_id)
        self_posts = Post.query.filter_by(user_id = self.user_id)
        all_posts = followed.union(self_posts).order_by(Post.date_created.desc())
        return all_posts
    
    ### PASSWORD CREATION/CHECK ###
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    

    ### METHODS TO TRANSFER USER INFO BETWEEN DIFF. STATES ###
    def from_dict(self, data):
        for field in ['email', 'password', 'first_name', 'last_name', 'icon']:
            if field in data:
                if field == 'password':
                    setattr(self, field, self.hash_password(data[field]))
                else:
                    setattr(self, field, data[field])

    def to_dict(self):
        return{
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_on': self.created_on,
            'modified_on': self.modified_on,
            'icon': self.icon,
            'token': self.token
        }
    
    ### METHODS TO SAVE USER TO DB ###
    def save(self):
        db.session.add(self)
        db.session.commit()

    
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default = dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate = dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant_id'))

    def __repr__(self):
        return f'<Post: {self.id} | {self.body[:15]}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
            'user_id': self.user_id
        }
    
    def edit(self, new_body):
        self.body = new_body
        self.save()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200), index=True)
    phone_number = db.Column(db.String(30), index=True)
    hours_of_op= db.Column(db.Text)
    map_location = db.Column(db.String, index=True)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    modified_on = db.Column(db.DateTime, onupdate=dt.utcnow)
    img = db.Column(db.String)
    cuisine = db.Column(db.String)
    speciality = db.Column(db.Text)
    posts = db.relationship('Review', backref='eatery', lazy='dynamic')
    rating = db.Column(db.Integer)
    














        




