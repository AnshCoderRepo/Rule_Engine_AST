"""
Database operations for the rule engine.

This module provides functions to interact with the database for
storing and retrieving rules.
"""

from sqlalchemy.orm import Session
from rule_engine.models import Rule


def get_rule(db: Session, rule_id: int) -> Rule:
    """
    Retrieve a rule from the database by its ID.

    Args:
        db (Session): The database session.
        rule_id (int): The ID of the rule to retrieve.

    Returns:
        Rule: The retrieved rule object.
    """
    return db.query(Rule).filter(Rule.id == rule_id).first()


def create_rule(db: Session, rule_name: str, ast_json: str) -> Rule:
    """
    Create a new rule in the database.

    Args:
        db (Session): The database session.
        rule_name (str): The name of the rule.
        ast_json (str): The JSON representation of the AST for the rule.

    Returns:
        Rule: The created rule object.
    """
    db_rule = Rule(name=rule_name, ast_json=ast_json)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
