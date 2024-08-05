import { CasinoLinkService } from './casino-link.service';
import environment from '@environment/oxygenEnvConfig';

describe('CasinoLinkService', () => {
  let service: CasinoLinkService;
  let deviceService;

  beforeEach(() => {
    deviceService = {};

    service = new CasinoLinkService(deviceService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('decorateCasinoLink', () => {
    service.uriDecoration = jasmine.createSpy().and.returnValue('');
    const items: any = [{}, {}];

    expect(service.decorateCasinoLink(items)).toEqual(jasmine.any(Array));
    expect(service.uriDecoration).toHaveBeenCalledTimes(2);
    items.forEach(item => expect(item.targetUri).toBeDefined());
  });

  it('decorateCasinoLinkInHtml', () => {
    deviceService.isWrapper = false;
    [
      {
        input: '<p><a href="http://www.mcasino.coral.uk">Casino</a></p>',
        output: '<p><a href="http://www.mcasino.coral.uk?deliveryPlatform=HTML5">Casino</a></p>'
      },
      {
        input: '<p><a href="https://srv1.mcasino.com?page=1">Casino</a></p>',
        output: '<p><a href="https://srv1.mcasino.com?page=1&deliveryPlatform=HTML5">Casino</a></p>'
      },
      {
        input: '<p><a href="https://google.com">Google</a></p>',
        output: '<p><a href="https://google.com">Google</a></p>'
      }
    ].forEach(item => {
      expect(service.decorateCasinoLinkInHtml(item.input)).toBe(item.output);
    });
  });

  it('decorateCasinoLinkInHtml (platform Wrapper)', () => {
    deviceService.isWrapper = true;
    [
      {
        input: '<p><a href="http://www.mcasino.coral.uk">Casino</a></p>',
        output: '<p><a href="http://www.mcasino.coral.uk?deliveryPlatform=Wrapper">Casino</a></p>'
      },
      {
        input: '<p><a href="https://srv1.mcasino.com?page=1">Casino</a></p>',
        output: '<p><a href="https://srv1.mcasino.com?page=1&deliveryPlatform=Wrapper">Casino</a></p>'
      },
      {
        input: '<p><a href="https://google.com">Google</a></p>',
        output: '<p><a href="https://google.com">Google</a></p>'
      }
    ].forEach(item => {
      expect(service.decorateCasinoLinkInHtml(item.input)).toBe(item.output);
    });
  });

  it('uriDecoration (platform HTML5)', () => {
    deviceService.isWrapper = false;
    [
      {
        input: 'https://google.com', output: 'https://google.com'
      },
      {
        input: 'https://mcasino.com?page=1', output: 'https://mcasino.com?page=1&deliveryPlatform=HTML5'
      },
      {
        input: 'https://mcasino.com?deliveryPlatform=HTML5', output: 'https://mcasino.com?deliveryPlatform=HTML5'
      },
    ].forEach(item => {
      expect(service.decorateCasinoLinkInHtml(item.input)).toBe(item.output);
    });
  });

  it('uriDecoration (platform Wrapper)', () => {
    deviceService.isWrapper = true;
    [
      {
        input: 'https://google.com', output: 'https://google.com'
      },
      {
        input: 'https://mcasino.com?page=1', output: 'https://mcasino.com?page=1&deliveryPlatform=Wrapper'
      },
      {
        input: 'https://mcasino.com?deliveryPlatform=Wrapper', output: 'https://mcasino.com?deliveryPlatform=Wrapper'
      },
    ].forEach(item => {
      expect(service.decorateCasinoLinkInHtml(item.input)).toBe(item.output);
    });
  });

  describe('#filterGamingLinkForIOSWrapper', () => {
    const links = [{
      targetUri: 'https://mcasino.com'
    }, {
      targetUri: environment.GAMING_URL[0]
    }];
    it('should call filterGamingLinkForIOSWrapper method when not IoS not Wrapper', () => {
      deviceService.isWrapper = false;
      deviceService.isIos = false;

      service.filterGamingLinkForIOSWrapper(links as any);

      expect(links).toEqual([{
        targetUri: 'https://mcasino.com'
      }, {
        targetUri: environment.GAMING_URL[0]
      }]);
    });

    it('should call filterGamingLinkForIOSWrapper method when wrapper but not IOS', () => {
      deviceService.isWrapper = true;
      deviceService.isIos = false;

      service.filterGamingLinkForIOSWrapper(links as any);

      expect(links).toEqual([{
        targetUri: 'https://mcasino.com'
      }, {
        targetUri: environment.GAMING_URL[0]
      }]);
    });

    it('should call filterGamingLinkForIOSWrapper method when wrapper but not IOS', () => {
      deviceService.isWrapper = true;
      deviceService.isIos = true;

      service.filterGamingLinkForIOSWrapper(links as any);

      expect(links).toEqual([{
        targetUri: 'https://mcasino.com'
      }]);
    });
  });
});
