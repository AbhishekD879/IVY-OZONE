import { AccountUpgradeLinkService } from './account-upgrade-link.service';

describe('AccountUpgradeLinkServiceTests', () => {
  let accountUpgradeLinkService,
    link,
    userService,
    productHomepagesConfig,
    userInterfaceConfig;

  beforeEach(() => {
    userService = {
      claims: new Map<string, string>([
        ['accbusinessphase', 'in-shop']
      ])
    };
    productHomepagesConfig = {
      portal: jasmine.createSpy()
    };
    userInterfaceConfig = {
      accountUpgradeLink: jasmine.createSpy()
    };

    accountUpgradeLinkService = new AccountUpgradeLinkService(userService, productHomepagesConfig, userInterfaceConfig);
  });

  describe('businessPhase()', () => {

    it('should call claims to get businessPhase', () => {
      expect(accountUpgradeLinkService.businessPhase).toEqual('in-shop');
    });
  });

  describe('inShopToMultiChannelLink()', () => {
    it('should return recently played games url', () => {
      link = 'http://dev.test.com';
      accountUpgradeLinkService.productHomepagesConfig.portal = 'http://dev.';
      accountUpgradeLinkService.userInterfaceConfig.accountUpgradeLink.imc = 'test.com';
      expect(accountUpgradeLinkService.inShopToMultiChannelLink).toEqual(link);
    });
  });

  describe('onlineToMultiChannelLink()', () => {
    it('should return recently played games url', () => {
      link = 'http://dev.test.com';
      accountUpgradeLinkService.productHomepagesConfig.portal = 'http://dev.';
      accountUpgradeLinkService.userInterfaceConfig.accountUpgradeLink.omc = 'test.com';
      expect(accountUpgradeLinkService.onlineToMultiChannelLink).toEqual(link);
    });
  });
});

