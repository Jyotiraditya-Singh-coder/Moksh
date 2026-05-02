const MysqlUser = require('../models/MysqlUser');
const { Webhook } = require('svix');
const { logger } = require('../middleware/logger');

// Clerk Webhook Secret from environment
const clerkWebhookSecret = process.env.CLERK_WEBHOOK_SECRET;

exports.clerkWebhook = async (req, res) => {
  if (!clerkWebhookSecret) {
    logger.error('CLERK_WEBHOOK_SECRET missing');
    return res.status(500).json({ error: 'Config missing' });
  }

  // Get the headers
  const svix_id = req.headers['svix-id'];
  const svix_timestamp = req.headers['svix-timestamp'];
  const svix_signature = req.headers['svix-signature'];

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return res.status(400).json({ error: 'Error occured -- no svix headers' });
  }

  // Get the body
  const payload = req.body;
  
  // Express usually parses to JSON. For svix we usually need raw string, 
  // so we might need `bodyParser.raw()` in the router specifically for this route.
  // Assuming it's passed from a raw middleware:
  const body = payload.toString('utf8');

  // Create a new webhooks instance
  const wh = new Webhook(clerkWebhookSecret);

  let evt;

  try {
    // Verify payload
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    });
  } catch (err) {
    logger.error('Error verifying webhook:', err.message);
    return res.status(400).json({ error: 'Error verifying webhook' });
  }

  const eventType = evt.type;

  // Handle User Creation and Updates
  if (eventType === 'user.created' || eventType === 'user.updated') {
    const { id, email_addresses, first_name, last_name } = evt.data;
    const primaryEmail = email_addresses?.length ? email_addresses[0].email_address : null;

    try {
      await MysqlUser.upsert({
        clerkId: id,
        email: primaryEmail,
        firstName: first_name || '',
        lastName: last_name || '',
        lastLoginAt: new Date()
      });
      logger.info(`User ${id} synced to MySQL successfully`);
    } catch (err) {
      logger.error('Error saving user to MySQL:', err);
      return res.status(500).json({ error: 'Database error' });
    }
  }

  // Handle User Deletion
  if (eventType === 'user.deleted') {
    const { id } = evt.data;
    try {
      await MysqlUser.destroy({ where: { clerkId: id } });
      logger.info(`User ${id} deleted from MySQL`);
    } catch (err) {
      logger.error('Error deleting user from MySQL:', err);
      return res.status(500).json({ error: 'Database error' });
    }
  }

  return res.status(200).json({ success: true });
};

// Fetch personalized details based on Clerk Authentication
exports.getUserProfile = async (req, res) => {
  try {
    // With @clerk/express, req.auth contains the authenticated user's clerk token info
    if (!req.auth || !req.auth.userId) {
      return res.status(401).json({ error: 'Unauthenticated' });
    }

    const { userId } = req.auth;
    const user = await MysqlUser.findOne({ where: { clerkId: userId } });

    if (!user) {
      return res.status(404).json({ error: 'User not found in local db' });
    }

    res.json({ user });
  } catch (error) {
    logger.error('user profile fetch error', error);
    res.status(500).json({ error: 'Server error fetching user profile' });
  }
};

exports.updateUserProfile = async (req, res) => {
  try {
    if (!req.auth || !req.auth.userId) {
      return res.status(401).json({ error: 'Unauthenticated' });
    }

    const { userId } = req.auth;
    const { preferences, learningGoals, role } = req.body;

    const [updated] = await MysqlUser.update({
      preferences,
      learningGoals,
      role
    }, { where: { clerkId: userId } });

    const updatedUser = await MysqlUser.findOne({ where: { clerkId: userId } });
    res.json({ user: updatedUser });
  } catch (error) {
    logger.error('user profile update error', error);
    res.status(500).json({ error: 'Server error updating user profile' });
  }
};

// Sync user from frontend immediately
exports.syncUser = async (req, res) => {
  try {
    if (!req.auth || !req.auth.userId) {
      return res.status(401).json({ error: 'Unauthenticated' });
    }

    const { userId } = req.auth;
    const { email, firstName, lastName } = req.body;

    await MysqlUser.upsert({
      clerkId: userId,
      email: email || '',
      firstName: firstName || '',
      lastName: lastName || '',
      lastLoginAt: new Date()
    });

    logger.info(User \ synced to MySQL successfully via generic sync);
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in syncUser:', error);
    res.status(500).json({ error: 'Server error syncing user' });
  }
};
