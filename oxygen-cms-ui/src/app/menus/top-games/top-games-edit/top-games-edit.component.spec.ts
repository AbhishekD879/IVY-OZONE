import { TopGamesEditComponent } from './top-games-edit.component';
import { of } from 'rxjs';

describe('TopGamesEditComponent', () => {
  let component: TopGamesEditComponent;
  let router;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let topGameService;

  beforeEach(() => {
    router = {};
    activatedRoute = {
      params: of({})
    };
    apiClientService = {
      topGame: () => topGameService
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    snackBar = {};
    topGameService = {
      findOne: jasmine.createSpy().and.returnValue(of({ body: {} }))
    };

    component = new TopGamesEditComponent(
      router, activatedRoute, apiClientService, dialogService, globalLoaderService, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(topGameService.findOne).toHaveBeenCalled();
  });
});
