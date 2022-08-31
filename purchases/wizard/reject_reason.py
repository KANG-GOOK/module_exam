from odoo import fields, models, api
import datetime


class RejectReason(models.TransientModel):
    _name = "reject.reason"

    date = fields.Date(default=fields.Datetime.now, string='Date')
    reason = fields.Text(string='Reason')
    purchase_request_id = fields.Many2one('purchase.request')

    def confirm(self):
        self.purchase_request_id.state = '5'

