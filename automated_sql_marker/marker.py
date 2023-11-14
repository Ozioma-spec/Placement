# imports
from project_helper_functions.project_helper_functions import get_file_contents, extract_comments, \
    get_task_and_question_numbers_to_mark, extract_task_question_mark, compare_found_marks_comments_expected, \
    extract_statements, get_explain_plan, get_id_prefix, strip_identifier, find_missing_tasks_and_questions
from marking_functions.marking_functions import *
from database_connection import create_connection
from project_classes.answer import Answer
from pathlib import Path
from tree_functions.tree_functions import createtree, print_tree
import time
from tabulate import tabulate
import os

def mark_script(home_dir, sample_file, student_file, display_detail=True):

    curs = create_connection()
    print('sample file actions')
    # sample file
    # sample_file = r'assignment_prep_file\bh38fa_golf_hotel2021_input.sql'
    sample_file_path = os.path.join(home_dir, sample_file)
    sample_file_contents = get_file_contents(Path(sample_file_path))

    # get all comments from sample file variable,
    # used to identify possible mark for each (see extract_task_question_mark)
    sample_file_comments = extract_comments(sample_file_contents)
    print(sample_file_comments)

    # create a dictionary of tasks and questions designated for marking
    tq_to_mark_dict = get_task_and_question_numbers_to_mark(sample_file_comments)
    print(tq_to_mark_dict)

    # use the task/questions dictionary to locate comments containing the mark for each question to mark
    # extract the mark available for said task/question
    # returns a list of tuples each containing (task, question, mark)
    task_question_mark_tuples_list = extract_task_question_mark(sample_file_comments, tq_to_mark_dict)

    # check that marks have been found in the sample file for all answers(statements) defined for marking
    questions_without_marks = compare_found_marks_comments_expected(task_question_mark_tuples_list, tq_to_mark_dict)

    # testing only
    if questions_without_marks:
        print(f"Missing mark criteria: {questions_without_marks}")
    else:
        print("All marks for specified questions were found")

    # extracts all sample answers(statements) for comparison/marking
    print("extract statements")
    print()
    sample_queries = extract_statements(sample_file_contents, task_question_mark_tuples_list)

    # print(task_question_mark_tuples_list)
    print()
    print("creating sample objects for each statement/answer")
    print()
    # create an answer instances for each answer(query) in the sample file
    sample_answer_objects = []
    for task, question, mark, statement in sample_queries:
        answer_objects = Answer(task, question, mark, statement)
        # print(answer_objects)
        # add to a list of sample statement answer objects
        sample_answer_objects.append(answer_objects)

    # get the explain plans for sample answers(queries)
    # set the object explain plan and dataframe attributes
    for answer_object in sample_answer_objects:
        # create id to set for plan
        statement_id = f't{answer_object.task_id}q{answer_object.question_id}'
        #print("QUERY IS " + answer_object.statement)
        # retrieve plan
        ex_plan = get_explain_plan(curs, statement_id, answer_object.query_text)
        # set instance variables explain_plan and plan_dataframe
        answer_object.set_explain_plan(ex_plan)
        answer_object.set_dataframe(ex_plan)
        # print(answer_object)

    # create a tree for each sample answer instance using the instance dataframe
    for answer_object in sample_answer_objects:
        tree = createtree(answer_object.plan_dataframe)
        answer_object.set_tree(tree)

    # print("sample __str__")
    # for answer_objects in sample_answer_objects:
    #     print(answer_objects.__str__())
    #     print()

    print()
    print("STUDENT FILE ACTIONS")
    print()
    # Work with student file
    # sample_file = r'assignment_prep_file\bh38fa_golf_hotel2021_complete.sql'
    student_file_path = os.path.join(home_dir, student_file)

    # get student identifier prefix from sample_file, used to strip from tables
    sid = get_id_prefix(student_file_path)
    student_file_contents = get_file_contents(student_file_path)

    # strip student identifier prefix from tables
    removed_identifier_contents = strip_identifier(sid, student_file_contents)

    # based on the information from the sample file, extract answers(queries) to be marked from student file
    student_queries = extract_statements(removed_identifier_contents, task_question_mark_tuples_list)

    # create a list of answer(query) objects from the statement(answers in the student file
    student_answer_objects = []
    for task, question, mark, statement in student_queries:
        answer_object = Answer(task, question, mark, statement)
        student_answer_objects.append(answer_object)

    # check for missing answers from student file
    # accept the list of sample file objects and list of student file objects
    # checks that answers exist in the student file for each query(question)
    missing_answers = find_missing_tasks_and_questions(sample_answer_objects, student_answer_objects)
    if missing_answers:
        print("Missing answers")
        print(missing_answers)
    else:
        print("All statements found")

    # get the explain plans for student queries
    # set the object explain plan and dataframe attributes
    for answer_object in student_answer_objects:
        statement_id = f't{answer_object.task_id}q{answer_object.question_id}'
        ex_plan = get_explain_plan(curs, statement_id, answer_object.query_text)
        answer_object.set_explain_plan(ex_plan)
        answer_object.set_dataframe(ex_plan)

    # create the tree for each instance of a answer(query/statement) from the student file
    for answer_object in student_answer_objects:
        tree = createtree(answer_object.plan_dataframe)
        answer_object.set_tree(tree)

    # print("student __str__")
    # for answer_objects in student_answer_objects:
    #     print(answer_objects.__str__())
    #     print()

    # Marking
    df_cell_compare_result_dict = compare_all_dataframes(sample_answer_objects, student_answer_objects)
    for key, value in df_cell_compare_result_dict.items():
        print(f"Question: {key} Result: {value}")

    for i, answer in enumerate(sample_answer_objects):
        tid = answer.task_id
        qid = answer.question_id
        for j, ans in enumerate(student_answer_objects):
            if ans.task_id == tid and ans.question_id == qid:
                if sample_answer_objects[i].plan_tree is not None and student_answer_objects[j].plan_tree is not None:
                    print()
                    print("------------------------------------------------------------------------------")
                    print()
                    print("Task:", tid, "Question:", qid)
                    print(f"Sample df {tid}, {qid} ")

                    print(sample_answer_objects[i].query_text)

                    # print(sample_answer_objects[i].display_plan_df())
                    print(f"Student df {student_answer_objects[j].task_id}, {student_answer_objects[j].question_id} ")
                    print(student_answer_objects[j].query_text)

                    # print(student_answer_objects[j].display_plan_df())
                    result = compare_trees(student_answer_objects[j].plan_tree,
                                           sample_answer_objects[i].plan_tree,
                                           display_detail)
                else:
                    if sample_answer_objects[i].plan_tree is not None and student_answer_objects[j].plan_tree is None:
                        print('sample has tree, student no tree')
                    elif sample_answer_objects[i].plan_tree is None and student_answer_objects[j].plan_tree is not None:
                        print('sample no tree, student has tree')
                    else:
                        print("No trees for either")

