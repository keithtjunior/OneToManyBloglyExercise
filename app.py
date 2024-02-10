"""Blogly application."""

from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'heartthrobnever1978'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.errorhandler(404) 
def not_found(e): 
    return render_template('error.html', e=e)

@app.route('/')
def home():
    # app.logger.info('variable: %s', variable)
    # import pdb;  pdb.set_trace()
    # records = [dict(zip(post.keys(), post)) for post in posts]
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

############ USERS ROUTES ############

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user-listing.html', users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = db.session.query(Post.id, Post.title, Post.created_at).filter(Post.user_id == user_id).order_by(Post.created_at.desc()).all()
    return render_template("user-detail.html", user=user, posts=posts)

@app.route('/users/new', methods=["GET"])
def new_user():
    """Create a new user form"""
    return render_template('user-create.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        first_name = request.form["first-name"].strip()
        last_name = request.form["last-name"].strip()
        img_url = request.form["img-url"].strip()
        img_url = img_url if img_url else None
        new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User [{new_user.full_name}] was successfully created', 'success')
        return redirect('/users')
    except:
        flash(f'There was an error creating user [{new_user.full_name}]', 'danger')
        return redirect('/users')

@app.route('/users/<int:user_id>/edit/', methods=["GET"])
def edit_user(user_id):
    """Edit a user's information"""
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update a user's information"""
    try:
        user = User.query.get_or_404(user_id)
        user.first_name = request.form["first-name"].strip()
        user.last_name = request.form["last-name"].strip()
        img_url = request.form["img-url"].strip()
        user.img_url = img_url if img_url else None
        db.session.commit()
        flash(f'User [{user.full_name}] was successfully updated', 'success')
        return redirect('/users')
    except:
        flash(f'There was an error updating user [{user.full_name}]', 'danger')
        return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f'User [{user.full_name}] was successfully deleted', 'success')
        return redirect('/users')
    except:
        flash(f'There was an error deleting user [{user.full_name}]', 'danger')
        return redirect('/users')

############ POSTS ROUTES ############

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details of post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post-detail.html", post=post)

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post(user_id):
    """Add a new post form"""
    user = User.query.get_or_404(user_id)
    return render_template('post-create.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add a new post"""
    try:
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post was successfully created', 'success')
        return redirect(f'/users/{user_id}')
    except:
        flash(f'There was an error creating post [{title}]', 'danger')
        return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit/', methods=["GET"])
def edit_post(post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post-edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Update a post"""
    try:
        post = Post.query.get_or_404(post_id)
        post.title = request.form["title"].strip()
        post.content = request.form["content"].strip()
        db.session.commit()
        flash('Post was successfully updated', 'success')
        return redirect(f'/posts/{post_id}')
    except:
        flash(f'There was an error updating post [{post.title}]', 'danger')
        return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a post"""
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post was successfully deleted', 'success')
        return redirect(f'/users/{post.user_id}')
    except:
        flash(f'There was an error deleting post [{post.title}]', 'danger')
        return redirect(f'/users/{post.user_id}')