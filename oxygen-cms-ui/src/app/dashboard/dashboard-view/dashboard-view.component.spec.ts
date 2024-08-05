import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { DashboardViewComponent } from './dashboard-view.component';

describe('DashboardViewComponent', () => {
  let component: DashboardViewComponent;
  let apiClientService;
  let globalLoaderService;
  let activatedRoute;

  beforeEach(() => {
    apiClientService = {
      dashboard: jasmine.createSpy('dashboard').and.returnValue({
        getById: jasmine.createSpy('getById').and.returnValue(of({
          body: {
            progressURI: ''
          }
        }))
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    activatedRoute = {
      params: of({})
    };

    component = new DashboardViewComponent(apiClientService, globalLoaderService, activatedRoute);
  });

  describe('ngOnInit', () => {
    it('should show loader', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(globalLoaderService.showLoader).toHaveBeenCalledBefore(apiClientService.dashboard);
    }));

    it('should hide loader', fakeAsync(() => {
      component.ngOnInit();
      tick();

      expect(globalLoaderService.hideLoader).toHaveBeenCalled();
    }));

    it('should get data for dashboard view', fakeAsync(() => {
      spyOn(component, 'setUri').and.callThrough();

      component.ngOnInit();
      tick();

      expect(component.purge).toBeDefined();
      expect(component.setUri).toHaveBeenCalled();
      expect(component.breadcrumbsData).toBeDefined();
    }));
  });
});
