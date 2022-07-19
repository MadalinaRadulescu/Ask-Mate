from crypt import methods
from flask import Flask, render_template, redirect, request, url_for, escape, session
import data_processing
from bonus_questions import SAMPLE_QUESTIONS
import os
from werkzeug.utils import secure_filename
import util
from flask_session import Session


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def main_page():
    if "username" in session:
        logged_message = "Logged in as %s" % escape(session["username"])
    else:
        logged_message = "You are not logged in"
    return render_template(
        "main.html",
        list_question=data_processing.sorting_sql(
            data_processing.QUESITON, "None", "None"
        )[:5],
        logged_message=logged_message,
    )


@app.route("/list")
def question_list():
    if "username" in session:
        logged_message = True
    else:
        logged_message = False
    sort_by = request.args.get("sort-by")
    asc_desc = request.args.get("asc-desc")
    list_question = data_processing.sorting_sql(
        data_processing.QUESITON, sort_by, asc_desc
    )

    return render_template("question-list.html", list_question=list_question, logged_message=logged_message)


@app.route("/question/<question_id>", methods=["GET", "POST"])
def answer_question(question_id):
    answer_list_dic = data_processing.get_all_dic(data_processing.ANSWER)
    list_question = data_processing.get_all_dic(data_processing.QUESITON)
    good_answer_list_dic = data_processing.answer_for_question_sql(question_id)
    tag_list_dic = data_processing.get_all_dic(data_processing.TAG)
    data_processing.update_views(question_id)

    return render_template(
        "answer_question.html",
        good_answer_list_dic=good_answer_list_dic,
        list_question=list_question,
        id=int(question_id),
        comments_list=data_processing.get_all_dic(data_processing.COMMENT),
        tag_list_dic=tag_list_dic,
        used_tags=data_processing.get_all_tags(),
    )


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    question_dic = {}
    list_question = data_processing.get_all_dic(data_processing.QUESITON)
    user_dic = data_processing.get_user_and_password(session["username"])
    if request.method == "POST":
        for title in data_processing.QUESTION_HEADER:
            question_dic["id"] = data_processing.new_max_id(
                data_processing.get_all_dic(data_processing.QUESITON)
            )
            question_dic["submission_time"] = str(data_processing.today_day())
            question_dic["view_number"] = str(0)
            question_dic["vote_number"] = str(0)
            question_dic[title] = request.form.get(title)
        try:
            question_dic["author"] = user_dic["id"]
            data_processing.update_user_interactions("questions_posted", user_dic["id"])
            
        except:
            question_dic["author"] = None
        image = None
        if request.files["File"]:
            f = request.files["File"]
            image = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], image))
        question_dic["image"] = image

        data_processing.add_to_sql(question_dic, data_processing.QUESITON)
        return redirect("/list")

    return render_template(
        "add-question.html", titles=data_processing.QUESTION_HEADER[4:]
    )


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):

    if request.method == "POST":
        data_processing.update_sql(
            question_id,
            data_processing.QUESITON,
            "submission_time",
            f"'{data_processing.today_day()}'",
        )
        for title in data_processing.QUESTION_HEADER[4:]:
            data_processing.update_sql(
                question_id,
                data_processing.QUESITON,
                title,
                request.form.get(title),
            )
        image = None
        if request.files["File"]:
            f = request.files["File"]
            image = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], image))
        data_processing.update_sql(
            question_id, data_processing.QUESITON, "image", f"'{image}'"
        )

        return redirect(url_for("question_list"))
    return render_template(
        "edit-question.html",
        question_id=question_id,
        titles=data_processing.QUESTION_HEADER[4:],
        question_dic=data_processing.select_from_sql(
            question_id, data_processing.QUESITON
        ),
    )


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer_to_question(question_id):
    answer_dic = {}
    answer_list = data_processing.get_all_dic(data_processing.ANSWER)
    user_dic = data_processing.get_user_and_password(session["username"])
    if request.method == "POST":
        for title in data_processing.ANSWER_HEADER:
            answer_dic["id"] = data_processing.new_max_id(
                data_processing.get_all_dic(data_processing.ANSWER)
            )
            answer_dic["submission_time"] = data_processing.today_day()
            answer_dic["vote_number"] = "0"
            answer_dic["question_id"] = question_id
            answer_dic[title] = request.form.get(title)
        try:
            answer_dic["author"] = user_dic["id"]
            data_processing.update_user_interactions("answers_posted", user_dic["id"])
        except:
            answer_dic["author"] = None
        image = None
        if request.files["File"]:
            f = request.files["File"]
            image = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], image))
        answer_dic["image"] = image

        data_processing.add_to_sql(answer_dic, data_processing.ANSWER)
        return redirect(url_for("answer_question", question_id=question_id))

    return render_template(
        "add-answer.html", titles=data_processing.ANSWER_HEADER[4:], id=question_id
    )


@app.route("/question/<question_id>/vote", methods=["GET", "POST"])
def modify_vote(question_id):
    if request.method == "POST":
        vote = request.form.get("vote")
        data_processing.update_voting(question_id, vote, data_processing.QUESITON)

    return redirect("/list")


@app.route("/question/<question_id>/answer/<answer_id>/vote", methods=["GET", "POST"])
def modify_answer_vote(question_id, answer_id):
    if request.method == "POST":
        vote = request.form.get("vote")
        data_processing.update_voting(answer_id, vote, data_processing.ANSWER)

    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    data_processing.delete_from_sql(question_id, data_processing.QUESITON, "id")
    return redirect("/list")


