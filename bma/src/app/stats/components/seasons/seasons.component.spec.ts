import { LeaguesSeasonsComponent } from './seasons.component';
import { of as observableOf, throwError } from 'rxjs';

const seasonsMock = [
  {
    id: '1',
    areaId: '1',
    competitionId: '1',
    endDate: 'Friday, 13th',
    name: 'season1',
    sportId: '1',
    startDate: 'Friday, 13th',
    uniqueId: '1',
    year: '2019'
  },
  {
    id: '2',
    areaId: '2',
    competitionId: '2',
    endDate: 'Friday, 13th',
    name: 'season2',
    sportId: '2',
    startDate: 'Friday, 13th',
    uniqueId: '2',
    year: '2019'
  }
];

describe('LeaguesSeasonsComponent', () => {
  let component: LeaguesSeasonsComponent;
  let leagueService, router, route, routingState;

  beforeEach(() => {
    leagueService = {
      getSeasons: jasmine.createSpy('leagueService.getSeasons')
    } as any;

    router = {
      navigate: jasmine.createSpy('router.navigate')
    } as any;

    route = {
      params: observableOf({})
    } as any;

    routingState = {
      getRouteParam: jasmine.createSpy('routingState.getRouteParam')
    } as any;

    component = new LeaguesSeasonsComponent(
      leagueService,
      router,
      route,
      routingState
    );
  });

  describe('#ngOnInit', () => {
    it('Sets season and season id', () => {
      leagueService.getSeasons.and.returnValue(observableOf(seasonsMock));
      routingState.getRouteParam.and.returnValue('1');
      component.hideSpinner = jasmine.createSpy('hideSpinner');

      component.ngOnInit();

      expect(component.seasons).toEqual(seasonsMock);
      expect(component.seasonId).toEqual('1');
      expect(component.selectedSeason).toEqual(seasonsMock[0]);
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it('Does not set season id', () => {
      leagueService.getSeasons.and.returnValue(observableOf(seasonsMock));
      routingState.getRouteParam.and.returnValue(undefined);
      component.goToStanding = jasmine.createSpy('goToStanding');

      component.ngOnInit();

      expect(component.selectedSeason).toEqual(seasonsMock[0]);
      expect(component.goToStanding).toHaveBeenCalled();
    });

    it('Throws error', () => {
      leagueService.getSeasons.and.returnValue(throwError('error'));
      routingState.getRouteParam.and.returnValue('1');
      component.showError = jasmine.createSpy('showError');

      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });
  });

  it('#goToStanding', () => {
    component.goToStanding(seasonsMock[0]);

    expect(router.navigate).toHaveBeenCalledWith(['/leagues', '1', '1', '1', '1']);
  });
});
