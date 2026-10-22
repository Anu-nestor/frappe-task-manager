# Copyright (c) 2026, Anu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Employee(Document):
	def validate(self):
		self.validate_user()

	def validate_user(self):
		if not self.user:
				frappe.throw("User is required for an employee.")

		if not frappe.db.exists("User", self.user):
				frappe.throw("The selected User does not exist.")

