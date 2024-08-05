import { BybApiService } from '@yourcall/services/BYB/byb-api.service';
import { EMPTY } from 'rxjs';

describe('#BybApiService', () => {

  let service,
    cmsService;

  beforeEach(() => {
    cmsService = {
      getYourCallBybMarkets: jasmine.createSpy('getYourCallBybMarkets')
    };

    service = new BybApiService(
      cmsService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  describe('#extendParams', () => {
    it('should return requestParams', () => {
      expect(service['extendParams']([])).toEqual([]);
    });
  });

  describe('#getUri', () => {
    it('should return Uri', () => {
      const yourcallAPI = {
        path: 'path',
      };
      const result = service.getUri(yourcallAPI);
      expect(result).toEqual(`${service.uri}${yourcallAPI.path}`);
    });
  });

  describe('#getLeagues', () => {
    it('should return Uri', () => {
      const result = service.getLeagues();
      expect(result).toEqual( {
        path: '/v1/leagues'
      });
    });
  });

  describe('#calculateAccumulatorOdds', () => {
    it('should calculate Accumulator Odds', () => {
      const data = {
        path: '/v1/price',
        method: 'POST',
        params: {
          marketIds: '111',
          obEventId: 10 }
      };
      expect( service['calculateAccumulatorOdds'](data.params)).toEqual(data);
    });
  });

  describe('#getUpcomingLeagues', () => {
    it('should return UpcomingLeagues', () => {
      expect(service['getUpcomingLeagues']()).toEqual({
        path: '/v1/leagues-upcoming',
        params: {
          days: 6,
          tz: jasmine.any(Number) // time zone can be different
        }
      });
    });
  });

  describe('#getLeagueEvents', () => {
    it('should return League Events', () => {
      const period = {
        dateFrom: 'dateFrom',
        dateTo: 'dateTo'
      };
      const leagueIds = [1, 2, 3, 4];
      const yourcallAPI = {
        path: '/v1/events',
        params: { leagueIds, dateFrom: period.dateFrom, dateTo: period.dateTo}
      };
      expect(service['getLeagueEvents'](leagueIds, period)).toEqual(yourcallAPI);
    });
  });

  describe('#getGameInfo', () => {
    it('should return Game Info', () => {
      const obEventId = '12';
      const data = {
        path: `/v1/events/${obEventId}`
      };
      expect(service['getGameInfo'](obEventId)).toEqual(data);
    });
  });

  describe('#getEDPMarkets', () => {
    it('should return EDP Markets', () => {
      cmsService.getYourCallBybMarkets.and.returnValue(EMPTY);

      service.getEDPMarkets();
      expect(cmsService.getYourCallBybMarkets).toHaveBeenCalled();
    });
  });

  describe('#getMatchMarkets', () => {
    it('should return Game Info', () => {
      const event = {
        obEventId: 10
      }as any;
      const data = {
        path: `/v2/markets-grouped`,
        params: { obEventId: event.obEventId}
      };
      expect(service['getMatchMarkets'](event)).toEqual(data);
    });
  });

  describe('#getMarketSelections', () => {
    it('should return Market Selections', () => {
      const data = {
        path: `/v1/selections`,
        params: {
          marketIds: '111',
          obEventId: 10 }
        };
      expect(service['getMarketSelections'](data.params)).toEqual(data);
    });
  });

  describe('#getPlayers', () => {
    it('should return Players', () => {
      const data = {
        path: `/v1/players`,
        params: {
          obEventId: 10
        }
      };
      expect(service['getPlayers'](10)).toEqual(data);
    });
  });

  describe('#getLeagueEventsWithoutPeriod', () => {
    it('should return leagues', () => {
      const data = {
        path: `/v1/events`
      };
      expect(service['getLeagueEventsWithoutPeriod']()).toEqual(data);
    });
  });

  describe('#getStatistics', () => {
    it('should return Statistics', () => {
      const data = {
        path: `/v1/player-statistics`,
        params: {
          obEventId: '111',
          playerId: 10
        }
      };
      expect(service['getStatistics'](data.params)).toEqual(data);
    });
  });

  describe('#getStatValues', () => {
    it('should return Statistics Values', () => {
      const data = {
        path: `/v1/statistic-value-range`,
        params: {
          obEventId: '111',
          playerId: 10
        }
      };
      expect(service['getStatValues'](data.params)).toEqual(data);
    });
  });

  describe('#calculateOdds', () => {
    it('should calculate  Odds', () => {
      const data = {
        resolve: {
          data: {} }
      };
      expect(service['calculateOdds'](10)).toEqual(data);
    });
  });

  describe('#getBets', () => {
    it('should return Bets', () => {
      const data = {
        resolve: {
          data: []
        }
      };
      expect(service['getBets'](10)).toEqual(data);
    });
  });

  describe('#getGames', () => {
    it('should return Games', () => {
      const data = {
        resolve: {
          data: [] }
      };
      expect(service['getGames'](10)).toEqual(data);
    });
  });

  describe('#getMaxExposure', () => {
    it('should return Max Exposure', () => {
      const data = {
        resolve: {}
      };
      expect(service['getMaxExposure'](10)).toEqual(data);
    });
  });
});
