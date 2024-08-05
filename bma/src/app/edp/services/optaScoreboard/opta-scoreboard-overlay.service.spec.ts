import { OptaScoreboardOverlayService } from '@edp/services/optaScoreboard/opta-scoreboard-overlay.service';
import environment from '@environment/oxygenEnvConfig';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OptaScoreboardOverlayService', () => {
  let service: OptaScoreboardOverlayService;
  let windowRef;
  let pubSubService;
  let wrapperElement;
  let overlayElement;

  beforeEach(() => {
    overlayElement = {
      tagName: 'scoreboard-overlay',
      addEventListener: jasmine.createSpy('addEventListener'),
      setAttribute: jasmine.createSpy('setAttribute'),
      removeEventListener: jasmine.createSpy('removeEventListener'),
      remove: jasmine.createSpy('remove')
    };
    wrapperElement = {
      tagName: 'div',
      classList: {
        add: jasmine.createSpy('classList.add'),
        remove: jasmine.createSpy('classList.remove')
      },
      querySelector: jasmine.createSpy('querySelector').and.returnValue(overlayElement),
      setAttribute: jasmine.createSpy('setAttribute'),
      appendChild: jasmine.createSpy('appendChild'),
      remove: jasmine.createSpy('remove')
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };

    windowRef = {
      document: {
        getElementById: jasmine.createSpy('getElementById').and.returnValue(null),
        createElement: jasmine.createSpy().and.returnValues(wrapperElement, overlayElement),
        body: {
          appendChild: jasmine.createSpy('appendChild'),
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    service = new OptaScoreboardOverlayService(windowRef, pubSubService);
  });

  it('should initialize properties', () => {
    expect((service as any).overlayElement).toEqual(null);
    expect((service as any).wrapperElement).toEqual(null);
    expect((service as any).wrapperId).toEqual('opta-scoreboard-overlay-wrapper');
    expect((service as any).overlayTagName).toEqual('scoreboard-overlay');
    expect((service as any).overlayShownBodyClass).toEqual('opta-scoreboard-overlay-shown');
    expect((service as any).closeOverlayEventName).toEqual('closeScoreboardOverlay');
    expect((service as any).optaEnv).toEqual(environment.OPTA_SCOREBOARD.ENV);
  });

  describe('initOverlay', () => {
    beforeEach(() => {
      spyOn(service as any, 'createOverlay').and.callThrough();
      spyOn(service, 'destroyOverlay').and.callThrough();
      windowRef.document.getElementById.and.returnValue(wrapperElement);
    });

    it('should remove eventlistener', () => {
      service.overlayElement = {removeEventListener: () => 'test'} as any;
      spyOn(service, 'hideOverlay');
      const retVal = service.initOverlay();
      expect(retVal).toEqual(service.overlayElement);
    });


    it('should look up the wrapper element and return its child overlay element, if both exist', () => {
      expect(service.initOverlay()).toEqual(overlayElement);
      expect(windowRef.document.getElementById).toHaveBeenCalledWith('opta-scoreboard-overlay-wrapper');
      expect(wrapperElement.querySelector).toHaveBeenCalledWith('scoreboard-overlay');
      expect(service.wrapperElement).toEqual(wrapperElement);
      expect(service.overlayElement).toEqual(overlayElement);
    });

    describe('it should create new overlay element', () => {
      it('when no wrapper element is found', () => {
        windowRef.document.getElementById.and.returnValue(null);
        expect(service.initOverlay()).toEqual(overlayElement);
      });
      it('when wrapper element is but it does not contain overlay element', () => {
        wrapperElement.querySelector.and.returnValue(null);
        expect(service.initOverlay()).toEqual(overlayElement);
      });
      afterEach(() => {
        expect((service as any).createOverlay).toHaveBeenCalled();
        expect(service.destroyOverlay).toHaveBeenCalledBefore(windowRef.document.createElement);
      });
    });
  });
  describe('destroyOverlay', () => {
    it('should clear overlayElement if one is defined', () => {
      service.overlayElement = overlayElement;
      service.destroyOverlay();
      expect(overlayElement.removeEventListener).toHaveBeenCalledWith('closeScoreboardOverlay', (service as any).hideOverlay);
      expect(overlayElement.remove).toHaveBeenCalled();
      expect(service.overlayElement).toEqual(null);
    });
    it('should clear wrapperElement if one is defined', () => {
      spyOn(service, 'hideOverlay').and.callThrough();
      service.wrapperElement = wrapperElement;
      service.destroyOverlay();
      expect(service.hideOverlay).toHaveBeenCalled();
      expect(wrapperElement.remove).toHaveBeenCalled();
      expect(service.wrapperElement).toEqual(null);
    });
    it('should not do actions if wrapperElement and overlayElement do not exist', () => {
      spyOn(service, 'hideOverlay').and.callThrough();
      service.wrapperElement = undefined;
      service.overlayElement = undefined;
      service.destroyOverlay();
      expect(service.hideOverlay).not.toHaveBeenCalled();
      expect(service.overlayElement).toEqual(null);
      expect(service.wrapperElement).toEqual(null);
    });
  });

  describe('hideOverlay', () => {
    it(`should remove class from body and wrapperElement if it exists`, () => {
      service.wrapperElement = wrapperElement;
      service.hideOverlay();
      expect(wrapperElement.classList.remove).toHaveBeenCalledWith('visible');
    });
    it(`should only remove class from body if wrapperElement does not exist`, () => {
      service.wrapperElement = null;
      service.hideOverlay();
    });
    afterEach(() => {
      expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('opta-scoreboard-overlay-shown');
    });
  });

  describe('showOverlay', () => {
    it(`should add class to body and wrapperElement if it exists`, () => {
      service.wrapperElement = wrapperElement;
      service.showOverlay();
      expect(wrapperElement.classList.add).toHaveBeenCalledWith('visible');
      expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('opta-scoreboard-overlay-shown');
    });
    it(`should not add class to body if wrapperElement does not exist`, () => {
      service.wrapperElement = null;
      service.showOverlay();
      expect(windowRef.document.body.classList.add).not.toHaveBeenCalledWith('opta-scoreboard-overlay-shown');
    });
  });

  describe('setOverlayData', () => {
    it('should not fail if overlayElement does not exist', () => {
      service.overlayElement = null;
      service.setOverlayData();
    });
    it('should set data to sb-attribute of overlayElement', () => {
      service.overlayElement = overlayElement;
      service.setOverlayData({ overlayKey: 'key' });
      expect(overlayElement.setAttribute).toHaveBeenCalledWith('sb-data',
        `{"env":"${(service as any).optaEnv}","sport":"FOOTBALL","provider":"digital","overlayKey":"key"}`);
    });
    it('should set data to sb-attribute of overlayElement (no argument)', () => {
      service.overlayElement = overlayElement;
      service.setOverlayData();
      expect(overlayElement.setAttribute).toHaveBeenCalledWith('sb-data',
        `{"env":"${(service as any).optaEnv}","sport":"FOOTBALL","provider":"digital"}`);
    });

  });

  describe('createOverlay', () => {
    beforeEach(() => {
      spyOn(service, 'destroyOverlay');
    });
    it('should return overlay element reference', () => {
      expect((service as any).createOverlay()).toEqual(overlayElement);
    });
    it('should create wrapper and overlay DOM elements', () => {
      (service as any).createOverlay();
      expect(service.destroyOverlay).toHaveBeenCalledBefore(windowRef.document.createElement);
      expect(windowRef.document.createElement).toHaveBeenCalledWith('div');
      expect(windowRef.document.createElement).toHaveBeenCalledWith('scoreboard-overlay');
      expect(wrapperElement.setAttribute).toHaveBeenCalledWith('id', 'opta-scoreboard-overlay-wrapper');
      expect(wrapperElement.appendChild).toHaveBeenCalledWith(overlayElement);
      expect(windowRef.document.body.appendChild).toHaveBeenCalledWith(wrapperElement);
    });
    it(`should add 'closeScoreboardOverlay' event listener to overlay element`, () => {
      (service as any).createOverlay();
      expect(overlayElement.addEventListener).toHaveBeenCalledWith('closeScoreboardOverlay', service.hideOverlay);
    });
  });
});
