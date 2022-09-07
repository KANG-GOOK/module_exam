from odoo import fields, models, api
from datetime import datetime


class RejectReason(models.TransientModel):
    _name = "reject.reason"

    date = fields.Date(default=fields.Datetime.now, string='Date')
    reason = fields.Text(string='Reason')
    purchase_request_id = fields.Many2one('purchase.request')

    def confirm(self):
        active_obj = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
        active_obj.write({'state': '5'})
        self.purchase_request_id.write({
            'reject_reason': str(datetime.now()) + ' ' + self.reason
        })

