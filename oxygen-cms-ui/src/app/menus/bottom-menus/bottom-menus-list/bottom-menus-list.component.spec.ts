import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { BottomMenusListComponent } from './bottom-menus-list.component';

describe('BottomMenusListComponent', () => {
  let component: BottomMenusListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;

  beforeEach(() => {
    apiClientService = {
      bottomMenu: jasmine.createSpy('bottomMenu').and.returnValue({
        findAllByBrand: jasmine.createSpy('findOne').and.returnValue(of({
          body: {}
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

    component = new BottomMenusListComponent(
      apiClientService,
      dialogService,
      globalLoaderService,
      snackBar,
      router
    );
  });

  describe('ngOnInit', () => {
    it('should show loader', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(globalLoaderService.showLoader).toHaveBeenCalled();
    }));

    it('should hide loader', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    }));

    it('should init data', fakeAsync(() => {
      component.ngOnInit();

      tick();

      expect(apiClientService.bottomMenu).toHaveBeenCalled();
      expect(component.bottomMenus).toBeDefined();
    }));
  });
});
