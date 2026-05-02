const { Sequelize } = require('sequelize');
const { logger } = require('../middleware/logger');

// Retrieve MySQL connection configuration from environment variables
const sequelize = new Sequelize(
  process.env.MYSQL_DATABASE || 'moksh_db',
  process.env.MYSQL_USER || 'root',
  process.env.MYSQL_PASSWORD || '',
  {
    host: process.env.MYSQL_HOST || 'localhost',
    dialect: 'mysql',
    logging: false, // Set to true to see SQL queries in the console
  }
);

const connectMysqlDB = async () => {
  try {
    await sequelize.authenticate();
    logger.info('MySQL connected successfully.');
    // Sync models
    await sequelize.sync({ alter: true }); // Automatically updates schema
  } catch (error) {
    logger.error('Unable to connect to the MySQL database:', error);
  }
};

module.exports = { sequelize, connectMysqlDB };
