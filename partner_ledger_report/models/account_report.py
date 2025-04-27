from odoo import models, api, _, _lt, fields
from odoo.tools.misc import format_date
from datetime import timedelta
from collections import defaultdict


class AccountReconciliationInherit(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    def _prepare_move_lines(self, move_lines, target_currency=False, target_date=False, recs_count=0):
        res = super()._prepare_move_lines(move_lines, target_currency=target_currency, target_date=target_date, recs_count=recs_count)
        move_line_map = {line.id: line for line in move_lines}
        for ret_line in res:
            line = move_line_map.get(ret_line['id'])
            if line:
                ret_line.update({
                    'source_document': line.move_id.invoice_origin or '',
                    'cust_ref': line.move_id.ref or '',
                })
        return res


class ReportPartnerLedger(models.AbstractModel):
    _inherit = "account.partner.ledger"


    def _get_columns_name(self, options):
        columns = super()._get_columns_name(options)

        new_columns = [
            {'name': _('Customer Invoice')},
            {'name': _('Source Document')},
            {'name': _('Customer Reference')},
        ]
        insert_position = 2
        for col in reversed(new_columns):
            columns.insert(insert_position, col)

        return columns

    @api.model
    def _get_report_line_move_line(self, options, partner, aml, cumulated_init_balance, cumulated_balance):
        res = super()._get_report_line_move_line(options, partner, aml, cumulated_init_balance, cumulated_balance)
        columns = res['columns']
        new_columns = [
            {'name': aml.get('inv_name', '')},
            {'name': aml.get('source_document', '')},
            {'name': aml.get('cust_ref', '')},
        ]
        insert_position = 1
        for col in reversed(new_columns):
            columns.insert(insert_position, col)
        res['columns'] = columns
        return res

    @api.model
    def _get_report_line_partner(self, options, partner, initial_balance, debit, credit, balance):
        res = super()._get_report_line_partner(options, partner, initial_balance, debit, credit, balance)
        res['colspan'] = 9
        return res

    @api.model
    def _get_report_line_total(self, options, initial_balance, debit, credit, balance):
        res = super()._get_report_line_total(options, initial_balance, debit, credit, balance)
        res['colspan'] = 9
        return res


    @api.model
    def _get_query_amls(self, options, expanded_partner=None, offset=None, limit=None):
        query, params = super()._get_query_amls(options, expanded_partner, offset, limit)
        select_insert = '''
                move.invoice_origin AS source_document,
                move.name AS inv_name,
                move.ref AS cust_ref
        '''
        query = query.replace(
            'journal.name                            AS journal_name',
            'journal.name                            AS journal_name,\n' + select_insert.strip()
        )

        return query, params
