from .import bp as social
from flask import render_template, flash, redirect, url_for, request
from app.models import *
from flask_login import login_required, current_user 

### METHOD PRODUCES A NEW POST, PRESENTS ALL OF THE POSTS FROM USERS THAT THE CURRENT_USER FOLLOWS ###
@social.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        body = request.form.get('body')
        new_post = Post(user_id=current_user.user_id, body=body)
        new_post.save()
        return redirect(url_for('social.index'))
    posts = current_user.followed_posts()
    return render_template('index.html.j2', posts=posts)


### METHOD SHOWS ALL USERS ###
@social.route('/show_users')
@login_required
def show_users():
    users = User.query.all()
    return render_template('show_users.html.j2', users=users)

### METHOD FOR FOLLOWING A USER ###
@social.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user_to_follow = User.query.get(user_id)
    current_user.follow(user_to_follow)
    flash(f'You are now following {user_to_follow.first_name} {user_to_follow.last_name}', 'success')
    return redirect(url_for('social.show_users'))

### METHOD FOR UNFOLLOWING A USER ###
@social.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get(user_id)
    current_user.unfollow(user_to_unfollow)
    flash(f'You are no longer following: {user_to_unfollow.first_name} {user_to_unfollow.last_name}', 'warning')
    return redirect(url_for('social.show_users'))

### METHOD TO RETRIEVE 1 POST BY ID ###
@social.route('/post/<int:id>')
@login_required
def get_post(id):
    post = Post.query.get(id)
    return render_template('single_post.html.j2', post=post, view_all=True)

### METHOD TO COLLECT ALL OF MY POSTS ###
@social.route('/post/my_posts')
@login_required
def my_posts():
    posts = current_user.posts
    return render_template('my_posts.html.j2', posts=posts)

### METHOD TO EDIT POST, GET BY POST ID ###
@social.route('edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    if post and post.user_id != current_user.user_id:
        flash('You are unable to edit this post.', 'danger')
        return redirect(url_for('social.index'))
    if request.method == 'POST':
        post.edit(request.form.get('body'))
        flash('Your post has been edited', 'success')
    return render_template('edit_post.html.j2', post=post)








