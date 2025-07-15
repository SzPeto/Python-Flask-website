from flask import Blueprint, flash, request, redirect, url_for, render_template, abort
from flask_login import login_user, current_user, login_required, logout_user

from website.db_models import Post, db
from website.blog.validators import *

blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route("/blog", methods=["GET", "POST"])
def blog():
    # get the page number from args - after ? in url, access the multidict value of "page", if no value, default it
    # to 1 and automatically convert the value to int
    user_id = request.args.get("user_id", None, type=int)
    page = request.args.get("page", 1, type=int)
    if user_id:
        user_posts = Post.query.filter_by(user_id=user_id)
        ordered_posts = user_posts.order_by(Post.date_posted.desc())
        posts = ordered_posts.paginate(page=page, per_page=5)
    else:
        ordered_posts = Post.query.order_by(Post.date_posted.desc())
        posts = ordered_posts.paginate(page=page, per_page=5)

    return render_template("blog.html", title="Blog", posts=posts,
                           current_user=current_user, current_page=page, user_id=user_id)

@blog_bp.route("/insert-post", methods=["GET", "POST"])
@login_required
def insert_post():
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.post_title.data
            content = form.post_content.data
            user_id = current_user.id
            entry = Post(content=content, title=title, user_id=user_id)
            db.session.add(entry)
            db.session.commit()
            flash("Post added", "success")
            return redirect(url_for("blog_bp.blog"))
        else:
            if form.post_title.errors:
                for error in form.post_title.errors:
                    flash(error, "warning")
            if form.post_content.errors:
                for error in form.post_content.errors:
                    flash(error, "warning")

    return render_template("insert-post.html", title="Insert post", current_user=current_user,
                           form=form)

@blog_bp.route("/blog/delete-post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    entry = db.session.get(Post, post_id)
    if not entry:
        abort(404)
    if current_user.id != entry.user.id and current_user.id != 1:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash("The post has been successfully deleted!", "success")

    return redirect(url_for("blog_bp.blog"))

@blog_bp.route("/blog/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = PostForm()
    entry = db.session.get(Post, post_id)
    if not entry:
        abort(404)
    if current_user.id != entry.user_id and current_user.id != 1:
        abort(403)
    if request.method == "POST":
        if form.validate_on_submit():
            entry.title = form.post_title.data
            entry.content = form.post_content.data
            db.session.commit()
            flash("Post successfully updated", "success")
            return redirect(url_for("blog_bp.blog"))
        else:
            if form.post_title.errors:
                for error in form.post_title.errors:
                    flash(error, "warning")
            if form.post_content.errors:
                for error in form.post_content.errors:
                    flash(error, "warning")


    form.post_title.data = entry.title
    form.post_content.data = entry.content

    return render_template("edit-post.html", title="Edit post", current_user=current_user,
                           form=form, entry=entry)