@app.route("/comments/<comment_id>/delete", methods=["GET", "POST"])
def delete_comment_question(comment_id):
    question_id = data_processing.get_question_id(comment_id, data_processing.COMMENT)[
        "question_id"
    ]
    data_processing.delete_from_sql(comment_id, data_processing.COMMENT, "id")
    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/answer/comments/<comment_id>/delete", methods=["GET", "POST"])
def delete_comment_answer(comment_id):
    answer_id = data_processing.get_answer_id(comment_id)["answer_id"]
    question_id = data_processing.get_question_id(answer_id, data_processing.ANSWER)[
        "question_id"
    ]
    data_processing.delete_from_sql(comment_id, data_processing.COMMENT, "id")
    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/question/<question_id>/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(question_id, answer_id):
    data_processing.delete_from_sql(answer_id, data_processing.ANSWER, "id")
    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        user_dic = data_processing.get_user_and_password(session["username"])
        comment_dic = {
            "id": data_processing.new_max_id(
                data_processing.get_all_dic(data_processing.COMMENT)
            ),
            "question_id": question_id,
            "answer_id": None,
            "message": request.form.get("message"),
            "submission_time": data_processing.today_day(),
        }
        try:
            comment_dic["author"] = user_dic["id"]
            data_processing.update_user_interactions("comments_posted", user_dic["id"])
        except:
            comment_dic["author"] = None
        data_processing.add_to_sql(comment_dic, data_processing.COMMENT)
        return redirect(url_for("answer_question", question_id=question_id))
    return render_template(
        "add-comment-question.html",
        id=question_id,
        header=data_processing.COMMENT_HEADER[3],
    )


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment(answer_id):
    question_id = data_processing.get_question_id(answer_id, data_processing.ANSWER)[
        "question_id"
    ]
    if request.method == "POST":
        user_dic = data_processing.get_user_and_password(session["username"])
        comment_dic = {
            "id": data_processing.new_max_id(
                data_processing.get_all_dic(data_processing.COMMENT)
            ),
            "question_id": None,
            "answer_id": answer_id,
            "message": request.form.get("message"),
            "submission_time": data_processing.today_day(),
        }
        try:
            comment_dic["author"] = user_dic["id"]
            data_processing.update_user_interactions("comments_posted", user_dic["id"])
        except:
            comment_dic["author"] = None
        data_processing.add_to_sql(comment_dic, data_processing.COMMENT)
        return redirect(url_for("answer_question", question_id=question_id))
    return render_template(
        "add-comment-answers.html",
        answer_id=answer_id,
        question_id=question_id,
        header=data_processing.COMMENT_HEADER[3],
    )


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    if request.method == "POST":
        question_id = data_processing.get_question_id(
            answer_id, data_processing.ANSWER
        )["question_id"]
        data_processing.update_sql(
            answer_id, data_processing.ANSWER, "message", request.form.get("message")
        )
        image = "no_image.jpg"
        if request.files["File"]:
            f = request.files["File"]
            image = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], image))
        data_processing.update_sql(answer_id, data_processing.ANSWER, "image", image)

        return redirect(url_for("answer_question", question_id=question_id))
    return render_template(
        "edit-answer.html",
        answer_id=answer_id,
        headers=data_processing.ANSWER_HEADER,
        list_dic_answers=data_processing.get_all_dic(data_processing.ANSWER),
    )


@app.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comments(comment_id):
    if request.method == "POST":
        question_id = data_processing.get_question_id(
            comment_id, data_processing.COMMENT
        )["question_id"]
        data_processing.update_sql(
            comment_id, data_processing.COMMENT, "message", request.form.get("message")
        )
        return redirect(url_for("answer_question", question_id=question_id))
    return render_template(
        "edit-comments.html",
        headers=data_processing.COMMENT_HEADER,
        comment_id=comment_id,
    )


@app.route("/question/<question_id>/new-tag", methods=["GET", "post"])
def add_new_tag(question_id):
    new_tag = {
        "id": data_processing.new_max_id(
            data_processing.get_all_dic(data_processing.TAG)
        ),
        "name": request.form.get("new-tag"),
        "question_id": question_id,
    }
    data_processing.add_to_sql(new_tag, data_processing.TAG)
    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_processing.delete_from_sql(tag_id, data_processing.TAG, "id")
    return redirect(url_for("answer_question", question_id=question_id))


@app.route("/bonus-questions")
def bonus_questions():
    return render_template("bonus_questions.html", questions=SAMPLE_QUESTIONS)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    new_user = {}
    if request.method == "POST":
        new_user["id"] = data_processing.new_max_id(
            data_processing.get_all_dic(data_processing.USERS)
        )
        new_user["username"] = request.form.get("username")
        new_user["registration_date"] = data_processing.today_day()
        new_user["questions_posted"] = 0
        new_user["answers_posted"] = 0
        new_user["comments_posted"] = 0
        new_user["reputation"] = 0
        new_user["password"] = util.hash_password(request.form.get("password"))
        data_processing.add_to_sql(new_user, data_processing.USERS)
        return redirect(url_for("main_page"))
    return render_template("registration.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    not_alert= True
    if request.method == "POST":
        user = data_processing.get_user_and_password(request.form["username"])
        if user:
            if util.verify_password(request.form['password'], user["password"]):
                session["username"] = request.form["username"]
                return redirect(url_for("main_page"))
        else:
            not_alert= False
    return render_template("login.html", not_alert=not_alert)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main_page"))

@app.route("/users")
def users_list():
    users_list = data_processing.get_users_list()
    return render_template('users_list.html', users_list=users_list)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
