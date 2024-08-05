var keystone = require('../../');

exports = module.exports = function(req, res) {
	if (req.cookies.brand === 'rcomb') {
		res.redirect('/keystone/banners')
	} else {
		keystone.render(req, res, 'home', {
			section: 'home',
			page: 'home',
			title: keystone.get('name') || 'Keystone',
			orphanedLists: keystone.getOrphanedLists()
		});
	}
};
