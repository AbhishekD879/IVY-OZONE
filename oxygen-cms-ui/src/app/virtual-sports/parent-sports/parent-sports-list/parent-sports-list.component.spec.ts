import { of } from 'rxjs';

import { ParentSportsListComponent } from './parent-sports-list.component';

describe('ParentSportsListComponent', () => {
  let component: ParentSportsListComponent;
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
      getVirtualSportsByBrand: jasmine.createSpy('getVirtualSportsByBrand').and.returnValue(of({}))
    };

    component = new ParentSportsListComponent(
      router,
      dialogService,
      dialog,
      snackBar,
      globalLoaderService,
      virtualSportsService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(virtualSportsService.getVirtualSportsByBrand).toHaveBeenCalled();
  });
});
