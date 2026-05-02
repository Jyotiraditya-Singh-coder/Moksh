const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/mysqlDb');

const MysqlUser = sequelize.define('User', {
  clerkId: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    primaryKey: true,
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true,
    },
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: true,
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: true,
  },
  role: {
    type: DataTypes.ENUM('student', 'teacher', 'admin'),
    defaultValue: 'student',
  },
  // Personalized tracking details
  preferences: {
    type: DataTypes.JSON, 
    allowNull: true,
    defaultValue: {}
  },
  learningGoals: {
    type: DataTypes.JSON,
    allowNull: true,
    defaultValue: []
  },
  lastLoginAt: {
    type: DataTypes.DATE,
    allowNull: true,
  }
}, {
  timestamps: true, // Adds createdAt and updatedAt
  tableName: 'users'
});

module.exports = MysqlUser;
