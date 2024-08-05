import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
  FiveASideEntryListOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
describe('FiveASideEntryListOverlayComponent', () => {

  let component: FiveASideEntryListOverlayComponent;

  let deviceService;
  let windowRef;
  let rendererService;
  let fiveASideEntryInfoService,pubsub,coreToolsService;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        clearTimeout: jasmine.createSpy('clearTimeout')
      },
      document: {
        getElementById: jasmine.createSpy(),
        querySelector: jasmine.createSpy().and.returnValue({})
      }
    };
    deviceService = {
      isMobile: false,
      isWrapper: true
    };
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()),
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    },
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass'),
        setStyle: jasmine.createSpy('setStyle'),
        listen: jasmine.createSpy('listen').and.callFake((a, b, cb) => cb && cb({}))
      }
    },
    coreToolsService = {
      uuid: jasmine.createSpy().and.returnValue('122344543')
    },
    fiveASideEntryInfoService = {
      entriesCreation: jasmine.createSpy('entriesCreation').and.returnValue(MY_ENTRIES_LIST),
      isOpened: jasmine.createSpy('isOpened').and.returnValue(MY_ENTRIES_LIST),
    };
    component = new FiveASideEntryListOverlayComponent(fiveASideEntryInfoService,
      rendererService,coreToolsService, windowRef, deviceService,pubsub);
  });

  describe('ngOnInit', () => {
    it('ngOnInit', () => {
      component['doNext'] = jasmine.createSpy('doNext');
      component['initElements'] = jasmine.createSpy('initElements');
      component.myEntriesList = MY_ENTRIES_LIST as any;
      component.ngOnInit();
      expect(component['initElements']).toHaveBeenCalled();
      expect(component['doNext']).toHaveBeenCalled();
    });
  });
  describe('ngOnDestroy', () => {
    it('ngOnDestroy', () => {
      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalled();
    });
  });
  describe('donext', () => {
    it('doNext', () => {
      component.next = 0;
      component.entries = MY_ENTRIES_LIST as any;
      component.staggering = [];
      component['doNext']();
      expect(component.staggering.length).toBe(1);
    });
    it('doNext with empty array', () => {
      component.next = 1;
      component.entries = [];
      component.staggering = [];
      component['doNext']();
      expect(component.staggering.length).toBe(0);
    });
  });
  describe('getBody', () => {
    it('getBody isWrapper true', () => {
      deviceService = {
        isWrapper: true,
        isMobile: true
      };
      component = new FiveASideEntryListOverlayComponent(fiveASideEntryInfoService,
        rendererService,coreToolsService, windowRef, deviceService,pubsub);
      component['getBody']();
      expect(windowRef.document.querySelector).toHaveBeenCalled();
    });
    it('getBody isWrapper false', () => {
      deviceService = {
        isWrapper: false,
        isMobile: true
      };
      component = new FiveASideEntryListOverlayComponent(fiveASideEntryInfoService,
        rendererService,coreToolsService, windowRef, deviceService,pubsub);
      component['getBody']();
      expect(windowRef.document.querySelector).toHaveBeenCalled();
    });
  });
  describe('initElements', () => {
    it('initElements with isWrapper true', () => {
      component['initElements']();
      expect(windowRef.document.getElementById).toHaveBeenCalled();
      expect(rendererService.renderer.addClass).toHaveBeenCalledTimes(2);
    });
    it('initElements with isWrapper false', () => {
      deviceService = {
        isWrapper: false,
        isMobile: true
      };
      component = new FiveASideEntryListOverlayComponent(fiveASideEntryInfoService,
        rendererService,coreToolsService, windowRef, deviceService,pubsub);
      component['initElements']();
      expect(windowRef.document.getElementById).toHaveBeenCalled();
      expect(rendererService.renderer.addClass).toHaveBeenCalledTimes(2);
    });
  });
  describe('close', () => {
    it('close', () => {
      spyOn(component.clearOverlay, 'emit');
      component['close']();
      expect(windowRef.document.getElementById).toHaveBeenCalled();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledTimes(2);
      expect(component.clearOverlay.emit).toHaveBeenCalled();
    });
    it('close with intial', () => {
      spyOn(component.clearOverlay, 'emit');
      component.homeBody = undefined as any;
      component.fiveASideOverlay = undefined as any;
      component['close']();
      expect(windowRef.document.getElementById).toHaveBeenCalled();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledTimes(2);
      expect(component.clearOverlay.emit).toHaveBeenCalled();
    });
    it('close when home and overlay stored', () => {
      spyOn(component.clearOverlay, 'emit');
      component.homeBody = { test: 'body' } as any;
      component.fiveASideOverlay = { fiveaside: 'fiveaside-element' } as any;
      component['close']();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledTimes(2);
      expect(component.clearOverlay.emit).toHaveBeenCalled();
    });
    it('close when isWrapper false', () => {
      deviceService = {
        isWrapper: false,
        isMobile: true
      };
      component = new FiveASideEntryListOverlayComponent(fiveASideEntryInfoService,
        rendererService,coreToolsService, windowRef, deviceService,pubsub);
      spyOn(component.clearOverlay, 'emit');
      component['close']();
      expect(windowRef.document.getElementById).toHaveBeenCalled();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledTimes(2);
      expect(component.clearOverlay.emit).toHaveBeenCalled();
    });
  });
});
