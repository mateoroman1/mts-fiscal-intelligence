ALLOWED_FILTER_OPERATORS = {
    "eq",
    "lt",
    "lte",
    "gt",
    "gte",
    "in",
}

DATASETS: dict[str, dict[str, str]] = {
    "reciepts_summary": {
        "endpoint": "/v1/accounting/mts/mts_table_1",
        "title": "Summary of Receipts, Outlays, and the Deficit/Surplus of the U.S. Government",
        "fields": {
            "record_date": "Record Date",
            "parent_id": "Parent ID",
            "classification_id": "Classification ID",
            "classification_desc": "Classification Description",
            "current_month_gross_rcpt_amt": "Current Month Gross Receipts Amount",
            "current_month_gross_outly_amt": "Current Month Gross Outlay Amount",
            "current_month_dfct_sur_amt": "Current Month Deficit Surplus Amount",
            "table_nbr": "Table Number",
            "src_line_nbr": "Source Line Number",
            "print_order_nbr": "Print Order Sequence Number",
            "line_code_nbr": "Line Code Number",
            "data_type_cd": "Data Type Code",
            "record_type_cd": "Record Type Code",
            "sequence_level_nbr": "Sequence Level Number",
            "sequence_number_cd": "Sequence Number Code",
            "record_fiscal_year": "Fiscal Year",
            "record_fiscal_quarter": "Fiscal Quarter Number",
            "record_calendar_year": "Calendar Year",
            "record_calendar_quarter": "Calendar Quarter Number",
            "record_calendar_month": "Calendar Month Number",
            "record_calendar_day": "Calendar Day Number"
        }
    },
    "budget_results_summary": {
        "endpoint": "/v1/accounting/mts/mts_table_2",
        "title": "Summary of Budget and Off-Budget Results and Financing of the U.S. Government",
        "fields": {
            "record_date": "Record Date",
            "parent_id": "Parent ID",
            "classification_id": "Classification ID",
            "classification_desc": "Classification Description",
            "current_month_budget_amt": "Current Month Budget Amount",
            "current_fytd_budget_amt": "Current Fiscal Year to Date Budget Amount",
            "prior_fytd_budget_amt": "Prior Fiscal Year to Date Budget Amount",
            "current_year_budget_est_amt": "Current Year Budget Estimate Amount",
            "next_year_budget_est_amt": "Next Year Budget Estimate Amount",
            "table_nbr": "Table Number",
            "src_line_nbr": "Source Line Number",
            "print_order_nbr": "Print Order Sequence Number",
            "line_code_nbr": "Line Code Number",
            "data_type_cd": "Data Type Code",
            "record_type_cd": "Record Type Code",
            "sequence_level_nbr": "Sequence Level Number",
            "sequence_number_cd": "Sequence Number Code",
            "record_fiscal_year": "Fiscal Year",
            "record_fiscal_quarter": "Fiscal Quarter Number",
            "record_calendar_year": "Calendar Year",
            "record_calendar_quarter": "Calendar Quarter Number",
            "record_calendar_month": "Calendar Month Number",
            "record_calendar_day": "Calendar Day Number"
        }
    }
}