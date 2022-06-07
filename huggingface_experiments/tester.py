from argparse import Namespace
import unittest
from huggingface_experiments.utils.args import apiArgs
import huggingface_experiments.api

class TestAPI(unittest.TestCase):
    args: Namespace = apiArgs()

    def test_CreateModelRepo(self):
        print("Testing if users can create models on other user accounts")
        self.assertEqual(api.createModelRepo(token=self.args.admin_token, name="test1", organization="NicholasSynovic").status_code, 200)
        self.assertEqual(api.createModelRepo(token=self.args.write_token, name="test1", organization="NicholasSynovic").status_code, 404)
        self.assertEqual(api.createModelRepo(token=self.args.read_token, name="test1", organization="NicholasSynovic").status_code, 404)
