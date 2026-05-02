exports.getTrendingTopics = (data) => client.post('/trending-topics', data);
exports.updateTrendingTopics = (data) => client.post('/trending-topics/update', data);