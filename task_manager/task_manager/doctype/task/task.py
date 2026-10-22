# Copyright (c) 2026, Anu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class Task(Document):
	def validate(self):
		self.validate_dates()
		self.validate_assignee()
		self.handle_completion_date()
		self.validate_revision()

	def validate_dates(self):
		if self.start_date and self.due_date:
			if getdate(self.due_date) < getdate(self.start_date):
				frappe.throw("Due Date cannot be earlier than Start Date.")

	
	
	def validate_assignee(self):
			# Assignment is optional
			if not self.assigned_to:
					return

			employee = frappe.db.get_value(
					"Employee",
					self.assigned_to,
					["status", "user"],
					as_dict=True,
			)

			if not employee:
					frappe.throw("The selected Employee does not exist.")

			if employee.status != "Active":
					frappe.throw(
							"Tasks cannot be assigned to an inactive employee."
					)

			if not employee.user:
					frappe.throw(
							"The selected Employee has no linked User account."
					)

			user_enabled = frappe.db.get_value(
					"User", employee.user, "enabled"
			)

			if not user_enabled:
					frappe.throw(
							"Tasks cannot be assigned to a disabled User account."
					)



	def handle_completion_date(self):
		if self.status == "Completed":
			if not self.completion_date:
					self.completion_date = today()
		else:
			self.completion_date = None

	def validate_revision(self):
		if self.is_new():
			return

		previous = self.get_doc_before_save()

		if not previous:
			return

		was_completed = previous.status == "Completed"
		is_reopened = self.status in ("In Progress", "Review", "Open")

		if was_completed and is_reopened:
			if not (self.reason or "").strip():
				frappe.throw("Please provide a reason for reopening the completed task.")

			self.completion_date = None
