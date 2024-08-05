const keystone = require('../bma-betstone'),
  apiManager = require('../lib/api'),
  Types = keystone.Field.Types,
  Logger = require('../lib/logger'),

  Widget = new keystone.List('widget', {
    nocreate: true,
    nodelete: true,
    map: { name: 'title' },
    autokey: { from: 'type brand', path: 'type_brand', unique: true },
    sortable: true,
    track: true
  });

function regenCache(brand) {
  return apiManager.run('widgets', {
    brand
  });
}

Widget.add({
  title: { type: Types.Text, required: true },
  type: { type: Types.Text, noedit: true, label: 'Type' },
  brand: { type: Types.Text, default: 'bma', hidden: true },
  disabled: { type: Types.Boolean, default: false, label: 'Inactive' },

  showExpanded: { type: Types.Boolean, default: true, label: 'Show expanded', initial: true },
  showFirstEvent: {
    type: Types.Boolean,
    default: true,
    label: 'Show first event',
    initial: true,
    hidden: true,
    dependsOn: { type: 'in-play' }
  },
  columns: {
    type: Types.Select,
    options: [
      { value: 'widgetColumn', label: 'Left column' },
      { value: 'rightColumn', label: 'Right column' },
      { value: 'both', label: 'Both' }
    ],
    default: 'rightColumn',
    emptyOption: false
  },
  showOn: {
    routes: {
      type: Types.Text,
      required: false,
      dependsOn: { type: 'match-centre' }
    },
    sports: {
      type: Types.Relationship,
      ref: 'sportCategory',
      many: true,
      required: false,
      dependsOn: { type: 'match-centre' }
    }
  },
  showOnMobile: { type: Types.Boolean, default: true, label: 'Show on Mobile', initial: true },
  showOnDesktop: { type: Types.Boolean, default: true, label: 'Show on Desktop', initial: true },
  showOnTablet: { type: Types.Boolean, default: true, label: 'Show on Tablet', initial: true }
});

Widget.schema.post('save', item => {
  keystone.list('User').model.findById(item.updatedBy, 'email').exec()
    .then(
      user => {
        Logger.info(
          'AKAMAI',
          'widget by user',
          user.email,
          '\t item:', item._id
        );
      },
      err => {
        Logger.error('AKAMAI', err);
      }
    );

  regenCache(item.brand);
});

Widget.schema.post('remove', item => {
  regenCache(item.brand);
});

Widget.defaultColumns = 'name, disabled, columns, showExpanded, showOnMobile, showOnDesktop, showOnTablet';
Widget.register();
