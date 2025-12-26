/** API service for chat functionality */
class ChatApiService {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  /**
   * Send a chat message and get a response
   * @param {string} query - The user's question
   * @param {string} mode - The chat mode ('full_book' or 'selected_text')
   * @param {string} [selectedText] - Text selected by the user (for selected_text mode)
   * @param {string} [sessionId] - Session identifier
   * @returns {Promise<Object>} The chat response
   */
  async sendMessage(query, mode = 'full_book', selectedText = null, sessionId = null) {
    const requestBody = {
      query,
      mode,
    };

    if (selectedText) {
      requestBody.selected_text = selectedText;
    }

    if (sessionId) {
      requestBody.session_id = sessionId;
    }

    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Get relevant context for a query without generating a response
   * @param {string} query - The query to search for
   * @param {number} [topK=5] - Number of results to return
   * @param {string} [selectedText] - Text to search within (for selected_text mode)
   * @returns {Promise<Object>} The retrieved context
   */
  async retrieveContext(query, topK = 5, selectedText = null) {
    const params = new URLSearchParams({
      query,
      top_k: topK.toString(),
    });

    if (selectedText) {
      params.append('selected_text', selectedText);
    }

    try {
      const response = await fetch(`${this.baseURL}/retrieve?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error retrieving context:', error);
      throw error;
    }
  }

  /**
   * Check if the chat API is healthy
   * @returns {Promise<Object>} Health check response
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * Ingest content into the knowledge base
   * @param {string} sourcePath - Path to the source content
   * @param {boolean} [reindex=false] - Whether to reindex existing content
   * @returns {Promise<Object>} Ingestion response
   */
  async ingestContent(sourcePath, reindex = false) {
    const requestBody = {
      source_path: sourcePath,
      reindex,
    };

    try {
      const response = await fetch(`${this.baseURL}/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error ingesting content:', error);
      throw error;
    }
  }
}

// Create a singleton instance
const chatApiService = new ChatApiService();

// Export both the class and the instance
export { ChatApiService };
export default chatApiService;