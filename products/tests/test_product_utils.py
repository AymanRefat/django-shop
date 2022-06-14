from django.test import TestCase
from products import utils

class TestUtils(TestCase):
		def setUp(self):
				self.allowed_params = ("name", "des")

		def test_valid_params(self):
				test_params = {"name": "", "param2": None, "right": "data"}
				data = utils.valid_params(**test_params)
				self.assertEqual(
						len(data),
						1,
						"Didn't Remove the Bad Params and Didn't Return The right Ones",
				)

		def test_empty_valid_params(self):
				data = utils.valid_params()
				self.assertEqual(data, {}, "Didn't Return Empty Dict")

		def test_bad_params_valid_params(self):
				data = utils.valid_params(hello=None, new="", bad="", p=None)
				self.assertEqual(data, {}, "Didn't Remove the Bad Params")

		def test_allowed_params(self):
				allowed = self.allowed_params
				test_params = {key: "d" for key in allowed}
				test_params["bad_params"] = "D"
				data = utils.allowed_params(self.allowed_params, d=test_params)
				self.assertEqual(len(data), len(self.allowed_params))

		def test_allowed_params_with_capital_letters(self):
				allowed = self.allowed_params
				test_params = {key: "d" for key in allowed}
				test_params["Name"] = "D"
				test_params["NAME"] = "D"
				data = utils.allowed_params(self.allowed_params, d=test_params)
				self.assertEqual(len(data), len(test_params))


		# TODO create this 
		def test_generate_image_name(self):
			pass 
