import frappe
from frappe.model.document import Document
from frappe.utils import cin, cstr
import json
import math
import re

class GhostPost(Document):
    def validate(self):
        self.generate_slug()
        self.calculate_reading_time()

    def generate_slug(self):
        if not self.slug and self.title:
            self.slug = frappe.scrub(self.title)
            # Ensure uniqueness
            if frappe.db.exists("Ghost Post", self.slug):
                count = frappe.db.count("Ghost Post", {"slug": ["like", f"{self.slug}%"]})
                self.slug = f"{self.slug}-{count + 1}"

    def calculate_reading_time(self):
        """Calculates reading time based on content blocks."""
        if not self.content:
            self.reading_time = 0
            return

        try:
            content_data = json.loads(self.content)
            text_content = ""
            
            if "blocks" in content_data:
                for block in content_data["blocks"]:
                    if block.get("type") in ["paragraph", "header"]:
                        text_content += " " + block.get("data", {}).get("text", "")
                    elif block.get("type") == "list":
                        items = block.get("data", {}).get("items", [])
                        text_content += " " + " ".join(items)

            # Average reading speed: 200 words per minute
            word_count = len(re.findall(r'\w+', text_content))
            self.reading_time = math.ceil(word_count / 200)
            
            # If there is a field for reading_time, set it. 
            # Otherwise it is available as an instance attribute during save.
            # self.db_set('reading_time', self.reading_time) 

        except Exception as e:
            frappe.log_error(f"Error calculating reading time for {self.name}: {str(e)}")
            self.reading_time = 0

    def get_reading_time(self):
        if not hasattr(self, 'reading_time'):
            self.calculate_reading_time()
        return self.reading_time
