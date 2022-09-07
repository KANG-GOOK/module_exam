from odoo import models


class ReportXLS(models.AbstractModel):
    _name = 'report.purchases.report_xlsx_wizard'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, obj):
        for i in obj:
            report_name = 'Báo cáo mua hàng'
            # state = i.state
            wait_trans = "Chờ duyệt"
            approved_trans = "Đã duyệt"
            done_trans = "Hoàn thành"
            # query = '''
            #                 select prl.id, pp.default_code, prl.requests_quantity
            #                 from purchase_request_line prl
            #                 inner join product_product pp on pp.id = prl.product_id
            #             '''
            # self._cr.execute(query)
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name)

            format_1 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
            format_2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': False})
            format_3 = workbook.add_format({'font_size': 18, 'align': 'center', 'bold': True, 'font_color': 'red'})
            format_4 = workbook.add_format({'font_size': 10, 'bold': True})
            format_5 = workbook.add_format({'font_size': 10, 'align': 'center'})
            # sheet = workbook.add_worksheet('excel')
            sheet.set_column('A:J', 25)
            sheet.set_row(4, 35)
            # sheet.set_row(1, 30)
            sheet.merge_range('C1:G1', 'CÔNG TY CỔ PHẦN QUÔC TẾ HOMEFARM', format_1)
            sheet.merge_range('C2:G2', 'Địa chỉ: 14 Nguyễn Cảnh Di, Hoàng Mai, Hà Nội', format_2)
            sheet.merge_range('C3:G3', 'hotline:    01234176300', format_2)
            sheet.merge_range('C4:G4', 'Email:  dathang@homefarm.vn      Website: https://homefarm.vn/', format_2)
            sheet.merge_range('A5:G5', 'PHIẾU YÊU CẦU MUA HÀNG', format_3)
            sheet.write('E6', 'Phiếu yêu cầu', format_4)
            sheet.write('E7', 'Ngày yêu cầu', format_4)
            sheet.write('E8', 'Trạng thái phiếu', format_4)
            sheet.write('F6', i.name, format_2)
            sheet.write('F7', i.creation_date.strftime('%d-%m-%Y'), format_2)
            # sheet.write('F8', state, format_2)

            sheet.write(10, 0, 'STT', format_1)
            sheet.write(10, 1, 'Mã sản phẩm', format_1)
            sheet.write(10, 2, 'Sản phẩm', format_1)
            sheet.write(10, 3, 'Đơn vị tính', format_1)
            sheet.write(10, 4, 'Số lượng yêu cầu', format_1)
            sheet.write(10, 5, 'Đơn giá dự kiến', format_1)
            sheet.write(10, 6, 'Chi phí dự kiến', format_1)

            row = 10
            col = 1
            n = 0
            sum_estimated_subtotal = 0
            for line in i.lines:
                row += 1
                n += 1
                line.estimated_subtotal = line.estimated_unit_price * line.requests_quantity
                sum_estimated_subtotal += line.estimated_subtotal
                sheet.write(row, 0, n, format_5)
                sheet.write(row, 1, line.product_id.id, format_5)
                sheet.write(row, 2, line.product_id.name, format_5)
                sheet.write(row, 3, line.product_uom_id.name, format_5)
                sheet.write(row, 4, line.requests_quantity, format_5)
                sheet.write(row, 5, line.estimated_unit_price, format_5)
                sheet.write(row, 6, line.estimated_subtotal, format_5)
                sheet.write(row + 1, 5, 'Tổng cộng', format_5)
                sheet.write(row + 1, 6, sum_estimated_subtotal, format_5)
                # sheet.write(row + 1, 5, sum_delivered_quantity, format_5)