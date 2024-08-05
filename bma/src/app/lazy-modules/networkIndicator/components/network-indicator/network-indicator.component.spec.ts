import { NetworkIndicatorComponent } from './network-indicator.component';
import { NETWORK_CONSTANTS } from './network-indicator.constants';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('NetworkIndicatorComponent', () => {
  const title = 'NetworkIndicatorComponent';

  let component: NetworkIndicatorComponent;
  let windowRef;
  location;

  let dialogService;
  let gtmService;
  let pubSubService;
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      },
      document: {
        querySelector: jasmine.createSpy()
      }
    } as any;
    dialogService = {
      ids: { connectionInterrupted: 'connectionInterrupted' },
      openDialog: jasmine.createSpy()
    };
    gtmService = { push: jasmine.createSpy() };
    pubSubService = {
      subscribe: jasmine.createSpy().and.callFake((sb, ch, fn) => {
        fn();
      }),
      cbMap: {},
      publish: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    } as any;
    component = new NetworkIndicatorComponent(windowRef, dialogService, gtmService, pubSubService);
  });


  describe('ngOnDestroy', () => {
    it('#ngOnDestroy cmsSubscription', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });
  });

  it('#ngOnChanges should call styleIndicatorOnType method', () => {
    component.styleIndicatorOnType = jasmine.createSpy('styleIndicatorOnType');
    component.ngOnChanges();
    expect(component.styleIndicatorOnType).toHaveBeenCalledTimes(1);
  });

  it('#onClose should make display as false', () => {
    component.onClose();
    expect(component.display).toBeFalse();
  });

  describe('#styleIndicatorOnType', () => {
    it('#should initialize isSlowEverCalled as true', () => {
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType({ networkSpeed: 'slow' } as any);
      expect(component.isSlowEverCalled).toBeTrue();
    });

    it('#should not enter into the method if config is null', () => {
      component.display = false;
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType(null);
      expect(component.display).toBeFalse();
    });

    it('#should initialize isSlowEverCalled as false and indicator with timeout', () => {
      component.isSlowEverCalled = true;
      const obj = { networkSpeed: 'online', timeout: 3000 } as any;
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType(obj);
      expect(component.isSlowEverCalled).toBeFalse();
    });
    it('#should initialize isSlowEverCalled as false and indicator without timeout', () => {
      component.isSlowEverCalled = true;
      const obj = { networkSpeed: 'online' } as any;
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType(obj);
      expect(component.isSlowEverCalled).toBeFalse();
    });
    it('#should initialize isSlowEverCalled as false and indicator', () => {
      component.isSlowEverCalled = false;
      const obj = { networkSpeed: 'online' } as any;
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType(obj);
      expect(component.isSlowEverCalled).toBeFalse();
    });
    it('#should initialize isSlowEverCalled as true and indicator', () => {
      const obj = { networkSpeed: 'offline' } as any;
      component['pushPreviousStateGTM'] = jasmine.createSpy('pushPreviousStateGTM');
      component.styleIndicatorOnType(obj);
      expect(component.isSlowEverCalled).toBeTrue();
    });
  });

  it('should call openDialog', () => {
    component.config = { displayText: '', infoMsg: '' } as any;
    component.onInfoIconClick();
    expect(dialogService.openDialog).toHaveBeenCalled();
  });

  it('should call pushToGTMService', () => {
    component['pushToGTMService'](NETWORK_CONSTANTS.GA_TAGS.CONTENT_VIEW, NETWORK_CONSTANTS.GA_TAGS.LOAD, NETWORK_CONSTANTS.GA_TAGS.NA, NETWORK_CONSTANTS.GA_TAGS.INTERRUPTED_POPUP, NETWORK_CONSTANTS.GA_TAGS.INTERRUPTED_POPUP);
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('#pushPreviousStateGTM', () => {
    it('should not call pushToGTMService when network states are same', () => {
      component['pushToGTMService'] = jasmine.createSpy('pushToGTMService');
      component['pushPreviousStateGTM']('online', 'online');
      expect(component['pushToGTMService']).not.toHaveBeenCalled();
    });
    it('should call pushToGTMService when network states are not same', () => {
      component['pushToGTMService'] = jasmine.createSpy('pushToGTMService');
      component['pushPreviousStateGTM']('online', 'offline');
      expect(component['pushToGTMService']).toHaveBeenCalled();
    });
  });

});
