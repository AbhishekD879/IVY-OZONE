import { of } from 'rxjs';

import { ChildSportsEditComponent } from '@app/virtual-sports/child-sports/child-sports-edit/child-sports-edit.component';

describe('ChildSportsEditComponent', () => {
  let component: ChildSportsEditComponent;
  let childSportsService;
  let parentSportsService;
  let dialogService;
  let snackBar;
  let router;
  let route;
  let dialog;

  beforeEach(() => {
    childSportsService = {
      getVirtualSportChild: jasmine.createSpy('getVirtualSportChild').and.returnValue(of({ body: {} })),
      getVirtualSportParent: jasmine.createSpy('getVirtualSportParent')
    };
    parentSportsService = {};
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
    dialog = {};

    component = new ChildSportsEditComponent(
      childSportsService, parentSportsService, dialogService, snackBar,
      router, route, dialog
    );
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
  });

  it('ngOnInit', () => {
    expect(component).toBeTruthy();
  });
});
