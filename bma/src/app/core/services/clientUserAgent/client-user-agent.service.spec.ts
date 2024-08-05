import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';

describe('ClientUserAgentService', () => {
  let service: ClientUserAgentService;
  let deviceService;

  beforeEach(() => {
    deviceService = {
      isIos: false,
      isDesktopWindows: false,
      isMobile: false,
      isTablet: false,
      isWrapper: false,
      isDesktop: false
    };

    service = new ClientUserAgentService(deviceService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('getMobileId method', () => {
    it('should return android mobile client user agent id', () => {
      const actualResult = service['getMobileId'];

      expect(actualResult).toEqual('S|H|A0000000');
    });

    it('should return ios mobile client user agent id', () => {
      deviceService.isIos = true;
      const actualResult = service['getMobileId'];

      expect(actualResult).toEqual('S|H|I0000000');
    });
  });

  describe('getWrapperId method', () => {
    it('should return android wrapper client user agent id', () => {
      const actualResult = service['getWrapperId'];

      expect(actualResult).toEqual('S|W|A0000000');
    });

    it('should return ios wrapper client user agent id', () => {
      deviceService.isIos = true;
      const actualResult = service['getWrapperId'];

      expect(actualResult).toEqual('S|W|I0000000');
    });
  });

  describe('getDesktopId method', () => {
    it('should return desktop OS X client user agent id', () => {
      const actualResult = service['getDesktopId'](false, false);

      expect(actualResult).toEqual('S|H|O0000000');
    });

    it('should return desktop windows client user agent id', () => {
      deviceService.isDesktopWindows = true;
      const actualResult = service['getDesktopId'](false, false);

      expect(actualResult).toEqual('S|H|W0000000');
    });

    it('should return desktop lotto OS X client user agent id', () => {
      const actualResult = service['getDesktopId'](false, true);

      expect(actualResult).toEqual('Y|H|O0000000');
    });

    it('should return desktop lotto windows client user agent id', () => {
      deviceService.isDesktopWindows = true;
      const actualResult = service['getDesktopId'](false, true);

      expect(actualResult).toEqual('Y|H|W0000000');
    });

    it('should return desktop virtuals OS X client user agent id', () => {
      const actualResult = service['getDesktopId'](true, false);

      expect(actualResult).toEqual('R|H|O0000000');
    });

    it('should return desktop virtuals windows client user agent id', () => {
      deviceService.isDesktopWindows = true;
      const actualResult = service['getDesktopId'](true, false);

      expect(actualResult).toEqual('R|H|W0000000');
    });
  });

  describe('getDesktopId method', () => {
    it('should return empty string', () => {
      const actualResult = service.getId(false, false);

      expect(actualResult).toEqual('');
    });

    it('should return android mobile client user agent id', () => {
      deviceService.isMobile = true;
      const actualResult = service.getId(false, false);

      expect(actualResult).toEqual('S|H|A0000000');
    });

    it('should return ios tablet client user agent id', () => {
      deviceService.isTablet = true;
      deviceService.isIos = true;
      const actualResult = service.getId(false, false);

      expect(actualResult).toEqual('S|H|I0000000');
    });

    it('should return android wrapper client user agent id', () => {
      deviceService.isWrapper = true;
      const actualResult = service.getId(false, false);

      expect(actualResult).toEqual('S|W|A0000000');
    });

    it('should return desktop OS X client user agent id', () => {
      deviceService.isDesktop = true;
      const actualResult = service.getId(false, false);

      expect(actualResult).toEqual('S|H|O0000000');
    });
  });
});
