<template>
  <div class="ollama-chat">
    <h2>Powered by Ollama and Flask-API</h2>
    <h4>
      Genereller Chatbot für die Kommunikation mit Ollama, einem KI-Modell, das auf der LLaMA-Architektur basiert.
    </h4>

    <!-- Dropdown zur Auswahl des KI-Modells -->
    <div class="model-selection" :class="{ 'dark-mode': isDarkMode }">
      <label for="model">Wähle ein KI-Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="llama3.2:1b">LLaMA 3.2 - 1B von Meta (Besonders schnell)</option>
        <option value="llama3.2">LLaMA 3.2 - 2B von Meta (neuestes Modell, langsamer als 1B)</option>
        <option value="gemma2">Gemma2 von Google (langsamer)</option>
        <option value="llama3.1">LLaMA 3.1 von Meta (älter und langsamer)</option>
        <option value="llava:13b">LLaVA 13B (am langsamsten)</option>
      </select>
    </div>

    <!-- Anzeige der Nachrichten im Chat-Format -->
    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.type, { 'dark-mode': isDarkMode }]"
      >
        <p v-if="message.type === 'user'">{{ message.text }}</p>
        <div v-else-if="message.type === 'ollama'" v-html="renderMarkdown(message.text)"></div>
      </div>
    </div>

    <!-- Eingabefeld und Button -->
    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Frag Ollama..."
        @keydown.enter="sendMessage"
        class="chat-input"
      />
      <button @click="sendMessage" class="send-button" :disabled="loading">
        <i class="fas fa-paper-plane"></i> Absenden
      </button>
    </div>

    <div v-if="loading" class="loading">Lädt...</div>
    <div v-if="error" class="error">
      <p>Es gab ein Problem bei der Kommunikation mit Ollama: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import MarkdownIt from "markdown-it";
import markdownItKatex from "markdown-it-katex";
import "katex/dist/katex.min.css";
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // Wähle ein beliebiges Theme

export default {
  data() {
    return {
      userInput: "",
      loading: false,
      error: "",
      messages: [], // Hier werden die Nachrichten (Benutzer + Ollama) gespeichert
      selectedModel: "llama3.2:1b", // Standardmäßig ausgewähltes Modell für Ollama
      isDarkMode: false, // Dark Mode Status
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "") {
        this.error = "Prompt darf nicht leer sein!";
        return;
      }

      // Füge die Benutzernachricht der Nachrichtenliste hinzu
      this.messages.push({ type: "user", text: this.userInput });

      this.loading = true;
      this.error = "";

      try {
        // Anfrage an Ollama senden
        const response = await axios.post("http://10.10.11.11:5000/ask_ollama", {
          prompt: this.userInput,
          model: this.selectedModel,
        });

        if (response.data.choices) {
          const botResponse = response.data.choices[0].text;
          this.messages.push({ type: "ollama", text: botResponse });
        } else if (response.data.error) {
          this.error = response.data.error;
        }
      } catch (err) {
        this.error = `Fehler: ${err.message}`;
      } finally {
        this.loading = false;
        this.userInput = ""; // Eingabefeld zurücksetzen
        this.$nextTick(() => {
          this.attachCopyButtons();
        });
      }
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.body.classList.toggle('dark-mode', this.isDarkMode);
      document.querySelector('.ollama-chat').classList.toggle('dark-mode', this.isDarkMode);
    },
    renderMarkdown(text) {
      const md = new MarkdownIt({
        html: true,
        linkify: true,
        typographer: true,
        breaks: true,
        highlight: function (str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return '<pre class="hljs"><code>' +
                     hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
                     '</code></pre>';
            } catch (__) {}
          }

          return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
        }
      }).use(markdownItKatex);

      // Überschreiben des Codeblock-Renderers
      const defaultFence = md.renderer.rules.fence || function(tokens, idx, options, env, self) {
        return self.renderToken(tokens, idx, options);
      };

      md.renderer.rules.fence = function (tokens, idx, options, env, self) {
        const token = tokens[idx];
        const code = token.content;
        const lang = token.info.trim().split(/\s+/g)[0];

        // Generiere eine eindeutige ID für den Codeblock
        const uniqueId = `copy-btn-${idx}-${Math.random().toString(36).substr(2, 9)}`;

        // Render den Codeblock mit einem Copy-Button
        return `
          <div class="code-block">
            <button class="copy-button" data-clipboard-target="#${uniqueId}">Copy</button>
            <pre class="hljs"><code id="${uniqueId}" class="${lang}">${md.utils.escapeHtml(code)}</code></pre>
          </div>
        `;
      };

      return md.render(text);
    },
    attachCopyButtons() {
      const buttons = this.$el.querySelectorAll('.copy-button');
      buttons.forEach(button => {
        button.addEventListener('click', () => {
          const target = button.getAttribute('data-clipboard-target');
          const codeElement = this.$el.querySelector(target);
          if (codeElement) {
            const text = codeElement.innerText;
            navigator.clipboard.writeText(text).then(() => {
              // Optional: Feedback für den Nutzer
              button.textContent = 'Copied!';
              setTimeout(() => {
                button.textContent = 'Copy';
              }, 2000);
            }).catch(err => {
              console.error('Kopieren fehlgeschlagen:', err);
            });
          }
        });
      });
    },
  },
  watch: {
    messages(newMessages) {
      this.$nextTick(() => {
        const chatBox = this.$el.querySelector('.chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    },
  },
  mounted() {
    // Initiales Anhängen der Copy-Buttons falls es schon Nachrichten gibt
    this.$nextTick(() => {
      this.attachCopyButtons();
    });
  },
};
</script>

<style scoped>
/* Grundlegende Stile für die Chat-Komponente */
.ollama-chat {
  font-family: 'Roboto', sans-serif;
  margin: 20px auto;
  padding: 25px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 12px;
  max-width: 700px;
  background-color: #f0f4f8; /* Helles Grau für den allgemeinen Hintergrund */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative; /* Für den Dark Mode Toggle Button */
}

/* Dark Mode Stile */
.ollama-chat.dark-mode {
  background-color: #1e1e1e; /* Dunkles Grau für den Hintergrund */
  border-color: #444; /* Dunkleres Grau für Ränder */
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1); /* Heller Schatten */
}

.ollama-chat.dark-mode h2 {
  color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

/* Überschrift */
.ollama-chat h2 {
  font-size: 1.8rem;
  color: #1e90ff; /* Kräftiges Blau */
  text-align: center;
  margin-bottom: 10px;
}

/* Modell-Auswahl */
.model-selection {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.model-selection label {
  font-weight: 500;
  color: #333;
}

.ollama-chat.dark-mode .model-selection label {
  color: #fff;
}

.model-selection select {
  padding: 10px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  transition: border-color 0.3s;
}

.ollama-chat.dark-mode .model-selection select {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

.model-selection select:focus {
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  outline: none;
}

.ollama-chat.dark-mode .model-selection select:focus {
  border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
}

/* Chat-Box */
.chat-box {
  flex: 1;
  max-height:
