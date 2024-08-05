import { FeatureEditComponent } from './feature-edit.component';
import { of } from 'rxjs';

describe('FeatureEditComponent', () => {
  let component: FeatureEditComponent;
  let snackBar;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let featureService;

  beforeEach(() => {
    snackBar = {};
    activatedRoute = {
      params: of({})
    };
    router = {};
    apiClientService = {
      feature: () => featureService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    featureService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new FeatureEditComponent(
      snackBar, activatedRoute, router, apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(featureService.getById).toHaveBeenCalled();
  });
});
