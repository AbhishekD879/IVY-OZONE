import { RetailRunService } from '@app/retail/services/retailRun/retail-run.service';

describe('ConnectRunService', () => {
  let service, upgradeAccountService, retailMenuService, retailService;

  beforeEach(() => {
    upgradeAccountService = jasmine.createSpyObj('UpgradeAccountService', ['subscribe']);
    retailMenuService = jasmine.createSpyObj('retailMenuService', ['subscribe']);
    retailService = jasmine.createSpyObj('retailService', ['subscribe']);
    service = new RetailRunService(upgradeAccountService, retailMenuService, retailService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('run', () => {
    service.run();

    expect(upgradeAccountService.subscribe).toHaveBeenCalled();
    expect(retailMenuService.subscribe).toHaveBeenCalled();
    expect(retailService.subscribe).toHaveBeenCalled();
  });
});
