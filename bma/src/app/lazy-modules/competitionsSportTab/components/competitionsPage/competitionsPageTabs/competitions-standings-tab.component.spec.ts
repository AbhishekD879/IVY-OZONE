import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { CompetitionsStandingsTabComponent } from './competitions-standings-tab.component';
import { IStatsResults } from '@app/stats/models';
import { IStatsRow } from '@app/stats/models/row.model';

let allCompetitions;
let allSeasons;
let competitions;

describe('CompetitionsStandingsTabComponent', () => {
  let component: CompetitionsStandingsTabComponent;
  let commandService;
  let commandServiceResolveData;
  let pubSubService;

  beforeEach(() => {
    allCompetitions = [
      { name: 'name3', id: '203' },
      { name: 'competition, name1', id: '201' },
      { name: 'competition, name2', id: '202' }
    ];
    allSeasons = [
      { areaId: 403, competitionIds: ['201', '203'], id: '303', sportId: '103', year: '2020', name: '2019/2020' },
      { areaId: 401, competitionIds: ['201', '202'], id: '301', sportId: '101', year: '2019' },
      { areaId: 402, competitionIds: ['202', '203'], id: '302', sportId: '102', year: '19/20' },
      { areaId: 404, competitionIds: ['204', '205'], id: '304', sportId: '104', year: '20/21' }
    ];
    competitions = {
      allCompetitions,
      allSeasons,
      competitionId: 201,
      status: 'status',
      competitionName: 'competitionName'
    };
    commandServiceResolveData = {
      GET_LEAGUE_TABLE: Promise.resolve(competitions),
      GET_RESULT_TABLES: Promise.resolve([])
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.callFake(apiKey => commandServiceResolveData[apiKey]),
      API: {
        GET_LEAGUE_TABLE: 'GET_LEAGUE_TABLE',
        GET_RESULT_TABLES: 'GET_RESULT_TABLES'
      }
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    };
    spyOn(console, 'warn');

    component = new CompetitionsStandingsTabComponent(commandService, pubSubService);
  });

  it('create', () => {
    expect(component).toBeTruthy();
    expect(component.tableLimit).toEqual(5);
    expect(component.seasonIndex).toEqual(0);
    expect(component.showLimit).toEqual(false);
    expect(component.seasons).toEqual([]);
    expect(component.state.loading).toEqual(true);
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      component.typeId = 'typeId';
      component.classId = 'classId';
      component.seasonId = '301';
      component.sportId = 101;
      spyOn(component, 'showSpinner').and.callThrough();
      spyOn(component, 'hideSpinner').and.callThrough();
    });

    it('should show spinner and call executeAsync the GET_LEAGUE_TABLE command', fakeAsync(() => {
      component.ngOnInit();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'view league table' }]);
      expect(component.state.loading).toEqual(true);
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_LEAGUE_TABLE',
        [{ typeId: 'typeId', classId: 'classId', sportId: 101 }], {});
    }));

    it('should hide spinner on failure', fakeAsync(() => {
      commandServiceResolveData.GET_LEAGUE_TABLE = Promise.reject('error');
      component.ngOnInit();
      tick();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.state.loading).toEqual(false);
    }));
    it('should exit if no mapping found', fakeAsync(() => {
      competitions.status = 'Mapping not found';
      component.ngOnInit();
      tick();

      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.state.loading).toEqual(false);
      expect(component.competitionId).toBeUndefined();
      expect(component.competitions).toBeUndefined();
      expect(component.seasons).toEqual([]);
      expect(component.activeTab).toBeUndefined();
    }));

    it('should update component with filtered and sorted competitions and other properties', fakeAsync(() => {
      spyOn(component, 'filterCompetition').and.callThrough();
      component.ngOnInit();
      tick();

      expect(component.seasons).toEqual(allSeasons);
      expect(component.competitionId).toEqual('201');
      expect(component.competitionName).toEqual('competitionName');
      expect(component.filterCompetition).toHaveBeenCalledTimes(3);
      expect(component.competitions).toEqual([
        { title: 'competition  name1', name: 'competition, name1', id: '201', hidden: jasmine.any(Boolean) },
        { title: 'competition  name2', name: 'competition, name2', id: '202', hidden: jasmine.any(Boolean) },
        { title: 'name3', name: 'name3', id: '203', hidden: jasmine.any(Boolean) }
      ] as any);
    }));

    it('should only hide spinner when seasons are not available', fakeAsync(() => {
      competitions.allSeasons = [];
      component.ngOnInit();
      tick();
      expect(commandService.executeAsync.calls.allArgs()).toEqual([ ['GET_LEAGUE_TABLE',
        [{ typeId: 'typeId', classId: 'classId', sportId: 101 }], {}] ]);
      expect(component.competitionId).toEqual('201');
      expect(component.activeTab).toBeUndefined();
      expect(component.seasonIndex).toEqual(0);
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component.state.loading).toEqual(false);
    }));

    describe('when seasons are available', () => {
      it('should set seasonIndex value which corresponds to provided seasonId', fakeAsync(() => {
        component.ngOnInit();
        tick();
        expect(component.seasonIndex).toEqual(1);
      }));

      it('should set seasonIndex to 0 if seasons do not contain provided seasonId', fakeAsync(() => {
        component.seasonId = '305';
        component.ngOnInit();
        tick();
        expect(component.seasonIndex).toEqual(0);
      }));

      describe('should update tabs visibility for current season', () => {
        it('and hide competitions, which are not present in current season', fakeAsync(() => {
          // component.seasonId === '302' so allowed competitionIds are ['202', '203']
          component.seasonId = '302';
          component.ngOnInit();
          tick();
          expect(component.seasonIndex).toEqual(2);
          expect(component.competitions).toEqual([
            { title: 'competition  name1', name: 'competition, name1', id: '201', hidden: true },
            { title: 'competition  name2', name: 'competition, name2', id: '202', hidden: false },
            { title: 'name3', name: 'name3', id: '203', hidden: false }
          ] as any);
        }));

        it('and select first available competition tab if the initial was filtered out by competitionId', fakeAsync(() => {
          // component.seasonId === '302' so allowed competitionIds are ['202', '203']
          component.seasonId = '302';
          component.ngOnInit();
          tick();
          expect(component.activeTab).toEqual({ title: 'competition  name2', name: 'competition, name2', id: '202', hidden: false } as any);
          expect(component.competitionId).toEqual('202');
        }));

        it('and select competition tab by initial competitionId if it is available', fakeAsync(() => {
          // component.seasonId === '301' so allowed competitionIds are ['201', '202']
          component.ngOnInit();
          tick();
          expect(component.activeTab).toEqual({ title: 'competition  name1', name: 'competition, name1', id: '201', hidden: false } as any);
          expect(component.competitionId).toEqual('201');
          expect(component.competitions).toEqual([
            { title: 'competition  name1', name: 'competition, name1', id: '201', hidden: false },
            { title: 'competition  name2', name: 'competition, name2', id: '202', hidden: false },
            { title: 'name3', name: 'name3', id: '203', hidden: true }
          ] as any);
        }));

        it('reset tab settings if no competition is available', fakeAsync(() => {
          // component.seasonId === '304' so allowed competitionIds are ['204', '205']
          component.seasonId = '304';
          component.ngOnInit();
          tick();
          expect(component.activeTab).toEqual(undefined);
          expect(component.competitionId).toEqual(undefined);
          expect(component.competitions).toEqual([
            { title: 'competition  name1', name: 'competition, name1', id: '201', hidden: true },
            { title: 'competition  name2', name: 'competition, name2', id: '202', hidden: true },
            { title: 'name3', name: 'name3', id: '203', hidden: true }
          ] as any);
        }));
      });

      describe('it should getCurrentSeason', () => {
        it('and hide spinner on success', fakeAsync(() => {
          component.ngOnInit();
          tick();
          expect(commandService.executeAsync.calls.allArgs()).toEqual([
            ['GET_LEAGUE_TABLE', [{ typeId: 'typeId', classId: 'classId', sportId: 101 }], {}],
            ['GET_RESULT_TABLES', [{ areaId: 401, competitionId: '201', seasonId: '301', sportId: '101' }], []]
          ]);
          expect(component.hideSpinner).toHaveBeenCalled();
          expect(component.state.loading).toEqual(false);
        }));
        it('and hide spinner on failure', fakeAsync(() => {
          commandServiceResolveData.GET_RESULT_TABLES = Promise.reject('error');
          component.ngOnInit();
          tick();
          expect(component.hideSpinner).toHaveBeenCalled();
          expect(component.state.loading).toEqual(false);
        }));
      });
    });
  });

  it('#trackById', () => {
    const result = component.trackById(1, {
      id: 'id'
    } as any);
    expect(result).toEqual('1_id');
  });

  it('#changeGroup', () => {
    component['getCurrentSeason'] = jasmine.createSpy('getCurrentSeason').and.returnValue(observableOf([]));
    component.seasons = [allSeasons[0]];
    component.changeGroup({ tab: { id: '1', areaId: '123' } } as any);
    expect(component.activeTab).toEqual({ id: '1', areaId: '123' } as any);
    expect(component['getCurrentSeason']).toHaveBeenCalledWith(allSeasons[0]);
    expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
      eventCategory: 'football', eventAction: 'league table', eventLabel: 'change league' }]);
  });

  describe('filterCompetition', () => {
    it('should return False if competition name has any excluded substring', () => {
      const strings = ['Playoff', 'KnockOut', 'Qualification', 'Preliminary Round'];
      expect(strings.some(s => component.filterCompetition({ name: `name, ${s}` } as any))).toBeFalsy();
    });

    it('should return True if competition name has excluded substring', () => {
      expect(component.filterCompetition({ name: 'name' } as any)).toBeTruthy();
    });

    it('should set the title of the competition', () => {
      const c1 = { name: ' name  ' } as any,
        c2 = { name: '  competition  , name  ' } as any,
        c3 = { name: ' competition , knockout' } as any;
      expect(component.filterCompetition(c1)).toBeTruthy();
      expect(component.filterCompetition(c2)).toBeTruthy();
      expect(component.filterCompetition(c3)).toBeFalsy();
      expect(c1.title).toEqual(c1.name.split(',').join(' ').trim());
      expect(c2.title).toEqual(c2.name.split(',').join(' ').trim());
      expect(c3.title).toEqual(c3.name.split(',').join(' ').trim());
    });
  });

  describe('goToNext', () => {
    beforeEach(() => {
      component.seasons = [allSeasons[0], allSeasons[0], allSeasons[0], allSeasons[0]];
      component.competitions = allCompetitions;
    });

    it('#goToNext', fakeAsync(() => {
      spyOn(component, 'showSpinner');
      spyOn(component, 'hideSpinner');
      component['handleDefaultError'] = jasmine.createSpy();
      component.goToNext();
      tick();

      expect(component.seasonIndex).toEqual(1);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'change season' }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component['handleDefaultError']).not.toHaveBeenCalled();
    }));

    it('#goToNext negative case', fakeAsync(() => {
      spyOn(component, 'showSpinner');
      spyOn(component, 'hideSpinner');
      component['handleDefaultError'] = jasmine.createSpy();
      commandServiceResolveData.GET_RESULT_TABLES = Promise.reject('error');
      component.goToNext();
      tick();

      expect(component.seasonIndex).toEqual(1);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'change season' }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.hideSpinner).not.toHaveBeenCalled();
      expect(component['handleDefaultError']).toHaveBeenCalled();
    }));

    it('#goToNext should not go to next table when seasonIndex is bigger then amount of seasons', () => {
      component.seasonIndex = 10;
      component.goToNext();

      expect(pubSubService.publish).not.toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'change season' }]);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

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
      spyOn(component, 'showSpinner');
      spyOn(component, 'hideSpinner');
      component['handleDefaultError'] = jasmine.createSpy();
      component.goToPrev();
      tick();

      expect(component.seasonIndex).toEqual(0);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football',
        eventAction: 'league table',
        eventLabel: 'change season'
      }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(component['handleDefaultError']).not.toHaveBeenCalled();
    }));

    it('#goToPrev negative case', fakeAsync(() => {
      spyOn(component, 'showSpinner');
      spyOn(component, 'hideSpinner');
      component['handleDefaultError'] = jasmine.createSpy();
      commandServiceResolveData.GET_RESULT_TABLES = Promise.reject('error');
      component.goToPrev();
      tick();

      expect(component.seasonIndex).toEqual(0);
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football',
        eventAction: 'league table',
        eventLabel: 'change season'
      }]);
      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.hideSpinner).not.toHaveBeenCalled();
      expect(component['handleDefaultError']).toHaveBeenCalled();
    }));

    it('#goToPrev should not go to prev table when seasonIndex is a negative number', () => {
      component.seasonIndex = -1;
      component.goToPrev();

      expect(pubSubService.publish).not.toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football',
        eventAction: 'league table',
        eventLabel: 'change season'
      }]);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    it(`should run 'createTabsForCurrentSeason'`, () => {
      spyOn(component as any, 'createTabsForCurrentSeason');

      component.goToPrev();

      expect(component['createTabsForCurrentSeason']).toHaveBeenCalled();
    });
  });


  describe('#isNoEvents', () => {
    it('should return true', () => {
      component.result = null;
      const result = component.isNoEvents();

      expect(result).toEqual(true);
    });

    it('should return false', () => {
      component.result = {
        rows: []
      } as any;
      component.seasons = [ 1 ] as any;
      const result = component.isNoEvents();

      expect(result).toEqual(false);
    });

    it('should return true', () => {
      component.result = {} as IStatsResults;
      component.seasons = [];
      const result = component.isNoEvents();

      expect(result).toEqual(true);
    });
  });

  describe('#createTabsForCurrentSeason', () => {
    it(`should hide not actual competitions in current season`, () => {
      component.seasons = [{ competitionIds: [] }] as any;
      component.competitions = [{ id: '1' }] as any;

      component['createTabsForCurrentSeason']();
      expect(component.competitions[0].hidden).toBeTruthy();
    });

    it(`should Not hide actual competitiona in current season`, () => {
      component.seasons = [{ competitionIds: ['1'] }] as any;
      component.competitions = [{ id: '1', hidden: true }] as any;

      component['createTabsForCurrentSeason']();
      expect(component.competitions[0].hidden).toBeFalsy();
    });

    it(`should activate first competition if current season Not have actual 'competitionId'`, () => {
      component.competitionId = '2';
      component.seasons = [{ competitionIds: ['1'] }] as any;
      component.competitions = [{ id: '1' }, { id: '2' }] as any;

      component['createTabsForCurrentSeason']();
      expect(component.competitionId).toEqual('1');
      expect(component.competitions[0].hidden).toBeFalsy();
      expect(component.competitions[1].hidden).toBeTruthy();
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

  it('getTableValue should return list item value by key', () => {
    const list = [{ key: 'k1', value: 'v1'}, { key: 'k2', value: 'v2'}, { key: 'k3', value: 'v3'}];
    expect(component.getTableValue(list, 'k2')).toEqual('v2');
    expect(component.getTableValue(list, 'k4')).toEqual(undefined);
  });

  describe('limitRows', () => {
    const rows = [{ id: '1' }, { id: '2' }, { id: '3' }, { id: '4' }, { id: '5' }] as IStatsRow[];

    beforeEach(() => {
      component.result = { rows } as IStatsResults;
      component.tableLimit = 3;
    });

    it('should keep tabledata if no limitation required', () => {
      component.showLimit = false;
      component.limitRows();
      expect(component.tableData).toEqual(rows);
    });

    it('should truncate tabledata to defined limit if required', () => {
      component.showLimit = true;
      component.limitRows();
      expect(component.tableData).toEqual([{ id: '1' }, { id: '2' }, { id: '3' }] as IStatsRow[]);
    });

    it('should return undefined if no rows defined', () => {
      component.result = undefined;
      component.limitRows();
      expect(component.tableData).toEqual(undefined);
    });
  });

  describe('sendCollapseGTM', () => {
    it('should do nothing if not first time collapsed', () => {
      component['isFirstTimeCollapsed'] = true;
      component.sendCollapseGTM();
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(component['isFirstTimeCollapsed']).toEqual(true);
    });
    it('should send tracking data for the first time collapsed', () => {
      component['isFirstTimeCollapsed'] = false;
      component.sendCollapseGTM();
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'collapse' }]);
    });
  });

  describe('showAll', () => {
    it('should invert showLimit value', () => {
      component.showLimit = false;
      component.showAll();
      expect(component.showLimit).toEqual(true);
      component.showLimit = true;
      component.showAll();
      expect(component.showLimit).toEqual(false);
    });

    it('should limit rows', () => {
      spyOn(component, 'limitRows');
      component.showAll();
      expect(component.limitRows).toHaveBeenCalled();
    });

    it('should not track action if showAll has been clicked already', () => {
      component['isShowAllClicked'] = true;
      component.showAll();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should track action if showAll has not been clicked already', () => {
      component['isShowAllClicked'] = false;
      component.showAll();
      expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
        eventCategory: 'football', eventAction: 'league table', eventLabel: 'show full table' }]);
      expect(component['isShowAllClicked']).toEqual(true);
    });
  });

  describe('#getCurrentSeason', () => {
    it('should return current season', fakeAsync(() => {
      const results = {
        rows: {
          data: 'data'
        },
        competitionId: 1
      };
      commandService.executeAsync.and.returnValue(Promise.resolve(results));
      component.competitionId = '1';
      component['getCurrentSeason']({
        areaId: 123,
        id: 123,
        sportId: 1,
        year: '19/20'
      } as any);
      tick();

      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.competitionYear).toEqual('2019/20');
    }));

    it('should return error for current season if parameters are not correct', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.resolve({}));
      component.competitionId = '1';
      component['getCurrentSeason']({} as any);
      tick();

      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(component.competitionYear).toEqual(undefined);
    }));

    it('should return error for current season', () => {
      commandService.executeAsync.and.returnValue(Promise.reject('error'));
      component.competitionId = '1';
      component['getCurrentSeason']({
        areaId: 123,
        id: 123,
        sportId: 1,
        year: '2019'
      } as any).subscribe(null, () => {
        expect(component.result).toEqual(null);
        expect(commandService.executeAsync).toHaveBeenCalled();
      });
      expect(component.competitionYear).toEqual('2019');
    });

    it('should return error for current season if competitionId is undefined', () => {
      component.competitionId = undefined;
      component['getCurrentSeason']({
        areaId: 123,
        id: 123,
        sportId: 1,
        year: '2019'
      } as any).subscribe(null, error => {
        expect(component.result).toEqual(null);
        expect(error).toEqual('competitionId is undefined');
      });

    });
  });

  describe('#getTableTitle', () => {
    it('should return table title', () => {
      component.seasons = allSeasons;
      component.seasonIndex = 0;
      const actualResult = component['getTableTitle']();

      expect(actualResult).toEqual('2019/2020');
    });

    it('should not return table title if no seasons were found', () => {
      component.seasonIndex = 0;
      component.seasons = [];
      const actualResult = component['getTableTitle']();

      expect(actualResult).toEqual(undefined);
    });

    it('should not return table title if seasons is unavailable', () => {
      component.seasonIndex = 0;
      component.seasons = undefined;
      const actualResult = component['getTableTitle']();

      expect(actualResult).toEqual(undefined);
    });
  });
});
