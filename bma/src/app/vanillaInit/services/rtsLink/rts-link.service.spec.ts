import { RtsLinkService } from './rts-link.service';

describe('RtsLinkServiceTests', () => {
  let rtsLinkService,
    link,
    productHomepagesConfig,
    userInterfaceConfig;

  beforeEach(() => {
    productHomepagesConfig = {
      portal: jasmine.createSpy()
    };
    userInterfaceConfig = {
      rtsLink: jasmine.createSpy()
    };

    rtsLinkService = new RtsLinkService(productHomepagesConfig, userInterfaceConfig);
  });

  describe('getRtsLink()', () => {

    it('should create RTS Link', () => {
      link = 'http://dev.test.com';
      rtsLinkService.productHomepagesConfig.portal = 'http://dev.';
      rtsLinkService.userInterfaceConfig.rtsLink = 'test.com';
      expect(rtsLinkService['getRtsLink']()).toEqual(link);
    });
  });
});
