import { YcMarketsEditComponent } from './yc-markets-edit.component';
import { of } from 'rxjs';

describe('YcMarketsEditComponent', () => {
  let component: YcMarketsEditComponent;
  let yourCallAPIService, activatedRoute, dialogService, router;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    dialogService = {};
    yourCallAPIService = {
      getSingleMarket: jasmine.createSpy('getSingleStaticBlock').and.returnValue(of({ body: {} }))
    };

    component = new YcMarketsEditComponent(
      yourCallAPIService,
      activatedRoute,
      dialogService,
      router
    );
    component.ngOnInit();
  });


  it('should call getSingleMarket', () => {
    expect(yourCallAPIService.getSingleMarket).toHaveBeenCalled();
  });
});
