from .import bp as api
from app.models import *
from flask import request, make_response, g, abort
from app.blueprints.auth.auth import token_auth

### RETURN ALL POSTS THE CURRENT USER FOLLOWS ###
@api.get('/posts')
@token_auth.login_required()
def get_posts():
    user = g.current_user
    posts = user.followed_posts()
    response_list = []
    for post in posts:
        response_list.append(post.to_dict())
    return make_response({'posts':response_list}, 200)

### RETURN 1 POST, BY POST ID ###
@api.get('/posts/<int:id>')
@token_auth.login_required()
def get_single_post(id):
    user = g.current_user
    post = Post.query.get(id)
    if not post:
        abort(404)
    if not user.is_following(post.author) and not post.author.user_id == user.user_id:
        abort(403, description='Please reauthorize your account to continue')
    return make_response(post.to_dict(), 200)

### CREATE A NEW POST ###
@api.post('/posts')
@token_auth.login_required()
def post_post():
    posted_data = request.get_json()
    u = g.current_user
    post = Post(**posted_data)
    post.save()
    u.posts.append(post)
    u.save()
    return make_response(f'Post id: {post.id} created', 200)


### EDIT POST ###
@api.put('/posts')
@token_auth.login_required()
def put_post():
    posted_data = request.get_json()
    post = Post.query.get(posted_data['id'])
    if not post:
        abort(404)
    if not post.author.user_id == g.current_user.user_id:
        abort(403)
    post.edit(posted_data['body'])
    return make_response(f'Post id: {post.id} has been changed', 200)

### DELETE POST ###
@api.delete('posts/<int:id>')
@token_auth.login_required()
def delete_post(id):
    user = g.current_user
    post = Post.query.get(id)
    if not post:
        abort(404)
    if not post.author.user_id == user.user_id:
        abort(403, description='Please reauthorize your account to continue')
    post.delete()
    return make_response(f'Success, post with id: {id} was deleted', 200)
