import unittest

from client import Client
from common.utils import get_configs

class ClientTestCase(unittest.TestCase):
    CONFIGS = get_configs()

    bad_message = {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad request'
    }

    good_message = {
        CONFIGS.get('RESPONSE'): 200,
        CONFIGS.get('ALERT'): 'Привет, клиент!'
    }

    test_error_message = f'400: Bad request'
    test_correct_message = f'200: OK!'

    def test_error_response(self):
        self.assertEqual(Client.check_response(Client(), self.bad_message, self.CONFIGS), self.test_error_message)

    def test_correct_response(self):
        self.assertEqual(Client.check_response(Client(), self.good_message, self.CONFIGS), self.test_correct_message)

if __name__ == '__main__':
    unittest.main()