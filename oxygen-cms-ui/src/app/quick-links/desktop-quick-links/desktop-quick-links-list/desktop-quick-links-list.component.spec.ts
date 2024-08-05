import { async } from '@angular/core/testing';

import {DesktopQuickLinksListComponent} from './desktop-quick-links-list.component';
import { of } from 'rxjs';

describe('DesktopQuickLinksListComponent', () => {
  let component,
    apiClientService,
    dialogService,
    globalLoaderService,
    snackBar,
    router;

  beforeEach(async(() => {
    apiClientService = {
      desktopQuickLink: jasmine.createSpy('desktopQuickLink').and.returnValue({
        findAllByBrand: jasmine.createSpy('desktopQuickLink.findOne').and.returnValue(of({
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

    component = new DesktopQuickLinksListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router
    );

    component.ngOnInit();
  }));

  it('should Init', () => {
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(apiClientService.desktopQuickLink).toHaveBeenCalled();

    expect(component.desktopQuickLinks).toBeDefined();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });
});
