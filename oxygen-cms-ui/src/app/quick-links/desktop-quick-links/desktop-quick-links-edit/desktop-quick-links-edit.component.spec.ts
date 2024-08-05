import { async } from '@angular/core/testing';

import {DesktopQuickLinksEditComponent} from './desktop-quick-links-edit.component';
import { of } from 'rxjs';

describe('DesktopQuickLinksEditComponent', () => {
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
      desktopQuickLink: jasmine.createSpy('desktopQuickLink').and.returnValue({
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

    component = new DesktopQuickLinksEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar
    );

    component.ngOnInit();
  }));

  it('should init', () => {
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.desktopQuickLink).toHaveBeenCalled();

    expect(component.desktopQuickLink).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
