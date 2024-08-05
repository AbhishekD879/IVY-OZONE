import { BetFinderHelperService } from './bet-finder-helper.service';
import environment from '@environment/oxygenEnvConfig';
import { of as observableOf, throwError } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';

describe('BetFinderHelperService', () => {
  let service: BetFinderHelperService;

  let storageService;
  let fracToDecService;
  let http;
  let userService;

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy().and.returnValue(null)
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy().and.returnValue(1.2)
    };
    userService = {
      username: 'M8sha',
      bppToken: 'token'
    };
    http = {
      get: jasmine.createSpy().and.returnValue(observableOf({
        body: {
          cypher: {
            meetings: [{
              courseShort: '',
              course: ''
            }],
            runners: [{
              raceId: '',
              horseId: '',
              raceDate: '',
              time: '',
              dayValue: '',
              course: '',
              courseShort: '',
              horseName: '',
              starRating: '',
              odds: '1/3',
              oddsLength: '',
              trainerForm: '',
              jockeyAbility: '',
              wellHandicapped: '',
              marketMover: '',
              courseWinner: '',
              distanceWinner: '',
              courseDistanceWinner: '',
              winnerLastTime: '',
              winnerLast3Starts: '',
              placedLastTime: '',
              placedLast3Starts: '',
              beatenFavLastTime: '',
              firstTimeHeadGear: '',
              headGear: '',
              provenGoing: '',
              provenDistance: '',
              form: '',
              potential: '',
              draw: '',
              horseToFollow: '',
              supercomputerSelection: '',
              attitude: '',
              jumping: '',
              fitness: '',
              improver: '',
              firstTimeOut: '',
              firstRunAfterWindOp: '',
              vibe: '',
              jockeyName: '',
              jockeyAliasName: '',
              trainerName: '',
              trainerAliasName: '',
              bookmakerEventId: '',
              bookmakerCompetitorId: '',
              silkID: '',
              number: '',
              formString: '',
              decimalOdds: 1.2,
              odds32: '',
              odds16: '',
              odds4: '',
              odds1: '',
              odds8: '',
              odds0: '',
            }]
          }
        }
      })),
      post: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    service = new BetFinderHelperService(
      storageService,
      fracToDecService,
      http,
      userService
    );
  });

  it('constructor', () => {
    expect(service.BET_FINDER_ENDPOINT).toEqual(environment.BET_FINDER_ENDPOINT);
  });

  it('setFilters', () => {
    service.setFilters({});
    expect(service.savedFilters).toEqual({});
  });

  it('getRacesList should return empty array when empty object or wrong data structure in response', () => {
    http.get.and.returnValue(observableOf({}));
    service.getRacesList().subscribe(res => {
      expect(res).toEqual([]);
    });
  });

  describe('getRunners', () => {
    beforeEach(() => {
      spyOn(service as any, 'getMeeting').and.callThrough();
      spyOn(service, 'filterRunners').and.callThrough();
    });

    it('should get meetings and filter runners', fakeAsync(() => {
      service.savedFilters = null;
      service.getRunners().subscribe();
      tick();
      expect(http.get).toHaveBeenCalledWith(environment.BET_FINDER_ENDPOINT, { observe: 'response' });
      expect(service['getMeeting']).toHaveBeenCalledTimes(1);
      expect(service['filterRunners']).toHaveBeenCalledTimes(1);
    }));

    it('should not get meetings and not filter runners', fakeAsync(() => {
      http.get.and.returnValue(throwError(null));
      service.getRunners().subscribe({ error: () => {} });
      tick();
      expect(service['getMeeting']).not.toHaveBeenCalled();
      expect(service['filterRunners']).not.toHaveBeenCalled();
    }));
  });

  describe('setOddsRange', () => {
    let runner;

    beforeEach(() => {
      runner = {};
    });

    it('should set odds0', () => {
      runner.decimalOdds = 1;
      service['setOddsRange'](runner);
      expect(runner.odds0).toBe('Y');
    });

    it('should set odds1', () => {
      runner.decimalOdds = 3;
      service['setOddsRange'](runner);
      expect(runner.odds1).toBe('Y');
    });

    it('should set odds4', () => {
      runner.decimalOdds = 5;
      service['setOddsRange'](runner);
      expect(runner.odds4).toBe('Y');
    });

    it('should set odds8', () => {
      runner.decimalOdds = 10;
      service['setOddsRange'](runner);
      expect(runner.odds8).toBe('Y');
    });

    it('should set odds16', () => {
      runner.decimalOdds = 20;
      service['setOddsRange'](runner);
      expect(runner.odds16).toBe('Y');
    });

    it('should set odds32', () => {
      runner.decimalOdds = 30;
      service['setOddsRange'](runner);
      expect(runner.odds32).toBe('Y');
    });
  });

  it('parseOdds', () => {
    const res = <any>{
      cypher: {
        runners: [
          {
            odds: ''
          }
        ]
      }
    };
    service['parseOdds'](res);
    expect(res.cypher.runners[0].decimalOdds).toEqual(0);

    res.cypher.runners[0].odds = '1/2';
    service['parseOdds'](res);
    expect(res.cypher.runners[0].decimalOdds).toEqual(1.2);
  });

  describe('filterByStars', () => {
    it('should return true (no star selection)', () => {
      expect(service['filterByStars']({} as any, null)).toBeTruthy();
    });

    it('should return true (star rating same as star selection)', () => {
      expect(service['filterByStars']({ starRating: '1' } as any, 1)).toBeTruthy();
    });

    it('should return false (star rating different than star selection)', () => {
      expect(service['filterByStars']({ starRating: '2' } as any, 1)).toBeFalsy();
    });
  });

  describe('filterByButton', () => {
    it('should return true', () => {
      expect( service['filterByButton']({} as any, 'btn', { btn: false } as any) ).toBeTruthy();
    });

    it('should return false', () => {
      expect( service['filterByButton']({ btn: 'N' } as any, 'btn', { btn: true } as any) ).toBeFalsy();
    });
  });

  describe('filterBySuperComputer', () => {
    it('should return true', () => {
      expect(service['filterBySuperComputer']('', {})).toBeTruthy();
    });

    it('should return false', () => {
      expect(service['filterBySuperComputer']('E', { eachWaySupercomputer: true } as any)).toBeTruthy();
    });
  });

  describe('filterByMeeting', () => {
    it('should return true', () => {
      expect(service['filterByMeeting']({} as any, 'All')).toBeTruthy();
    });

    it('should return false', () => {
      expect(service['filterByMeeting']({ courseShort: '1' } as any, '')).toBeFalsy();
    });
  });

  describe('filterByName', () => {
    let runner;

    beforeEach(() => {
      runner = { horseName: '', jockeyName: '', trainerName: '' };
    });

    it('should return true (no name)', () => {
      expect(service['filterByName'](runner, '')).toBeTruthy();
    });

    it('should return true (horse name match)', () => {
      runner.horseName = 'horse';
      expect(service['filterByName'](runner, 'horse')).toBeTruthy();
    });

    it('should return true (jockey name match)', () => {
      runner.jockeyName = 'jockey';
      expect(service['filterByName'](runner, 'jockey')).toBeTruthy();
    });

    it('should return true (trainer name match)', () => {
      runner.trainerName = 'trainer';
      expect(service['filterByName'](runner, 'trainer')).toBeTruthy();
    });

    it('should return false', () => {
      expect(service['filterByName'](runner, 'name')).toBeFalsy();
    });
  });

  describe('filterByPriceButtons', () => {
    it('should return true', () => {
      expect(service['filterByPriceButtons']({} as any, {})).toBeTruthy();
    });

    it('should return true', () => {
      expect(
        service['filterByPriceButtons']({ odds0: 'Y' } as any, { odds0: true } as any)
      ).toBeTruthy();
    });
  });

  describe('getContestIdsForFiveASideBets', () => {
    it('getContestIdsForFiveASideBets', () => {
      const userName = 'M8sha';
      const bppToken = 'token';
      const betIds = ["12345", "23423432"];
      const BRAND = environment.brand;
      const params = {
        userId: userName,
        token: bppToken,
        betIds: betIds,
        brand: BRAND
      };
      service.getContestIdsForFiveASideBets(betIds).subscribe();
      expect(http.post).toHaveBeenCalledWith(
        `${environment.SHOWDOWN_MS}/${BRAND}/mybets-widget`, params, Object({ observe: 'response' }));
    });
  });

});
