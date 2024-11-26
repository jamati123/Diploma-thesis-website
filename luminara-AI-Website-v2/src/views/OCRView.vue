<template>
    <div class="ocr-container">
      <h1>OCR Verarbeitung</h1>
      <div class="upload-section">
        <input type="file" @change="handleFileUpload" accept="image/*" />
        <img v-if="imageSrc" :src="imageSrc" alt="Bildvorschau" class="image-preview" />
        <button @click="processImage" :disabled="!imageFile || loading">
          {{ loading ? 'Verarbeiten...' : 'Bild verarbeiten' }}
        </button>
      </div>
      <div v-if="loading" class="loading-section">
        <div class="spinner"></div>
        <p>OCR läuft, bitte warten...</p>
      </div>
      <div v-if="ocr_text || markdown" class="result-section">
        <h2>Ergebnis:</h2>
        <div class="toggle-section">
          <label>
            <input type="radio" value="ocr" v-model="selectedVersion" />
            Rohe OCR-Ausgabe
          </label>
          <label>
            <input type="radio" value="markdown" v-model="selectedVersion" />
            Verbesserte Version
          </label>
        </div>
        <div v-if="selectedVersion === 'ocr'" class="raw-ocr-content">
          <h3>Rohe OCR-Ausgabe:</h3>
          <pre>{{ ocr_text }}</pre>
          <button @click="copyToClipboard(ocr_text)">Text kopieren</button>
        </div>
        <div v-if="selectedVersion === 'markdown'" class="markdown-content" v-html="renderedMarkdown"></div>
        <button v-if="selectedVersion === 'markdown'" @click="copyToClipboard(markdown)">
          Text kopieren
        </button>
        <p v-if="copySuccess" class="copy-success">Text wurde in die Zwischenablage kopiert!</p>
        <p v-if="copyError" class="copy-error">Kopieren fehlgeschlagen. Bitte versuche es erneut.</p>
      </div>
    </div>
  </template>
  
  <script>
  import MarkdownIt from 'markdown-it';
  import markdownItKatex from 'markdown-it-katex';
  import 'katex/dist/katex.min.css';
  import axios from 'axios';
  
  export default {
    name: 'OCRView',
    data() {
      return {
        imageFile: null,
        imageSrc: '',
        ocr_text: '',
        markdown: '',
        renderedMarkdown: '',
        loading: false, // Neuer Ladezustand
        selectedVersion: 'ocr', // Standardmäßig rohe OCR-Ausgabe
        copySuccess: false, // Erfolg beim Kopieren
        copyError: false,   // Fehler beim Kopieren
      };
    },
    methods: {
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (file && this.isAllowedFile(file.name)) {
          this.imageFile = file;
          this.imageSrc = URL.createObjectURL(file);
        } else {
          alert('Ungültiger Dateityp. Bitte lade ein Bild hoch.');
        }
      },
      isAllowedFile(filename) {
        const allowedExtensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'];
        const extension = filename.split('.').pop().toLowerCase();
        return allowedExtensions.includes(extension);
      },
      async processImage() {
        if (!this.imageFile) {
          alert('Bitte wähle ein Bild aus, bevor du es verarbeitest.');
          return;
        }
  
        const formData = new FormData();
        formData.append('image', this.imageFile);
  
        this.loading = true; // Ladezustand aktivieren
        this.copySuccess = false; // Rücksetzen des Kopier-Status
        this.copyError = false;
        this.ocr_text = '';
        this.markdown = '';
        this.renderedMarkdown = '';
  
        try {
          const response = await axios.post('http://localhost:5000/api/ocr', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
  
          if (response.data.ocr_text) {
            this.ocr_text = response.data.ocr_text;
          }
  
          if (response.data.markdown) {
            this.markdown = response.data.markdown;
            this.renderMarkdown();
          }
        } catch (error) {
          console.error('Fehler bei der Verarbeitung:', error);
          if (error.response && error.response.data && error.response.data.error) {
            alert(`Fehler: ${error.response.data.error}`);
          } else {
            alert('Es gab einen Fehler bei der Verarbeitung des Bildes.');
          }
        } finally {
          this.loading = false; // Ladezustand deaktivieren
        }
      },
      renderMarkdown() {
        const md = new MarkdownIt({
          html: true,
          linkify: true,
          typographer: true,
          breaks: true,
        }).use(markdownItKatex, {
          throwOnError: false,
          errorColor: '#cc0000',
        });
  
        this.renderedMarkdown = md.render(this.markdown);
      },
      async copyToClipboard(text) {
        if (!text) return;
  
        try {
          await navigator.clipboard.writeText(text);
          this.copySuccess = true;
          this.copyError = false;
          setTimeout(() => {
            this.copySuccess = false;
          }, 3000); // Erfolgsnachricht nach 3 Sekunden ausblenden
        } catch (error) {
          console.error('Kopieren fehlgeschlagen:', error);
          this.copyError = true;
          this.copySuccess = false;
          setTimeout(() => {
            this.copyError = false;
          }, 3000); // Fehlermeldung nach 3 Sekunden ausblenden
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .ocr-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .upload-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .upload-section input[type="file"] {
    margin-bottom: 10px;
  }
  
  .image-preview {
    max-width: 100%;
    height: auto;
    margin-top: 10px;
    border: 1px solid #ddd;
    padding: 5px;
    border-radius: 5px;
  }
  
  .loading-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
  }
  
  .spinner {
    border: 8px solid #f3f3f3; /* Light grey */
    border-top: 8px solid #007bff; /* Blue */
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 2s linear infinite;
    margin-bottom: 10px;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .result-section {
    margin-top: 20px;
  }
  
  .toggle-section {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
  
  .toggle-section label {
    margin: 0 10px;
    font-weight: bold;
  }
  
  .raw-ocr-content {
    background-color: #f1f1f1;
    padding: 15px;
    border-radius: 5px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
  }
  
  .markdown-content {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 5px;
    overflow: auto;
    border: 1px solid #ddd;
    margin-bottom: 10px;
  }
  
  .markdown-content h1,
  .markdown-content h2,
  .markdown-content h3,
  .markdown-content h4,
  .markdown-content h5,
  .markdown-content h6 {
    margin-top: 20px;
  }
  
  .markdown-content p {
    line-height: 1.6;
  }
  
  .markdown-content pre {
    background-color: #eee;
    padding: 10px;
    border-radius: 5px;
    overflow-x: auto;
  }
  
  .markdown-content code {
    background-color: #eee;
    padding: 2px 4px;
    border-radius: 3px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }
  
  button:hover:not(:disabled) {
    background-color: #0056b3;
  }
  
  /* Feedback-Nachrichten */
  .copy-success {
    color: green;
    margin-top: 10px;
  }
  
  .copy-error {
    color: red;
    margin-top: 10px;
  }
  </style>
  