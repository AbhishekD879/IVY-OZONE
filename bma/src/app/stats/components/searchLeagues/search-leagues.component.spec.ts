import { SearchLeaguesComponent } from './search-leagues.component';
import { of as observableOf, throwError } from 'rxjs';

const areasMock = [
  { name: 'area_1', sportId: '1'},
  { name: 'area_2', sportId: '2'},
] as any;

describe('#SearchLeaguesComponent ', () => {
  let component: SearchLeaguesComponent ;

  let leagueService;

  beforeEach(() => {
    leagueService = {
      getAreas: jasmine.createSpy('leagueService.getAreas')
    };

    component = new SearchLeaguesComponent(leagueService);
  });


  describe('#ngOnInit', () => {
    it('Sets areas', () => {
      leagueService.getAreas.and.returnValue(observableOf(areasMock));

      component.ngOnInit();

      expect(leagueService.getAreas).toHaveBeenCalled();
      expect(component.areas).toEqual(areasMock);
    });

    it('Throw error', () => {
      leagueService.getAreas.and.returnValue(throwError('error'));
      component.showError = jasmine.createSpy('showError');
      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });
  });
});
