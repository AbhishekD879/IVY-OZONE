import { RetailService } from '@app/retail/services/retail/retail.service';
import { Observable } from 'rxjs';

describe('RetailService', () => {
  let service: RetailService, storageService, pubSubService, nativeBridgeService, deviceService, router;

  beforeEach(() => {
    storageService = jasmine.createSpyObj('StorageService', ['setCookie', 'getCookie']);
    nativeBridgeService = jasmine.createSpyObj('NativeBridgeService', ['checkConnect', 'checkGrid']);

    deviceService = {
      isWrapper: null
    };

    router = jasmine.createSpyObj('routerSpy', ['navigateByUrl']);

    pubSubService = {
      API: {
        CHECK_RETAIL_NATIVE: 'CHECK_RETAIL_NATIVE',
        REDIRECT_TO_URL: 'REDIRECT_TO_URL'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        channelFunction(true);
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };

    service = new RetailService(
      storageService,
      nativeBridgeService,
      pubSubService,
      deviceService,
      router);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('isWrapper', () => {
    it('checkRetail when cookies found', (done) => {
      storageService.getCookie.and.returnValue('false');
      deviceService.isWrapper = true;

      const result = service.checkRetail();
      result.subscribe();

      expect(storageService.getCookie).toHaveBeenCalledWith('CONNECT_TRACKER');
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'checkRetailNative', pubSubService.API.CHECK_RETAIL_NATIVE, jasmine.any(Function)
      );
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('checkRetailNative');
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
      expect(nativeBridgeService.checkConnect).toHaveBeenCalled();
      done();

      expect(result).toEqual(jasmine.any(Observable));
    });

    it('checkRetail when cookies found', (done) => {
      deviceService.isWrapper = false;
      const result = service.checkRetail();
      result.subscribe();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(0);
      done();

      expect(result).toEqual(jasmine.any(Observable));
    });

    it('checkGridRetail when cookies found', (done) => {
      storageService.getCookie.and.returnValue('false');
      deviceService.isWrapper = true;

      const result = service.checkGridRetail();
      result.subscribe();

      expect(storageService.getCookie).toHaveBeenCalledWith('grid');
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'checkRetailNative', pubSubService.API.CHECK_RETAIL_NATIVE, jasmine.any(Function)
      );
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('checkRetailNative');
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
      expect(nativeBridgeService.checkGrid).toHaveBeenCalled();
      done();

      expect(result).toEqual(jasmine.any(Observable));
    });

    it('checkGridRetail when cookies found', (done) => {
      deviceService.isWrapper = false;
      const result = service.checkGridRetail();
      result.subscribe();

      expect(pubSubService.subscribe).toHaveBeenCalledTimes(0);
      done();

      expect(result).toEqual(jasmine.any(Observable));
    });

    it('check subscription', () => {
      service.subscribe();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'retailThirdPartyRedirection', pubSubService.API.REDIRECT_TO_URL, jasmine.any(Function));
    });
  });
});
