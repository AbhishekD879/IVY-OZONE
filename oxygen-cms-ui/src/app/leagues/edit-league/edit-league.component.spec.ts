import { EditLeagueComponent } from './edit-league.component';
import { of } from 'rxjs';

describe('EditLeagueComponent', () => {
  let component: EditLeagueComponent;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let leagueService;

  beforeEach(() => {
    activatedRoute = {
      params: of({})
    };
    router = {};
    apiClientService = {
      league: () => leagueService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    leagueService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new EditLeagueComponent(
      activatedRoute, router, apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(leagueService.getById).toHaveBeenCalled();
  });
});
