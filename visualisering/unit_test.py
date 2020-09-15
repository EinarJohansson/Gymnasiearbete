import unittest
from tests.klient import Klient

class Testa(unittest.TestCase):
    def test_udp(self):
        """
        Testa om det går att skicka meddelanden till servern.
        """
        klient = Klient()
        resultat = klient.skicka('test')
        self.assertEqual(resultat, 'success')

if __name__ == '__main__':
    unittest.main()