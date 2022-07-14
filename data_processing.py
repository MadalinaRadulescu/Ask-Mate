import csv
from datetime import datetime

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
    query = f"""
        SELECT *
        FROM {file}
        """
    cursor.execute(query)
    return cursor.fetchall()



@database_common.connection_handler
def sorting_sql(cursor,table,column,desc_or_asc):
    if column == "None" or column == None:
        column = "submission_time"
    if desc_or_asc =="None" or desc_or_asc== None:
        desc_or_asc = "DESC"

    query = F"""
        SELECT *
        FROM {table}
        ORDER BY {column} {desc_or_asc}
        """
    cursor.execute(query)
    return cursor.fetchall()



def new_max_id(list_dic):
    return str(int(max([dic["id"] for dic in list_dic])) + 1)



@database_common.connection_handler
def add_to_sql(cursor, dict, table):
    placeholder = ", ".join(["%s"] * len(dict))
    query = "insert into {table} ({columns}) values ({values});".format(
        columns=",".join(dict.keys()), values=placeholder, table=table
    )
    cursor.execute(query, list(dict.values()))


@database_common.connection_handler
def answer_for_question_sql(cursor, id):
    query = """
    SELECT id,vote_number,message
    FROM answer
    WHERE question_id = %(id)s
    """
    user_input = {"id": id}
    cursor.execute(query, user_input)
    return cursor.fetchall()


@database_common.connection_handler
def update_voting(cursor, id, up_down, table):
    vote = 1 if up_down == "vote-up" else -1
    print(vote)
    query = f"UPDATE {table} SET vote_number = vote_number + %(vote)s WHERE id = {id};"
    cursor.execute(query, {"vote": vote})


@database_common.connection_handler
def delete_from_sql(cursor, id, table,column):
    query = f"""
    DELETE FROM {table}
    WHERE {column} = %(id)s
    """
    cursor.execute(query,{"id":id})


@database_common.connection_handler
def update_sql(cursor, id, table, column, user_input):
    query = f"""
    UPDATE {table}
    SET {column} = %(user_input)s
    WHERE id = %(id)s
    """
    cursor.execute(query,{"user_input":user_input,"id": id})


@database_common.connection_handler
def select_from_sql(cursor, id, table):
    query = f"""
    SELECT title,message,image
    FROM {table}
    WHERE id = {id} 
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_question_id(cursor,answer_id,table):
    query = f"""
    SELECT question_id
    FROM {table}
    WHERE id = %(answer_id)s
    """
    cursor.execute(query,{"answer_id":answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_id(cursor,comment_id):
    query = """
    SELECT answer_id
    FROM comment
    WHERE id = %(comment_id)s
    """
    cursor.execute(query,{"comment_id":comment_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_all_tags(cursor):
    query="""
    SELECT name
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


