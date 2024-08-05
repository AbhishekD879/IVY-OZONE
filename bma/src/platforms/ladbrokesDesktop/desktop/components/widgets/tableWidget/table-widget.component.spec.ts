import { fakeAsync, tick } from '@angular/core/testing';

import { TableWidgetComponent } from './table-widget.component';
import { IAllSeasons } from '@app/stats/models/br-competition-season.model';

const allCompetitions = [{
  areaId: '123',
  name: 'competition',
  sportId: '111',
  uniqIdentifier: 'unique1',
  displayOrder: '123123',
  title: 'title',
  id: '1'
}];
const allSeasons = [{
  areaId: 'string',
  competitionIds: ['1'],
  endDate: 'string',
  id: 'string',
  name: 'string',
  sportId: '111',
  startDate: 'startDate',
  year: 'year',
  _id: '_id'
}];
const competitions = {
  competitionId: '1',
  allCompetitions,
  allSeasons,
  status: 'status',
  sportId: 111,
  sportName: '',
  areaId: 131,
  areaName: 'areaName',
  competitionName: 'competitionName'
};

describe('TableWidgetComponent', () => {
  let component;
  let commandService;
  let pubSubService;

  beforeEach(() => {
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(competitions)),
      API: {
        GET_SEASONS: 'GET_SEASONS',
        GET_LEAGUE_TABLE: 'GET_LEAGUE_TABLE',
        GET_RESULT_TABLES: 'GET_RESULT_TABLES'
      }
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        WIDGET_VISIBILITY: 'WIDGET_VISIBILITY',
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    };

    component = new TableWidgetComponent(
      commandService,
      pubSubService
    );
    component.params = {} as any;
  });

  it('create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', fakeAsync(() => {
    spyOn(component as any, 'setSeasonIndex').and.returnValue(0);
    component.ngOnInit();
    tick();

    expect(component.competitionId as any).toEqual('1');
    expect(component.competitions).toEqual(allCompetitions);
    expect(component.seasons).toEqual(allSeasons);
    expect(component.activeTab).toEqual(allCompetitions[0]);
  }));

  it('#trackById', () => {
    const result = component.trackById(1, {
      id: 'id'
    } as any);
    expect(result).toEqual('1_id');
  });

  it('#changeGroup', () => {
    component.seasons = [allSeasons[0]];
    component.changeGroup({
      tab: {
        id: '1',
        areaId: '123'
      }
    } as any);
    expect(component.activeTab).toEqual({
      id: '1',
      areaId: '123'
    } as any);
  });

  describe('filterCompetition', () => {
    it(`should return False if competition name has 'preliminary round'`, () => {
      expect(component.filterCompetition({ name: 'UEFA Champions League, Preliminary Round' } as any)).toBeFalsy();
    });

    it(`should return True if competition name has Not 'preliminary round'`, () => {
      expect(component.filterCompetition({ name: 'UEFA Champions League' } as any)).toBeTruthy();
    });
  });

  describe('goToNext', () => {
    beforeEach(() => {
      component.seasons = [allSeasons[0], allSeasons[0], allSeasons[0], allSeasons[0]];
      component.competitions = allCompetitions;
    });

    it('#goToNext', fakeAsync(() => {
      component.goToNext();
      tick();

      expect(component.seasonIndex).toEqual(1);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'widget',
        eventAction: 'league table',
        eventLabel: 'change season'
      }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
    }));

    it(`should run 'createTabsForCurrentSeason'`, () => {
      spyOn(component as any, 'createTabsForCurrentSeason');

      component.goToNext();

      expect(component['createTabsForCurrentSeason']).toHaveBeenCalled();
    });
  });

  describe('goToPrev', () => {
    beforeEach(() => {
      component.seasons = [allSeasons[0], allSeasons[0], allSeasons[0], allSeasons[0]];
      component.competitions = allCompetitions;
      component.seasonIndex = 1;
    });

    it('#goToPrev', fakeAsync(() => {
      component.goToPrev();
      tick();

      expect(component.seasonIndex).toEqual(0);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'widget',
        eventAction: 'league table',
        eventLabel: 'change season'
      }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
    }));

    it(`should run 'createTabsForCurrentSeason'`, () => {
      spyOn(component as any, 'createTabsForCurrentSeason');

      component.goToPrev();

      expect(component['createTabsForCurrentSeason']).toHaveBeenCalled();
    });
  });


  describe('#isNoEvents', () => {
    it('should return true', () => {
      component.result = null;
      const resilt = component.isNoEvents();

      expect(resilt).toEqual(true);
    });

    it('should return false', () => {
      component.result = {
        rows: []
      } as any;
      const resilt = component.isNoEvents();

      expect(resilt).toEqual(false);
    });
  });

  describe('#createTabsForCurrentSeason', () => {
    it(`should hide not actual competitiona in current season`, () => {
      component.seasons = [{ competitionIds: [] }] as any;
      component.competitions = [{ id: '1' }] as any;

      component['createTabsForCurrentSeason']();

      expect(component.competitions[0].hidden).toBeTruthy();
    });

    it(`should Not hide actual competitiona in current season`, () => {
      component.seasons = [{ competitionIds: ['1'] }] as any;
      component.competitions = [{ id: '1' }] as any;

      component['createTabsForCurrentSeason']();

      expect(component.competitions[0].hidden).toBeFalsy();
    });

    it(`should activate first competition if current season Not have actual 'competitionId'`, () => {
      component.competitionId = '2';
      component.seasons = [{ competitionIds: ['1'] }] as any;
      component.competitions = [{ id: '1' }, { id: '2' }] as any;

      component['createTabsForCurrentSeason']();

      expect(component.competitionId).toEqual('1');
      expect(component.activeTab).toEqual(component.competitions[0]);
    });

    it(`should hide parent competition and activate next competition id in season`, () => {
      component.seasons = [{ competitionIds: ['1','2'] }] as any;
      component.competitions = [{ id: '1', type: 'parent' }, {id: '2', type: 'child'}] as any;

      component['createTabsForCurrentSeason']();

      expect(component.competitions[0].hidden).toBeTruthy();
      expect(component.competitions[1].hidden).toBeFalsy();
      expect(component.activeTab).toEqual(component.competitions[1]);
    });
  });

  describe('showTabs', () => {
    it(`should return true if more than one competion has hidden false'`, () => {
      expect(component.showTabs([{hidden: true},{hidden: false},{hidden: false}] as any)).toBeTruthy();
    });

    it(`should return false if only one competition has hidden false`, () => {
      expect(component.showTabs([{hidden: true},{hidden: false}] as any)).toBeFalsy();
    });
  });

  describe('#getCurrentSeason', () => {
    it('should return current season', fakeAsync(() => {
      const results = {
        rows: {
          data: 'data'
        }
      };
      commandService.executeAsync.and.returnValue(Promise.resolve(results));
      component.competitionId = '1';
      component['getCurrentSeason']({
        areaId: 123,
        id: 123,
        sportId: 1
      } as any);
      tick();

      expect(commandService.executeAsync).toHaveBeenCalled();
    }));

    it('should return error for current season', () => {
      commandService.executeAsync.and.returnValue(Promise.reject('error'));
      component.competitionId = '1';
      component['getCurrentSeason']({
        areaId: 123,
        id: 123,
        sportId: 1
      } as any).subscribe(null, () => {
        expect(component.result).toEqual(null);
        expect(commandService.executeAsync).toHaveBeenCalled();
      });

    });
  });
  it('#setSeasonIndex', () => {
    const seasonsMock = [
      {
        id: '1',
        name: 'Premier League 16/17',
        areaId: '1',
        sportId: '1',
        startDate: '2016-08-13T00:00:00+02:00',
        endDate: '2017-05-25T23:59:00+02:00',
        year: '16/17',
        competitionIds: [
          '1'
        ]
      },
      {
        id: '2',
        name: 'Premier League 17/18',
        areaId: '1',
        sportId: '1',
        startDate: '2017-08-12T00:00:00+02:00',
        endDate: '2018-05-27T23:59:00+02:00',
        year: '17/18',
        competitionIds: [
          '1'
        ]
      },
      {
        id: '3',
        name: 'Premier League 18/19',
        areaId: '1',
        sportId: '1',
        startDate: '2018-08-11T00:00:00+02:00',
        endDate: '2019-05-13T23:59:00+02:00',
        year: '18/19',
        competitionIds: [
          '1'
        ]
      }
    ] as IAllSeasons[];

    component['setSeasonIndex'](seasonsMock);

    expect(component.seasonIndex).toEqual(2);
  });
});
