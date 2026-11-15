"""Automated test suite for Hermetic Code Sandbox."""
import unittest
from agent_hermetic_code_sandbox_isolator.core import HermeticSandbox

class TestHermeticSandbox(unittest.TestCase):
    def test_clean_execution(self):
        sandbox = HermeticSandbox()
        res = sandbox.execute_code("print(2 + 2)")
        self.assertTrue(res.is_success)
        self.assertEqual(res.stdout.strip(), "4")
