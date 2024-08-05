import { of } from 'rxjs';

import { ChildSportsListComponent } from '@app/virtual-sports/child-sports/child-sports-list/child-sports-list.component';

describe('ChildSportsListComponent', () => {
  let component: ChildSportsListComponent;
  let router;
  let dialogService;
  let dialog;
  let snackBar;
  let globalLoaderService;
  let virtualSportsService;

  beforeEach(() => {
    router = {};
    dialogService = {};
    dialog = {};
    snackBar = {};

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    virtualSportsService = {
      getVirtualSportsChildrenByParentSportId: jasmine.createSpy('getVirtualSportsChildrenByParentSportId').and.returnValue(of({}))
    };

    component = new ChildSportsListComponent(
      router,
      dialog,
      dialogService,
      snackBar,
      globalLoaderService,
      virtualSportsService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(virtualSportsService.getVirtualSportsChildrenByParentSportId).toHaveBeenCalled();
  });
});
