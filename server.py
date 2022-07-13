from codecs import ascii_decode
from crypt import methods
from flask import Flask, render_template, redirect, request, url_for
import data_processing
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/images"


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/list")
def question_list():
    sort_by = request.args.get("sort-by")
    asc_desc = request.args.get("asc-desc")
    if sort_by:
        list_question = data_processing.sorting_dictionary_list(
            data_processing.get_all_dic(data_processing.QUESITON), sort_by, False
        )
    if asc_desc:
        list_question = data_processing.sorting_dictionary_list(
            data_processing.get_all_dic(data_processing.QUESITON),
            "submission_time",
            asc_desc,
        )
    if sort_by and asc_desc:
        list_question = data_processing.sorting_dictionary_list(
            data_processing.get_all_dic(data_processing.QUESITON), sort_by, asc_desc
        )

    else:
        list_question = data_processing.sorting_dictionary_list(
            data_processing.get_all_dic(data_processing.QUESITON), "id", False
        )
    return render_template("question-list.html", list_question=list_question)


@app.route("/question/<question_id>", methods=["GET", "POST"])
def answer_question(question_id):
    answer_list_dic = data_processing.get_all_dic(data_processing.ANSWER)
    list_question = data_processing.get_all_dic(data_processing.QUESITON)
    good_answer_list_dic = data_processing.answer_for_question_sql(question_id)

    return render_template(
        "answer_question.html",
        good_answer_list_dic=good_answer_list_dic,
        list_question=list_question,
        id=int(question_id),
        comments_list = data_processing.get_all_dic(data_processing.COMMENT)
    )


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    question_dic = {}
    list_question = data_processing.get_all_dic(data_processing.QUESITON)
    if request.method == "POST":
        for title in data_processing.QUESTION_HEADER:
            question_dic["id"] = data_processing.new_max_id(data_processing.get_all_dic(data_processing.QUESITON))
            question_dic["submission_time"] = str(data_processing.today_day())
            question_dic["view_number"] = str(0)
            question_dic["vote_number"] = str(0)
            question_dic[title] = request.form.get(title)
        image = "no_image.jpg"
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
        image = "no_image.jpg"
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
    if request.method == "POST":
        for title in data_processing.ANSWER_HEADER:
            answer_dic["id"] = data_processing.new_max_id(data_processing.get_all_dic(data_processing.ANSWER))
            answer_dic["submission_time"] = data_processing.today_day()
            answer_dic["vote_number"] = "0"
            answer_dic["question_id"] = question_id
            answer_dic[title] = request.form.get(title)
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
    if request.method == "POST":
        data_processing.delete_from_sql(question_id, data_processing.QUESITON)
    return redirect("/list")


@app.route("/question/<question_id>/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(question_id, answer_id):
    data_processing.delete_from_sql(answer_id, data_processing.ANSWER)
    return redirect("/list")

@app.route("/question/<question_id>/new-comment",methods=["GET","POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        comment_dic ={
            "id": data_processing.new_max_id(data_processing.get_all_dic(data_processing.COMMENT)),
            "question_id":question_id,
            "answer_id": None,
            "message" : request.form.get("message"),
            "submission_time": data_processing.today_day(),
           

        }
        data_processing.add_to_sql(comment_dic,data_processing.COMMENT)
        return redirect(url_for('answer_question',question_id=question_id))
    return render_template(
        "add-comment-question.html",
        id=question_id,
        header=data_processing.COMMENT_HEADER[3],
        )

@app.route("/answer/<answer_id>/new-comment",methods=["GET","POST"])
def add_answer_comment(answer_id):
    question_id = data_processing.get_question_id_by_answer_id(answer_id)["question_id"]
    if request.method == "POST":
        
        comment_dic ={
            "id": data_processing.new_max_id(data_processing.get_all_dic(data_processing.COMMENT)),
            "question_id":None,
            "answer_id": answer_id,
            "message" : request.form.get("message"),
            "submission_time": data_processing.today_day(),
        }
        data_processing.add_to_sql(comment_dic,data_processing.COMMENT)
        return redirect(url_for('answer_question',question_id=question_id))
    return render_template(
        "add-comment-answers.html",
        answer_id=answer_id,
        question_id=question_id,
        header=data_processing.COMMENT_HEADER[3]
        )
    


if __name__ == "__main__":
    app.run(debug=True,
    port=5002)
