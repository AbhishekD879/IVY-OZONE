import { MaintenanceListComponent } from './maintenance-list.component';
import { of } from 'rxjs';

describe('MaintenanceListComponent', () => {
  let component: MaintenanceListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let maintenanceService;

  beforeEach(() => {
    apiClientService = {
      maintenance: () => maintenanceService
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    maintenanceService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
    };

    component = new MaintenanceListComponent(
      apiClientService, dialogService, globalLoaderService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(maintenanceService.findAllByBrand).toHaveBeenCalled();
  });
});
