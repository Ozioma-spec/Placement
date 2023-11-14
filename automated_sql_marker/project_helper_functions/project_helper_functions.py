# imports
import oracledb
import sys
import re
from utility_functions.utilities import mid_string, validate_number_in_string
from pathlib import Path
from typing import List, Tuple
from project_classes.answer import Answer


def get_id_prefix(file_path):
    """
    get all filenames or student identifiers from directory to which they have been copied
        -makes all filepaths or identifiers lowercase
        -assumes that files in directory have been previously filtered for .sql extension
    :param file_path: director of previously copied sql files
    :return: student identifier(True)
    """
    # define the pattern to identify student id at start of file name
    # bh27pf, fg35hh etc
    file_path = Path(file_path)
    filename = file_path.name
    sid_pattern = re.compile(r'^[a-z]{2}[0-9]{2}[a-z]{2}', re.IGNORECASE)
    sid_match = sid_pattern.match(filename)
    if sid_match:
        return sid_match.group()
    else:
        raise "Missing student identifier"


def strip_identifier(student_id, file_contents):
    pattern = re.compile(r'{}_'.format(student_id), re.I)
    mo = re.search(pattern, file_contents)
    if mo:
        file_contents = re.sub(mo.group(), '', file_contents)
    return file_contents


def get_file_contents(file_path):
    """
    Read each file in a directory to a variable
    strip any tab whitespace
    Add file contents variable to list
    :param file_path:
    :return: contents of file as string
    """
    # if file_path == "";
    #     raise ('No file path supplied')
    try:
        with open(Path(file_path), "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
            return "\n".join(lines)

    except FileNotFoundError:
        print("Error! No such file or directory")
    except PermissionError:
        if file_path == '':
            print("Error! Invalid file path supplied")
    except Exception as ex:
        print(ex)
        print("Error! Please supply a valid file path")


def extract_comments(sql_file_contents):
    """
    Takes the contents of a sql file and extracts the comment lines to a list
    :param sql_file_contents:
    :return: List comments or empty list if none found
    """
    comments = []
    if sql_file_contents:
        for line in sql_file_contents.splitlines():
            if line.strip().startswith('/*') and line.strip().endswith('*/'):
                # check there is valid data between the comment delimiters
                if mid_string(line, '/*', '*/').strip():
                    # add to comments list
                    comments.append(line)

    return comments


def get_task_and_question_numbers_to_mark(comments_list):
    """
    Takes sql sample file content as a string:
    if the file contains details of task and questions to mark it extracts them to
    a dictionary with task as key and list of questions as values {task:[questions to mark]}
    line containing questions must be structured as: /* <task: n - questions: n1, n2, n3, n......> */
    :return: dictionary
    """
    task_and_questions = {}
    # split content on newline:
    for comment in comments_list:
        task_number = ''
        question_numbers = []
        # locate delimited line, if not found dictionary will return none type:
        if "/* <" in comment and "> */" in comment:
            # uses a utility method mid-string  to substring between delimiters('task:' and '-'):
            task_number_string = mid_string(comment, "task:", "-").replace(" ", "")

            questions_number_string = mid_string(comment, "questions:", ">").replace(" ", "")
            try:
                # audit for valid number and not empty string:
                task_number = validate_number_in_string(task_number_string)
                if task_number == '':
                    raise ValueError("No task value provided")
            except ValueError:
                print("\nError reading marking criteria!\n"
                      "No task number provided or formatting issue in marking details\n")
                sys.exit(1)

            try:
                # test and validate question numbers:
                # if no numbers are provided question_numbers will return empty and be handled by try/except:
                for number in questions_number_string.split(","):
                    # test for valid number/digit:
                    question = validate_number_in_string(number)
                    # if valid add to list
                    if question:
                        question_numbers.append(question)
                # remove duplicate question numbers by converting to a set:
                question_numbers = (list(set(question_numbers)))
                # raise exception if no question numbers found to mark:
                if not question_numbers:
                    raise ValueError("Invalid question number provided")
            except ValueError:
                print("\nError reading marking criteria!\n"
                      "No question numbers provided or formatting issue in marking details of file\n")
                sys.exit(1)
            task_and_questions[task_number] = sorted(question_numbers, key=lambda x: int(x))
    # Ensure task_and_questions dictionary contains data
    # catches files with no marking criteria provided
    try:
        if task_and_questions:
            return task_and_questions
        else:
            raise ValueError("No comment lines in file or marking criteria not supplied")
    except ValueError:
        print("\nError! No valid comment lines in file or\n"
              "marking criteria not provided!\n")
        sys.exit(1)


def extract_task_question_mark(comments_list, tq_to_mark_dict):
    """
    Takes a dictionary of task:[questions_list], uses the dictionary to locate matching task/questions within the comment_lines list
    If found the mark for task/question is extracted and a tuple made to hold the combination of (task, question, mark)
    :return: tuple: (task, question, mark)
    """
    t_q_m_tuples_list = []
    # missing_questions = []  # remove when moved to new function
    # TODO:
    #   add exception try catch

    # use the tasks & questions numbers in tq_to_mark_dict to identify the associated mark
    # in the comment line of the specified question.
    # Searches the list of comments previously extracted from the file contents
    for comment in comments_list:
        # strip common delimiter/separation characters and spaces for easier patter detection
        comment = comment.translate(str.maketrans({':': '', '-': '', ' ': ''}))
        pattern = re.compile(r'task(\d+)question(\d+)\w*\[(\d+)]', re.IGNORECASE)
        match = pattern.search(comment)
        # check each comment for pattern match
        # if a match is found in comments, check if it is a task/question that should be marked
        if match:
            task_number = match.group(1)
            question_number = match.group(2)
            # check if the task and question in the comment line exist in the tq_to_mark_dict
            # if yes, it needs to be marked. capture the mark from the comment line,
            # append a tuple of (task, question, mark) for every task/question found that needs to be marked
            if task_number in tq_to_mark_dict:
                if question_number in tq_to_mark_dict[task_number]:
                    t_q_m_tuples_list.append(match.groups())
    return t_q_m_tuples_list


def compare_found_marks_comments_expected(found_marks_tuples_list, tq_to_mark_dict):
    tq_without_marks_tuples_list = []
    try:

        if found_marks_tuples_list:
            # ensure all questions specified for marking have an accompanying mark defined
            # iterate each task/key in dictionary
            for task, questions in tq_to_mark_dict.items():
                # iterate through questions for task
                for question in questions:
                    # set to not found
                    found = False
                    # check that all tasks and questions required for marking have an accompanying possible mark
                    # by checking they exist in the task, question, mark tuples
                    for t, q, m in found_marks_tuples_list:
                        # if task and question found, a mark must have been located in the comment line
                        if t == task and q == question:
                            found = True
                            break
                        # if the task and question exist in the task/question dictionary but not in the tuples,
                        # No mark was found and needs to be flagged
                    if not found:
                        # create a list of task/question tuples missing a mark
                        tq_without_marks_tuples_list.append((task, question))
        else:
            raise ValueError('No marks supplied for questions')
    except ValueError:
        print('Error! No marks supplied for any question you requested marking')

    return tq_without_marks_tuples_list


def extract_table_aliases(sql_statement):
    """
    Accepts a sql statement, parses the statement to locate table aliases.
    if table aliases are found they are added to a dictionary of
    :param sql_statement:
    :return:
    """
    # Replace all SQL keywords with commas
    keywords = [
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'AND', 'OR', 'ORDER BY',
        'GROUP BY', 'HAVING', 'AS', 'IN', 'LIKE', 'NOT', 'NULL', 'IS',
        'BETWEEN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'EXISTS', 'ALL',
        'ANY', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN',
        'NATURAL JOIN', 'USING', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX',
        'ROUND', 'CAST', 'AS', 'DISTINCT', 'UNION', 'INTERSECT', 'EXCEPT',
        'AS', 'ON', 'AS', 'ASC', 'DESC', 'LIMIT', 'OFFSET', 'FETCH', 'FIRST',
        'NEXT', 'ONLY', 'ROW', 'ROWS', 'OVER', 'PARTITION', 'BY', 'RANK',
        'DENSE_RANK', 'NTILE', 'LAG', 'LEAD', 'FIRST_VALUE', 'LAST_VALUE',
        'NTH_VALUE', 'PERCENT_RANK', 'CUME_DIST', 'IGNORE NULLS', 'RESPECT NULLS',
        'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'LOCALTIME', 'LOCALTIMESTAMP, USING'
    ]

    for keyword in keywords:
        sql_statement = re.sub(rf'(?i)\b{keyword}\b', ',', sql_statement, re.IGNORECASE)
    sql_statement = sql_statement.strip()
    # Extract table names and aliases using regular expressions
    table_aliases = {}
    for s in sql_statement.split(','):
        pattern = re.compile(r'\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*')
        match = re.search(pattern, s)
        if match:
            table_aliases[match.group(2)] = match.group(1)
    return table_aliases


def normalise_table_aliases(sql_statement):
    table_aliases = extract_table_aliases(sql_statement)
    # Replace table aliases with table names in columns
    for table_alias, table_name in table_aliases.items():
        pattern = re.compile(rf'\b{table_alias}\.(\w+)\b')
        sql_statement = re.sub(pattern, rf'{table_name}.\1', sql_statement)

    # Remove table aliases from table names
    for table_alias, table_name in table_aliases.items():
        pattern = re.compile(rf'\b{table_name}\s+{table_alias}\b')
        sql_statement = re.sub(pattern, table_name, sql_statement)

    return sql_statement


def extract_statements(sql_file_contents, tqm_tuples_list):
    found_statements = []

    # read the SQL file line by line
    # with open(sql_file_path, 'r') as f:
    lines = sql_file_contents.splitlines()

    # loop through each tuple in the list of tuples containing task, question mark
    for task_number, question_number, mark_available in tqm_tuples_list:
        # create a matchable string variable for task and question
        # used to locate delimiter comment containing the strings 'task(n) and question(n)
        task_n = "task" + str(task_number)
        question_n = "question" + str(question_number)

        # loop through the SQL file lines to locate comments containing task(n) AND question(n)
        # capture all lines that follow until ';' is found or another comment line, this should construct the SQL statement
        sql_statement_lines = []
        # flag for found comment line
        found_task = False
        for i, line in enumerate(lines):
            # sanitize each line, to make the comment line uniform for comparison
            sanitized_line = line.lower().translate(str.maketrans({':': '', '-': '', ' ': ''}))

            # if line contains both task(n) and question(n) flag as found
            # once comment line found, capture the lines that follow (building the sql statement).
            if task_n in sanitized_line and question_n in sanitized_line:
                found_task = True
            elif found_task:  # when comment line matches task and question

                if line.startswith('/*'):
                    break
                    # add line to current collection of lines
                else:
                    sql_statement_lines.append(line)
                    # break out of current task/question capture loop.
                    # end of statement found.

        # join and clean extracted lines to create single statement
        sql_statement = ' '.join(sql_statement_lines).strip(';')
        sql_statement = re.sub(r"[ \t]+", " ", sql_statement).strip()

        # normalise select statement table aliases
        if sql_statement.lower().startswith('select'):
            sql_statement = normalise_table_aliases(sql_statement)

            found_statements.append((task_number, question_number, mark_available, sql_statement))
        # filter for select statements or return all
        elif sql_statement != '':
            found_statements.append((task_number, question_number, mark_available, sql_statement))
            # found_statements.append(sql_statement)
    return found_statements


def get_explain_plan(cursor, statement_id, query):
    # list to hold explain plan(rows) for each statement/query
    plan = []
    # set statement ID for reference in explain table
    query_id = f"\'{statement_id}\'"

    # prepare statement to remove any previous reference from the explain plan table which would collide with the
    # current statement ID
    del_plan = f"DELETE FROM plan_table WHERE statement_id = {query_id}"

    # Execute the prepared delete statement
    cursor.execute(del_plan)

    # Prepare the statement to set ID and retrieve explain plan
    explain_query = f"EXPLAIN PLAN SET STATEMENT_ID = {query_id} FOR {query}"

    try:
        # Execute explain query
        cursor.execute(explain_query)

        # Prepare query statement to retrieve explain plan
        plan_table_query = f'SELECT operation, object_name, object_type, id, parent_id, depth, position, access_predicates, projection FROM plan_table WHERE statement_id = {query_id}'
        # Execute the retrieval of the explain plan from the plan table
        returned_plan = cursor.execute(plan_table_query)

        for row in returned_plan:
            # Add row to list
            plan.append(row)

    except oracledb.DatabaseError as exc:
        error, = exc.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
    else:
        return plan


def find_missing_tasks_and_questions(sample_list: List[Answer], test_list: List[Answer]) -> List[Tuple[str, str]]:
    missing_tasks_and_questions = []
    for sample_ans in sample_list:
        found = False
        for student_ans in test_list:
            if sample_ans.task_id == student_ans.task_id and sample_ans.question_id == student_ans.question_id:
                found = True
                break
        if not found:
            missing_tasks_and_questions.append((sample_ans.task_id, sample_ans.question_id))
    return missing_tasks_and_questions



# if __name__ == '__main__':
