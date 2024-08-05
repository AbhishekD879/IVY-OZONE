import { WMiniGamesIframeComponent } from './w-mini-games-iframe.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('WMiniGamesIframeComponent', () => {
  let component, casinoGamesService, sanitizer, pubSubService;
  const miniGamesUrl = 'https://some-url';

  beforeEach(() => {
    sanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy().and.returnValue(miniGamesUrl)
    };

    casinoGamesService = {
      miniGamesUrl: jasmine.createSpy().and.returnValue('miniGamesUrl')
    };

    pubSubService = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, methods, callback) => {
        callback();
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    component = new WMiniGamesIframeComponent(
      casinoGamesService,
      sanitizer,
      pubSubService
    );
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component['setIframeUrl'] = jasmine.createSpy('setIframeUrl');
    component.ngOnInit();

    expect(component['setIframeUrl']).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith('wMiniGamesIframeComponent', 'SESSION_LOGIN', jasmine.any(Function));
  });

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('wMiniGamesIframeComponent');
  });

  it('should call handleMessage method when receives post message', () => {
    const event = {} as MessageEvent;
    component['handleMessage'] = jasmine.createSpy();
    component.onMessage(event);
    expect(component['handleMessage']).toHaveBeenCalledWith(event);
  });

  it('should call openIFrame method', () => {
    const event = { data: { type: 'LOBBY_LOADED' } } as MessageEvent;
    component['openIFrame'] = jasmine.createSpy();
    component.handleMessage(event);
    expect(component['openIFrame']).toHaveBeenCalled();
  });

  it('should call openLoginDialog method', () => {
    const event = { data: { type: 'SHOW_LOGIN' } } as MessageEvent;
    component['openLoginDialog'] = jasmine.createSpy();
    component.handleMessage(event);
    expect(component['openLoginDialog']).toHaveBeenCalled();
  });

  it('should call handleErrorIFrame method', () => {
    const event = { data: { type: 'LOBBY_FEED_ERROR' } } as MessageEvent;
    component['handleErrorIFrame'] = jasmine.createSpy();
    component.handleMessage(event);
    expect(component['handleErrorIFrame']).toHaveBeenCalled();
  });

  it('should call handleMessage method when receives post message has wrong type', () => {
    const event = { data: 'action%3D'} as MessageEvent;
    component['openIFrame'] = jasmine.createSpy();
    component['handleErrorIFrame'] = jasmine.createSpy();
    component.handleMessage(event);
    expect(component['openIFrame']).not.toHaveBeenCalled();
    expect(component['handleErrorIFrame']).not.toHaveBeenCalled();
  });

  it('#setIframeUrl',  () => {
    component['setIframeUrl']();
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith(casinoGamesService.miniGamesUrl);
    expect(component.miniGamesUrl).toBe(miniGamesUrl);
    expect(component.showContent).toBeFalsy();
    expect(component.showLoadingSpinner).toBeTruthy();
  });

  it('#openIFrame',  () => {
    component['openIFrame']();
    expect(component.showContent).toBeTruthy();
    expect(component.isError).toBeFalsy();
    expect(component.showLoadingSpinner).toBeFalsy();
  });

  it('#openLoginDialog',  () => {
    component['openLoginDialog']();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG);
  });

  it('#handleErrorIFrame',  () => {
    component['handleErrorIFrame']();
    expect(component.showContent).toBeFalsy();
    expect(component.isError).toBeTruthy();
    expect(component.showLoadingSpinner).toBeFalsy();
  });

});
