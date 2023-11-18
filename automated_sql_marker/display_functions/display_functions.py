# imports
from typing import List, Tuple
from project_classes.answer import Answer
from tabulate import tabulate


def display_sample_student_dataframes(sample_ans_objects, student_ans_objects):
    for i in range(len(sample_ans_objects)):
        print()
        print(f"Sample: {sample_ans_objects[i].query_text}")
        print()
        print(
            tabulate(
                sample_ans_objects[i].plan_dataframe, headers="keys", tablefmt="grid"
            )
        )
        print()
        print(f"Student: {student_ans_objects[i].query_text}")
        print()
        print(
            tabulate(
                student_ans_objects[i].plan_dataframe, headers="keys", tablefmt="grid"
            )
        )
        print()


def display_sample_student_for_question(
    sample_ans_objects, student_ans_objects, task_number, question_number
):
    for i, ans in enumerate(sample_ans_objects):
        if ans.task_id == str(task_number) and ans.question_id == str(question_number):
            print()
            print(f"Sample: {sample_ans_objects[i].query_text}")
            print()
            print(
                tabulate(
                    sample_ans_objects[i].plan_dataframe,
                    headers="keys",
                    tablefmt="grid",
                )
            )
            print()
            print(f"Student: {student_ans_objects[i].query_text}")
            print()
            print(
                tabulate(
                    student_ans_objects[i].plan_dataframe,
                    headers="keys",
                    tablefmt="grid",
                )
            )
            print()


def display_single_df_based_on_question(d_frames, question_number=0):
    print()
    print(
        tabulate(
            d_frames[question_number - 1].plan_dataframe,
            headers="keys",
            tablefmt="grid",
        )
    )


def display_sample_student_for_question(
    sample_ans_objects, student_ans_objects, task_number, question_number
):
    for i, ans in enumerate(sample_ans_objects):
        if ans.task_id == str(task_number) and ans.question_id == str(question_number):
            print()
            print(f"Sample: {sample_ans_objects[i].query_text}")
            print()
            print(
                tabulate(
                    sample_ans_objects[i].plan_dataframe,
                    headers="keys",
                    tablefmt="grid",
                )
            )
            print()
            print(f"Student: {student_ans_objects[i].query_text}")
            print()
            print(
                tabulate(
                    student_ans_objects[i].plan_dataframe,
                    headers="keys",
                    tablefmt="grid",
                )
            )
            print()
