"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template, make_response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def base():
    users = User.query.all()

    return render_template('home.html', users=users)


@app.route('/add_user')
def add_user_form():

    return render_template('addUser.html')


@app.route('/add_user', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')


@app.route('/<int:user_id>')
def user_details(user_id):

    user = User.query.get_or_404(user_id)

    if Post.query.filter_by(user=user_id) == True:
        all_posts = Post.query.filter_by(user=user_id)

        resp = make_response(render_template(
            'details.html', user=user, posts=all_posts))
        resp.set_cookie('current_user', str(user_id))
        return resp
    else:
        resp = make_response(render_template(
            'details.html', user=user))
        resp.set_cookie('current_user', str(user_id))
        return resp


@app.route('/about')
def about():

    return render_template('about.html')


@app.route('/update_user')
def update_user():
    user_id = int(request.cookies.get('current_user'))

    user = User.query.get_or_404(user_id)

    return render_template('update_user.html', user=user)


@app.route('/update_user', methods=["POST"])
def update_user_info():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user_id = int(request.cookies.get('current_user'))

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url

    db.session.commit()

    return redirect(f'/{user_id}')


@app.route('/delete_user', methods=["POST", "GET"])
def delete_user():
    user_id = int(request.cookies.get('current_user'))
    all_user_posts = Post.query.filter(Post.user == user_id).all()
    for post in all_user_posts:
        post.delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/')


@app.route('/add_post')
def add_post():
    user_id = int(request.cookies.get('current_user'))
    user = User.query.get_or_404(user_id)

    return render_template('addPost.html', user=user)


@app.route('/add_post', methods=["POST"])
def post_add_post():

    title = request.form["title"]
    content = request.form["content"]
    user_id = int(request.cookies.get('current_user'))

    new_post = Post(title=title, content=content, user=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user_id}')


@app.route('/<int:user_id>/<int:post_id>')
def post_details(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    resp = make_response(render_template(
        'postdetails.html', user=user, post=post))
    resp.set_cookie('selected_post', str(user_id))
    return resp


@app.route('/edit_post', methods=["POST", "GET"])
def edit_post():

    post_id = int(request.cookies.get('selected_post'))
    user_id = int(request.cookies.get('current_user'))
    user = User.query.get_or_404(user_id)
    post = Post.query.filter(Post.id == post_id, Post.user == user_id)

    if request.method == 'POST':

        updated_title = request.form["title"]
        updated_content = request.form["content"]

        # post_id = int(request.cookies.get('selected_post'))
        user_id = int(request.cookies.get('current_user'))

        # post = Post.query.get_or_404(post_id)

        post.title = updated_title
        post.content = updated_content

        db.session.commit()

        return redirect(f'/{user_id}/{post_id}')
    else:

        # user_id = int(request.cookies.get('current_user'))

        # user = User.query.get_or_404(user_id)

        return render_template('edit_post_page.html', user=user, post=post)
