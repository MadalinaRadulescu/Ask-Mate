from datetime import datetime
from subprocess import list2cmdline
from typing import List, Dict
import psycopg2
import database_common
import util

QUESITON = "question"
ANSWER = "answer"
COMMENT = "comment"
TAG = "tag"
USERS = "users"

QUESTION_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image",
]
ANSWER_HEADER = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]

COMMENT_HEADER = [
    "id",
    "question_id",
    "answer_id",
    "message",
    "submission_time",
    "edited_count",
]


def today_day():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@database_common.connection_handler
def get_all_dic(cursor, file):
    cursor.execute(f" SELECT * FROM {file} ")
    return cursor.fetchall()


@database_common.connection_handler
def sorting_sql(cursor, table, column, desc_or_asc):
    if column == "None" or column == None:
        column = "submission_time"
    if desc_or_asc == "None" or desc_or_asc == None:
        desc_or_asc = "DESC"
    cursor.execute(f""" SELECT * FROM {table} ORDER BY {column} {desc_or_asc} """)
    return cursor.fetchall()


def new_max_id(list_dic):
    return str(int(max([dic["id"] for dic in list_dic])) + 1)


@database_common.connection_handler
def add_to_sql(cursor, dict, table):
    cursor.execute(
        "insert into {table} ({columns}) values ({values});".format(
            columns=",".join(dict.keys()),
            values=", ".join(["%s"] * len(dict)),
            table=table,
        ),
        list(dict.values()),
    )


@database_common.connection_handler
def answer_for_question_sql(cursor, id):
    cursor.execute(
        """ SELECT id,vote_number,message,accepted,image FROM answer WHERE question_id = %(id)s """,
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def update_voting(cursor, id, up_down, table):
    vote = 1 if up_down == "vote-up" else -1
    cursor.execute(
        f"UPDATE {table} SET vote_number = vote_number + %(vote)s WHERE id = {id};",
        {"vote": vote},
    )


@database_common.connection_handler
def delete_from_sql(cursor, id, table, column):
    cursor.execute(f""" DELETE FROM {table} WHERE {column} = %(id)s """, {"id": id})


@database_common.connection_handler
def update_sql(cursor, id, table, column, user_input):
    cursor.execute(
        f""" UPDATE {table} SET {column} = %(user_input)s WHERE id = %(id)s """,
        {"user_input": user_input, "id": id},
    )


@database_common.connection_handler
def select_from_sql(cursor, id, table):
    cursor.execute(f""" SELECT title,message,image FROM {table} WHERE id = {id} """)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_id(cursor, answer_id, table):
    cursor.execute(
        f" SELECT question_id FROM {table} WHERE id = %(answer_id)s ",
        {"answer_id": answer_id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_id(cursor, comment_id):
    cursor.execute(
        """ SELECT answer_id FROM comment WHERE id = %(comment_id)s """,
        {"comment_id": comment_id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute(""" SELECT name FROM tag """)
    return cursor.fetchall()


@database_common.connection_handler
def update_views(cursor, question_id):
    cursor.execute(
        "UPDATE question SET view_number = view_number + 1 WHERE id = %(id)s;",
        {"id": question_id},
    )


@database_common.connection_handler
def get_user_and_password(cursor, user):
    cursor.execute(
        "SELECT id, username, password FROM users WHERE username = %(user)s;",
        {"user": user},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_users_list(cursor):
    cursor.execute(
        "SELECT id, username, registration_date, questions_posted, answers_posted, comments_posted, reputation FROM users",
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_user_by_id(cursor, user_id):
    cursor.execute(
        "SELECT id, username, registration_date, questions_posted, answers_posted, comments_posted, reputation FROM users WHERE id = %(id)s;",
        {"id": user_id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def update_user_interactions(cursor, column, user_id):
    cursor.execute(
        f"UPDATE users SET {column} = {column} + 1 WHERE id = %(user_id)s",
        {"column": column, "user_id": user_id},
    )


@database_common.connection_handler
def get_acceptance(cursor, answer_id):
    cursor.execute(
        "SELECT accepted FROM answer where id = %(answer_id)s", {"answer_id": answer_id}
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_user_posts(cursor, user_id, table):
    cursor.execute(
        f""" SELECT * FROM {table} WHERE author = %(id)s """, {"id": user_id}
    )
    return cursor.fetchall()


def insert_tag(cursor, question_id, tag_text):
    cursor.execute(
        "INSERT INTO tag (name) VALUES (%(tag_text)s) RETURNING id;",
        {"tag_text": tag_text},
    )
    new_id = cursor.fetchone()["id"]
    cursor.execute(
        "INSERT INTO question_tag (question_id, tag_id) VALUES (%(qid)s, %(tid)s);",
        {"qid": question_id, "tid": new_id},
    )


@database_common.connection_handler
def update_answer_acceptance(cursor, answer_id):
    parameter = get_acceptance(answer_id)["accepted"]
    cursor.execute(
        f"UPDATE answer SET accepted = NOT %(parameter)s WHERE id = %(answer_id)s",
        {
            "answer_id": answer_id,
            "parameter": parameter,
        },
    )


@database_common.connection_handler
def update_user_reputation(cursor, user_id, value):
    cursor.execute(
        "UPDATE users SET reputation = reputation + %(value)s WHERE id = %(user_id)s",
        {"user_id": user_id, "value": value},
    )


@database_common.connection_handler
def get_author_id(cursor, question_id, table):
    cursor.execute(
        f"SELECT author FROM {table} WHERE id = %(question_id)s",
        {"question_id": question_id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute(
        "SELECT id FROM users WHERE username=%(username)s", {"username": username}
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_tags(cursor):
    cursor.execute(
        " SELECT DISTINCT name, count(tag.name) FROM tag GROUP BY tag.name"
    )
    return cursor.fetchall()


@database_common.connection_handler
def count_edit_comments(cursor,comment_id):
    cursor.execute(
        " UPDATE comment SET edited_count = edited_count + 1 WHERE id=%(comment_id)s ",
        {"comment_id":comment_id},
    )



