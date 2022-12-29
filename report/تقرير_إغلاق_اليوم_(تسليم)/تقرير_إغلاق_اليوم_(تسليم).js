// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["تقرير إغلاق اليوم (تسليم)"] = {
	"filters": [
		{
            fieldname:"from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.add_days(frappe.datetime.get_today(), -1)
        },
        {
            fieldname:"to_date",
            label: "To Date",
            fieldtype: "Date"
        },
	]
    ,
    "tree":true,
	"name_field":"mode_of_payment",
	"parent_field":"mode_of_payment",
	"initial_depth":2
};

// erpnext.utils.add_dimensions('تقرير إغلاق اليوم (تسليم)', 6);
