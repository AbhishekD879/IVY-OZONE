import { of } from 'rxjs';
import { LeaguesListComponent } from './leagues-list.component';

describe('LeaguesListComponent', () => {
  let component: LeaguesListComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let router;
  let leagueService;

  beforeEach(() => {
    apiClientService = {
      league: () => leagueService
    };
    globalLoaderService = {
      hideLoader: jasmine.createSpy('hideLoader'),
      showLoader: jasmine.createSpy('showLoader')
    };
    dialogService = {};
    router = {};
    leagueService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({}))
    };

    component = new LeaguesListComponent(
      apiClientService, globalLoaderService, dialogService, router
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(leagueService.findAllByBrand).toHaveBeenCalled();
  });
});
