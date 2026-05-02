const redis = require('redis');
const { logger } = require('../middleware/logger');

const client = redis.createClient({ url: process.env.REDIS_URL });

client.on('error', (err) => logger.error('Redis error:', err));
client.on('connect', () => logger.info('Redis connected'));

client.connect();

module.exports = client;