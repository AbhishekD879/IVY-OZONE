import { MaintenanceEditPageComponent } from './maintenance-edit-page.component';
import { of } from 'rxjs';

describe('MaintenanceEditPageComponent', () => {
  let component: MaintenanceEditPageComponent;
  let router;
  let globalLoaderService;
  let apiClientService;
  let activatedRoute;
  let dialogService;
  let snackBar;
  let maintenanceService;

  beforeEach(() => {
    router = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    apiClientService = {
      maintenance: () => maintenanceService
    };
    activatedRoute = {
      params: of({})
    };
    dialogService = {};
    snackBar = {};
    maintenanceService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new MaintenanceEditPageComponent(
      router, globalLoaderService, apiClientService, activatedRoute, dialogService, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.form).toBeDefined();
    expect(maintenanceService.getById).toHaveBeenCalled();
  });
});
