import { of as observableOf, throwError } from 'rxjs';
import { OlympicsRunService } from '@app/olympics/services/olympics-run.service';

describe('OlympicsRunService', () => {
  let service: OlympicsRunService;
  let moduleExtensionsStorageService, olympicsService;

  beforeEach(() => {
    moduleExtensionsStorageService = {
      addToList: jasmine.createSpy('addToList')
    };

    olympicsService = {
      extensionName: 'lorem',
      getCMSConfig: jasmine.createSpy('getCMSConfig').and.returnValue(observableOf({ id: '1'} as any)),
      getSportsConfigs: jasmine.createSpy('getSportsConfigs').and.returnValue({}),
      getMenuConfigs: jasmine.createSpy('getMenuConfigs').and.returnValue([]),
      extendCacheParams: jasmine.createSpy('extendCacheParams')
    };

    service = new OlympicsRunService(moduleExtensionsStorageService, olympicsService);
  });

  it('#run success', () => {
    service.run();
    expect(olympicsService.getCMSConfig).toHaveBeenCalled();
    expect(olympicsService.getSportsConfigs).toHaveBeenCalledWith({ id: '1'});
    expect(olympicsService.getMenuConfigs).toHaveBeenCalledWith({ id: '1'});
    expect(moduleExtensionsStorageService.addToList).toHaveBeenCalledWith({
      name: 'lorem',
      extendsModule: 'sb',
      sportsConfig: {},
      menuConfig: []
    } as any);
    expect(olympicsService.extendCacheParams).toHaveBeenCalled();
  });

  it('run failed', () => {
    olympicsService.getCMSConfig.and.returnValue(throwError({ error: 'error' }));
    service.run();
    expect(olympicsService.getSportsConfigs).not.toHaveBeenCalled();
  });

  it('run failed (no error)', () => {
    olympicsService.getCMSConfig.and.returnValue(throwError(null));
    service.run();
    expect(olympicsService.getSportsConfigs).not.toHaveBeenCalled();
  });
});
