'use strict';
const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  Logs = new keystone.List('dashboard', {
    nocreate: true,
    nodelete: true,
    noedit: true,
    defaultSort: '-currentTime',
    track: true,
    map: { name: 'currentTime' }
  });

Logs.add({
  domains: { type: Types.Text, label: 'Filenames' },
  status: { type: Types.Text, label: 'HTTP Status' },
  currentTime: { type: Types.Datetime, label: 'Submission Time' },
  estimatedTime: { type: Types.Text, label: 'Estimated Time (sec)' },
  purgeID: { type: Types.Text, label: 'Purge ID' },
  progressURI: { type: Types.Text, label: 'Progress URI' },
  type: { type: Types.Text, label: 'Request Type' },
  supportID: { type: Types.Text, label: 'Support ID' }
});

/**
 * Registration
 */

Logs.defaultColumns = 'currentTime, type, status, estimatedTime, purgeID, progressURI, supportID';
Logs.register();
