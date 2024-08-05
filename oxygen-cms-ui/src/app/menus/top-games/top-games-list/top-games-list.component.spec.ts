import { of } from 'rxjs';
import { TopGamesListComponent } from './top-games-list.component';

describe('TopGamesListComponent', () => {
  let component: TopGamesListComponent;
  let apiClientService;
  let dialogService;
  let globalLoaderService;
  let snackBar;
  let router;
  let topGameService;

  beforeEach(() => {
    apiClientService = {
      topGame: () => topGameService
    };
    dialogService = {};
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    snackBar = {};
    router = {};
    topGameService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
    };

    component = new TopGamesListComponent(
      apiClientService, dialogService, globalLoaderService, snackBar, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(globalLoaderService.showLoader).toHaveBeenCalled();
    expect(topGameService.findAllByBrand).toHaveBeenCalled();
  });
});
