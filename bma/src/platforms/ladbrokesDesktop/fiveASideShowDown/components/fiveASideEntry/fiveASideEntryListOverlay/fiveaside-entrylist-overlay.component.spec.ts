import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
  FiveASideEntryListOverlayComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
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
 });
