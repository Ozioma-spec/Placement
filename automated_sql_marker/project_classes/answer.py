# imports
# imports
import pandas as pd
import tabulate
from tree_functions.tree_functions import print_tree


class Answer:
    def __init__(
        self, task_id: str, question_id: str, available_mark: str, query_text: str
    ) -> None:
        self.task_id = task_id
        self.question_id = question_id
        self.statement_id = (int(task_id), int(question_id))  # creates tnqn for ref
        self.available_mark = available_mark
        self.query_text = query_text
        self.explain_plan = None
        self.plan_dataframe = None
        self.plan_tree = None

    def set_explain_plan(self, explain_plan):
        # execute database query to retrieve explain plan based on self.query_text
        # update self.explain_plan with the retrieved information
        self.explain_plan = explain_plan

    def set_dataframe(self, explain_plan):
        df = pd.DataFrame(
            self.explain_plan,
            columns=[
                "operation",
                "object_name",
                "object_type",
                "id",
                "parent_id",
                "depth",
                "position",
                "access_predicates",
                "projection",
            ],
        )

        self.plan_dataframe = df.sort_values("id")

    def set_tree(self, tree):
        if tree is None:
            pass
        else:
            self.plan_tree = tree

    def display_tree(self):
        if self.plan_tree is None:
            print("No tree Available")
        else:
            print_tree(self.plan_tree, level=0)

    def display_statement_id(self):
        print(self.statement_id)

    def display_plan_df(self):
        print(tabulate.tabulate(self.plan_dataframe, headers="keys", tablefmt="grid"))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"task_id={self.task_id!r}, "
            f"question_id={self.question_id!r}, "
            f"statement_id={self.statement_id!r}, "
            f"available_mark={self.available_mark!r}, "
            f"query_text={self.query_text!r}, "
            f"explain_plan={self.explain_plan}, "
            f"plan_dataframe=\n{self.plan_dataframe}\n"
            f"plan_tree={self.display_tree()}"
            f")\n"
        )

    def __str__(self):
        title_divide = f"QUERY: t{self.task_id}q{self.question_id}"
        print("{:*^200}".format(title_divide))
        print(f"TASK ID:" f"{self.task_id}")
        print(f"QUESTION ID:" f"{self.question_id}\n")
        print(f"QUERY STATEMENT: " f"{self.query_text}\n")
        print(f"EXPLAIN PLAN:" f"{self.explain_plan}\n")
        print(f"PLAN TABLE:")
        if self.plan_dataframe is None:
            print("No plan table")
        else:
            print(f"{self.plan_dataframe.to_markdown()}\n")
        print(f"PLAN TREE:")
        print(f"{self.display_tree()}\n")

        # print(tabulate(self.explain_dataframe, headers='keys', tablefmt="grid"))
