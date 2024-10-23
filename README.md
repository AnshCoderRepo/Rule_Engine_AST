## Table of Contents
- [Introduction](#introduction)
- [Technical Parts](#technical-parts)
  - [Installation](#installation)
  - [How to run](#how-to-run)
- [About Solution](#about-solution)
  - [Solution Overview](#solution-overview)
  - [Code Structure](#code-structure)
- [Non Technical Parts](#non-technical-parts)
  - [My Approach](#my-approach)
  - [Feedback](#feedback)
- [Outro](#outro)
>I've gone through the assignment description multiple times to ensure that nothing important was missed.

>The code has been written in a way that reads almost like a story. But don’t worry, this README is concise and focused. Below you'll find detailed explanations in a structured format.

**Here’s what to expect:**

The code is thoroughly commented with appropriate docstrings (React code is compatible with Doxygen, and Python code with Sphinx).
Unit tests account for edge cases, both positive and negative, with over 80% coverage.
This README prioritizes technical explanations first, followed by a discussion of the solution. It will also touch on more subjective aspects like my approach and design thoughts.
Technical Details
##  Installation
This project has been designed to be platform agnostic. You can either use Docker or run it on your machine directly. Here’s how to get started:

## Frontend
```
cd frontend/
npm install
```
### Backend
If poetry isn’t installed, you'll need to set it up:
```
python3 -m venv $VENV_PATH
$VENV_PATH/bin/pip install -U pip setuptools
$VENV_PATH/bin/pip install poetry
```
Then, create a virtual environment and install the necessary dependencies:
```
cd backend/
poetry install
```
## Database
Once the backend is set up, configure the database using the following command. Ensure your connection credentials are populated in the .env file.
```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```
## How to Run
Assuming installation went smoothly, run the following to start each service:

## Frontend
```
npm run dev
```
## Backend
```
poetry run python main.py --dev
```

## Database
```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```
## Solution Breakdown
**Overview**
The solution encompasses a UI, API, and a database.

UI: Developed with Next.js for efficient server-side rendering and better SEO. It communicates with the backend via HTTP calls, visualizing the Abstract Syntax Tree (AST) using react-d3-tree.

API: Built with FastAPI for its speed and simplicity, the backend processes input, tokenizes it using tokenizer(), and parses the token stream into an AST structure using a Parser object.

Database: The AST is serialized into JSON and stored. A more optimized solution could involve a key-value storage model where the hash of a node acts as the key, allowing us to store only unique nodes and efficiently traverse the tree to save space.

## Code Structure
**Backend**
File Path	Description
```
main.py	Entrypoint for the server
poetry.lock	Backend dependencies managed by Poetry
pyproject.toml	Project metadata
rule_engine/ast_utils.py	Definitions and utilities for AST classes and Nodes
rule_engine/database.py	Database functions and ORM setup
rule_engine/main.py	API definitions and routes
rule_engine/models.py	Database schema
rule_engine/parser_utils.py	Parser and tokenizer logic
```
**Frontend**
File Path	Description
```
app/	Main source code for the frontend app
app/components/ASTTree.tsx	Component for rendering the AST visualization
app/services/api.ts	Utility for handling API requests
app/page.tsx	Main entry point for the UI
```
**Design Discussion**
The low-level design of the classes revolves around creating and evaluating an AST. Here’s a brief outline of how the system works:
java
Class Node:
    Attribute node_type: String  // "operand" or "operator"
    Attribute left: Node
    Attribute right: Node
    Attribute value: Condition or Operator

Class Operator:
    Method evaluate(left: Node, right: Node) -> Boolean

Class ANDOperator inherits Operator:
    Method evaluate(left: Node, right: Node) -> Boolean:
        return left.value.evaluate() AND right.value.evaluate()

Class OROperator inherits Operator:
    Method evaluate(left: Node, right: Node) -> Boolean:
        return left.value.evaluate() OR right.value.evaluate()

Generic Type T
```Class Condition<T>:```
  Attribute lvariable: String
    Attribute rvalue: T
    Attribute comparison_type: String  // "gt", "lt", "eq", "lteq", "gteq", "neq"

    Method evaluate(input_value: T) -> Boolean:
        If comparison_type == "gt":
            return input_value > rvalue
        If comparison_type == "lt":
            return input_value < rvalue
        If comparison_type == "eq":
            return input_value == rvalue
        If comparison_type == "lteq":
            return input_value <= rvalue
        If comparison_type == "gteq":
            return input_value >= rvalue
        If comparison_type == "neq":
            return input_value != rvalue

Class AST:
    Attribute root: Node

    Method evaluate_rule(json_data: Dictionary) -> Boolean:
        return _evaluate_node(root, json_data)

    Method _evaluate_node(node: Node, data: Dictionary) -> Boolean:
        If node.node_type == "operand":
            return node.value.evaluate(data[node.value.lvariable])
        If node.node_type == "operator":
            return node.value.evaluate(node.left, node.right)

    Method create_rule(rule: String) -> Boolean:
        tokens = tokenize(rule)
        parser = Parser(tokens)
        root = parser.parse()
        return True

    Function combine_rules(rules: List<String>) -> Boolean:
      // Step 1: Parse each rule into its AST form
      Attribute asts: List<Node> = []
      For each rule in rules:
          tokens = tokenize(rule)
          parser = Parser(tokens)
          asts.append(parser.parse())

      // Step 2: Determine the most frequent operator
      Attribute operator_count: Dictionary<String, Integer> = {'AND': 0, 'OR': 0}
      For each rule in rules:
          operator_count['AND'] += count_occurrences(rule, 'AND')
          operator_count['OR'] += count_occurrences(rule, 'OR')

      Attribute most_frequent_operator: String
      If operator_count['AND'] >= operator_count['OR']:
          most_frequent_operator = 'AND'
      Else:
          most_frequent_operator = 'OR'

      Attribute operator_class: Class
      If most_frequent_operator == 'AND':
          operator_class = ANDOperator
      Else:
          operator_class = OROperator

      // Step 3: Combine all ASTs using the most frequent operator
      While length(asts) > 1:
          left_ast = asts.pop(0)
          right_ast = asts.pop(0)
          combined_ast = Node(
              node_type="operator",
              left=left_ast,
              right=right_ast,
              value=operator_class()
          )
          asts.append(combined_ast)

      root = asts[0]
      Return True


Parser and Tokenizer

java
Function tokenize(rule: String) -> List<String]:
    token_pattern = compile_regex('\s*(=>|<=|>=|&&|\|\||[()=><!]|[\w]+)\s*')
    Return [token for token in find_all(token_pattern, rule) if token.strip()]

Class Parser:
    Attribute tokens: List<String>
    Attribute pos: Integer

    Constructor(tokens: List<String>):
        tokens = tokens
        pos = 0

    Method parse() -> Node:
        If tokens is empty:
            Raise ValueError("Empty tokens list")
        Return parse_expression()

    Method parse_expression() -> Node:
        node = parse_term()
        While pos < length(tokens) AND tokens[pos] in ('AND', 'OR'):
            operator = tokens[pos]
            pos += 1
            right = parse_term()
            If operator == 'AND':
                node = Node("operator", left=node, right=right, value=ANDOperator())
            Else If operator == 'OR':
                node = Node("operator", left=node, right=right, value=OROperator())
        Return node

    Method parse_term() -> Node:
        If tokens[pos] == '(':
            pos += 1
            node = parse_expression()
            pos += 1  // skip ')'
            Return node
        Else:
            Return parse_condition()

    Method parse_condition() -> Node:
        lvariable = tokens[pos]
        pos += 1
        comparison_type = tokens[pos]
        pos += 1
        rvalue = tokens[pos]
        pos += 1
        If is_digit(rvalue):
            rvalue = to_integer(rvalue)
        Else If is_float(rvalue):
            rvalue = to_float(rvalue)
        Else:
            rvalue = strip_quotes(rvalue)
        condition = Condition(lvariable, rvalue, comparison_type)
        Return Node("operand", value=condition)


**Key Classes**
Node: Represents individual nodes in the AST. Each node can be an operator (e.g., AND, OR) or an operand (e.g., a condition).

Condition: Defines a condition with a left variable, right value, and a comparison type (like "gt", "eq", etc.).

Operators: ANDOperator and OROperator classes inherit from the Operator base class. They define how to evaluate the tree based on logical operations.

Parser: Tokenizes and parses input strings, generating the AST from rules expressed in logical terms like AND/OR conditions.

**Example: AST Evaluation**
Tree Creation: A rule is tokenized, and the parser builds an AST by creating nodes for conditions and logical operators.
Evaluation: The tree is traversed to evaluate conditions and apply logical operations to determine whether a rule is satisfied.
More details on this design are included in the code comments and docstrings for each class.

**Non-Technical Insights**
Now that the technical aspects are covered, let’s dive into some non-technical (but still relevant) insights, focusing on my thought process and approach.

**My Approach**
Here’s a summary of how I approached this project:

Understanding the Assignment: My first step was to thoroughly read the assignment, ensuring I fully understood the problem before jumping into coding.

Research: I researched topics such as frequent operator heuristics, which guided my approach to parsing and rule combination.

Parser Design: Drawing from my experience with compilers (particularly lex and bison), I applied similar concepts here to build the AST. This included breaking down conditions, operators, and optimizing storage.

## Optimization: While implementing the solution, I considered more efficient ways to store and traverse ASTs, proposing improvements like shared nodes for common conditions to save space.

## How to Use

### 1. Creating a Rule

- Navigate to the "Create Rule" section on the homepage.
- Enter a rule string in the input field. Example:
```bash
age > 30 AND salary > 50000
```
- Click "Create Rule". If successful, you'll receive a message with the created rule ID.

### 2. Evaluating a Rule

- Navigate to the "Evaluate Rule" section on the homepage.
- Enter the rule ID you received when creating the rule.
- Enter a data set (in JSON format) to evaluate the rule. Example:
```bash
{
  "age": 35,
  "salary": 60000
}
```
- Click "Evaluate Rule". You will see the result of the evaluation (either true or false).

## API Endpoints

### 1. Create Rule

- URL: /api/create_rule
- Method: POST
- Request Body:
```bash
{
  "rule": "age > 30 AND salary > 50000"
}
```
- Response:
Success: 201 Created
```bash
{
  "message": "Rule created successfully",
  "rule_id": "6144f0e1f3b60f2f5b6a254e"
}
```
Error: 400 Bad Request
```bash
{
  "error": "Rule string is required"
}
```

### 2. Evaluate Rule

- URL: /api/evaluate_rule
- Method: POST
- Request Body:
```bash
{
  "rule_id": "6144f0e1f3b60f2f5b6a254e",
  "data": {
    "age": 35,
    "salary": 60000
  }
```
- Response:
Success: 200 OK
```bash
{
  "result": true
}
```
- Error: 404 Not Found
```bash
{
  "error": "Rule not found"
}
```


## Feedback
This assignment was a fantastic blend of three key areas: academic knowledge, algorithmic thinking, and practical software engineering. It challenged me to apply theoretical concepts to a real-world problem, all while keeping performance and design in mind.

## Conclusion
Thank you for this opportunity. It was an engaging and educational experience, allowing me to explore new heuristics and improve my understanding of ASTs and rule parsing.
