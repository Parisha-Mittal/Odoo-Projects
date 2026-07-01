from odoo import models, fields


class UpdateFeesWizard(models.TransientModel):
    _name = "update.fees.wizard"
    _description = "Update Fees Status Wizard"

    fees_status = fields.Selection(
        [
            ("paid", "Paid"),
            ("unpaid", "Unpaid")
        ],
        string="Fees Status",
        required=True
    )

    def action_update(self):

        student = self.env["student.data"].browse(
            self.env.context.get("active_id")
        )

        student.write({
            "fees_status": self.fees_status
        })

        return {
            "type": "ir.actions.act_window_close"
        }