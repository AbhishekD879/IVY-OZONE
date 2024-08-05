import { YcLeaguesEditComponent } from './yc-leagues-edit.component';
import { of } from 'rxjs';

describe('YcLeaguesEditComponent', () => {
  let component: YcLeaguesEditComponent;
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
      getSingleLeague: jasmine.createSpy('getSingleStaticBlock').and.returnValue(of({ body: {} }))
    };

    component = new YcLeaguesEditComponent(
      yourCallAPIService,
      activatedRoute,
      dialogService,
      router
    );
    component.ngOnInit();
  });

  it('should call getSingleLeague', () => {
    expect(yourCallAPIService.getSingleLeague).toHaveBeenCalled();
  });
});
