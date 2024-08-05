import { of } from 'rxjs';

import { BybMarketsListComponent } from './byb-markets-list.component';

describe('BybMarketsListComponent', () => {
  let component: BybMarketsListComponent;
  let snackBar;
  let dialogService;
  let dialog;
  let bybAPIService;
  let brandService;
  let router;

  beforeEach(() => {
    snackBar = {};
    dialogService = {};
    dialog = {};
    bybAPIService = {
      getMarketsList: jasmine.createSpy('getMarketsList').and.returnValue(of({
        body: {}
      }))
    };
    brandService = {};
    router = {};

    component = new BybMarketsListComponent(
      snackBar,
      dialogService,
      dialog,
      bybAPIService,
      brandService,
      router);
  });

  describe('ngOnInit', () => {
    it('should call getMarketsList', () => {
      component.ngOnInit();

      expect(bybAPIService.getMarketsList).toHaveBeenCalled();
    });

    it('should init marketsData', () => {
      component.ngOnInit();

      expect(component.marketsData).toBeDefined();
    });
  });
});
