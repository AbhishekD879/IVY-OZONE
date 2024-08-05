import { CasinoGamesService } from './casino-games.service';

describe('CasinoGamesServiceTests', () => {
  let casinoGamesService,
    link,
    userService,
    casinoGamesConfig,
    productHomepagesConfig,
    claimsConfig;

  beforeEach(() => {
    userService = {
      claims: new Map<string, string>([
        ['currency', 'EUR'],
        ['ssotoken', '12345abcde']
      ])
    };
    casinoGamesConfig = {
      miniGamesEnabled: jasmine.createSpy(),
      miniGamesHost: jasmine.createSpy(),
      miniGamesTemplate: jasmine.createSpy(),
      recentlyPlayedGamesEnabled: jasmine.createSpy(),
      recentlyPlayedGamesUrl: jasmine.createSpy(),
      userHostAddress: jasmine.createSpy().and.returnValue('127.0.01'),
      seeAllEnabled: jasmine.createSpy(),
      seeAllUrl: jasmine.createSpy()
    };
    productHomepagesConfig = {
      casino: jasmine.createSpy().and.returnValue('http://dev.casino.coral.co.uk'),
      sports: jasmine.createSpy().and.returnValue('http://dev.sports.coral.co.uk')
    };
    claimsConfig = {
      'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier': 'arsh'
    };

    casinoGamesService = new CasinoGamesService(userService, casinoGamesConfig, productHomepagesConfig, claimsConfig);

    casinoGamesService.casinoGamesConfig.miniGamesTemplate =
      '/userIp=$USERIP$&currency=$CURRENCY$&sessionKey=$SESSION_KEY$&hosturl=$HOSTURL$&accountName=$accountName$';
  });

  describe('isMiniGamesEnabled()', () => {
    it('should return whether mini games is enabled or not', () => {
      casinoGamesConfig.miniGamesEnabled = true;
      expect(casinoGamesService.isMiniGamesEnabled).toBe(true);
    });
  });

  describe('miniGamesUrl()', () => {
    it('should return recently played games url', () => {
      link =
        'http://www.minigames/userIp=127.0.01&currency=EUR&sessionKey=12345abcde&hosturl=http://dev.sports.coral.co.uk&accountName=arsh';
      casinoGamesService.casinoGamesConfig.miniGamesHost = 'http://www.minigames';
      expect(casinoGamesService.miniGamesUrl).toEqual(link);
    });
  });

  describe('isRecentlyPlayedGamesEnabled()', () => {
    it('should return whether recently played games is enabled or not', () => {
      casinoGamesConfig.recentlyPlayedGamesEnabled = true;
      expect(casinoGamesService.isRecentlyPlayedGamesEnabled).toBe(true);
    });
  });

  describe('recentlyPlayedGamesUrl()', () => {
    it('should return recently played games url', () => {
      link = 'http://dev.test.com';
      casinoGamesService.productHomepagesConfig.casino = 'http://dev.';
      casinoGamesService.casinoGamesConfig.recentlyPlayedGamesUrl = 'test.com';
      expect(casinoGamesService.recentlyPlayedGamesUrl).toEqual(link);
    });
  });

  describe('isSeeAllEnabled()', () => {
    it('should return whether see all games is enabled or not', () => {
      casinoGamesConfig.seeAllEnabled = true;
      expect(casinoGamesService.isSeeAllEnabled).toBe(true);
    });
  });

  describe('seeAllUrl()', () => {
    it('should return see all games url', () => {
      link = 'http://dev.test.com';
      casinoGamesService.productHomepagesConfig.casino = 'http://dev.';
      casinoGamesService.casinoGamesConfig.seeAllUrl = 'test.com';
      expect(casinoGamesService.seeAllUrl).toEqual(link);
    });
  });
});

