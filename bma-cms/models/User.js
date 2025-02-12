const keystone = require('../bma-betstone'),
  Types = keystone.Field.Types,
  User = new keystone.List('User');

User.add({
  name: { type: Types.Name, required: true, index: true },
  email: { type: Types.Email, initial: true, required: true, index: true },
  brandCode: { type: Types.Text, default: 'bma', hidden: true },
  password: { type: Types.Password, initial: true, required: true }
},
  'Permissions',
  {
    isAdmin: { type: Boolean, label: 'Can access Keystone', index: true }
  });

// Provide access to Keystone
User.schema.virtual('canAccessKeystone').get(function() {
  return this.isAdmin;
});

/**
 * Registration
 */

User.defaultColumns = 'name, email, isAdmin';
User.register();
