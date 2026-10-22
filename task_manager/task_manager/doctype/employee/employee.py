
# Copyright (c) 2026, Anu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Employee(Document):
    def validate(self):
        self.validate_user()
        self.validate_inactive_employee()

    def validate_user(self):
        if not self.user:
            frappe.throw("User is required for an employee.")

        if not frappe.db.exists("User", self.user):
            frappe.throw("The selected User does not exist.")
            

    def validate_inactive_employee(self):
        # Only check when the employee is being made inactive
        if self.status != "Inactive":
            return

        # Find unfinished tasks assigned to this employee
        tasks = frappe.get_all(
            "Task",
            filters={
                "assigned_to": self.name,
                "status": ["!=", "Completed"],
            },
            fields=["name", "title", "status"],
        )

        if tasks:
            task_details = "<br>".join(
                f"- {task.title} ({task.status})"
                for task in tasks
            )

            frappe.throw(
                "Cannot deactivate this employee because they have "
                "unfinished tasks assigned to them:<br><br>"
                f"{task_details}<br><br>"
                "Please reassign or complete these tasks first."
            )
