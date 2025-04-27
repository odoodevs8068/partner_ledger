{
    'name': 'Partner Ledger Report',
    'version': '1.2',
    'sequence': 99,
    'author': "JD DEVS",
    'category': 'Accounting/Accounting',
    'depends': ['account_accountant', 'account_reports'],
    'assets': {
        'web.assets_backend': [],

        'web.assets_qweb': [
            "partner_ledger_updates/static/src/xml/reconcil.xml",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/assets/screenshots/banner.png'],
}