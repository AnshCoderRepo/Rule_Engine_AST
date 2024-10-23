import unittest
from rule_engine.ast_utils import Node, AST, Condition, ANDOperator, OROperator

class TestRuleEngine(unittest.TestCase):
    def test_condition_evaluate(self):
        condition_gt = Condition("age", 30, 'gt')
        self.assertTrue(condition_gt.evaluate(35))
        self.assertFalse(condition_gt.evaluate(25))

        condition_eq = Condition("department", "Sales", 'eq')
        self.assertTrue(condition_eq.evaluate("Sales"))
        self.assertFalse(condition_eq.evaluate("Marketing"))

    def test_and_operator(self):
        left_condition = Condition("age", 30, 'gt')
        right_condition = Condition("salary", 50000, 'gt')

        left_node = Node("operand", value=left_condition)
        right_node = Node("operand", value=right_condition)

        and_node = Node("operator", left=left_node, right=right_node, value=ANDOperator())

        data = {"age": 35, "salary": 60000}
        self.assertTrue(and_node.evaluate(data))

        data = {"age": 35, "salary": 40000}
        self.assertFalse(and_node.evaluate(data))

    def test_or_operator(self):
        left_condition = Condition("age", 30, 'gt')
        right_condition = Condition("salary", 50000, 'gt')

        left_node = Node("operand", value=left_condition)
        right_node = Node("operand", value=right_condition)

        or_node = Node("operator", left=left_node, right=right_node, value=OROperator())

        data = {"age": 35, "salary": 40000}
        self.assertTrue(or_node.evaluate(data))

        data = {"age": 25, "salary": 60000}
        self.assertTrue(or_node.evaluate(data))

        data = {"age": 25, "salary": 40000}
        self.assertFalse(or_node.evaluate(data))

    def test_ast_evaluate_rule(self):
        age_condition = Condition("age", 30, 'gt')
        department_condition = Condition("department", "Sales", 'eq')
        left_and_node = Node("operator", left=Node("operand", value=age_condition), right=Node("operand", value=department_condition), value=ANDOperator())

        age_condition = Condition("age", 25, 'lt')
        department_condition = Condition("department", "Marketing", 'eq')
        right_and_node = Node("operator", left=Node("operand", value=age_condition), right=Node("operand", value=department_condition), value=ANDOperator())

        or_node = Node("operator", left=left_and_node, right=right_and_node, value=OROperator())

        salary_condition = Condition("salary", 50000, 'gt')
        experience_condition = Condition("experience", 5, 'gt')
        and_node = Node("operator", left=Node("operand", value=salary_condition), right=Node("operand", value=experience_condition), value=ANDOperator())

        root = Node("operator", left=or_node, right=and_node, value=ANDOperator())

        ast = AST(root)

        json_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        self.assertFalse(ast.evaluate_rule(json_data))

        json_data = {"age": 22, "department": "Marketing", "salary": 45000, "experience": 6}
        self.assertFalse(ast.evaluate_rule(json_data))

        json_data = {"age": 40, "department": "HR", "salary": 40000, "experience": 4}
        self.assertFalse(ast.evaluate_rule(json_data))

if __name__ == '__main__':
    unittest.main()
