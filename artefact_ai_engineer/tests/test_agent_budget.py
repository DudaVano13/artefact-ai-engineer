import unittest
from unittest.mock import patch
from agent import Agent

class AgentBudgetTests(unittest.TestCase):
    def test_catalog_budget_uses_csv_instead_of_guessing(self):
        with patch.object(Agent, '__init__', lambda obj: setattr(obj, 'history', [])):
            agent = Agent()
            answer = agent.reply('Quais violões vocês têm disponíveis por até R$ 1.000?')
        self.assertIn('Yamaha C40', answer)
        self.assertIn('Tagima Memphis', answer)
        self.assertIn('12 opções', answer)
        self.assertIn('R$ 1.000,00', answer)
