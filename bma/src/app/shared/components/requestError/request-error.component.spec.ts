import { RequestErrorComponent } from '@shared/components/requestError/request-error.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('RequestErrorComponent', () => {
  let component: RequestErrorComponent;
  let pubSubService, windowRefService;

  beforeEach(() => {
    pubSubService = {
      publish: jasmine.createSpy('pubSub.publish'),
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((arg: string, p: string | string[], fn: Function) => fn()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn: Function) => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
      }
    };
    component = new RequestErrorComponent(pubSubService, windowRefService);
  });

  describe('isServerError', () => {
    it('should return false if login is pending', () => {
      component.loginPending = true;

      expect(component.isServerError).toBeFalsy();
    });

    it('should return false if load is not failed', () => {
      component.loginPending = false;
      component.loadFailed = false;

      expect(component.isServerError).toBeFalsy();
    });

    it('should return true if load is failed and login is not pending', () => {
      component.loginPending = false;
      component.loadFailed = true;

      expect(component.isServerError).toBeTruthy();
    });
  });

  it('#reloadSection should reload section', () => {
    spyOn(component.reloadFn, 'emit');
    component.reloadSection();

    expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
    expect(component.reloadPending).toBe(false);
    expect(component.reloadFn.emit).toHaveBeenCalled();
  });

  it('openLoginDialog should publish OPEN_LOGIN_DIALOG event', () => {
    component.insertedPlace = 'insertedPlace';
    component.openLoginDialog();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'insertedPlace' });
  });

  it('#ngOnInit', () => {
    component.loginNeed = true;
    component.ngOnInit();

    expect(component['title']).toContain('RequestError_');
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['title'], 'LOGIN_PENDING', jasmine.any(Function));
  });

  it('@ngOnDestroy should unsubscribe', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });
});
