import { of } from 'rxjs';

import { EditBrandComponent } from './edit-brand.component';

describe('EditBrandComponent', () => {
  let component: EditBrandComponent;
  let globalLoaderService;
  let brandsAPIService;
  let activatedRoute;
  let dialogService;
  let router;

  beforeEach(() => {
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    brandsAPIService = {
      getSingleBrandData: jasmine.createSpy('getSingleBrandData').and.returnValue(of({}))
    };
    activatedRoute = {
      params: of({})
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    router = {};

    component = new EditBrandComponent(
      globalLoaderService, brandsAPIService, activatedRoute, dialogService, router
    );
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(brandsAPIService.getSingleBrandData).toHaveBeenCalled();
  });
});
