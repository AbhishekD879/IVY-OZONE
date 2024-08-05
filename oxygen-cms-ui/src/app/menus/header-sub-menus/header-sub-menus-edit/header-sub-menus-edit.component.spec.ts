import { HeaderSubMenusEditComponent } from './header-sub-menus-edit.component';
import { of } from "rxjs";

describe('HeaderSubMenusEditComponent', () => {
  let component: HeaderSubMenusEditComponent;
  let router, activatedRoute, apiClientService, dialogService, globalLoaderService;
  let headerSubMenus;

  beforeEach(() => {
    headerSubMenus = [
      {
        id: 1,
        disabled: false,
        inApp: false,
        lang: '',
        linkTitle: '',
        targetUri: ''
      }
    ]

    router = {};

    activatedRoute = {
      params: of({id: 1})
    };

    apiClientService = {
      headerSubMenu: jasmine.createSpy('headerMenu').and.returnValue(
        { findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({body: headerSubMenus}))}
        )
    };

    dialogService = {};

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new HeaderSubMenusEditComponent(router, activatedRoute, apiClientService, dialogService, globalLoaderService)
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.headerSubMenu).toHaveBeenCalled();
  });
});
