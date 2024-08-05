import { YcMarketsListComponent } from './yc-markets-list.component';
import { of } from 'rxjs';

describe('YcMarketsListComponent', () => {
  let component: YcMarketsListComponent;
  let snackBar, dialogService, dialog, marketsAPIService, router;

  beforeEach(() => {
    router = {};
    dialogService = {};
    snackBar = {};
    dialog = {};
    marketsAPIService = {
      getMarketsList: jasmine.createSpy('getMarketsList').and.returnValue(of({ body: 'test' }))
    };
    component = new YcMarketsListComponent(
      snackBar, dialogService, dialog, marketsAPIService, router
    );
    component.ngOnInit();
  });

  it('should call getMarketsList', () => {
    const data = 'test' as any;
    expect(marketsAPIService.getMarketsList).toHaveBeenCalled();
    expect(component.marketsData).toEqual(data);
  });
});
