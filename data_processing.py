import csv
from typing import List
from datetime import datetime

from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

QUESITON = "question"
ANSWER = "answer"
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


def today_day():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@database_common.connection_handler
def get_all_dic(cursor,file):
    query = f"""
        SELECT *
        FROM {file}
        """
    cursor.execute(query)
    return cursor.fetchall()


def sorting_dictionary_list(list1, title, desc_or_asc):
    if desc_or_asc == "desc":
        return sorted(list1, key=lambda dic: dic[(title)], reverse=False)
    else:
        return sorted(list1, key=lambda dic: dic[(title)], reverse=True)


def new_max_id():
    return str(int(max([dic["id"] for dic in get_all_dic(QUESITON)])) + 1)


@database_common.connection_handler
def add_to_sql(cursor,dict,table):
    placeholder = ", ".join(["%s"] * len(dict))
    query = "insert into {table} ({columns}) values ({values});".format( columns=",".join(dict.keys()), values=placeholder,table=table)
    cursor.execute(query, list(dict.values()))



@database_common.connection_handler
def answer_for_question_sql(cursor,id):
    query="""
    SELECT message
    FROM answer
    WHERE question_id = %(id)s
    """
    user_input = {"id":id}
    cursor.execute(query,user_input)
    return cursor.fetchall()

@database_common.connection_handler
def update_voting(cursor,id,up_down,table):
    print(up_down)
    if up_down == "vote-up":
        query = f"""
        UPDATE {table}
        SET vote_number = vote_number + 1
        WHERE id = {id};
        """
        cursor.execute(query,table)  
      
    if up_down == "vote-down":
        query = f"""
        UPDATE {table}
        SET vote_number = vote_number - 1
        WHERE id = {id};
        """
        cursor.execute(query,table)



def rewrite_csv(filename, list_of_dic):
    with open(filename, "r+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list_of_dic[0].keys())
        csv_file.truncate()
        writer.writeheader()
        for dic in list_of_dic:
            writer.writerow(dic)


# def remove_dic_from_list(id, list_dic, value):
#     updated_list_dic = []
#     for dic in list_dic:
#         if dic[value] != str(id):
#             updated_list_dic.append(dic)
#     return updated_list_dic


@database_common.connection_handler
def delete_from_sql(cursor,id,table):
    query =f"""
    DELETE FROM {table}
    WHERE id = {id}
    """
    cursor.execute(query)

