import { async } from '@angular/core/testing';
import { HrQuickLinksEditComponent } from './hr-quick-links-edit.component';
import { of } from 'rxjs';

describe('HrQuickLinksEditComponent', () => {
  let component,
    router,
    activatedRoute,
    apiClientService,
    dialogService,
    globalLoaderService,
    snackBar;

  beforeEach(async(() => {
    router = {};
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    apiClientService = {
      hrQuickLink: jasmine.createSpy('desktopQuickLink').and.returnValue({
        findOne: jasmine.createSpy('desktopQuickLink.findOne').and.returnValue(of({
          body: {}
        }))
      })
    };
    dialogService = {};
    globalLoaderService = {
      hideLoader: jasmine.createSpy('hideLoader'),
      showLoader: jasmine.createSpy('showLoader')
    };
    snackBar = {};

    component = new HrQuickLinksEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar
    );

    component.ngOnInit();
  }));

  it('should Init', () => {
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.hrQuickLink).toHaveBeenCalled();

    expect(component.hrQuickLink).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
