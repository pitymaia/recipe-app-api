from django.test import TestCase

from app.calc import add, subtract


class CalcTests(TestCase):

	def test_add_numbers(self):
		"""Test add two numbers"""
		self.assertEqual(add(5, 5), 10)
		self.assertEqual(add(-5, 5), 0)

	def test_subtract_numbers(self):
		"""Subtract numbers"""
		self.assertEqual(subtract(10, 5), 5)