import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { BottomMenusEditComponent } from './bottom-menus-edit.component';

describe('BottomMenusEditComponent', () => {
  let component: BottomMenusEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({ id: 0 })
    };
    apiClientService = {
      bottomMenu: jasmine.createSpy('bottomMenu').and.returnValue({
        findOne: jasmine.createSpy('findOne').and.returnValue(of({
          body: {}
        }))
      })
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new BottomMenusEditComponent(
      router,
      activatedRoute,
      apiClientService,
      dialogService,
      globalLoaderService);
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
      expect(component.form).toBeDefined();
      expect(component.breadcrumbsData).toBeDefined();
    }));
  });
});
