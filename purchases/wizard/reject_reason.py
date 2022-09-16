from odoo import fields, models, api
from datetime import datetime


class RejectReason(models.TransientModel):
    _name = "reject.reason"

    date = fields.Date(default=fields.Datetime.now, string='Date')
    reason = fields.Text(string='Reason')
    purchase_request_id = fields.Many2one('purchase.request')

    # def confirm(self):
    #     # self.reason += self.reason
    #     active_obj = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
    #     active_obj.write({'state': '5'})
    #     self.purchase_request_id.write({
    #         'reject_reason': str(self.date) + ' ' + self.reason
    #     })

    def confirm(self):
        for i in self:
            active_obj = i.env[i.env.context.get('active_model')].browse(i.env.context.get('active_id'))
            active_obj.write({'state': '5'})
            i.purchase_request_id.write({
                'reject_reason': str(i.date) + ' ' + i.reason
            })

