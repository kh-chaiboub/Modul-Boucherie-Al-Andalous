# coding: utf-8

from odoo import  fields, models,api
from odoo.exceptions import Warning
from docutils.nodes import field

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

        
    ms_number = fields.Char("Numéro",track_visibility='onchange')
    payment_method_code = fields.Char(
        related='payment_method_id.code',
        help="Technical field used to adapt the interface to the payment type selected.")
    
    
    def _create_payments(self):
        payment_ids = super(AccountPaymentRegister, self)._create_payments()
        for payment_id in payment_ids:
            if self.ms_number:
                payment_id.ms_number=self.ms_number
                ref=payment_id._ms_get_move_ref('')
                payment_id.move_id.write({'ref':ref})
        return payment_ids
        
class AccountPayment(models.Model):
    _inherit = 'account.payment'

        
    ms_number = fields.Char("Numéro",track_visibility='onchange')
                


    def _ms_get_move_ref(self,aml_name):
        res_str=aml_name
        if self.ms_number :
            res_str =res_str + ' ' + self.payment_method_id.code + ': '+ self.ms_number
        if self.ref:
            res_str =res_str + ' (' + self.ref +')'
        return res_str
    
    # def _get_liquidity_move_line_vals(self, amount):
    #     vals=super(AccountPayment, self)._get_liquidity_move_line_vals(amount)
    #     if not self.hide_payment_method and self.payment_method_id.chq_acc_id:
    #         vals['account_id'] = self.payment_method_id.chq_acc_id.id
    #         vals['name'] = self._ms_get_move_ref(vals['name'])
    #     return vals
    
    def action_post(self):
        for rec in self:
            res=super(AccountPayment, rec).action_post()
            ref=self._ms_get_move_ref('')
            rec.move_id.write({'ref':ref})
        return True
    
        
        
