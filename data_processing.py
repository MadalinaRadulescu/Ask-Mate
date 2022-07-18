import csv
from datetime import datetime
from subprocess import list2cmdline

from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

QUESITON = "question"
ANSWER = "answer"
COMMENT = "comment"
TAG = "tag"

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
    cursor.execute(f""" SELECT * FROM {file} """)
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
        """ SELECT id,vote_number,message FROM answer WHERE question_id = %(id)s """,
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
        f""" SELECT question_id FROM {table} WHERE id = %(answer_id)s """,
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
