import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { NavigationService } from './navigation.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('NavigationService', () => {
  const origin: string = 'http://google.com';

  let service: NavigationService;

  let
    windowRefService,
    deviceService,
    router,
    domToolsService,
    localeService,
    userService,
    nativeBridgeService,
    gtmService,
    ngZone,
    cmsService,
    pubSubService,
    navigationUriService,
    awsService,
    routingStateService,
    arcUserService;

    const verticalMenuMock = {
      action: () => of({targetUri: '/foo'} as any),
      inApp: true,
      isTopSport: true,
      title: 'Fanzone',
      imageTitle: 'Fanzone'
    } as any;

    const verticalMenuMock2 = {
      action: () => of({targetUri: '/foo'} as any),
      inApp: true,
      isTopSport: false,
      title: 'Fanzone',
      imageTitle: 'Fanzone'
    } as any;

  beforeEach(() => {

    windowRefService = {
      nativeWindow: {
        document: {
          location: 'https://my-domain.com/home'
        },
        location: {
          href: '/home',
          origin: 'https://my-domain.com'
        },
        open: jasmine.createSpy('open')
      }
    };

    deviceService = {
      isAndroid: true
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };

    router = jasmine.createSpyObj(['navigateByUrl', 'navigate', 'url']);

    domToolsService = jasmine.createSpyObj(['scrollPageTop', 'getPageScrollTop']);

    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };

    userService = {
      status: false,
      username: 'name'
    };

    nativeBridgeService = {
      onGaming: jasmine.createSpy('onGaming'),
    };

    gtmService = jasmine.createSpyObj(['push']);

    ngZone = {
      run: jasmine.createSpy('run').and.callFake((cb) => cb && cb())
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        GamingEnabled: {
          enabledGamingOverlay: true,
          gamingUrl: 'https://gaming.coral.co.uk'
        }
      }))
    };

    navigationUriService = {
      isInternalUri: jasmine.createSpy('isInternalUri'),
      isAbsoluteUri: jasmine.createSpy('isAbsoluteUri').and.callFake((uri: string = '') => {
        return /^https?:\/\//.test(uri.trim());
      }),
      isSameOriginUri: jasmine.createSpy('isSameOriginUri').and.callFake((uri: string = '') => {
        return uri.includes(origin);
      }),
      origin
    };
    awsService = {
      addAction: jasmine.createSpy('addAction'),
      API: {
        NOT_FOUND_PAGE_HIT: 'NOT_FOUND_PAGE_HIT'
      }
    };
    routingStateService = {
      routingStateService: jasmine.createSpy('routingStateService'),
      getPreviousUrl: jasmine.createSpy('getPreviousUrl').and.returnValue('/')
    };
    arcUserService = {
      fetchArcCms: jasmine.createSpy('fetchArcCms')
    };

    service = new NavigationService(
      windowRefService,
      deviceService,
      router,
      domToolsService,
      localeService,
      userService,
      nativeBridgeService,
      gtmService,
      ngZone,
      cmsService,
      pubSubService,
      navigationUriService,
      awsService,
      routingStateService,
      arcUserService
    );
  });

  it('should be created', () => {
    expect(service).toBeDefined();
  });

  describe('window.goToPage', () => {

    beforeEach(() => {
      spyOn(service, 'openUrl');
    });

    it('goToPage should navigate to an correct page (racing)', () => {
      windowRefService.nativeWindow.goToPage('/event/horse-racing');

      expect(ngZone.run).toHaveBeenCalled();
      expect(service.openUrl).toHaveBeenCalledWith('/horse-racing');
    });

    it('goToPage should navigate to an correct page (greyhound)', () => {
      windowRefService.nativeWindow.goToPage('/event/greyhound-racing');

      expect(ngZone.run).toHaveBeenCalled();
      expect(service.openUrl).toHaveBeenCalledWith('/greyhound-racing');
    });
  });

  describe('openUrl', () => {
    let isInternalUriSpy, redirectCurrPageSpy, openNewPageSpy;

    beforeEach(() => {
      isInternalUriSpy = spyOn(service, 'isInternalUri');
      redirectCurrPageSpy = spyOn(service, 'redirectCurrPage');
      openNewPageSpy = spyOn(service, 'openNewPage');
      router.navigateByUrl.and.returnValue(Promise.resolve(null));
    });

    it('should check whether link is internal', () => {
      service.openUrl('/foo');

      expect(isInternalUriSpy).toHaveBeenCalled();
    });

    it('should add ga tracking if menuItem data present', () => {
      service.openUrl('/fanzone',true,false,verticalMenuMock);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent',{ eventCategory: 'navigation', eventAction: 'a-z sports', eventLabel: 'Fanzone', eventDetails: 'featured' });
    });

    it('should add ga tracking if menuItem data present', () => {
      service.openUrl('/fanzone',true,false,verticalMenuMock2,'sb.azSports');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent',{ eventCategory: 'navigation', eventAction: 'a-z sports', eventLabel: 'Fanzone', eventDetails: 'a-z betting' });
    });

    it('should not add ga tracking if menuItem data not present', () => {
      service.openUrl('/fanzone',true,false);

      expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('should not add ga tracking if menuItem data  present as empty object', () => {
      service.openUrl('/fanzone',true,false,{});

      expect(gtmService.push).not.toHaveBeenCalled();
    });

    describe('native bridge gaming', () => {
      it('should call onGaming method', () => {
        deviceService.isWrapper = true;
        service.openUrl('https://gaming.coral.co.uk');
        expect(openNewPageSpy).toHaveBeenCalledWith('https://gaming.coral.co.uk');
      });

      it('should not call onGaming method when bad url', () => {
        service.openUrl('bad url');

        expect(nativeBridgeService.onGaming).not.toHaveBeenCalled();
      });

      it('should not call onGaming method when gaming disabled', () => {
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: false,
            url: 'https://gaming.coral.co.uk'
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(nativeBridgeService.onGaming).not.toHaveBeenCalled();
      });

      it('should not call onGaming method when no config', () => {
        cmsService.getSystemConfig.and.returnValue(of({}));
        service.openUrl('https://gaming.coral.co.uk');

        expect(nativeBridgeService.onGaming).not.toHaveBeenCalled();
      });

      it('should open gaming overlay for Android', () => {
        router.url = '/virtual-sports/virtual-horse-racing';
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = true;
        deviceService.isIos = false;
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
        expect(router.navigate).toHaveBeenCalledWith(['/']);
      });

      it('should open gaming overlay for iOS', () => {
        router.url = '/virtual-sports/virtual-horse-racing';
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = false;
        deviceService.isIos = true;
        deviceService.osVersion = '13.1.0';
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
        expect(router.navigate).toHaveBeenCalledWith(['/']);
      });

      it('should not open gaming overlay for Android when user status false', () => {
        router.url = '/virtual-sports/virtual-horse-racing';
        userService.status = false;
        deviceService.isWrapper = false;
        deviceService.isAndroid = true;
        deviceService.isIos = false;
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).not.toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
      });

      it('should not open user dialog if gaming overlay is enabled but user login', () => {
        router.url = '/sport/football/matches';
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = false;
        deviceService.isIos = true;
        deviceService.osVersion = '13.1.0';
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');
        expect(router.navigate).not.toHaveBeenCalled();
        expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.GAMING_OVERLAY_OPEN);
      });

      it('should NOT open gaming overlay for iOS < 13 when when user status false', () => {
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = false;
        deviceService.isIos = true;
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: '',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).not.toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
      });

      it('should NOT open gaming overlay if it is not android or iOS', () => {
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = false;
        deviceService.isIos = false;
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).not.toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
      });

      it('should NOT open gaming overlay if iOS osVersion < 13', () => {
        router.url = '/virtual-sports/virtual-horse-racing';
        userService.status = true;
        deviceService.isWrapper = false;
        deviceService.isAndroid = false;
        deviceService.isIos = true;
        deviceService.osVersion = '12.0.0';
        cmsService.getSystemConfig.and.returnValue(of({
          GamingEnabled: {
            enabledGamingOverlay: true,
            gamingUrl: 'https://gaming.coral.co.uk',
            overlayUrl: 'https://gaming.coral.co.uk',
          }
        }));
        service.openUrl('https://gaming.coral.co.uk');

        expect(pubSubService.publish).not.toHaveBeenCalledWith('GAMING_OVERLAY_OPEN');
      });
    });

    describe('for internal links', () => {

      beforeEach(() => {
        isInternalUriSpy.and.returnValue(true);
        cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({}));
      });

      it('should open link via router for inApp links (default)', () => {
        service.openUrl('/foo');

        expect(router.navigateByUrl).toHaveBeenCalledWith('/foo');
      });

      it('should open link via router for inApp links (forced)', () => {
        service.openUrl('/foo', true);

        expect(router.navigateByUrl).toHaveBeenCalledWith('/foo');
      });

      it('should redirect current page with non-inApp links (forced)', () => {
        service.openUrl('/foo', false);

        expect(redirectCurrPageSpy).toHaveBeenCalledWith('/foo');
      });

      it('should try to fix internal links', () => {
        service['removeCurrOrigin'] = jasmine.createSpy().and.returnValue('/foo');
        service.openUrl('https://my-domain.com/foo', true);
        expect(router.navigateByUrl).toHaveBeenCalledWith('/foo');
      });

      it('should remember but not restore scroll (default)', () => {
        service.openUrl('/foo', true);

        expect(domToolsService.getPageScrollTop).toHaveBeenCalled();
        expect(domToolsService.scrollPageTop).not.toHaveBeenCalled();
      });

      it('should remember and restore scroll', fakeAsync(() => {
        domToolsService.getPageScrollTop.and.returnValue(50);
        service.openUrl('/foo', true, true);
        tick();
        expect(domToolsService.getPageScrollTop).toHaveBeenCalled();
        expect(domToolsService.scrollPageTop).toHaveBeenCalledWith(50);
      }));
    });

    describe('for external links', () => {

      beforeEach(() => {
        isInternalUriSpy.and.returnValue(false);
      });

      it('should open new window for non inApp links (default)', () => {
        service.openUrl('/foo');

        expect(openNewPageSpy).toHaveBeenCalledWith('/foo');
      });

      it('should open new window for non inApp links (forced)', () => {
        service.openUrl('/foo', false);

        expect(openNewPageSpy).toHaveBeenCalledWith('/foo');
      });

      it('should redirect current page with inApp links (forced)', () => {
        service.openUrl('/foo', true);

        expect(redirectCurrPageSpy).toHaveBeenCalledWith('/foo');
      });
    });
  });

  describe('redirectCurrPage', () => {

    describe('old android device', () => {

      it('should change location of given window but not current', () => {
        const newWin = {document: {location: ''}} as any;
        service.redirectCurrPage('/foo', newWin);

        expect(newWin.document.location).toBe('/foo');
        expect(windowRefService.nativeWindow.document.location).toBe('https://my-domain.com/home');
      });

      it('should change location of current window (default)', () => {
        service.redirectCurrPage('/foo');

        expect(windowRefService.nativeWindow.document.location).toBe('/foo');
      });
    });

    describe('modern devices', () => {

      beforeEach(() => {
        deviceService.isAndroid = false;
      });

      it('should change location of given window but not current', () => {
        const newWin = {location: {href: ''}} as any;
        service.redirectCurrPage('/foo', newWin);

        expect(newWin.location.href).toBe('/foo');
        expect(windowRefService.nativeWindow.location.href).toBe('/home');
      });

      it('should change location of current window (default)', () => {
        service.redirectCurrPage('/foo');

        expect(windowRefService.nativeWindow.location.href).toBe('/foo');
      });
    });
  });

  describe('openNewPage', () => {
    let newWinRefStub;

    beforeEach(() => {
      newWinRefStub = jasmine.createSpyObj(['focus']);
      windowRefService.nativeWindow.open.and.returnValue(newWinRefStub);
    });

    it('should open new window and focus on it', () => {
      service.openNewPage('/foo');

      expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('/foo', '_blank');
      expect(newWinRefStub.focus).toHaveBeenCalled();
    });

    it('should not focus new window if empty link', () => {
      windowRefService.nativeWindow.open.and.returnValue(null);

      expect(service.openNewPage('')).toBeNull();
      expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('', '_blank');
      expect(newWinRefStub.focus).not.toHaveBeenCalled();
    });

    it('should return new window reference', () => {
      expect(service.openNewPage('/foo')).toBe(newWinRefStub);
    });
  });

  describe('openNewPageAsync', () => {
    let newWinRefStub, openNewPageSpy, redirectCurrPageSpy;

    beforeEach(() => {
      newWinRefStub = {
        document: {
          body: {innerText: ''}
        },
        focus: jasmine.createSpy('focus')
      };

      openNewPageSpy = spyOn(service, 'openNewPage').and.returnValue(newWinRefStub);
      redirectCurrPageSpy = spyOn(service, 'redirectCurrPage');
    });

    it('should open blank new page and populate its content with placeholder', () => {
      service.openNewPageAsync();

      expect(openNewPageSpy).toHaveBeenCalled();
      expect(localeService.getString).toHaveBeenCalledWith('bma.asyncOpeningMessage');
      expect(newWinRefStub.document.body.innerText).toBe('string');
    });

    it('should return callback that opens passed url and makes a focus', () => {
      const openPageCallback = service.openNewPageAsync();
      expect(openPageCallback).toEqual(jasmine.any(Function));

      openPageCallback('/foo');
      expect(redirectCurrPageSpy).toHaveBeenCalledWith('/foo', newWinRefStub);
      expect(newWinRefStub.focus).toHaveBeenCalled();
    });

    it('sdfgsdfg', () => {
      openNewPageSpy.and.returnValue(null);

      try {
        service.openNewPageAsync();
      } catch (err: any) {
        expect(err.message).toBe(`Error opening new window for async navigation!`);
      }

      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });

  describe('#trackGTMEvent', () => {

    it('should send data to GTM (default category)', () => {
      service.trackGTMEvent('eventAction', 'eventLabel');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'navigation',
        eventAction: 'eventAction',
        eventLabel: 'eventLabel',
        eventDetails: 'a-z betting'
      });
    });

    it('should send data to GTM (custom category)', () => {
      service.trackGTMEvent('eventAction', 'eventLabel', 'main');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'main',
        eventAction: 'eventAction',
        eventLabel: 'eventLabel',
        eventDetails: 'a-z betting' 
      });
    });
  });

  describe('isInternalUri', () => {
    it('should check if uri is internal', () => {
      const uri = 'test';
      service.isInternalUri(uri);

      expect(navigationUriService.isInternalUri).toHaveBeenCalledWith(uri);
    });

    it('should return true if no uri was given', () => {
      navigationUriService.isInternalUri.and.callFake((uri: string = '') => {
        return !navigationUriService.isAbsoluteUri(uri) || navigationUriService.isSameOriginUri(uri);
      });

      expect(service.isInternalUri()).toBeTruthy();
      expect(navigationUriService.isInternalUri).toHaveBeenCalledWith('');
    });
  });

  describe('isAbsoluteUri', () => {
    it('should check if uri is absolute', () => {
      const uri = 'test';
      service.isAbsoluteUri(uri);

      expect(navigationUriService.isAbsoluteUri).toHaveBeenCalledWith(uri);
    });

    it('should return false if uri is not absolute', () => {
      expect(service.isAbsoluteUri('')).toBeFalsy();
      expect(navigationUriService.isAbsoluteUri).toHaveBeenCalledWith('');
    });
  });

  describe('isSameOriginUri', () => {
    it('should check for same origin', () => {
      const uri = 'test';
      service.isSameOriginUri(uri);

      expect(navigationUriService.isSameOriginUri).toHaveBeenCalledWith(uri);
    });

    it('should return false if origins do not match', () => {
      expect(service.isSameOriginUri()).toBeFalsy();
      expect(navigationUriService.isSameOriginUri).toHaveBeenCalledWith('');
    });
  });

  describe('removeCurrOrigin', () => {
    it('should remove origin if matches', () => {
      const uri = 'http://google.com/tab';

      expect(service.removeCurrOrigin(uri)).toBe('/tab');
    });

    it('should make no changes if origin not matches', () => {
      const uri = 'https://example.com/tab';

      expect(service.removeCurrOrigin(uri)).toBe(uri);
    });

    it('should return empty string if no origin was given', () => {
      expect(service.removeCurrOrigin()).toBe('');
    });
  });

  describe('handleHomeRedirect', () => {
    const activeUrl = '/incorrect-page';
    const previousUrl = '/';

    beforeEach(() => {
      routingStateService.getPreviousUrl.and.returnValue(previousUrl);
      router.url = '/incorrect-page';
    });

    it('should track default location value', () => {
      service.handleHomeRedirect();

      expect(gtmService.push).toHaveBeenCalledWith('not-found-page', {
        location: 'general',
        activeUrl,
        previousUrl
      });
      expect(awsService.addAction).toHaveBeenCalledWith('NOT_FOUND_PAGE_HIT', {
        location: 'general',
        activeUrl,
        previousUrl
      });
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });

    it('should track passed location value', () => {
      const location = 'edp';

      service.handleHomeRedirect(location);

      expect(gtmService.push).toHaveBeenCalledWith('not-found-page', {
        location,
        activeUrl,
        previousUrl
      });
      expect(awsService.addAction).toHaveBeenCalledWith('NOT_FOUND_PAGE_HIT', {
        location,
        activeUrl,
        previousUrl
      });
    });

    it('should track setted activeUrl', () => {
      const wrongUrl = '/test/url';
      service.handleHomeRedirect('general', wrongUrl);

      expect(gtmService.push).toHaveBeenCalledWith('not-found-page', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl
      });
      expect(awsService.addAction).toHaveBeenCalledWith('NOT_FOUND_PAGE_HIT', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl
      });
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });
  });

  describe('handleHomeRedirect', () => {
    beforeEach(() => {
      router.url = '/incorrect-page';
    });

    it('should track setted activeUrl on application init', () => {
      const wrongUrl = '/test/url';
      service.handleHomeRedirect('general', wrongUrl);

      expect(gtmService.push).toHaveBeenCalledWith('not-found-page', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl: '/'
      });
      expect(awsService.addAction).toHaveBeenCalledWith('NOT_FOUND_PAGE_HIT', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl: '/'
      });
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });
  });

  describe('handleHomeRedirect', () => {
    const previousUrl = '/';

    beforeEach(() => {
      router.url = '/incorrect-page';
    });

    it('should track setted activeUrl on application init', () => {
      const wrongUrl = '/test/url';
      service.handleHomeRedirect('general', wrongUrl);

      expect(gtmService.push).toHaveBeenCalledWith('not-found-page', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl
      });
      expect(awsService.addAction).toHaveBeenCalledWith('NOT_FOUND_PAGE_HIT', {
        location: 'general',
        activeUrl: wrongUrl,
        previousUrl
      });
      expect(router.navigate).toHaveBeenCalledWith(['/']);
    });
  });

  describe('#openRouterUrl', () => {
    beforeEach(() => {
      spyOn(service as any, 'getOffsetAndUrl').and.returnValue({
        offsetTop: 2, fixedUrl: '5-a-side/lobby'
      });
      router.navigateByUrl.and.returnValue(Promise.resolve(null));
    });
    it('should navigate but not restore scroll (default)', () => {
      service.openRouterUrl('5-a-side/lobby', false);
      expect(domToolsService.scrollPageTop).not.toHaveBeenCalled();
    });
    it('should navigate and restore scroll', fakeAsync(() => {
      service.openRouterUrl('5-a-side/lobby', true);
      tick();
      expect(domToolsService.scrollPageTop).toHaveBeenCalled();
    }));
  });
});
