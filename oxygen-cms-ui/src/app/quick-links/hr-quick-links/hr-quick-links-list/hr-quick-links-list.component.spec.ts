import { HrQuickLinksListComponent } from './hr-quick-links-list.component';
import { of } from 'rxjs';

describe('HrQuickLinksListComponent', () => {
  let component,
    apiClientService,
    dialogService,
    globalLoaderService,
    snackBar,
    router;

  beforeEach(() => {
    apiClientService = {
      hrQuickLink: jasmine.createSpy('hrQuickLink').and.returnValue({
        findAllByBrand: jasmine.createSpy('hrQuickLink.findAllByBrand').and.returnValue(of({
          body: []
        }))
      })
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = {};
    router = {};

    component = new HrQuickLinksListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router
    );

    component.ngOnInit();
  });

  it('should create', () => {
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.hrQuickLink).toHaveBeenCalled();

    expect(component.hrQuickLinks).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
