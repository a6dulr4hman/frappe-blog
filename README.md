# Ghost on Frappe

A professional, headless-ready blogging platform on the Frappe Framework.

## Installation

1.  Get the app:
    ```bash
    bench get-app ghost_frappe https://github.com/yourusername/ghost_frappe
    ```

2.  Install the app on your site:
    ```bash
    bench --site your-site.name install-app ghost_frappe
    ```

3.  Migrate database:
    ```bash
    bench --site your-site.name migrate
    ```

## Editor.js Vue Component Setup

To enable the custom "Ghost-like" writing experience, you need to set up the Vue.js component in the Desk.

### 1. Create the Vue Component

Create a file at `ghost_frappe/public/js/post_editor.vue` with the following content:

```vue
<template>
  <div class="ghost-editor-container">
    <div class="editor-header">
      <input v-model="title" placeholder="Post Title" class="title-input" @blur="saveDraft" />
    </div>
    <div id="editorjs" class="editor-canvas"></div>
  </div>
</template>

<script>
import EditorJS from '@editorjs/editorjs';
import Header from '@editorjs/header';
import List from '@editorjs/list';
import ImageTool from '@editorjs/image';

export default {
  data() {
    return {
      editor: null,
      title: '',
      docName: null,
    };
  },
  mounted() {
    this.initEditor();
    // Load existing data if editing
    const route = frappe.get_route();
    if (route[0] === 'ghost-editor' && route[1]) {
        this.docName = route[1];
        this.loadDoc();
    }
  },
  methods: {
    initEditor(data = {}) {
      this.editor = new EditorJS({
        holder: 'editorjs',
        tools: {
          header: Header,
          list: List,
          image: {
            class: ImageTool,
            config: {
              endpoints: {
                byFile: '/api/method/upload_file', // Frappe upload endpoint
              }
            }
          }
        },
        data: data,
        onChange: () => {
            this.saveDraft();
        }
      });
    },
    loadDoc() {
        frappe.db.get_doc('Ghost Post', this.docName).then(doc => {
            this.title = doc.title;
            if (doc.content) {
                this.editor.isReady.then(() => {
                    this.editor.render(JSON.parse(doc.content));
                });
            }
        });
    },
    saveDraft() {
        if (!this.docName) return; // Handle new creation logic separately
        
        this.editor.save().then((outputData) => {
            frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    doctype: 'Ghost Post',
                    name: this.docName,
                    fieldname: {
                        'title': this.title,
                        'content': JSON.stringify(outputData)
                    }
                }
            });
        });
    }
  }
};
</script>

<style scoped>
.ghost-editor-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
    background: white;
    min-height: 100vh;
}
.title-input {
    font-size: 2.5rem;
    font-weight: bold;
    border: none;
    width: 100%;
    outline: none;
    margin-bottom: 20px;
}
</style>
```

### 2. Register the Page in `hooks.py`

Ensure your `hooks.py` includes the compiled JS bundle. If you are using the standard build system, add:

```python
app_include_js = "/assets/ghost_frappe/js/ghost_frappe.bundle.js"
```

### 3. Build the Assets

Run the build command to compile the Vue component:

```bash
bench build --app ghost_frappe
```

### 4. Create a Page in Desk

1.  Go to **Desk > Page List**.
2.  Create a new Page named `ghost-editor`.
3.  Set the **Module** to `Ghost`.
4.  In the **Page Controller**, you can link to the JavaScript file that mounts this Vue component.

Alternatively, you can use a **Client Script** or **Form Script** on the `Ghost Post` doctype to redirect the "Edit" button to this custom page:

```javascript
frappe.ui.form.on('Ghost Post', {
    refresh: function(frm) {
        frm.add_custom_button('Open Ghost Editor', () => {
            frappe.set_route('ghost-editor', frm.doc.name);
        });
    }
});
```
