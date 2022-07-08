import csv
from typing import List
from datetime import datetime

QUESITON = "question.csv"
ANSWER = "answer.csv"
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



def get_all_dic(filename):
    list_dictionary_question = []
    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            list_dictionary_question.append(row)
    return list_dictionary_question


def sorting_dictionary_list(list1, title, desc_or_asc):
    if desc_or_asc == "desc":
        return sorted(list1, key=lambda dic: dic[(title)], reverse=False)
    else:
        return sorted(list1, key=lambda dic: dic[(title)], reverse=True)
    

def add_to_csv(filename, dictionary):
    with open(filename, "a") as csv_file:
        writer_csv = csv.DictWriter(csv_file, fieldnames=dictionary.keys())
        writer_csv.writerow(dictionary)


def answer_for_question(id, answer_dic_list):
    good_answer_list = []
    for dic in answer_dic_list:
        if str(id) in list(dic.values())[3]:
            good_answer_list.append(dic["message"])
    return (
        good_answer_list
        if len(good_answer_list) > 0
        else ["This question has no answer"]
    )


def updatate_voting(id, up_down, list_of_dic):
    for dic in list_of_dic:
        if str(id) in list(dic.values())[0]:
            if up_down == "vote-up":
                dic["vote_number"] = int(dic["vote_number"]) + 1
            if up_down == "vote-down":
                dic["vote_number"] = int(dic["vote_number"]) - 1
    return list_of_dic


def rewrite_csv(filename, list_of_dic):
    with open(filename, "r+") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list_of_dic[0].keys())
        csv_file.truncate()
        writer.writeheader()
        for dic in list_of_dic:
            writer.writerow(dic)


def remove_dic_from_list(id, list_dic, value):
    updated_list_dic = []
    for dic in list_dic:
        if dic[value] != str(id):
            updated_list_dic.append(dic)
    return updated_list_dic
