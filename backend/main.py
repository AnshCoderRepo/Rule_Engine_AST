"""
Main script file to run backend and database.
"""

import argparse
import unittest
import uvicorn
import tests.test_parser
import tests.test_tree_traversal

def _run_tests():
    """Run tests."""
    print("--test: running tests")

    loader = unittest.TestLoader()
    suite_parser = loader.loadTestsFromModule(tests.test_parser)
    suite_tree = loader.loadTestsFromModule(tests.test_tree_traversal)

    runner = unittest.TextTestRunner()
    runner.run(suite_parser)
    runner.run(suite_tree)

def _run_dev_api_server(host = None, port = None):
    """Run a dev instance of the FastAPI server."""
    if not host:
        host = "0.0.0.0"

    if not port:
        port = 5000

    uvicorn.run('rule_engine.main:app', host=host, port=port, reload=True)

def _run_db_migrate():
    """Instantiate Postgres DB with schema, and empty tables."""
    print("--migrate: running DB Migrate")

def _run_start_db():
    """Start the DB instance on local machine."""
    print("--db: starting DB")

def _show_help():
    """Show help information."""
    help_string = (
        "usage: main.py [-h] [--tests] [--dev] [--host HOST] [--port PORT]\n\n"
        "options:\n"
        "-h, --help         show this help message and exit\n"
        "--tests            Run tests for Parser and AST\n"
        "--dev              Run dev FastAPI Server\n"
        "--host HOST        Add host address to run the FastAPI Server\n"
        "--port PORT        Add port address to run the FastAPI Server\n"
    )

    print(help_string)

def main():
    """
    Entry into the app, execute commands according to the arguments supplied.
    """
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--tests', action='store_true', help='Run tests for Parser and AST')
    parser.add_argument('--dev', action='store_true', help='Run dev FastAPI Server')
    parser.add_argument('--host', dest='host', type=str, help='Add host address to run the FastAPI Server')
    parser.add_argument('--port', dest='port', type=int, help='Add port address to run the FastAPI Server')

    args = parser.parse_args()

    if args.tests:
        _run_tests()
    elif args.dev:
        _run_dev_api_server(args.host, args.port)
    else:
        _show_help()

if __name__ == "__main__":
    main()
