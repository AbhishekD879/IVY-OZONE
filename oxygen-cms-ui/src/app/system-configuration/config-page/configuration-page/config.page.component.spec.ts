import {ConfigPageComponent} from './config.page.component';
import { of } from 'rxjs';

describe('ConfigPageComponent', () => {
  let component: ConfigPageComponent;
  let dialogService, globalLoaderService, systemConfigAPIService;

  beforeEach(() => {
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    systemConfigAPIService = {
      getConfigurationData: jasmine.createSpy('getConfigurationData').and.returnValue(of([{body: {config: 'test1'}}]))
    };
    component = new ConfigPageComponent(
      dialogService, globalLoaderService, systemConfigAPIService
    );

    component.ngOnInit();
  });

  it('should сall getConfigurationData', () => {
    expect(systemConfigAPIService.getConfigurationData).toHaveBeenCalled();
  });
});
