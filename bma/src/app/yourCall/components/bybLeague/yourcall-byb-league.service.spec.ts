import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { YourcallBybLeagueService } from './yourcall-byb-league.service';

describe('YourcallBybLeagueService', () => {
  let service: YourcallBybLeagueService;
  let yourcallProviderService;
  let timeService;
  let routingHelperService;
  let filterService;
  let sportsConfigHelperService;

  beforeEach(() => {
    yourcallProviderService = {
      useOnce: jasmine.createSpy('useOnce').and.returnValue({
        getLeagueEvents: jasmine.createSpy('getLeagueEvents').and.returnValue(Promise.resolve({
          data: {
            homeTeam: {
              id: 'id1'
            },
            visitingTeam: {
              id: 'id2'
            },
            status: '1',
            hasPlayerProps: false
          }
        }))
      })
    };
    timeService = {
      dateTimeOfDayInISO: jasmine.createSpy().and.returnValue('today')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    filterService = {
      clearEventName: jasmine.createSpy('clearEventName').and.returnValue('team1 vs team2')
    };
    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(of(''))
    };

    service = new YourcallBybLeagueService(
      yourcallProviderService,
      timeService,
      routingHelperService,
      filterService,
      sportsConfigHelperService
    );
  });

  it('getEventPath', fakeAsync(() => {
    service['getEventPath']({} as any, {} as any).subscribe();
    tick();
    expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
  }));

  describe('#getTeamName', () => {
    it('should get empty string', () => {
      filterService.clearEventName = jasmine.createSpy('clearEventName').and.returnValue('team1');
      const res = service.getTeamName('', 1);

      expect(res).toEqual('');
    });

    it('should get Team Name', () => {
      const res = service.getTeamName('team1 vs team2', 0);

      expect(res).toEqual('team1');
    });

    it('case when we have arr of title but invalide index', () => {
      const res = service.getTeamName('team1 vs team2', 4);

      expect(res).toEqual('');
    });
  });

  describe('#getInterval', () => {
    it('should get Interval', () => {
     const filter = 'today';

     const res = service.getInterval(filter);
     expect(res).toEqual({
       dateFrom: 'today',
       dateTo: 'today'
      });
    });

    it('should get Interval', () => {
      const filter = 'tomorrow';
      timeService.dateTimeOfDayInISO = jasmine.createSpy().and.returnValue('tomorrow');
      const res = service.getInterval(filter);

      expect(res).toEqual({
        dateFrom: 'tomorrow',
        dateTo: 'tomorrow'
      });
    });
  });

  describe('#parse', () => {
    it('should parse events data', () => {
      const events = [{
        date: '1eee1',
        title: 'test',
        homeTeam: {
          title: 'home'
        },
        visitingTeam: {
          title: 'visiting'
        }
      }, {
        date: '1new',
        title: 'test',
        homeTeam: {
          title: 'home'
        },
        visitingTeam: {
          title: 'visiting'
        }
      }] as any;

      const res = service.parse(events);
      expect(res).toEqual([
        { date: '1eee1',
          title: 'test',
          id: undefined,
          homeTeam: {
            title: 'home'
          },
          visitingTeam: {
            title: 'visiting'
          },
          teamHome: 'team1',
          teamAway: 'team2'
        }, {
          date: '1new',
          title: 'test',
          id: undefined,
          homeTeam: {
            title: 'home'
          },
          visitingTeam: {
            title: 'visiting'
          },
          teamHome: 'team1',
          teamAway: 'team2'
        }] as any);
    });

    it('should parse events data and check get team', () => {
      filterService.clearEventName = jasmine.createSpy('clearEventName').and.returnValue('');
      const events = [{
        date: '1eee1',
        title: 'test',
        homeTeam: {
          title: 'home'
        },
        visitingTeam: {
          title: 'visiting'
        }
      },
        {
          date: '1eee1',
          title: 'test',
          homeTeam: {
            title: 'home'
          },
          visitingTeam: {
            title: 'visiting'
          }
        }] as any;

      const res = service.parse(events);
      expect(res).toEqual([
        { date: '1eee1',
          title: 'test',
          id: undefined,
          homeTeam: {
            title: 'home'
          },
          visitingTeam: {
            title: 'visiting'
          },
          teamHome: 'home',
          teamAway: 'visiting'
        },
        { date: '1eee1',
          title: 'test',
          id: undefined,
          homeTeam: {
            title: 'home'
          },
          visitingTeam: {
            title: 'visiting'
          },
          teamHome: 'home',
          teamAway: 'visiting'
        }] as any);
    });
  });

  describe('#getLeagueEvents', () => {
    it('Should return response data', () => {
      const league = {
          obTypeId: 345
        } as any,
        filter = {} as any;

      service.getLeagueEvents(league, filter).then(response => {
        expect(response).toEqual({
          homeTeam: {
            id: 'id1'
          },
          visitingTeam: {
            id: 'id2'
          },
          status: '1',
          hasPlayerProps: false
        } as any);
      });
    });

    it('Should return error', fakeAsync( () => {
      yourcallProviderService.useOnce = jasmine.createSpy('useOnce').and.returnValue({
          getLeagueEvents: jasmine.createSpy('getLeagueEvents').and.returnValue(Promise.reject('error'))
        });

      const league = {} as any,
            filter = {} as any;
      service.getLeagueEvents(league, filter);
      tick();

      service.getLeagueEvents(league, filter).then(response => {
        expect(response).toEqual( [] as any);
      });
    }));
  });
});
