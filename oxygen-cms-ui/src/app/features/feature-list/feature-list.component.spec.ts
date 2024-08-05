import { FeatureListComponent } from './feature-list.component';
import { of } from 'rxjs';

describe('FeatureListComponent', () => {
  let component: FeatureListComponent;
  let snackBar;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let featureService;

  beforeEach(() => {
    snackBar = {};
    apiClientService = {
      feature: () => featureService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    dialogService = {};
    featureService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
    };

    component = new FeatureListComponent(
      snackBar, apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(featureService.findAllByBrand).toHaveBeenCalled();
  });
});
