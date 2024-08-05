import * as oxygenRetailConstants from '@app/retail/constants/retail.constant';

export const UPGRADE_ACCOUNT_DIALOG = {
  ...oxygenRetailConstants.UPGRADE_ACCOUNT_DIALOG,
  inshopUpgrade: {
    ...oxygenRetailConstants.UPGRADE_ACCOUNT_DIALOG.inshopUpgrade,
    dialogHeader: 'inshop-upgrade-dialog-header',
    dialogButton: 'inshop-upgrade-dialog-button',
    inshopGrid: 'inshop-upgrade-grid'
  },
  onlineUpgrade: {
    dialogHeader: 'online-upgrade-dialog-header',
    dialogBody: 'online-upgrade-dialog-body',
    dialogButton: 'online-upgrade-dialog-button',
    onlineGrid: 'online-upgrade-grid'
  }
};

export const LINK_TITLE = {
  useGridOnline: 'Use GRID Online',
  activateCard: 'Activate Card'
};

export const RETAIL_PAGE = {
  title: 'Grid',
  bannersPage: 'retail',
  trackingLocation: 'grid'
};

export const RETAIL_OVERLAY = {
  retailOverlay: 'retailOverlayRemain',
  grid: 'grid',
  domain: '.ladbrokes.com'
};
