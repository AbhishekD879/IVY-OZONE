const keystone = require('../bma-betstone'),
  FooterLogoModel = keystone.list('footerLogos').model,
  StaticBlockModel = keystone.list('staticBlock').model;

// Populates footer logos and markup for BMA brand with data.

const footerLogos = [{
  title: 'GamCare certification',
  target: 'http://www.coral.co.uk/gamecare-certified',
  sortOrder: 0
}, {
  title: 'GamCare',
  target: 'http://www.gamcare.org.uk',
  sortOrder: 1
}, {
  title: '18+',
  target: 'http://responsiblegambling.coral.co.uk/',
  sortOrder: 2
}, {
  title: 'Norton secured',
  target: 'https://sealinfo.verisign.com/splash?form_file=fdf/splash.fdf&dn=www.coral.co.uk&lang=en&lang=20&sid=20&ms=MS',
  sortOrder: 3
}, {
  title: 'IBAS',
  target: 'http://www.ibas-uk.com',
  sortOrder: 4
}, {
  title: 'Gibraltar Gov',
  target: 'https://www.gibraltar.gov.gi/new/remote-gambling',
  sortOrder: 5
}, {
  title: 'GBGA',
  target: 'http://gbga.gi',
  sortOrder: 6
}, {
  title: 'When fun stops',
  target: 'http://www.coral.co.uk/whenthefunstopsstop',
  sortOrder: 7
}];

const footerMarkup = [{
  title: 'Footer Markup Top',
  uri: 'footer-markup-top',
  htmlMarkup: '<p>Coral.co.uk is operated by Coral Interactive (Gibraltar) Limited (company number 106323). Coral Interactive (Gibraltar) Limited&rsquo;s address is Suite 711, 1st Floor, Europort, Europort Road, Gibraltar GX11 1AA. Coral Interactive (Gibraltar) Limited is licensed by the Government of Gibraltar &amp; regulated by the&nbsp;<a target=\"_blank\" href=\"https:\/\/www.gibraltar.gov.gi\/new\/remote-gambling\">Gibraltar Gambling Commissioner<\/a>&nbsp;(RGL 059 &amp; 060). For customers accessing Coral.co.uk from Great Britain, the service is licensed and regulated by the&nbsp;<a target=\"_blank\" href=\"https:\/\/secure.gamblingcommission.gov.uk\/gccustomweb\/PublicRegister\/PRSearch.aspx?ExternalAccountId=39071\">Gambling Commission.<\/a>&nbsp;Coral is the registered&nbsp;trade mark&nbsp;of Coral Group Trading Ltd &copy; Gala Coral Group Ltd. All rights reserved.&nbsp;<\/p>\r\n<p>In-Play Information is for guidance only and can be subject to delays.&nbsp;<a target=\"_blank\" href=\"https:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/2141\">Click here<\/a>&nbsp;for more details.&nbsp;<\/p>'
}, {
  title: 'Footer Markup Bottom',
  uri: 'footer-markup-bottom',
  htmlMarkup: '<p>Bet Responsibly.&nbsp;<a target=\"_blank\" href=\"http:\/\/www.gambleaware.co.uk\">www.gambleaware.co.uk<\/a><\/p>\r\n<p><a target=\"_blank\" href=\"http:\/\/responsiblegambling.coral.co.uk\/\">Responsible Gambling&nbsp;<\/a>-&nbsp;<a target=\"_blank\" href=\"https:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/1700\">Shop rules<\/a>&nbsp;-&nbsp;<a target=\"_blank\" href=\"https:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/2141\">Online rules<\/a><\/p>\r\n<p><a target=\"_blank\" href=\" http:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/2130\/session\/L3RpbWUvMTQyNTk4NTgwNy9zaWQvLWtPNGlZZ20%3D\">Terms &amp; Conditions<\/a>&nbsp;-&nbsp;<a target=\"_blank\" href=\"https:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/2132\">Privacy policy<\/a>&nbsp;-&nbsp;<a target=\"_blank\" href=\"https:\/\/coral-eng.custhelp.com\/app\/answers\/detail\/a_id\/1719\">Fairness<\/a><\/p>\r\n<p><\/p>'
}];

function populateFooterLogos() {
  return Promise.all(
    footerLogos.map(logo => {
      const model = new FooterLogoModel(logo);
      return model.save();
    })
  );
}

function populateFooterMarkup() {
  return Promise.all(
    footerMarkup.map(staticBlock => {
      const model = new StaticBlockModel(staticBlock);
      return model.save();
    })
  );
}

module.exports = next => {
  return Promise.all([
    populateFooterLogos(),
    populateFooterMarkup()
  ]).then(
    () => next(),
    next
  );
};
