import { HeaderMenusEditComponent } from './header-menus-edit.component';
import { of } from "rxjs";

describe('HeaderMenusEditComponent', () => {
  let component: HeaderMenusEditComponent;
  let router, activatedRoute, apiClientService, dialogService, globalLoaderService;
  let headerMenus;

  beforeEach(() => {
    headerMenus = [
      {
        id: 1,
        disabled: false,
        inApp: false,
        lang: '',
        linkTitle: '',
        targetUri: '',
        level: '2',
        parent: ''
      }
    ];

    router = {};
    activatedRoute = {
      params: of({id: 1})
    };
    apiClientService = {
      headerMenu: jasmine.createSpy('headerMenu').and.returnValue(
        { findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({body: headerMenus}))}
      )
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new HeaderMenusEditComponent(router, activatedRoute, apiClientService, dialogService, globalLoaderService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.headerMenu().findAllByBrand).toHaveBeenCalled();
  });
});
