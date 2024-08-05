import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { BybMarketsEditComponent } from './byb-markets-edit.component';

describe('BybMarketsEditComponent', () => {
  let component: BybMarketsEditComponent;
  let bybAPIService;
  let activatedRoute;
  let dialogService;
  let router;

  beforeEach(() => {
    bybAPIService = {
      getSingleMarket: jasmine.createSpy('getSingleMarket').and.returnValue(of({
        body: {
          name: ''
        }
      }))
    };
    activatedRoute = {
      params: of({})
    };
    dialogService = {};
    router = {};

    component = new BybMarketsEditComponent(
      bybAPIService,
      activatedRoute,
      dialogService,
      router);
  });

  it('ngOnInit', fakeAsync(() => {
    spyOn<any>(component, 'loadInitData').and.callThrough();

    component.ngOnInit();
    tick();

    expect(component['loadInitData']).toHaveBeenCalled();
  }));
});
