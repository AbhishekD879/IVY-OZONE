import { fakeAsync, tick } from '@angular/core/testing';
import { RacingResultsService } from '@core/services/sport/racing-results.service';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IRacingResultedEventResponse } from '@core/models/racing-result-response.model';
import { IRacingMarket } from '@core/models/racing-market.model';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@shared/services/routingState/routing-state.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TemplateService } from '@shared/services/template/template.service';
import {
  expectedResultedOutcomes,
  expectedResultedWEWMarket,
  virtualRacingResultMock,
  resultedMarketWinorEachWay
} from '@core/services/sport/racing-results.service.mock';
import { IOutcome } from '@core/models/outcome.model';
import { IRaceResultRunnersData } from '../racing/racingPost/racing-post.model';

describe('RacingResultsService', () => {
  let service: RacingResultsService;

  let loadByPortionsService: Partial<LoadByPortionsService>,
    localeService: Partial<LocaleService>,
    siteServerRequestHelperService: Partial<SiteServerRequestHelperService>,
    siteServer: Partial<SiteServerService>,
    horseRacingService: Partial<HorseracingService>,
    greyhoundService: Partial<GreyhoundService>,
    routingState: Partial<RoutingState>,
    templateService: Partial<TemplateService>;

  let racingResult: IRacingResultedEventResponse,
    event: IRacingEvent;
  let winHorses: IOutcome[];
  let loseHorses: IOutcome[];
  let resultedHorsesData: IRaceResultRunnersData[];

  beforeEach(() => {
    event = {
      id: '12200197',
      categoryName: 'Horse Racing',
      isUKorIRE: true,
      markets: [{
        id: 1,
        hasResults: true,
        templateMarketName: 'top 3 first'
      } as any, {
        id: 2,
        templateMarketName: 'win or each way'
      } as any, {
        id: 3,
        hasResults: true,
        templateMarketName: 'win or each way',
        outcomes: [{
          id: 1,
          nonRunner: true
        }, {
          id: 2,
          name: 'lorem'
        }, {
          id: 3,
          name: 'ipsum'
        }, {
          id: 5,
          name: 'dolor'
        }, {
          id: 4,
          name: 'ameno',
          nonRunner: true
        }, {
          id: 7,
          name: 'avizo'
        }]
      } as any],
      sortedMarkets: [
        {
          id: 3,
          priceTypeCodes: 'SP,',
          ncastTypeCodes: 'Lorem',
          hasResults: true,
          outcomes: [{
            id: 91,
            results: {
              position: '1',
              resultCode: 'P',
              priceDec: '2.3'
            },
          }, {
            id: 1,
            nonRunner: true
          }, {
            id: 3,
            results: {}
          }]
        },
        {
          id: 5,
          outcomes: [{
            id: 141,
            results: {
              position: '2'
            },
          }]
        }
      ],
      resultedWEWMarket: {
        hasResults: true,
        hasPositions: true,
        outcomes: [
          {
            name: 'N/R test',
            results : {
              resultCode : 'V',
              position: 1
            }
          }
        ],
        unPlaced: [
          {
            name: 'N/R test',
            results : {
              resultCode : 'V',
              position: 1
            }
          }
        ],
        nonRunners : []
      }
    } as any;

    racingResult = [
      {
        resultedEvent: {
          drilldownTagNames:'EVFLAG_AVD',
          children: [{
            resultedMarket: {
              id: 3,
              children: [{
                resultedOutcome: {
                  id: 2,
                  children: [{
                    resultedPrice: {
                      priceTypeCode: 'SP',
                      priceNum: 4,
                      priceDec: '1.2'
                    }
                  },
                    {
                      resultedPrice: {
                        priceTypeCode: 'LP',
                        priceNum: 3
                      }
                    }],
                  position: 3,
                  resultCode: 'P'
                }
              }, {
                resultedOutcome: {
                  id: 3,
                  children: [{
                    resultedPrice: {
                      priceTypeCode: 'SP',
                      priceNum: 4
                    }
                  }],
                  resultCode: 'L'
                }
              }, {
                resultedOutcome: {
                  id: 1,
                  children: [{
                    resultedPrice: {
                      priceTypeCode: 'SP',
                      priceNum: 1,
                      priceDec: 3.4
                    }
                  }],
                  resultCode: 'W',
                  position: 1
                }
              }, {
                resultedOutcome: {
                  id: 4,
                  children: [{
                    resultedPrice: {
                      priceTypeCode: 'SP',
                      priceNum: 2.3
                    }
                  }],
                  resultCode: 'P',
                  position: 3
                }
              }, {
                resultedOutcome: {
                  id: 7,
                  children: [{
                    resultedPrice: {
                      priceTypeCode: 'SP'
                    }
                  }],
                  resultCode: 'V'
                }
              }]
            }
          }]
        }
      }
    ] as any;

    winHorses = [
      {
        id: "1715708791",
        isDisplayed: "true",
        isFinished: "true",
        isResulted: "true",
        marketId: "536934943",
        name: "|B B King|",
        outcomeMeaningMajorCode: "--",
        position: "1",
        resultCode: "W",
        results: {
          id: "1715708791_2",
          outcomeId: "1715708791",
          position: "1",
          priceDec: "4.50",
          priceDen: "2",
          priceNum: "7",
          priceTypeCode: "SP",
          resultCode: "W",
        },
        runnerNumber: "1",
        siteChannels: "P,Q,C,I,M,"
      }
    ] as any;

    loseHorses = [
      {
        id: "1715708791",
        isDisplayed: "true",
        isFinished: "true",
        isResulted: "true",
        marketId: "536934943",
        name: "|B B King|",
        outcomeMeaningMajorCode: "--",
        position: "0",
        resultCode: "L",
        results: {
          id: "1715708791_2",
          outcomeId: "1715708791",
          position: "1",
          priceDec: "4.50",
          priceDen: "2",
          priceNum: "7",
          priceTypeCode: "SP",
          resultCode: "W",
        },
        runnerNumber: "1",
        siteChannels: "P,Q,C,I,M,"
      }
    ] as any;

    resultedHorsesData = [
      {
        comment: "in touch with leaders, steady headway on outer halfway, ridden and edged right under 2f out, no extra when hampered inside final 110yds",
        saddle: "1",
        jockeyName: "Jack Garritty",
        distanceToWinner: "3.8",
        position: "0",
        horseName: "Ebony Maw",
        distanceHif: "nk",
        rpHorseId: 2863059,
        odds: "33/1",
        raceOutcomeCode: "6",
        raceOutcomeDesc: "6th"
      }
    ] as any;

    localeService = {
      getString: jasmine.createSpy().and.returnValue('Lorem')
    };
    siteServerRequestHelperService = {
      getRacingResultsForEvent: jasmine.createSpy().and.returnValue(Promise.resolve([racingResult]))
    };
    siteServer = {
      loadResultsOfEvent: jasmine.createSpy().and.returnValue(Promise.resolve(racingResult))
    };
    horseRacingService = {
      getConfig: jasmine.createSpy().and.returnValue({ request: 'Lorem' }),
      addFavouriteLabelToOutcomesWithResults: jasmine.createSpy('addFavouriteLabelToOutcomesWithResults')
    };
    greyhoundService = {
      getConfig: jasmine.createSpy().and.returnValue({ request: 'Lorem' }),
      addFavouriteLabelToOutcomesWithResults: jasmine.createSpy('addFavouriteLabelToOutcomesWithResults')
    };
    routingState = {
      getCurrentSegment: jasmine.createSpy().and.returnValue('horseracing')
    };
    loadByPortionsService = {
      get: (func: Function, ...args) => {
        return func();
      }
    } as any;
    templateService = {
      genTerms: jasmine.createSpy().and.returnValue('Each Way: 1/5 Odds - Places 1-2-3')
    } as any;

    service = new RacingResultsService(
      loadByPortionsService as LoadByPortionsService,
      localeService as LocaleService,
      siteServerRequestHelperService as SiteServerRequestHelperService,
      siteServer as SiteServerService,
      horseRacingService as HorseracingService,
      greyhoundService as GreyhoundService,
      routingState as RoutingState,
      templateService as TemplateService
    );
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('makeVoidMarket', () => {
    it('should create', () => {
      const market: any =  {
        cashoutAvail: 'cashoutAvail',
        correctPriceTypeCode: 'correctPriceTypeCode',
        dispSortName: 'dispSortName',
        eachWayFactorNum: 1,
        eachWayFactorDen: 1,
        eachWayPlaces: 'eachWayPlaces',
        outcomes: [
          {
            runnerNumber: 11,
            nonRunner: false,
            name: 'eachWayPlaces'
          }, {
            runnerNumber: 21,
            nonRunner: false,
            name: 'eachWayPlaces'
          }, {
            runnerNumber: 31,
            nonRunner: false,
            name: 'eachWayPlaces'
          }
        ]
      };
      service['makeVoidMarket'](market);
      expect(service['makeVoidMarket']).toBeTruthy();
    });
  });

  describe('#getRacingResults should concatenate all data', () => {
    it('#getRacingResults should attach results to event', fakeAsync(() => {
      service['mapResultsToOutcomes'] = jasmine.createSpy();
      service['getRacingRulesAndDividends'] = jasmine.createSpy();
      service['sortOutcomesByPositions'] = jasmine.createSpy().and.callFake(data => data);

      service.getRacingResults(event, false);
      tick();
      expect(siteServer.loadResultsOfEvent).toHaveBeenCalled();
      expect(service['mapResultsToOutcomes']).toHaveBeenCalledWith(racingResult as any, event);
      expect(service['racingService'].addFavouriteLabelToOutcomesWithResults).toHaveBeenCalled();
      expect(event.sortedMarkets[0].outcomes.length).toEqual(3);
      expect(service['sortOutcomesByPositions']).toHaveBeenCalledWith(event.resultedWEWMarket);
      expect(service['getRacingRulesAndDividends']).toHaveBeenCalled();
    }));

    it('#getRacingResults case with resultMarket.priceTypeCodes', fakeAsync(() => {
      service['mapResultsToOutcomes'] = jasmine.createSpy();
      service['getRacingRulesAndDividends'] = jasmine.createSpy();
      service['sortOutcomesByPositions'] = jasmine.createSpy().and.callFake(data => data);
      
      event.sortedMarkets[0].priceTypeCodes = 'LP,';
      event.resultedWEWMarket.hasResults = false;
      event.isUKorIRE = true;
      event.categoryCode === 'GREYHOUNDS';
      service.getRacingResults(event, true);
      tick();
      expect(service['racingService'].addFavouriteLabelToOutcomesWithResults).not.toHaveBeenCalled();
      expect(service['sortOutcomesByPositions']).toHaveBeenCalled();
      expect(service['getRacingRulesAndDividends']).toHaveBeenCalled();
    }));

    it('#getRacingResults case with no market hasResults', fakeAsync(() => {
      event.sortedMarkets[0].hasResults = undefined;
      event.resultedWEWMarket.hasPositions = false;
      service['mapResultsToOutcomes'] = jasmine.createSpy();
      service['getRacingRulesAndDividends'] = jasmine.createSpy();
      service['sortOutcomesByPositions'] = jasmine.createSpy().and.callFake(data => data);
      service['makeVoidMarket'] = jasmine.createSpy();

      service.getRacingResults(event, false);
      tick();
      expect(service['racingService'].addFavouriteLabelToOutcomesWithResults).not.toHaveBeenCalled();
      expect(service['sortOutcomesByPositions']).not.toHaveBeenCalled();
      expect(service['getRacingRulesAndDividends']).not.toHaveBeenCalled();
      expect(service['makeVoidMarket']).toHaveBeenCalled();
      expect(event.voidResult).toBeTruthy();
    }));

    it('#getRacingResults case with lose runners', fakeAsync(() => {
      service['getRacingResults'] = jasmine.createSpy();
      service['mapResultsToOutcomes'] = jasmine.createSpy();
      service.getRacingResults(event, true);
      expect(event.categoryName).toBe('Horse Racing');
      expect(event.isUKorIRE).toBeTrue;
    }));

    describe('#mapResultsToOutcomes cases with rasing exceptions', () => {
      it('response = []', () => {
        service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue(undefined);
        expect((): void => service['mapResultsToOutcomes']([] as any, event)).toThrow();
      });

      it('response with children = []', () => {
        service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue(undefined);
        expect((): void => service['mapResultsToOutcomes']([{
          resultedEvent: {
            children: []
          }
        }] as any, event)).toThrow();
      });

      it('response with no resulted market', () => {
        service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue({
          resultedMarket: {
            children: []
          }
        });
        expect((): void => service['mapResultsToOutcomes']([{
          resultedEvent: {
            children: [{
              resultedMarket: {
                children: []
              }
            }]
          }
        }] as any, event)).toThrow();
      });
    });
  });

  it('#getRacingRulesAndDividends should get rules and dividend to event', fakeAsync(() => {
    service['mapRulesDividendsToOutcomes'] = jasmine.createSpy();
    service['filterDividends'] = jasmine.createSpy();
    service['filterRulesDeduction'] = jasmine.createSpy();
    const resultedMarket = event.markets[0];

    service.getRacingRulesAndDividends(event, resultedMarket, false);
    tick();

    expect(siteServerRequestHelperService.getRacingResultsForEvent).toHaveBeenCalled();
    expect(service['mapRulesDividendsToOutcomes']).toHaveBeenCalledWith([racingResult] as any, resultedMarket, false);
    expect(service['filterDividends']).toHaveBeenCalledWith(resultedMarket);
    expect(service['filterRulesDeduction']).toHaveBeenCalledWith(resultedMarket);
  }));

  describe('racingService', () => {
    it('should return HorseracingService instance', () => {
      expect(service['racingService']).toEqual(horseRacingService as any);
    });

    it('should return GreyhoundService instance', () => {
      routingState.getCurrentSegment = jasmine.createSpy().and.returnValue('greyhound');

      expect(service['racingService']).toEqual(greyhoundService as any);
    });

    it('should set GreyhoundService instance to racing Service', () => {
      service['racingService']  =  greyhoundService as any;
    });
  });

  describe('loseRunners', () => {
    let market;

    beforeEach(() => {
      market = {
        outcomes: [{
          results: {
            resultCode: 'L',
            position: '5'
          }
        },
        {
          results: {
            resultCode: 'L',
          }
        }]
      } as any;
    });
    it('should add outcomes with resultCode Lose and position to Unplaced', () => {
      service['loseRunners'](market);
      expect(market.outcomes[0].results.resultCode).toEqual('L');
      expect(market.outcomes[0].results.position).toEqual('5');
    });
    it('should add outcomes with resultCode Lose and no position to Unplaced', () => {
      service['loseRunners'](market);
      expect(market.outcomes[1].results.resultCode).toEqual('L');
      expect(market.outcomes[1].results.position).toEqual(undefined);
    });
  });
  describe('removeVoidRunners', () => {
    let market;

    beforeEach(() => {
      market = {
        outcomes: [{
          results: {
            resultCode: 'V',
            priceDec: 10
          }
        }, {
          results: {
            resultCode: 'L',
          }
        }]
      } as any;
    });

    it('should remove outcomes with resultCode Void (=nonRunners)', () => {
      service['removeVoidRunners'](market, event);
      expect(market.outcomes).toEqual([]);
    });

    it('should extract outcomes with no void resultCode', () => {
      market.outcomes[0].results.resultCode = '';
      service['removeVoidRunners'](market, event);
      expect(market.outcomes).toEqual(market.outcomes);
    });

    it('should populate outcomes with no sp price in outcomesWithoutPrices for greyhounds', () => {
      event.isUKorIRE = true;
      event.categoryCode = 'GREYHOUNDS';
      service['removeVoidRunners'](market, event);
      expect(market.outcomes).toEqual([]);
      expect(market.outcomesWithoutPrices.length).toEqual(1);
    });
  });

  describe('mapResultPosition', () => {
    it('#mapResultPositionPlaced should map positions in placed section', () => {
      const horse = winHorses[0];
      const item = resultedHorsesData[0];
      const isHorseExists = horse;
      service.mapResultPositionPlaced(winHorses, resultedHorsesData);
      expect(horse.runnerNumber).toEqual(item.saddle);
      expect(isHorseExists).toEqual(horse);
      expect(winHorses).toBe(winHorses);
    })

    it('#mapResultPositionUnplaced should map positions in Unplaced section', () => {
      const horse = loseHorses[0];
      const item = resultedHorsesData[0];
      const isHorseExists = horse;
      service.mapResultPositionUnplaced(loseHorses, resultedHorsesData, event);
      expect(horse.runnerNumber).toEqual(item.saddle);
      expect(isHorseExists).toEqual(horse);
      expect(isHorseExists.position).toBeTruthy;
      expect(isHorseExists.position).toEqual('0');
    })

    it('#mapResultPositionUnplaced function call when position is empty and resultCode is L', () => {
      const horse = loseHorses[0];
      const item = resultedHorsesData[0];
      const isHorseExists = horse;
      event.resultedWEWMarket.unPlaced[0].results.position = '';
      event.resultedWEWMarket.unPlaced[0].results.resultCode = 'L';
      service.mapResultPositionUnplaced(loseHorses, resultedHorsesData, event);
      expect(isHorseExists).toEqual(horse);
    })
  });

  it('#mapResultsToOutcomes should map results to event', () => {
    service['formMarketInfo'] = jasmine.createSpy();
    service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue(resultedMarketWinorEachWay);
    service['mapResultsToOutcomes'](virtualRacingResultMock as any, event);

    expect(event.markets[2].outcomes).toEqual(expectedResultedOutcomes);
    expect(service['formMarketInfo']).toHaveBeenCalled();
  });
  it('#mapResultsToOutcomes should map results to event not exist drilldown tag', () => {
    service['formMarketInfo'] = jasmine.createSpy();
    service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue(resultedMarketWinorEachWay);
    virtualRacingResultMock[0].resultedEvent.drilldownTagNames='test';
    service['mapResultsToOutcomes'](virtualRacingResultMock as any, event);

    expect(event.markets[2].outcomes).toEqual(expectedResultedOutcomes);
    expect(service['formMarketInfo']).toHaveBeenCalled();
  });

  it('#mapResultsToOutcomes should map results to virtual event', () => {
    service['formMarketInfo'] = jasmine.createSpy();
    service['getWinOrEachWay'] = jasmine.createSpy().and.returnValue(resultedMarketWinorEachWay);
    event.isVirtual = true;
    service['mapResultsToOutcomes'](virtualRacingResultMock as any, event);

    expect(event.resultedWEWMarket).toEqual(expectedResultedWEWMarket);
    expect(service['formMarketInfo']).toHaveBeenCalled();
  });

  describe('#formMarketInfo add some properties to resulted market', () => {
    it('resultedMarket has all needed data', () => {
      const evt = {
        resultedWEWMarket: {
          id: 1,
          cashoutAvail: 'Y',
          viewType: 'handicaps',
          drilldownTagNames: 'MKTFLAG_BBAL'
        },
        sortedMarkets: []
      } as any;

      service['formMarketInfo'](evt);
      expect(evt.resultedWEWMarket.terms).toBe('Each Way: 1/5 Odds - Places 1-2-3');
      expect(evt.resultedWEWMarket.cashoutAvail).toBe('Y');
      expect(evt.resultedWEWMarket.viewType).toBe('handicaps');
      expect(evt.resultedWEWMarket.drilldownTagNames).toBe('MKTFLAG_BBAL');
    });

    it('resultedMarket has no needed data but sortedMarket[0] as wew has', () => {
      const evt = {
        resultedWEWMarket: {
          id: 1,
        },
        sortedMarkets: [{
          id: 1,
          cashoutAvail: 'Y',
          viewType: 'handicaps',
          drilldownTagNames: 'MKTFLAG_BBAL'
        }]
      } as any;

      service['formMarketInfo'](evt);
      expect(evt.resultedWEWMarket.terms).toBe('Each Way: 1/5 Odds - Places 1-2-3');
      expect(evt.resultedWEWMarket.cashoutAvail).toBe('Y');
      expect(evt.resultedWEWMarket.viewType).toBe('handicaps');
      expect(evt.resultedWEWMarket.drilldownTagNames).toBe('MKTFLAG_BBAL');
    });

    it('resultedMarket has no needed data but sortedMarket[0] is not wew', () => {
      const evt = {
        resultedWEWMarket: {
          id: 1,
        },
        sortedMarkets: [{
          id: 2,
          cashoutAvail: 'Y',
          viewType: 'handicaps',
          drilldownTagNames: 'MKTFLAG_BBAL'
        }]
      } as any;

      service['formMarketInfo'](evt);
      expect(evt.resultedWEWMarket.terms).toBe('Each Way: 1/5 Odds - Places 1-2-3');
      expect(evt.resultedWEWMarket.cashoutAvail).toBe('');
      expect(evt.resultedWEWMarket.viewType).toBe('');
      expect(evt.resultedWEWMarket.drilldownTagNames).toBe('');
    });
  });

  it('#mapRulesDividendsToOutcomes should map results', () => {
    // 1 case
    const response = [{
      racingResult: {
        children: [{
          ncastDividend: {
            type: 'FC',
            marketId: 3,
            dividend: '10',
            runnerNumbers: '2,6,'
          }
        }, {
          rule4Deduction: {
            marketId: 3
          }
        }, undefined]
      }
    }] as any;

    service['mapRulesDividendsToOutcomes'](response, event.sortedMarkets[0], true);
    expect(event.sortedMarkets[0].dividends).toEqual([{
            type: 'FC',
            name: 'Lorem',
            value: '10',
            runnerNumbers: '2,6,'
          }] as any);
    expect(event.sortedMarkets[0].rulesFourDeduction).toEqual([{
            marketId: 3
          }] as any);

  // 2 case
    const market = {
        id: 3,
        outcomes: [{}]
    } as any;
    service['mapRulesDividendsToOutcomes'](response, market, false);
    expect(market.dividends).toEqual([] as any);
    expect(market.rulesFourDeduction).toEqual(null);
  });

  it('#sortOutcomesByPositions should sort list', () => {
    const market = {
      outcomes : [{
        name: '2nd',
        results: {
          position: '2',
        },
      }, {
        name: '1st',
        results: {
          position: '1'
        },
      }],
      unPlaced : [{
        name: '2nd',
        results: {
          position: '2',
        },
      }, {
        name: '1st',
        results: {
          position: '1'
        },
      }],
    } as any;

    service['sortOutcomesByPositions'](market);
    expect(market.outcomes[0].name).toBe('1st');
    expect(market.unPlaced[0].name).toBe('1st');
  });

  it('#filterDividends (incl. #isNCastEnabled) should filter dividends', () => {
    // 1 case
    const market: IRacingMarket = {
      ncastTypeCodes: 'CT,TC,SF,CF,RF',
      dividends: [
        { type: 'FC', runnerNumbers: '3,4,' },
        { type: 'TC', runnerNumbers: '8,9,6,' },
        { type: 'FC', runnerNumbers: '7,8,' },
        { type: 'TC', runnerNumbers: '3,4,7,' }
      ],
      outcomes: [
        { runnerNumber: '3' },
        { runnerNumber: '4' },
        { runnerNumber: '7' }
      ]
    } as any;
    let resDiv = [
      { type: 'FC', runnerNumbers: '3-4' },
      { type: 'TC', runnerNumbers: '3-4-7' }
    ];
    service['filterDividends'](market);
    expect(market.dividends).toEqual(resDiv as any);

    // 2 case
    market.ncastTypeCodes = 'CT,TC';
    market.dividends = [
      { type: 'FC', runnerNumbers: '3,4,' },
      { type: 'TC', runnerNumbers: '3,4,7,' }
    ] as any;
    service['filterDividends'](market);
    resDiv = [
      { type: 'TC', runnerNumbers: '3-4-7' }
    ];
    expect(market.dividends).toEqual(resDiv as any);

    // 3 case
    market.ncastTypeCodes = 'SF,CF,RF';
    market.dividends = [
      { type: 'FC', runnerNumbers: '3,4,' },
      { type: 'TC', runnerNumbers: '3,4,7,' }
    ] as any;
    service['filterDividends'](market);
    resDiv = [
      { type: 'FC', runnerNumbers: '3-4' }
    ];
    expect(market.dividends).toEqual(resDiv as any);

    // 4 case
    market.ncastTypeCodes = undefined;
    market.dividends = [] as any;
    service['filterDividends'](market);
    expect(market.dividends).toEqual([]);

    // 5 case
    market.ncastTypeCodes = 'CT,TC,SF,CF,RF';
    market.dividends = [
      { type: 'TC', runnerNumbers: '3,4,7,' },
      { type: 'FC', runnerNumbers: '3,4,' }
    ] as any;
    service['filterDividends'](market);
    resDiv = [
      { type: 'FC', runnerNumbers: '3-4' },
      { type: 'TC', runnerNumbers: '3-4-7' }
    ];
    expect(market.dividends).toEqual(resDiv as any);
  });

  it('#isNCastEnabled should return false for unknown nCastCode param', () => {
    expect(service['isNCastEnabled']({} as any, 'RT')).toBe(false);
  });

  it('#filterRulesDeduction should filter rules for deduction', () => {
    let market: IRacingMarket = {
      rulesFourDeduction: [
        { id: 1, toDate: '2019-02-01T14:53:08.756Z' },
        { id: 2, toDate: '2019-02-03T14:53:08.756Z' },
        { id: 3, toDate: '2019-02-06T14:53:08.756Z' },
        { id: 4, toDate: '2019-02-02T14:53:08.756Z' },
        { id: 5, toDate: '2019-02-07T14:53:08.756Z' }
      ]
    } as any;
    service['filterRulesDeduction'](market);
    expect(market).toEqual({ rulesFourDeduction: [{ id: 5, toDate: '2019-02-07T14:53:08.756Z' }] } as any);

    market = {} as any;
    service['filterRulesDeduction'](market);
    expect(market).toEqual({} as any);
  });

  describe('#getWinOrEachWay from children1/2 resulted market case senstive', () => {
    it('1resultedMarket has all needed data ', () => {
      const evt = [{
        resultedEvent: { children : [ {resultedMarket: {
          name: '|Win or Each Way|'
        }}]}
      }] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).not.toBeNull();
    });

    it('2resultedMarket has all needed data first obj small case ', () => {
      const evt = [{
        resultedEvent: { children : [ {resultedMarket: {
          name: '|win or each way|'
        }}]}
      }] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).not.toBeNull();
    });

    it('3resultedMarket has all needed data second obj  case senstive ', () => {
      const evt = [{
        resultedEvent: { children : [
          {resultedMarket: {
          name: '|Win Only|'
          }},
          {resultedMarket: {
            name: '|Win or Each Way|'
            }}
        ]}
      }] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).not.toBeNull();
    });

    it('4resultedMarket has all needed data second obj small case ', () => {
      const evt = [{
        resultedEvent: { children : [
          {resultedMarket: {
          name: '|Win Only|'
          }},
          {resultedMarket: {
            name: '|win or each way|'
            }}
        ]}
      }] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).not.toBeNull();
    });

    it('5resultedMarket has all needed data evt empty ', () => {
      const evt = [] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).toBe(undefined);
    });

    it('6resultedMarket has all needed data resultedEvent null', () => {
      const evt = [{resultedEvent: null}] as any;
      const result = service['getWinOrEachWay'](evt);
      expect(result).toBe(undefined);
    });

  });
});
