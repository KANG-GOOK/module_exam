{
    'name': 'PURCHASE REQUIREMENTS',
    'version': '1.0',
    'summary': 'CHỨC NĂNG YÊU CẦU MUA HÀNG',
    'description': """
    ***CHỨC NĂNG YÊU CẦU MUA HÀNG***
    ***purchase_request*** 
    ***purchase_request_line***
    ***reject_reason***
    """,
    'category': 'Other',
    'author': 'Khanh HQ 720',
    'depends': ['product', 'report_xlsx', 'purchase'],
    'data': [
        'security/security.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/purchase_request.xml',
        # 'views/purchase_request_line.xml',
        'wizard/reject_reason_view.xml',
        'wizard/import_purchase_request_line.xml',
        'wizard/report_purchase.xml',
        'report/report_xlsx.xml'
        # 'report/purchase_xls_line.xml'
    ],
    'sequence': 2,
    'installable': True,  # odoo cho phép cài đặt module, và ngược lại
    'auto_install': False,
    # nếu là true module này là module cầu nối và sẽ được tự động cài đặt khi tất cả các module nó phụ thuộc (khóa depends) được cài đặt
    'application': True,  # Nếu được đặt là True, module sẽ được đánh dấu là ứng dụng
}
