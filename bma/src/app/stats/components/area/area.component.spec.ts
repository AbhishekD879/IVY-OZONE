import { LeaguesAreaComponent } from './area.component';
import { of as observableOf, throwError } from 'rxjs';

const statsAreasAndCompetitionsMock = {
  area: 'test_area',
  competitions: [
    {
      areaId: '1',
      id: '1',
      name: 'test_ar_1',
      sportId: 's1',
      uniqIdentifier: 'id1',
      displayOrder: '1',
      title: 'title1',
      hidden: false
    },
    {
      areaId: '2',
      id: '2',
      name: 'test_ar_2',
      sportId: 's2',
      uniqIdentifier: 'id2',
      displayOrder: '2',
      title: 'title2',
      hidden: false
    }
  ] as any
};

const statsDataMock = {
  value: statsAreasAndCompetitionsMock
};

describe('#LeaguesAreaComponent', () => {
  let component: LeaguesAreaComponent;
  let leagueService, router, route, routingState;

  beforeEach(() => {
    leagueService = {
      getAreaAndCompetitions: jasmine.createSpy('leagueService.getAreaAndCompetitions')
    } as any;
    router = {
      navigate: jasmine.createSpy('router.navigate')
    } as any;
    route = {} as any;
    routingState = {
      getRouteParam: jasmine.createSpy('routingState.getRouteParam')
    } as any;

    component = new LeaguesAreaComponent(
      leagueService,
      router,
      route,
      routingState
    );
  });

  describe('#ngOnInit', () => {
    it('Sets index and competitions', () => {
      routingState.getRouteParam.and.returnValue('2');
      leagueService.getAreaAndCompetitions.and.returnValue(observableOf(statsDataMock));

      component.ngOnInit();

      expect(component.area).toBe('test_area');
      expect(component.competitions).toEqual(statsAreasAndCompetitionsMock.competitions);
      expect(component.index).toBe(1);
      expect(component.competition).toEqual(statsAreasAndCompetitionsMock.competitions[1]);
    });

    it('Does not set index and competitions', () => {
      routingState.getRouteParam.and.returnValue(undefined);
      leagueService.getAreaAndCompetitions.and.returnValue(observableOf(statsDataMock));

      component.ngOnInit();

      expect(component.index).toBe(0);
      expect(router.navigate).toHaveBeenCalled();
    });

    it('Should throw error', () => {
      routingState.getRouteParam.and.returnValue(null);
      leagueService.getAreaAndCompetitions.and.returnValue(throwError('error'));
      component.showError = jasmine.createSpy('showError');

      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });
  });

  describe('#GoToNext and GoToPrev', () => {
    beforeEach(() => {
      component['loadCompetition'] = jasmine.createSpy('loadCompetition');
      component.competitions = statsAreasAndCompetitionsMock.competitions;
      component.index = 2;
    });

    it('#goToNext', () => {
      component.goToNext();

      expect(component.index).toBe(3);
      expect(component['loadCompetition']).toHaveBeenCalled();
    });

    it('#goToPrev', () => {
      component.goToPrev();

      expect(component.index).toBe(1);
      expect(component['loadCompetition']).toHaveBeenCalled();
    });
  });
});
