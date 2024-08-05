import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { DashboardListComponent } from './dashboard-list.component';

describe('DashboardListComponent', () => {
  let component: DashboardListComponent;
  let apiClientService;
  let globalLoaderService;
  let brandService;

  beforeEach(() => {
    apiClientService = {
      dashboard: jasmine.createSpy('dashboard').and.returnValue({
        findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
      })
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    brandService = {};

    component = new DashboardListComponent(apiClientService, globalLoaderService, brandService);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn<any>(component, 'loadInitialData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component['loadInitialData']).toHaveBeenCalled();
  }));
});
