import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from store import catalog,get_product,order_status,policy_lookup

class StoreTests(unittest.TestCase):
    def test_budget(self):
        results=catalog(category='Violões',max_price=1000)
        self.assertGreater(results['total_matches'],0)
        self.assertTrue(all(x['stock']>0 for x in results['results']))
    def test_takamine(self):
        p=get_product('Takamine GD20')
        self.assertTrue(p['found'])
        self.assertEqual(p['list_price'],'R$ 2.199,00')
    def test_no_order_leak(self):
        self.assertFalse(order_status(8,'wrong@email.com')['verified'])
    def test_order_verified(self):
        self.assertTrue(order_status(8,'anacarol.ferreira@coldmail.com')['verified'])
    def test_pdf_policy(self):
        p=policy_lookup('troca devolução arrependimento')
        self.assertTrue(any(x['page']==4 for x in p['pages']))
    def test_promotion(self):
        p=get_product('Taylor 110e')
        self.assertEqual(p['promotion_percent'],8)

if __name__=='__main__': unittest.main()
