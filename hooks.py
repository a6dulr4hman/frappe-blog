app_name = "ghost_frappe"
app_title = "Ghost on Frappe"
app_publisher = "Ghost Architect"
app_description = "A professional, headless-ready blogging platform on Frappe."
app_email = "admin@example.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ghost_frappe/css/ghost_frappe.css"
# app_include_js = "/assets/ghost_frappe/js/ghost_frappe.js"

# include js, css files in header of web template
# web_include_css = "/assets/ghost_frappe/css/ghost_frappe.css"
# web_include_js = "/assets/ghost_frappe/js/ghost_frappe.js"

# Website Route Rules
# -------------------
# Map /news to the index page or a custom controller
website_route_rules = [
    {"from_route": "/news", "to_route": "ghost_frappe/www/index"},
    {"from_route": "/", "to_route": "ghost_frappe/www/index"},
    # API Routes
    {"from_route": "/api/method/ghost_frappe.api.get_posts", "to_route": "ghost_frappe.api.get_posts"},
]

# Disable default blog routes if necessary by overriding or handling 404s in controller
# Note: Frappe's default blog uses 'blog' route. We are using 'news' or root.

# DocType Class
# ---------------
# Override standard doctype classes
# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "Ghost Post": {
        "validate": "ghost_frappe.ghost_frappe.doctype.ghost_post.ghost_post.validate",
        "before_insert": "ghost_frappe.ghost_frappe.doctype.ghost_post.ghost_post.before_insert"
    }
}

# Role Based Permissions
# ----------------------
# While permissions are typically set in the database, we can define default roles here if using fixtures
# or enforce logic in 'has_permission' hooks.

# has_permission = {
#     "Ghost Post": "ghost_frappe.ghost_frappe.doctype.ghost_post.ghost_post.has_permission"
# }
