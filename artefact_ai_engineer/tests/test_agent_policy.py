"""Tests policy routing without calling a model or remote API."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import Agent

class PolicyRoutingTests(unittest.TestCase):
    def setUp(self):
        self.agent=Agent.__new__(Agent)
        self.agent.history=[{'role':'system','content':'test'}]
        # No client is initialized: if routing falls through to an LLM, test fails.

    def test_address_and_hours(self):
        answer=self.agent.reply('Qual o endereço e horário de funcionamento da loja?')
        self.assertIn('Rua 14 de Maio, 3200',answer)
        self.assertIn('9h às 18h',answer)
        self.assertIn('página 2',answer)

    def test_return_within_five_days(self):
        answer=self.agent.reply('Comprei online e me arrependi. Posso devolver depois de 5 dias?')
        self.assertIn('7 dias corridos',answer)
        self.assertIn('5 dias',answer)
        self.assertIn('página 4',answer)

if __name__=='__main__':
    unittest.main()
