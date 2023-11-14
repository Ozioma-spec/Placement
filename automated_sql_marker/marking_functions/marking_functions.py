# imports
import pandas as pd
import Levenshtein
from fuzzywuzzy import fuzz
import re


def compare_two_dataframes(df1_sample, df2_student, digits_only=False):
    """
    compares each cell in df2 against the corresponding cell in df1
    any differences or missing values in df2 will be counted as non-matching cells.
    :param df1_sample:
    :param df2_student:
    :param digits_only: default False return string result, True: returns tuple of digits (matching cells, total number of cells in df1, percentage of matches)
    :return: tuple of digits or string based on digits_only boolean
    """
    # Count total cells
    total_cells = df1_sample.size

    # Compare each cell of df2 against df1, count matching cells
    total_cells = df1_sample.size
    matching_cells = 0
    for i in range(df1_sample.shape[0]):
        for j in range(df1_sample.shape[1]):
            if df1_sample.iloc[i, j] == df2_student.iloc[i, j]:
                matching_cells += 1

    # Calculate percentage of matching cells
    percent_matched = round((matching_cells / total_cells) * 100, 2)
    if digits_only:
        # return a tuple of digits only if digits_only set to True
        return matching_cells, total_cells, percent_matched
    else:
        # return a string
        return f"{matching_cells} cells matched out of {total_cells} total cells ({percent_matched}%)"


def compare_all_dataframes(sample_objects, student_objects, digits_only=False):
    """
    compares one dataframe against another on a cell by cell basis
    uses the compare_two_dataframes function bust accepts two lists of answer objects to
    allow for bulk processing
    :param sample_objects: List[Answer]
    :param student_objects: List[Answers]
    :param digits_only: default False: boolean,  if True returns tuple of integers/digits
    :return: dictionary containing a string result or tuple containing
    """
    results_dict = {}
    for i, answer in enumerate(sample_objects):
        tid = answer.task_id
        qid = answer.question_id
        for j, ans in enumerate(student_objects):
            if ans.task_id == tid and ans.question_id == qid:
                result = compare_two_dataframes(sample_objects[i].plan_dataframe,
                                                student_objects[j].plan_dataframe, digits_only=False)
                results_dict[f"t{tid}q{qid}"] = result
    return results_dict


def compare_sql_statements(s1, s2):
    # Tokenize the statements by splitting them into words
    # Not currently used - just compares if the two SQL statements are identical
    # So could be used to return 100% before any further checking is done to enhance efficiency
    words1 = re.findall(r'\w+', s1)
    words2 = re.findall(r'\w+', s2)

    # Compute the number of common words between the two statements
    common_words = set(words1) & set(words2)
    num_common_words = len(common_words)

    # Compute the total number of words in the two statements
    total_words = len(words1) + len(words2)

    # Compute the percentage match between the two statements
    percent_match = (num_common_words / total_words) * 100

    return percent_match


def compare_predicates(pred1, pred2):

    if pred1 is None or pred2 is None:
        return None
    else:
        # Split each predicate on the equals sign (=)
        split1 = pred1.split('=')
        split2 = pred2.split('=')

        # Sort each side of the predicate by table/column name
        split1.sort()
        split2.sort()

    # Compare the sorted predicates
        return split1 == split2


def compare_tree_level(sample_tree, student_tree, results, level=0, print_detail=True):
    node1 = sample_tree.get_node(sample_tree.root)
    node2 = student_tree.get_node(student_tree.root)


    if node1.data['access_predicates'] == node2.data['access_predicates']:
        lev_pred = 0
        fuzz_pred_pr = 100
        fuzz_pred_tsr = 100

    else:
        lev_pred = Levenshtein.distance(node1.data['access_predicates'], node2.data['access_predicates'])
        fuzz_pred_pr = fuzz.partial_ratio(node1.data['access_predicates'], node2.data['access_predicates'])
        fuzz_pred_tsr = fuzz.token_sort_ratio(node1.data['access_predicates'], node2.data['access_predicates'])

    if node1.data['projection'] != node2.data['projection']:
        lev_proj = Levenshtein.distance(node1.data['projection'], node2.data['projection'])
        fuzz_proj_pr = fuzz.partial_ratio(node1.data['access_predicates'], node2.data['access_predicates'])
        fuzz_proj_tsr = fuzz.token_sort_ratio(node1.data['projection'], node2.data['projection'])
    else:
        lev_proj = 0
        fuzz_proj_pr = 100
        fuzz_proj_tsr = 100

    # if we want to print the entire tree
    if print_detail:
        print("\t" * level, node1.identifier, node2.identifier, "\tlev_Pred:", lev_pred, "\tFz-pr_Pred:", fuzz_pred_pr, "\tFz-tsr_Pred:", fuzz_pred_tsr,
            "\tlev_Project:", lev_proj, "\tFz-pr_Project:", fuzz_proj_pr, "\tFz-tsr_project", fuzz_proj_tsr)

    results['Lev_Pred'] += lev_pred
    results['Fz-pr_Pred'] += fuzz_pred_pr
    results['Fz-tsr_Pred'] += fuzz_pred_tsr
    results['Lev_Project'] += lev_proj
    results['Fz-pr_Project'] += fuzz_proj_pr
    results['Fz-tsr_project'] += fuzz_proj_tsr
    results['Tree_levels'] += 1

    for c1 in student_tree.children(student_tree.root):
        compare_tree_level(student_tree.subtree(c1.identifier), sample_tree.subtree(c1.identifier), results, level + 1, print_detail)

def compare_trees(sample_tree, student_tree, display_detail=True):
    results_dict = {'Lev_Pred': 0, 'Fz-pr_Pred': 0, 'Fz-tsr_Pred': 0, 'Lev_Project': 0, 'Fz-pr_Project': 0, 'Fz-tsr_project': 0, 'Tree_levels': 0}
    compare_tree_level(sample_tree, student_tree, results_dict, print_detail=display_detail)
    print("Levenshtein average (Predicate):", 100 - results_dict['Lev_Pred']/results_dict['Tree_levels'], "%")
    print("Fuzzy partial ratio (Predicate):", results_dict['Fz-pr_Pred']/results_dict['Tree_levels'], "%")
    print("Fuzzy token sort ratio (Predicate", results_dict['Fz-tsr_project']/results_dict['Tree_levels'], '%')
    print("Levenshtein average (Projection):", 100 - results_dict['Lev_Project']/results_dict['Tree_levels'], '%')
    print("Fuzzy partial ratio (Projection):", results_dict['Fz-pr_Project']/results_dict['Tree_levels'], '%')
    print("Fuzzy token sort ratio (Projection):", results_dict['Fz-tsr_project']/results_dict['Tree_levels'], "%")
    # Needs updated to print all results and then maybe average
