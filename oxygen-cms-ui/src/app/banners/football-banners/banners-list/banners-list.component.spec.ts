import { of } from 'rxjs';
import { BannersListComponent } from './banners-list.component';

describe('BannersListComponent', () => {
  let component: BannersListComponent;
  let snackBar;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let footballBannersService;

  beforeEach(() => {
    apiClientService = {
      footballBannersService: () => footballBannersService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    snackBar = {};
    router = {};
    footballBannersService = {
      getFootball3DFootball3DBanners: jasmine.createSpy('getFootball3DFootball3DBanners').and.returnValue(of({}))
    };

    component = new BannersListComponent(
      snackBar, apiClientService, globalLoaderService, dialogService, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(footballBannersService.getFootball3DFootball3DBanners).toHaveBeenCalled();
  });
});
