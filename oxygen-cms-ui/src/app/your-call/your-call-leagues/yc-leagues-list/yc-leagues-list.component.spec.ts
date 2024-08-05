import { YcLeaguesListComponent } from './yc-leagues-list.component';
import { of } from 'rxjs';

describe('YcLeaguesListComponent', () => {
  let component: YcLeaguesListComponent;
  let dialog, dialogService, router, leaguesAPIService, snackBar;

  beforeEach(() => {
    dialog = {};
    dialogService = {};
    router = {};
    snackBar = {};
    leaguesAPIService = {
      getLeaguesList: jasmine.createSpy('getLeaguesList').and.returnValue(of({ body: 'test' }))
    };
    component = new YcLeaguesListComponent(
      snackBar, dialogService, dialog, leaguesAPIService, router
    );

    component.ngOnInit();
  });

  it('should call getLeaguesList', () => {
    const data = 'test' as any;
    expect(leaguesAPIService.getLeaguesList).toHaveBeenCalled();
    expect(component.leaguesData).toEqual(data);
  });
});
