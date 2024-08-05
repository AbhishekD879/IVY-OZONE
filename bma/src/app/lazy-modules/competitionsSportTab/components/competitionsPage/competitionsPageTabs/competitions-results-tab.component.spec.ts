import {
  CompetitionsResultsTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitionsPageTabs/competitions-results-tab.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('#CompetitionsResultsTabComponent', () => {
  let component: CompetitionsResultsTabComponent,
    commandService,
    matchesData,
    matches;

  beforeEach(() => {
    matchesData = [{
      id: '15511538',
      date: 1544644800000,
      teamA: { name: 'teamA' },
      teamB: { name: 'teamB' }
    }];

    matches = { '12 Dec 2018': matchesData };

    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(new Promise(null)),
      API: { GET_MATCHES_BY_SEASON: 'GET_MATCHES_BY_SEASON' }
    };
    spyOn(console, 'warn');

    component = new CompetitionsResultsTabComponent(commandService);
  });

  it('constructor', () => {
    expect(component.isSpinnerVisible).toEqual(false);
    expect(component.isShowMoreAvailable).toEqual(false);
    expect(component.results).toEqual([] as any);
  });

  it('@ngOnInit', () => {
    spyOn(component, 'loadResultsData');
    component.ngOnInit();
    expect(component.loadResultsData).toHaveBeenCalled();
  });

  describe('@loadResultsData', () => {
    beforeEach(() => {
      spyOn(component, 'extendResultsData');
      component.seasonId = 'seasonId';
    });

    describe('should load limited portion of results and', () => {
      beforeEach(() => {
        commandService.executeAsync.and.returnValue(Promise.resolve({ showButton: true, matches: { matchId: [] } }));
      });

      it('should update results data', fakeAsync(() => {
        component.loadResultsData();
        expect(component.isSpinnerVisible).toEqual(true);
        tick();
        expect(component.isShowMoreAvailable).toEqual(true);
        expect(component.extendResultsData).toHaveBeenCalledWith({ matchId: [] });
        expect(component.isSpinnerVisible).toEqual(false);
      }));

      it('should load next portion of results on consecutive call', fakeAsync(() => {
        component.loadResultsData();

        expect(component.isSpinnerVisible).toBeTruthy();
        expect(component.isLoadingMore).toBeFalsy();
        tick();
        expect(component.isSpinnerVisible).toBeFalsy();

        component.loadResultsData(true);
        expect(component.isLoadingMore).toBeTruthy();

        tick();
        expect(component.isLoadingMore).toBeFalsy();

        component.loadResultsData(true);
        expect(component.isLoadingMore).toBeTruthy();
        tick();

        expect(commandService.executeAsync.calls.allArgs()).toEqual([
          ['GET_MATCHES_BY_SEASON', ['seasonId', 0, 8], {}],
          ['GET_MATCHES_BY_SEASON', ['seasonId', 7, 8], {}],
          ['GET_MATCHES_BY_SEASON', ['seasonId', 14, 8], {}]
        ]);
        expect(component.isSpinnerVisible).toBeFalsy();
        expect(component.isLoadingMore).toBeFalsy();
      }));
    });

    it('shouldn`t load results on error', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.reject({ error: 'error' }));
      component.loadResultsData();
      expect(component.isSpinnerVisible).toBeTruthy();
      tick();
      expect(component.isSpinnerVisible).toBeFalsy();
    }));

    it('shouldn`t load results on error when show more', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.reject('error'));
      component.loadResultsData(true);
      expect(component.isLoadingMore).toBeTruthy();
      tick();
      expect(component.isLoadingMore).toBeFalsy();
    }));

    it('shouldn`t load results if no seasonId is provided', () => {
      component.seasonId = '';
      component.loadResultsData();

      expect(commandService.executeAsync).not.toHaveBeenCalled();
      expect(component.isSpinnerVisible).toEqual(false);
      expect(component.results).toEqual([]);
    });
  });

  describe('@extendResultsData', () => {
    it('should extendResultsData', () => {
      component.extendResultsData(matches);
      expect(component.results).toEqual([{ matches: matchesData, title: '12 Dec 2018' }]);
    });

    it('should extendResultsData if data exist', () => {
      component.results = [{ matches: matchesData, title: '12 Dec 2018' }];
      component.extendResultsData(matches);
      expect(component.results).toEqual([{ matches: [matchesData[0], matchesData[0]], title: '12 Dec 2018' }]);
    });
  });

  describe('@sortResultsData', () => {
    it('should extendResultsData', () => {
      matchesData[1] = {
        id: '25511538',
        date: 1544666800000,
        teamA: { name: 'teamA2' },
        teamB: { name: 'teamB2' }
      };
      expect(component.sortResultsData(matchesData)).toEqual([matchesData[1], matchesData[0]]);
    });
  });
});
