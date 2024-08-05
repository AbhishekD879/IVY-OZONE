import { ITrackEvent } from '@core/services/gtm/models';

export const BET_FILTER = {
  BOOTSTRAP_BET_FILTER: 'BOOTSTRAP_BET_FILTER',
  DESTROY_BET_FILTER: 'DESTROY_BET_FILTER',
  BF_ADD_TO_BETSLIP: 'BF_ADD_TO_BETSLIP',
  REDIRECT_TO_PREV_PAGE_BET_FILTER: 'REDIRECT_TO_PREV_PAGE_BET_FILTER'
};

export const DIGITAL_COUPONS = {
  BOOTSTRAP_DIGITAL_COUPONS: 'BOOTSTRAP_DIGITAL_COUPONS',
  DESTROY_DIGITAL_COUPONS: 'DESTROY_DIGITAL_COUPONS',
  REDIRECT_TO_PREV_PAGE_DIGITAL_COUPONS: 'REDIRECT_TO_PREV_PAGE_DIGITAL_COUPONS'
};

export const SAVED_BETCODES = {
  REDIRECT_TO_PREV_PAGE_SAVED_BETCODES: 'REDIRECT_TO_PREV_PAGE_SAVED_BETCODES'
};

export const UPGRADE_ACCOUNT_DIALOG = {
  inshopUpgrade: {
    dialogBody: 'inshop-upgrade-dialog-body'
  }
};

export const RETAIL_PAGE = {
  title: 'Connect',
  bannersPage: 'retail',
  trackingLocation: 'connect'
};

export const BET_FILTER_DIALOG = {
  modes: {
    online: 'online',
    inshop: 'inshop'
  }
};

export const BET_TRACKER = {
  BOOTSTRAP_BET_TRACKER: 'BOOTSTRAP_BET_TRACKER',
  DESTROY_BET_TRACKER: 'DESTROY_BET_TRACKER',
  DESTROY_SUBSCRIPTIONS: 'DESTROY_SUBSCRIPTIONS'
};

export const UPGRADE_ACCOUNT_MENU_ITEMS: string[] = [
  'deposit',
  'deposit/registered',
  'withdraw',
  'freebets',
];

// config constants
export type RETAIL_MENU_LOCATION = 'HUB' | 'RHM' | 'AZ';
export type UPGRADE_DIALOG_LOCATION = 'LOGIN' | 'HUB';

// Football filter confirm dialog constants
export const FOOTBALL_FILTER_CONFIRM = {
  CONFIRM_ONLINE: 'football-bet-filter-confirm-online',
  CONFIRM_INSHOP: 'football-bet-filter-confirm-inshop',
  DEFAULT_RADIO_BUTTON: 'inshop',
  INSHOP_RADIO: 'inshop',
  ONLINE_RADIO: 'online'
};

// Shop Locator constants
export const SHOP_LOCATOR_PARAMS = {
  ALLOW: 'Ok',
  DENY: 'Dont Allow',
  SHOP_LOCATION_POPUP: 'Shop Locator Pop-up',
  SHOP_LOCATION_LOCATION: 'locationPermission'
};

export const GRID_GA_TRACKING: ITrackEvent = {
  event: 'trackEvent',
  eventCategory: 'Grid',
  eventAction: null,
  eventLabel: null
};
