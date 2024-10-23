"""
FastAPI application for the rule engine.

This module provides API endpoints for creating, combining, and evaluating rules.
"""

import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from rule_engine import models, database
from rule_engine.parser_utils import Parser, tokenize
from rule_engine.ast_utils import ANDOperator, Condition, Node, AST, OROperator

app = FastAPI()

class RuleString(BaseModel):
    """Pydantic model for a rule string."""
    rule: str
    name: str

class RuleList(BaseModel):
    """Pydantic model for a list of rule strings."""
    rules: List[str]

class EvaluateRequest(BaseModel):
    """Pydantic model for an evaluation request."""
    rule_id: int
    data: Dict

class ASTNode(BaseModel):
    """Pydantic model for an AST node."""
    node_type: str
    left: Dict = None
    right: Dict = None
    value: Dict = None

def get_db():
    """
    Dependency for obtaining the database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_rule", response_model=ASTNode)
def create_rule(rule_string: RuleString, db: Session = Depends(get_db)):
    """
    Create a new rule and store it in the database.

    Args:
        rule_string (RuleString): The rule string and name.
        db (Session): The database session.

    Returns:
        ASTNode: The root node of the created AST.
    """
    tokens = tokenize(rule_string.rule)
    parser = Parser(tokens)
    try:
        root = parser.parse()
        ast_json = root_to_json(root)
        database.create_rule(db, rule_string.name, ast_json)
        return JSONResponse(ast_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules", response_model=ASTNode)
def combine_rules(rule_list: RuleList):
    """
    Combine multiple rules into a single AST.

    Args:
        rule_list (RuleList): The list of rule strings.

    Returns:
        ASTNode: The root node of the combined AST.
    """
    combined_root = None
    for rule in rule_list.rules:
        tokens = tokenize(rule)
        parser = Parser(tokens)
        root = parser.parse()
        if combined_root is None:
            combined_root = root
        else:
            combined_root = Node(
                node_type="operator",
                left=combined_root,
                right=root,
                value=ANDOperator()
            )
    return JSONResponse(root_to_json(combined_root))

@app.post("/evaluate_rule")
def evaluate_rule(request: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Evaluate a rule against provided data.

    Args:
        request (EvaluateRequest): The evaluation request containing rule ID and data.
        db (Session): The database session.

    Returns:
        Dict: The evaluation result.
    """
    db_rule = database.get_rule(db, request.rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    ast = json_to_ast(db_rule.ast_json)
    result = ast.evaluate_rule(request.data)
    return {"result": result}

def root_to_json(root: Node) -> str:
    """
    Convert an AST root node to JSON.

    Args:
        root (Node): The root node of the AST.

    Returns:
        str: The JSON representation of the AST.
    """
    if root is None:
        return ""
    return json.dumps(root, default=lambda o: o.__dict__)

def json_to_ast(json_str: str) -> AST:
    """
    Convert a JSON string to an AST.

    Args:
        json_str (str): The JSON string representing the AST.

    Returns:
        AST: The AST object.
    """
    data = json.loads(json_str)
    root = dict_to_node(data)
    return AST(root)

def dict_to_node(data: dict) -> Node:
    """
    Convert a dictionary to an AST node.

    Args:
        data (dict): The dictionary representing the node.

    Returns:
        Node: The AST node.
    """
    if data is None:
        return None
    node = Node(node_type=data['node_type'])
    node.left = dict_to_node(data.get('left'))
    node.right = dict_to_node(data.get('right'))
    if data['node_type'] == 'operand':
        node.value = Condition(
            lvariable=data['value']['lvariable'],
            rvalue=data['value']['rvalue'],
            comparison_type=data['value']['comparison_type']
        )
    else:
        operator = data['value']
        if operator == 'ANDOperator':
            node.value = ANDOperator()
        elif operator == 'OROperator':
            node.value = OROperator()
    return node

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
