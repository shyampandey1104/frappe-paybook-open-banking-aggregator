# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "paybook_sync"
app_title = "Frappe Paybook Open Banking Aggregator"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Paybook Open Banking Aggregator for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/paybook_sync/css/paybook_sync.bundle.css"
app_include_js = "/assets/paybook_sync/js/paybook_sync.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "paybook_sync.engine.on_document_submit",
        "on_cancel": "paybook_sync.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "paybook_sync.engine.daily_scheduled_sync"
    ]
}
