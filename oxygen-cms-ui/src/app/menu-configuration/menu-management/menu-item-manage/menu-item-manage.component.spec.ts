import { of } from 'rxjs';
import { MenuItemManageComponent } from './menu-item-manage.component';

describe('MenuItemManageComponent', () => {
  let component: MenuItemManageComponent;
  let dialogService;
  let dialog;
  let activatedRoute;
  let router;
  let brandService;
  let apiClientService;
  let brandMenuesService;

  beforeEach(() => {
    dialogService = {};
    dialog = {};
    activatedRoute = {
      params: of({})
    };
    router = {};
    brandService = {};
    apiClientService = {
      menues: () => brandMenuesService
    };
    brandMenuesService = {
      getMenu: jasmine.createSpy('getMenu').and.returnValue(of({ body: {} }))
    };

    component = new MenuItemManageComponent(
      dialogService, dialog, activatedRoute, router, brandService, apiClientService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(brandMenuesService.getMenu).toHaveBeenCalled();
  });
});
