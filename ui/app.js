// app.js - Vue Application
const { createApp } = Vue;

const app = createApp({
  data() {
    return {
      baseUrl: 'http://localhost:3000',
      textInput: '',
      isLoading: false,
      response: null,
      logs: [],
      status: {
        type: 'ready',
        message: 'Ready'
      },
      logIdCounter: 0
    };
  },
  
  methods: {
    updateBaseUrl(value) {
      this.baseUrl = value;
    },
    
    updateText(value) {
      this.textInput = value;
    },
    
    async handleStart() {
      await this.makeRequest('GET', '/start');
    },
    
    async handleStop() {
      await this.makeRequest('GET', '/stop');
    },
    
    async handleSendText() {
      if (!this.textInput.trim()) {
        this.showError('Please enter some text first');
        return;
      }
      
      await this.makeRequest('POST', '/text', { text: this.textInput });
    },
    
    async makeRequest(method, endpoint, data = null) {
      if (!this.baseUrl.trim()) {
        this.showError('Please enter a base URL');
        return;
      }
      
      this.isLoading = true;
      this.setStatus('loading', `${method} ${endpoint}...`);
      this.addLog(`Making ${method} request to ${endpoint}`, 'info');
      
      try {
        const result = await window.electronAPI.makeApiCall(method, endpoint, this.baseUrl, data);
        
        if (result.success) {
          this.setStatus('success', `${method} ${endpoint} successful`);
          this.response = result;
          this.addLog(`✅ ${method} ${endpoint} - ${result.status} ${result.statusText}`, 'success');
        } else {
          this.setStatus('error', `${method} ${endpoint} failed`);
          this.response = result;
          this.addLog(`❌ ${method} ${endpoint} - ${result.status} ${result.statusText}`, 'error');
        }
      } catch (error) {
        this.setStatus('error', 'Request failed');
        this.showError(`Request failed: ${error.message}`);
        this.addLog(`❌ ${method} ${endpoint} - ${error.message}`, 'error');
      } finally {
        this.isLoading = false;
      }
    },
    
    setStatus(type, message) {
      this.status = { type, message };
    },
    
    showError(message) {
      this.response = {
        success: false,
        error: message,
        status: 0,
        statusText: 'Client Error'
      };
    },
    
    addLog(message, type = 'info') {
      const log = {
        id: ++this.logIdCounter,
        message,
        type,
        timestamp: new Date().toLocaleTimeString()
      };
      
      this.logs.unshift(log);
      
      // Keep only last 50 log entries
      if (this.logs.length > 50) {
        this.logs = this.logs.slice(0, 50);
      }
    },
    
    clearResponse() {
      this.response = null;
    },
    
    clearLogs() {
      this.logs = [];
    }
  },
  
  components: {
    AppHeader,
    ConfigSection,
    ControlsSection,
    TextSection,
    ResponseSection,
    LogsSection
  }
});

app.mount('#app');
