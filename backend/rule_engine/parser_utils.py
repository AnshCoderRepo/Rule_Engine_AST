"""
Tokenization and parsing utilities for rule engine AST creation.

This module provides functions and classes for tokenizing rule strings and
parsing them into abstract syntax trees (ASTs).
"""

import re
from typing import List
from rule_engine.ast_utils import Node, ANDOperator, OROperator, Condition

def tokenize(rule: str) -> List[str]:
    """
    Tokenize a rule string into a list of tokens.

    Args:
        rule (str): The rule string to tokenize.

    Returns:
        List[str]: A list of tokens.
    """
    token_pattern = re.compile(r'\s*(=>|<=|>=|&&|\|\||[()=><!]|[\w]+)\s*')
    return [token for token in token_pattern.findall(rule) if token.strip()]

class Parser:
    """
    A parser to convert a list of tokens into an AST.

    Attributes:
        tokens (List[str]): The list of tokens to parse.
        pos (int): The current position in the token list.
    """
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Node:
        """
        Parse the tokens into an AST.

        Returns:
            Node: The root node of the AST.

        Raises:
            ValueError: If the token list is empty.
        """
        if not self.tokens:
            raise ValueError("Empty tokens list")
        return self.parse_expression()

    def parse_expression(self) -> Node:
        """
        Parse an expression from the tokens.

        Returns:
            Node: The root node of the expression.
        """
        node = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('AND', 'OR'):
            operator = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            if operator == 'AND':
                node = Node("operator", left=node, right=right, value=ANDOperator())
            elif operator == 'OR':
                node = Node("operator", left=node, right=right, value=OROperator())
        return node

    def parse_term(self) -> Node:
        """
        Parse a term from the tokens.

        Returns:
            Node: The root node of the term.
        """
        if self.tokens[self.pos] == '(':
            self.pos += 1
            node = self.parse_expression()
            self.pos += 1  # skip ')'
            return node
        else:
            return self.parse_condition()

    def parse_condition(self) -> Node:
        """
        Parse a condition from the tokens.

        Returns:
            Node: The node representing the condition.
        """
        lvariable = self.tokens[self.pos]
        self.pos += 1
        comparison_type = self.tokens[self.pos]
        self.pos += 1
        rvalue = self.tokens[self.pos]
        self.pos += 1
        if rvalue.isdigit():
            rvalue = int(rvalue)
        elif rvalue.replace('.', '', 1).isdigit():
            rvalue = float(rvalue)
        else:
            rvalue = rvalue.strip("'")
        condition = Condition(lvariable, rvalue, comparison_type)
        return Node("operand", value=condition)
