"""
Module for rule engine AST and related classes.

This module defines the classes and methods to create and evaluate
an Abstract Syntax Tree (AST) for rules, as well as to combine
multiple rules into a single AST.
"""

from typing import List, TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T')

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def evaluate(self, data):
        if self.node_type == 'operand':
            return self.value.evaluate(data[self.value.lvariable])
        elif self.node_type == 'operator':
            return self.value.evaluate(self.left, self.right, data)


class Condition:
    def __init__(self, lvariable, rvalue, comparison_type):
        self.lvariable = lvariable
        self.rvalue = rvalue
        self.comparison_type = comparison_type

    def evaluate(self, input_value):
        if self.comparison_type == 'gt':
            return input_value > self.rvalue
        elif self.comparison_type == 'lt':
            return input_value < self.rvalue
        elif self.comparison_type == 'eq':
            return input_value == self.rvalue
        # Add more comparison types as needed
        return False

class Operator(ABC):
    """
    Abstract base class for operators.
    """

    @abstractmethod
    def evaluate(self, left: Node, right: Node) -> bool:
        """
        Evaluate the operator with given left and right nodes.

        Args:
            left (Node): The left child node.
            right (Node): The right child node.

        Returns:
            bool: The result of the evaluation.
        """
        pass

class ANDOperator(Operator):
    def evaluate(self, left, right, data):
        return left.evaluate(data) and right.evaluate(data)


class OROperator(Operator):
    def evaluate(self, left, right, data):
        return left.evaluate(data) or right.evaluate(data)


class AST:
    def __init__(self, root=None):
        self.root = root

    def evaluate_rule(self, data):
        return self._evaluate_node(self.root, data)

    def _evaluate_node(self, node, data):
        if node is None:
            return True
        return node.evaluate(data)

    def create_rule(self, rule: str) -> bool:
        """
        Create an AST from a rule string.

        Args:
            rule (str): The rule string.

        Returns:
            bool: True if the rule was created successfully.
        """
        from rule_engine.parser_utils import tokenize, Parser

        tokens = tokenize(rule)
        parser = Parser(tokens)
        self.root = parser.parse()
        return True

    def combine_rules(self, rules: List[str]) -> bool:
        """
        Combine multiple rules into a single AST.

        Args:
            rules (List[str]): The list of rule strings.

        Returns:
            bool: True if the rules were combined successfully.
        """
        from rule_engine.parser_utils import tokenize, Parser
        
        # Parse each rule into its AST form
        asts = []
        for rule in rules:
            tokens = tokenize(rule)
            parser = Parser(tokens)
            asts.append(parser.parse())

        # Determine the most frequent operator to use as the root
        operator_count = {'AND': 0, 'OR': 0}
        for rule in rules:
            operator_count['AND'] += rule.count('AND')
            operator_count['OR'] += rule.count('OR')

        most_frequent_operator = 'AND' if operator_count['AND'] >= \
            operator_count['OR'] else 'OR'
        operator_class = ANDOperator if most_frequent_operator == 'AND' \
            else OROperator

        # Combine all ASTs into one using the most frequent operator
        while len(asts) > 1:
            left_ast = asts.pop(0)
            right_ast = asts.pop(0)
            combined_ast = Node(
                node_type="operator",
                left=left_ast,
                right=right_ast,
                value=operator_class()
            )
            asts.append(combined_ast)

        self.root = asts[0]
        return True
