import { ScorecastService } from '@edp/components/markets/scorecast/scorecast.service';

describe('ScorecastService', () => {
  let service;

  const scoreMarketService: any = {
    getMaxScoreValues: jasmine.createSpy('getMaxScoreValues')
  };
  const isPropertyAvailableService: any = {};
  const cashOutLabelService: any = {};
  const gtmService: any = {
    push: jasmine.createSpy('push')
  };
  
  beforeEach(() => {
    service = new ScorecastService(
      scoreMarketService,
      isPropertyAvailableService,
      cashOutLabelService,
      gtmService
    );
  });

  it('should test getOutcomeCombinations', () => {
    const scorecastsMock = [
      {
        scorerOutcomeId: '1111',
        scorecastPrices: '10,20,30,40,50'
      },
      {
        scorerOutcomeId: '22222',
        scorecastPrices: '10,20,30,40,50'
      }
    ];
    const expectedScorecastsCompinationsResult = {
      10: ['10', '20', '30', '40']
    };
    const goalscorerOutcomeIdMock = '1111';
    const result = service['getOutcomeCombinations'](scorecastsMock, goalscorerOutcomeIdMock);

    expect(result).toEqual(expectedScorecastsCompinationsResult);
  });

  it('should test getOutcomeCombinations with no Id matched', () => {
    const scorecastsMock = [
      {
        scorerOutcomeId: '1111',
        scorecastPrices: '10,20,30,40,50'
      }
    ];
    const goalscorerOutcomeIdMock = '22222';
    const result = service['getOutcomeCombinations'](scorecastsMock, goalscorerOutcomeIdMock);

    expect(result).toEqual({});
  });

  it('getMaxScoreValues', () => {
    service.getMaxScoreValues([]);
    expect(scoreMarketService.getMaxScoreValues).toHaveBeenCalled();
  });

  describe('getCombinedOutcome', ()  => {
    const teams =  {
      teamA: {
        name: 'teamA',
        score: 23,
      },
      teamH: {
        name: 'teamB',
        score: 23,
      },
    };
    it('should call scoreMarketService getCombinedOutcome', function () {
      const outComes = {
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 213,
        displayOrder: 11,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        isUS: true,
        liveServChannels: 'liveServChannels',
        liveServChildrenChannels: 'liveServChildrenChannels',
        name: 'liveServChildrenChannels',
        outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
        outcomeMeaningMinorCode: 1123,
        outcomeStatusCode: 'outcomeMeaningMinorCode'
      };
      scoreMarketService['getCombinedOutcome'] = jasmine.createSpy('getCombinedOutcome');
      service.getCombinedOutcome(teams, outComes);
      expect(scoreMarketService.getCombinedOutcome).toHaveBeenCalled();
    });
  });

  describe('isAnyCashoutAvailable', ()  => {
    it('should call isPropertyAvailableService', function () {

      scoreMarketService['getCombinedOutcome'] = jasmine.createSpy('getCombinedOutcome');
      cashOutLabelService['checkCondition'] = jasmine.createSpy('checkCondition');
      isPropertyAvailableService['isPropertyAvailable'] = jasmine.createSpy('isPropertyAvailable').and.callFake((cb) => {
        return true;
      });
      const result = service['isAnyCashoutAvailable'];
      expect(result).toBe(true);
    });
  });

  describe('getTeams', () => {
    it('should call isPropertyAvailableService', function () {
      const marketEntity = {
        outcomes: {
          filter: jasmine.createSpy().and.callFake((p1) => {
            return {
              correctPriceType: 'correctPriceType',
              correctedOutcomeMeaningMinorCode: 111,
              displayOrder: 1223,
              fakeOutcome: true,
              icon: true
            };
          })
        }
      };
      scoreMarketService['getTeams'] = jasmine.createSpy('checkCondition').and.returnValue(marketEntity);

      const result = service['getTeams']();
      expect(result).toEqual(marketEntity);
    });
  });
  describe('getMarketOutcomesByTeam', () => {
    it('should call true', function () {
      const teamsArray = [{
        name: 'testName',
        outcomeMeaningMinorCode: 111
      }];
      const marketEntity = {
        outcomes: [{
          correctPriceType: 'correctPriceType',
          correctedOutcomeMeaningMinorCode: 111,
          outcomeMeaningMinorCode: 111,
          displayOrder: 1223,
          fakeOutcome: true,
          icon: true
        }]
      };

      const result = service['getMarketOutcomesByTeam'](teamsArray, marketEntity);
      expect(result).toEqual({testName: marketEntity.outcomes});
    });
  });

  describe('getCombinedOutcomePrices', () => {
    it('should return null', function () {

      const scoreCast = {
        scorerOutcomeId: 'scorerOutcomeId',
        scorecastPrices: 'scorecastPrices',
      };
      const marketEntity = {
        outcomes: {
          filter: jasmine.createSpy().and.callFake((p1) => {
            return {
              correctPriceType: 'correctPriceType',
              correctedOutcomeMeaningMinorCode: 111,
              displayOrder: 1223,
              fakeOutcome: true,
              icon: true
            };
          })
        }
      };
      scoreMarketService['getTeams'] = jasmine.createSpy('checkCondition').and.returnValue(marketEntity);

      const result = service['getCombinedOutcomePrices'](scoreCast, 'goalscorerOutcomeId', 'correctScoreOutcomeId');
      expect(result).toEqual(null);
    });
    it('should return scoreCast', function () {

      const scoreCast = {
        scorerOutcomeId: 'scorerOutcomeId',
        scorecastPrices: 'scorecastPrices',
        correctScoreOutcomeId: 'correctScoreOutcomeId',
      };
      service['getOutcomeCombinations'] = jasmine.createSpy('checkCondition').and.returnValue(scoreCast);

      service['getCombinedOutcomePrices'](scoreCast, 'goalscorerOutcomeId', 'correctScoreOutcomeId');
      expect(service['getOutcomeCombinations'] ).toHaveBeenCalled();
    });
  });

  describe('getMarketByMarketNamePattern', ()  => {
    it('should call getMarketByMarketNamePattern', function () {

      const marketAray = [{
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 'eachWayFactorNum',
        eachWayFactorDen: 'eachWayFactorDen',
        eachWayPlaces: 'eachWayPlaces',
        header: 'header',
        id: 'id',
        name: 'nameTest'
        }];

      const result = service['getMarketByMarketNamePattern'](marketAray, 'marketEntity');
      expect(result).toEqual(undefined);
    });

    it('should call getMarketByMarketNamePattern with markets array', function () {

      const marketAray = [{
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 'eachWayFactorNum',
        eachWayFactorDen: 'eachWayFactorDen',
        eachWayPlaces: 'eachWayPlaces',
        header: 'header',
        id: 'id',
        name: 'marketEntity/i'
        },
        {
          cashoutAvail: 'cashoutAvail',
          correctPriceTypeCode: 'correctPriceTypeCode',
          dispSortName: 'dispSortName',
          eachWayFactorNum: 'eachWayFactorNum',
          eachWayFactorDen: 'eachWayFactorDen',
          eachWayPlaces: 'eachWayPlaces',
          header: 'header',
          id: 'id',
          name: 'nameTest'
        },
        {
          cashoutAvail: 'cashoutAvail',
          correctPriceTypeCode: 'correctPriceTypeCode',
          dispSortName: 'dispSortName',
          eachWayFactorNum: 'eachWayFactorNum',
          eachWayFactorDen: 'eachWayFactorDen',
          eachWayPlaces: 'eachWayPlaces',
          header: 'header',
          id: 'id',
          name: 'nameTest'
        }];

      const result = service['getMarketByMarketNamePattern'](marketAray, 'marketEntity');
      expect(result).toEqual(marketAray[0]);
    });
  });


  describe('getDefaultScorecastMarketName', ()  => {

    it('should return 0', function () {
      const scorecastMarkets = [
        {
          teamsGoalscorers: ['teamsGoalscorers'],
          market: {
            marketStatusCode: 'P'
          },
          name: 'name',
          localeName: 'localeName',
          goalscorerMarket: {
            marketStatusCode: 'P'
          },
          outcome:
            {
              correctPriceType: 'correctPriceType',
              correctedOutcomeMeaningMinorCode: 213,
              displayOrder: 11,
              fakeOutcome: true,
              icon: true,
              id: 'id',
              isUS: true,
              liveServChannels: 'liveServChannels',
              liveServChildrenChannels: 'liveServChildrenChannels',
              name: 'liveServChildrenChannels',
              outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
              outcomeMeaningMinorCode: 1123,
              outcomeStatusCode: 'outcomeMeaningMinorCode'
            },
          scorecasts: [],
        }
      ];

      const result = service['getDefaultScorecastMarketName'](scorecastMarkets);
      expect(result).toEqual('0');
    });

    it('should return scoreMarkets[0]', function () {
      const scorecastMarkets = [
        {
          teamsGoalscorers: ['teamsGoalscorers'],
          market: {
            marketStatusCode: 'S'
          },
          name: 'name',
          localeName: 'localeName',
          goalscorerMarket: {
            marketStatusCode: 'S'
          },
          outcome:
            {
              correctPriceType: 'correctPriceType',
              correctedOutcomeMeaningMinorCode: 213,
              displayOrder: 11,
              fakeOutcome: true,
              icon: true,
              id: 'id',
              isUS: true,
              liveServChannels: 'liveServChannels',
              liveServChildrenChannels: 'liveServChildrenChannels',
              name: 'liveServChildrenChannels',
              outcomeMeaningMajorCode: 'outcomeMeaningMajorCode',
              outcomeMeaningMinorCode: 1123,
              outcomeStatusCode: 'outcomeMeaningMinorCode'
            },
          scorecasts: [],
        }
      ];

      const result = service['getDefaultScorecastMarketName'](scorecastMarkets);
      expect(result).toEqual('0');
    });
  });

  it('should call setGtmData', ()=> {
     service.setGtmData('switcherText');
     expect(gtmService.push).toHaveBeenCalled();
  });
  it('should call setBetslipGtmData', ()=> {
    const eventData = {
      teamname: 'teamname',
      playerName: 'playerName',
      result: 12,
      selectedScorecastTab: 'selectedScorecastTab',

    }
     service.setBetslipGtmData(eventData);
     expect(gtmService.push).toHaveBeenCalled();
  });

});