#     def refrech_ms_amount_residual(self):
#         print('_________refrech_ms_amount_residual__',self)
#         dest_aml_ids=self.move_line_ids.filtered(lambda x : x.account_id.user_type_id.type in ['receivable','payable'] and x.journal_id.id == self.journal_id.id)#.type in ['bank','cash']
#         amount_to_show=0
#         for dest_aml_id in dest_aml_ids:
#             if len(dest_aml_id)>1:
#                 print(1)
#             if dest_aml_id.currency_id and dest_aml_id.currency_id == self.currency_id:
#                 amount_to_show += abs(dest_aml_id.amount_residual_currency)
#             else:
#                 currency = dest_aml_id.company_id.currency_id
#                 amount_to_show += currency._convert(abs(dest_aml_id.amount_residual), self.currency_id, self.company_id, dest_aml_id.date or fields.Date.today())
#         if self.ms_amount_residual - amount_to_show != 0:
#             self.write({'ms_amount_residual':amount_to_show})
#
#     @api.model
#     def refresh_all_payment_ms_amount_residual_cron(self):
#         print('cron______________refresh_all_payment_ms_amount_residual')
#         payment_ids=self.sudo(1).search([])
#         for payment_id in payment_ids:
#             payment_id.refrech_ms_amount_residual()
#
#     def refresh_all_payment_ms_amount_residual(self):
#         payment_ids=self.sudo(1).search([])
#         for payment_id in payment_ids:
#             payment_id.refrech_ms_amount_residual()     
#
#     def ms_cancel_delete_payments(self):
#         moves=self.env['account.move'].search([('ref','like',self.move_name)])
#         for move in moves:
#             move.button_cancel()
# #             print('________',move.display_name)
# #             if move.id==1436:
# #                 print(1)
#             ids = []
#             for aml in move.line_ids:
#                 if aml.account_id.reconcile:
#                     ids.extend([r.debit_move_id.id for r in aml.matched_debit_ids] if aml.credit > 0 else [r.credit_move_id.id for r in aml.matched_credit_ids])
#                     ids.append(aml.id)
#             if ids:
#                 self.env['account.move.line'].browse(ids).remove_move_reconcile()
#             move.unlink()
# #         if res :
# #             raise Warning("can't delete this payment because it has account.move (%s)"%res[0].name)
# #         else:
#         self.cancel()
#         self.move_name=False
#         self.unlink()
#
#
#
#
#
#     def convert_to_advance(self):
#         msg=False
#         if self.payment_type=='inbound':
#             new_acount_id=self.move_line_ids[0].account_id.search([('code','=','44210000')])
#             if self.ms_amount_residual != self.amount:
#                 msg="Monatant libre <> mantant reglement"
#             elif  self.has_invoices:#self.invoice_ids
#                 msg="there is invoices"
#                 if new_acount_id.id in self.move_line_ids.mapped('account_id').ids:
#                         msg="Impossible ce paiement était déjà une avance"
#             if not msg:
#                 if not len(self.move_line_ids)==2:
#                     msg="Cas impossible 8757647658"
#             if not msg:
#                 if fields.Datetime.now().year <= self.payment_date.year :
#                     msg='impossible de convertir un paiement de cette année'
#             if not msg:
#                 for move_line_id in self.move_line_ids:
#                     if not move_line_id.account_id.internal_type in ('liquidity','bank'):
#                         if move_line_id.account_id.internal_type =='receivable':
#                             if new_acount_id:
#                                 self._cr.execute("update account_move_line set account_id=%s where id=%s"%(new_acount_id.id,move_line_id.id))
# #                                 move_line_id.write({'account_id':new_acount_id.id})
# #                                 self.merge_in_table_by_sql(move_line_id, new_acount_id, 'account_move_line')
#                                 self.write({'ms_type':'avance'})
#                             else:
#                                 msg="cas impossible 5454dsffdf"
#         if msg:
#             raise Warning(msg)
#
#     def convert_advance_to_payment(self):
#         msg=False
#         if self.ms_type=='avance':
#             if not self.partner_id:
#                 msg="la partenaire est obligatoire pour cet operation djkhjklghjfffkfg54789"
#             for move_line_id in self.move_line_ids:
#                 if move_line_id.account_id.internal_type =='receivable':
#                     msg="cas impossible contacter l'admin djkhjklghjkfg54789"
#             if not msg:
#                 new_date_payment=fields.Datetime.from_string(str(fields.Datetime.now().year)+"-01-01").date()
#                 if new_date_payment < self.payment_date:
#                     msg="probleme des dates "
#             if not msg:
#                 for move_line_id in self.move_line_ids:
#                     frm_acount_id=move_line_id.account_id.search([('code','=','44210000')])
#                     if move_line_id.account_id.id == frm_acount_id.id:
#                         to_account_id=self.partner_id.property_account_receivable_id
#                         if move_line_id.account_id.id ==frm_acount_id.id:
#                             line=[]
#                             line.append((0, 0, {'account_id': frm_acount_id.id,'partner_id':self.partner_id.id,'debit':move_line_id.credit,'name':'transféré au paiement'}))#,'payment_id':self.id
#                             line.append((0, 0, {'account_id': to_account_id.id,'partner_id':self.partner_id.id,'credit':move_line_id.credit,'name':'transféré au paiement'}))#,'payment_id':self.id
#
#                             move_vals = {
#                             'line_ids': line,
#                             'journal_id': self.journal_id.id,
#                             'date': new_date_payment,
#                             }
#                             move_id=self.env['account.move'].create(move_vals)
#                             move_id.post()
#                             for aml_id in move_id.line_ids:
#                                 self._cr.execute("update account_move_line set payment_id=%s where id=%s"%(self.id,aml_id.id))
#                                 if aml_id.account_id.id == frm_acount_id.id:
#                                     (aml_id + move_line_id).reconcile(writeoff_acc_id=False, writeoff_journal_id=False)
#                             self.write({'ms_type':'normal'})
#         if msg:
#             raise Warning(msg)
#
# #     def ms_type_change(self):
# #         if self.ms_type=='reglement':
# #             self.write({'ms_type':'avance'})
# #         elif self.ms_type=='avance':
# #             self.write({'ms_type':'reglement'}) 
#
#     def its_payment_ecart(self):
#         self.env['ms.global_acc_functions'].create_ecart_move(payment_id=self)
# #             msg=False
# #             if  self.ms_amount_residual == 0:
# #                 msg="Monatant libre == 0"
# #             elif  self.ms_amount_residual == self.amount:
# #                 msg="Monatant libre == mantant reglement"
# #             elif self.ms_type=='avance':
# #                 msg="C'est une avance"
# #             elif self.payment_type not in ('inbound','outbound'):
# #                 msg="not inbound and not outbound lkjfddh873HJH"
# #             elif not self.invoice_ids:
# #                 msg="cas non traité 876765 contacter les responsable du MAROCSYS"
# #             if  msg:
# #                 raise Warning(msg)
# #             else:
# #                 
# #                 amount=self.ms_amount_residual
# #                 debit, credit=amount,0
# #                 journal_id=self.company_id.ecart_journal_id
# #                 account_id=self.company_id.ecart_outbound_account_id
# # #                 outbound=self.env['account.account'].search([('code','=','65812000')])
# #                 ref='écart de paiement'
# #                 
# #                 old_aml_id=self.move_line_ids.filtered(lambda x: x.account_id.internal_type in ('receivable','payable'))
# #                 data = self.env['account.partial.reconcile'].search(['|',('debit_move_id','=',old_aml_id.id),('credit_move_id','=',old_aml_id.id)])
# #                 if not data :
# #                     raise Warning("cas non traité 87676554 contacter les responsable du MAROCSYS")
# #                 date=data[0].max_date
# #                 for line in data:
# #                     if date<line.max_date:
# #                         date=line.max_date
# #                         
# #                 if self.payment_type =='inbound':
# # #                     inbound=self.env['account.account'].search([('code','=','75812000')])
# #                     account_id=self.company_id.ecart_inbound_account_id
# #                     debit, credit=0,amount
# #                     ref='écarts de règlement'
# #                 if not account_id :
# #                     raise Warning("les comptes des écart non spécifié pour cette société")
# # #                 journal_id=self.env['account.journal'].search([('type','=','general'),('id','=',3)])
# #                 
# #                 
# #                 journal_id=self.journal_id.search([('type','=','general'),('code','=','OD')])
# #                 move_id = self.env['account.move'].create({'journal_id':journal_id.id,
# #                                                         'date':date,
# #                                                         'ref':ref,
# #                                                         })
# #         
# #                 vals={'line_ids':[]}
# #                 vals['line_ids'].append([0,0, {'move_id':move_id.id,
# #                                                'account_id':account_id.id,
# #                                                'partner_id':self.partner_id.id,
# #                                                'name':ref,
# #                                                'credit':credit,
# #                                                'debit':debit 
# #                                                }])
# #                 
# #                 
# #                 vals['line_ids'].append([0,0, {'move_id':move_id.id,
# #                                                'account_id':old_aml_id.account_id.id,
# #                                                'partner_id':self.partner_id.id,
# #                                                'name':ref,
# #                                                'credit':debit,
# #                                                'debit':credit,
# #                                                }])
# #                 move_id.write(vals)
# #                 move_id.post()
# #                 for aml_id in move_id.line_ids:
# #                     self._cr.execute("update account_move_line set payment_id=%s where id=%s"%(self.id,aml_id.id))
# #                 new_aml_id=move_id.line_ids.filtered(lambda x: x.account_id.internal_type in ('receivable','payable'))
# #                 (new_aml_id + old_aml_id).reconcile(False, False)
# #                 print('_____test',move_id)
# #                 return True
#
#     def show_reconciled_absl(self):
#         absl_ids=self.move_line_ids.mapped('statement_line_id')
#         if absl_ids:
#             action = self.env.ref('account.action_bank_statement_line').read()[0] 
#             action['domain']=[('id','in',absl_ids.ids)]
#             return action  
#         raise Warning("Ce paiement non lettré ")
#
#     def show_move_ids(self):
#         move_ids=self.move_line_ids.mapped('move_id')
# #         if move_ids:
#         action = self.env.ref('account.action_move_journal_line').read()[0] 
#         action['domain']=[('id','in',move_ids.ids)]
#         action['context']={}
#         return action  

  