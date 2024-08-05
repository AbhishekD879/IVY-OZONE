const keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),
  initialDataManager = require('../lib/api/initialDataManager'),

  homeModule = keystone.mongoose.Schema({
    title: String,
    visibility: {
      enabled: Boolean,
      displayFrom: Date,
      displayTo: Date
    },
    eventsSelectionSettings: {
      from: Date,
      to: Date
    },
    displayOrder: Number,
    showExpanded: Boolean,
    badge: { type: String, default: '' },
    navItem: String,
    publishToChannels: [String],
    publishedDevices: {},
    maxSelections: Number,
    maxRows: Number,
    totalEvents: Number,
    footerLink: {
      text: String,
      url: String
    },
    dataSelection: {
      selectionType: String,
      selectionId: String
    },
    data: [keystone.mongoose.Schema.Types.Mixed]
  });

function regenCache(brand) {
  apiManager.run('modularContent', { brand });
  initialDataManager.regenCache(brand);
}

homeModule.post('save', item => {
  for (let i = 0; i < item.publishToChannels.length; i++) {
    const brand = item.publishToChannels[i];
    regenCache(brand);
  }
});

homeModule.post('remove', item => {
  for (let i = 0; i < item.publishToChannels.length; i++) {
    const brand = item.publishToChannels[i];
    regenCache(brand);
  }
});

module.exports = keystone.mongoose.model('HomeModule', homeModule);
