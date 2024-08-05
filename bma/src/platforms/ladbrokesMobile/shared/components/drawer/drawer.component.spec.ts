import { LadbrokesDrawerComponent } from './drawer.component';
import { DrawerComponent } from '@shared/components/drawer/drawer.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LadbrokesDrawerComponent', () => {
  let component: LadbrokesDrawerComponent;
  let windowRefService;
  let domToolsService;
  let changeDetector;
  let deviceService;
  let pubSubService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval')
      }
    };
    domToolsService = {
      getPageScrollTop: jasmine.createSpy('getPageScrollTop'),
      scrollPageTop: jasmine.createSpy('scrollPageTop')
    };
    changeDetector = {
      detectChanges: jasmine.createSpy(),
      detach: jasmine.createSpy()
    };
    deviceService = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
      subscribe: jasmine.createSpy('publish')
    };
    component = new LadbrokesDrawerComponent(
      windowRefService,
      domToolsService,
      deviceService,
      changeDetector,
      pubSubService
    );
  });

  describe('instance', () => {
    it('should be created', () => {
      expect(component).toBeTruthy();
    });

    it('should extend DrawerComponent', () => {
      expect(component instanceof DrawerComponent).toBeTruthy();
    });
  });

  describe('check methods', () => {
    beforeEach(() => {
      spyOn(DrawerComponent.prototype, 'closeClick');
      spyOn(DrawerComponent.prototype, 'overlayClick');
    });

    it('#closeClick', () => {
      component.closeClick();
      expect(DrawerComponent.prototype.closeClick).toHaveBeenCalled();
    });

    it('#overlayClick', () => {
      component.overlayClick();
      expect(DrawerComponent.prototype.overlayClick).toHaveBeenCalled();
    });
  });
});
