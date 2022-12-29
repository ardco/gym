# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	
	# get current user branch
	userBranch = frappe.db.get_value("Employee", {'user_id':frappe.session.user}, ["branch"])
	columns = get_columns()
	data = get_data(filters, userBranch)
	
	return columns, data

def get_data(filters, userBranch):

	payment_modes = []
	data = []

	# if user branch has value then list (mode of payments) that has the (branch name) in them
	# if empty show error message.
	if(userBranch):
		payment_modes = frappe.db.get_list('Mode of Payment', filters={'name':["like",f"%{userBranch}%"]}, order_by='name desc')
	else:
		frappe.msgprint('هذا التقرير لإغلاق الحساب فقط, الرجاء الدخول بحساب مدير محل')
		return data

	# loop through mode of payments and add them to the result list as heads
	for p in payment_modes:
		list_head = [{'mode_of_payment': p.name,'indent':0, 'has_value': True}]
		data.append(list_head[0])

		# get the data for each mode of payment
		node_data = frappe.db.get_list('Payment Entry',
			fields=['mode_of_payment','name','paid_from_account_balance','base_paid_amount','received_amount', ('received_amount-base_paid_amount as diff'), 'posting_date', '1 as indent'],		
			filters={
			'status':"Submitted",
			'mode_of_payment':p.name,
			'posting_date':["between", (filters.get("from_date"),filters.get("to_date"))]}
			,order_by='posting_date desc')
		
		# loop through the data for said mode of payment and add it under its appropriate node
		# and add it to result list
		total_paid = 0
		total_recieved = 0
		total_diff = 0

		for nd in node_data:
			nd["has_value"] = False
			total_paid += nd.base_paid_amount
			total_recieved += nd.received_amount
			total_diff += nd.diff

			data.append(nd)
		
		c_total_row = {'paid_from_account_balance':'الاجمـالي','base_paid_amount': total_paid, 'received_amount': total_recieved,'diff': total_diff, 'indent':0, 'has_value': False}
		data.append(c_total_row)

		data.append({'mode_of_payment': '', 'indent':0, 'has_value': False})


	#return data list
	return data


def get_columns():

	return [
		# Mode of payment
		{
			"fieldname": "mode_of_payment",
			"label": _("طريقة الدفع"),
			"fieldtype": "Data",
			# "options": "Mode of Payment",
			"width": 130
		}
		,
		{
			"fieldname": "posting_date",
			"label": _("التاريخ"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		# name
		{
			"fieldname": "name",
			"label": _("الرقم الإشاري"),
			"fieldtype": "Data",
			"width": 150
		}
		,
		{
			"fieldname": "paid_from_account_balance",
			"label": _("رصيد الحساب"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "base_paid_amount",
			"label": _("الحساب"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "received_amount",
			"label": _("المسلم"),
			"fieldtype": "Data",
			"width": 100
		}
		,
		{
			"fieldname": "diff",
			"label": _("الفروقات"),
			"fieldtype": "Data",
			"width": 100
		}
		
		
	]