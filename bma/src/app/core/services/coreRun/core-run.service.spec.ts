import { CoreRunService } from './core-run.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { BetPlacementErrorTrackingService } from '@core/services/betPlacementErrorTracking/bet-placement-error-tracking';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SubscribersRouteService } from '@core/services/subscribersRoute/subscribers-route.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

describe('CoreRunService', () => {
  let service: CoreRunService;
  let command;
  let injector;
  let homePageLoaderService;

  beforeEach(() => {
    command = {
      register: jasmine.createSpy('register'),
      API: commandApi
    };
    injector = {
      get: jasmine.createSpy('injector get').and.returnValue({
        init: jasmine.createSpy('init'),
        subscribe: jasmine.createSpy('subscribe'),
        loadModule: jasmine.createSpy('loadModule'),
        sendBetSlip: jasmine.createSpy('sendBetSlip')
      })
    };
    homePageLoaderService = {
      init: jasmine.createSpy('init')
    };

    service = new CoreRunService(
      command,
      injector,
      homePageLoaderService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  describe('CoreRunService', () => {
    it('should init', () => {
      service.init();

      expect(command.register).toHaveBeenCalledTimes(2);
      expect(homePageLoaderService.init).toHaveBeenCalledTimes(1);
      expect(service.nativeBridgeService.init).toHaveBeenCalled();
      expect(service.betslipSelectionsDataService.subscribe).toHaveBeenCalled();
      expect(service.gtmService.init).toHaveBeenCalled();
      expect(service.subscribersRouteService.init).toHaveBeenCalled();
    });

    it('should call callback for BESTLIP_ERROR_TRACKING', () => {
      let callback: Function;

      command.register.and.callFake((api: string, cb: Function) => {
        callback = api === command.API.BESTLIP_ERROR_TRACKING && cb && cb();
      });

      service.init();

      callback && callback();

      expect(service.betPlacementErrorTrackingService.sendBetSlip).toHaveBeenCalled();
    });

    describe('should call callback for LAZY_LOAD', () => {
      it('when module path is relevant', () => {
        command.register.and.callFake((api: string, cb: Function) => {
          (api === command.API.LAZY_LOAD) && cb && cb('module/path:custom');
        });

        service.init();

        expect(service.dynamicComponentLoader.loadModule)
          .toHaveBeenCalledWith('module/path', injector);
      });

      it('when module path is not relevant', () => {
        let res: Promise<any>;

        command.register.and.callFake((api: string, cb: Function) => {
          if (api === command.API.LAZY_LOAD) {
            res = cb && cb('module/path');

            res.then(d => {
              expect(d).toBeUndefined();
            });
          }
        });

        service.init();

        expect(service.dynamicComponentLoader.loadModule).not.toHaveBeenCalled();
      });
    });
  });

  describe('injector', () => {
    let loader: any;

    it('should return dynamicComponentLoader', () => {
      loader = service.dynamicComponentLoader;

      expect(injector.get).toHaveBeenCalledWith(DynamicLoaderService);
    });

    it('should return NativeBridgeService', () => {
      loader = service.nativeBridgeService;

      expect(injector.get).toHaveBeenCalledWith(NativeBridgeService);
    });

    it('should return betPlacementErrorTrackingService', () => {
      loader = service.betPlacementErrorTrackingService;

      expect(injector.get).toHaveBeenCalledWith(BetPlacementErrorTrackingService);
    });

    it('should return betslipSelectionsDataService', () => {
      loader = service.betslipSelectionsDataService;

      expect(injector.get).toHaveBeenCalledWith(BetslipSelectionsDataService);
    });

    it('should return gtmService', () => {
      loader = service.gtmService;

      expect(injector.get).toHaveBeenCalledWith(GtmService);
    });

    it('should return subscribersRouteService', () => {
      loader = service.subscribersRouteService;

      expect(injector.get).toHaveBeenCalledWith(SubscribersRouteService);
    });

    it('should return asyncScriptLoaderService', () => {
      loader = service.asyncScriptLoaderService;

      expect(injector.get).toHaveBeenCalledWith(AsyncScriptLoaderService);
    });

    afterEach(() => {
      const keys: string[] = Object.keys(loader);

      expect(injector.get).toHaveBeenCalled();
      expect(keys[0]).toBe('init');
      expect(keys[1]).toBe('subscribe');
      expect(keys[2]).toBe('loadModule');
      expect(keys[3]).toBe('sendBetSlip');
    });
  });
});
