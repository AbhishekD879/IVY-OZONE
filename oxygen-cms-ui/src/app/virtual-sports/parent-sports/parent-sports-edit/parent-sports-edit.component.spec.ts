import { of } from 'rxjs';

import { ParentSportsEditComponent } from './parent-sports-edit.component';

describe('ParentSportsEditComponent', () => {
  let component: ParentSportsEditComponent;
  let virtualSportsService;
  let dialogService;
  let snackBar;
  let router;
  let route;
  let brandService;

  beforeEach(() => {
    virtualSportsService = {
      getVirtualSportParent: jasmine.createSpy('getVirtualSportParent').and.returnValue(of({ body: {} }))
    };
    dialogService = {};
    snackBar = {};
    router = {};
    route = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get')
        }
      }
    };
    brandService = {
      isIMActive: jasmine.createSpy('isIMActive')
    };

    component = new ParentSportsEditComponent(
      virtualSportsService, dialogService, snackBar, router, route, brandService
    );
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(virtualSportsService.getVirtualSportParent).toHaveBeenCalled();
  });
});
