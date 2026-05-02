const axios = require('axios');
const { logger } = require('../middleware/logger');

const httpClient = (baseURL) => {
  const client = axios.create({ baseURL, timeout: 30000 });

  client.interceptors.request.use((config) => {
    logger.info(`Outgoing request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  });

  client.interceptors.response.use(
    (response) => response.data,
    (error) => {
      logger.error('HTTP client error:', error.message);
      throw error;
    }
  );

  return client;
};

module.exports = httpClient;