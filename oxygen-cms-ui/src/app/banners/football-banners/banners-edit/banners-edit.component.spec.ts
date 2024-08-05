import { of } from 'rxjs';
import { BannersEditComponent } from './banners-edit.component';

describe('BannersEditComponent', () => {
  let component: BannersEditComponent;
  let snackBar;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let footballBannersService;

  beforeEach(() => {
    snackBar = {};
    activatedRoute = {
      params: of({})
    };
    router = {};
    apiClientService = {
      footballBannersService: () => footballBannersService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    footballBannersService = {
      getSingleFootball3DBanner: jasmine.createSpy('getSingleFootball3DBanner').and.returnValue(of({ body: {} }))
    };

    component = new BannersEditComponent(
      snackBar, activatedRoute, router, apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(footballBannersService.getSingleFootball3DBanner).toHaveBeenCalled();
  });
});
