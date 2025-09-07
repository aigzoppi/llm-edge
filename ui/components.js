// components.js - Vue Components
const { createApp } = Vue;

// Header Component
const AppHeader = {
  template: `
    <header class="header">
      <h1>🔗 Egde LLM Demo</h1>
      <p>TestBed for Edge AI</p>
    </header>
  `
};

// Configuration Component
const ConfigSection = {
  props: ['baseUrl'],
  emits: ['update-base-url'],
  template: `
    <div class="section config-section">
      <h2>⚙️ Configuration</h2>
      <div class="form-group">
        <label for="baseUrl">Base URL:</label>
        <input 
          type="text" 
          id="baseUrl" 
          :value="baseUrl"
          @input="$emit('update-base-url', $event.target.value)"
          placeholder="http://localhost:3000"
          class="input-field">
      </div>
    </div>
  `
};

// Controls Component
const ControlsSection = {
  props: ['isLoading', 'status'],
  emits: ['start', 'stop'],
  template: `
    <div class="section controls-section">
      <h2>🎮 Controls</h2>
      <div class="button-group">
        <button 
          @click="$emit('start')" 
          :disabled="isLoading"
          class="btn btn-start">
          <span v-if="!isLoading">▶️ Start</span>
          <span v-else class="spinner">⏳</span>
          {{ isLoading ? 'Loading...' : 'Start' }}
        </button>
        
        <button 
          @click="$emit('stop')" 
          :disabled="isLoading"
          class="btn btn-stop">
          <span v-if="!isLoading">⏹️ Stop</span>
          <span v-else class="spinner">⏳</span>
          {{ isLoading ? 'Loading...' : 'Stop' }}
        </button>
      </div>
      
      <div class="status-indicator">
        <span class="status-dot" :class="status.type"></span>
        <span class="status-text">{{ status.message }}</span>
      </div>
    </div>
  `
};

// Text Section Component
const TextSection = {
  props: ['isLoading', 'textInput'],
  emits: ['update-text', 'send-text'],
  template: `
    <div class="section text-section">
      <h2>📝 Text Support</h2>
      <div class="form-group">
        <label for="textInput">Enter text:</label>
        <textarea 
          id="textInput" 
          :value="textInput"
          @input="$emit('update-text', $event.target.value)"
          placeholder="Enter your text here..." 
          rows="4"
          class="textarea-field">
        </textarea>
      </div>
      <div class="form-group">
        <button 
          @click="$emit('send-text')" 
          :disabled="isLoading || !textInput.trim()"
          class="btn btn-primary">
          <span v-if="!isLoading">📤 Send Text</span>
          <span v-else class="spinner">⏳ Sending...</span>
        </button>
      </div>
    </div>
  `
};

// Response Section Component
const ResponseSection = {
  props: ['response'],
  emits: ['clear'],
  computed: {
    hasResponse() {
      return this.response !== null;
    }
  },
  template: `
    <div class="section response-section">
      <h2>📡 Response</h2>
      <div class="response-area">
        <div v-if="!hasResponse" class="placeholder">
          API responses will appear here...
        </div>
        
        <div v-else-if="response.success" class="response-success">
          <strong>✅ Success ({{ response.status }})</strong><br>
          <pre>{{ JSON.stringify(response.data, null, 2) }}</pre>
        </div>
        
        <div v-else class="response-error">
          <strong>❌ Error ({{ response.status }})</strong><br>
          <strong>Message:</strong> {{ response.error }}<br>
          <strong>Status:</strong> {{ response.statusText }}
        </div>
      </div>
      
      <button @click="$emit('clear')" class="btn btn-secondary">
        🗑️ Clear
      </button>
    </div>
  `
};

// Logs Section Component
const LogsSection = {
  props: ['logs'],
  emits: ['clear'],
  template: `
    <div class="section logs-section">
      <h2>📊 Activity Log</h2>
      <div class="log-area">
        <div v-if="logs.length === 0" class="placeholder">
          Activity logs will appear here...
        </div>
        
        <div 
          v-for="log in logs" 
          :key="log.id"
          class="log-entry"
          :class="log.type">
          <div class="log-timestamp">[{{ log.timestamp }}]</div>
          <div class="log-message">{{ log.message }}</div>
        </div>
      </div>
      
      <button @click="$emit('clear')" class="btn btn-secondary">
        🗑️ Clear Logs
      </button>
    </div>
  `
};
