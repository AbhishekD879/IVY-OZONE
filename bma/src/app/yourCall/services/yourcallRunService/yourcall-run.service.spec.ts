import { YourcallRunService } from '@yourcall/services/yourcallRunService/yourcall-run.service';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { of } from 'rxjs';

describe('YourcallRunService', () => {
  let service: YourcallRunService;
  let commandService: any;
  let injector: any;

  beforeEach(() => {
    commandService = {
      register: jasmine.createSpy('register'),
      API: commandApi
    };
    injector = {
      get: jasmine.createSpy('get').and.returnValue({})
    };

    service = new YourcallRunService(commandService, injector);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('run should run all internal functions', () => {
    spyOnProperty<any>(service, 'yourCallMarketsService', 'get').and.returnValue({
      getGame: jasmine.createSpy('getGame'),
    });

    spyOnProperty<any>(service, 'yourCallProvider', 'get').and.returnValue({
      useOnce: jasmine.createSpy('useOnce').and.returnValue({
        getBets: () => {
        }
      }),
    });

    spyOnProperty<any>(service, 'yourCallService', 'get').and.callFake(() => ({
      whenYCReady: jasmine.createSpy('whenYCReady').and.returnValue(of([])),
      getStaticBlocks: jasmine.createSpy('getStaticBlocks'),
      getYCTab: jasmine.createSpy('getYCTab'),
      get5ASideTab: jasmine.createSpy('get5ASideTab'),
      isBYBIconAvailable: jasmine.createSpy('isBYBIconAvailable'),
      isBYBIconAvailableForEvents: jasmine.createSpy('isBYBIconAvailableForEvents')
    }));
    commandService.register.and.callFake((a, b) => b());

    service.run();

    expect(commandService.register).toHaveBeenCalledTimes(8);
  });

  it('yourCallService should call injector get method with YourcallService', () => {
    expect(service['yourCallService']).toBeTruthy();
    expect(service['injector'].get).toHaveBeenCalledWith(YourcallService);
  });

  it('YourcallMarketsService should call injector get method with YourcallMarketsService', () => {
    expect(service['yourCallMarketsService']).toBeTruthy();
    expect(service['injector'].get).toHaveBeenCalledWith(YourcallMarketsService);
  });

  it('yourCallProvider should call injector get method with YourcallMarketsService', () => {
    expect(service['yourCallProvider']).toBeTruthy();
    expect(service['injector'].get).toHaveBeenCalledWith(YourcallProviderService);
  });
});
