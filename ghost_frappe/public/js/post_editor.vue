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
