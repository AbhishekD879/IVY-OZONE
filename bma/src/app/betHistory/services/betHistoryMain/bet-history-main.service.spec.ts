import { of as observableOf, throwError } from 'rxjs';
import { tick, fakeAsync } from '@angular/core/testing';

import environment from '@environment/oxygenEnvConfig';
import { betHistoryConstants } from '../../constants/bet-history.constant';
import { IBetHistoryBet, IBetReturns, IBetReturnsValue, IPageBets } from '@app/betHistory/models/bet-history.model';
import { IYourCallBetStatuses } from '@app/betHistory/models/your-call-bet-statuses.model';
import { IGetBetHistoryRequest } from '@app/bpp/services/bppProviders/bpp-providers.model';

import { BetHistoryMainService } from './bet-history-main.service';
import { LocaleService } from 'app/core/services/locale/locale.service';
import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { YourCallHistoryBetBuilderService } from '../../services/yourCallHistoryBetBuilder/your-call-history-bet-builder.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';


describe('BetHistoryMainService', () => {
  let service: BetHistoryMainService;
  let serviceHacked: any;
  let localeService: LocaleService;
  let timeService: TimeService;

  let filtersService: FiltersService;
  let bppService: BppService;
  let userService;
  let commandService: CommandService;
  let yourCallHistoryBetBuilderService: YourCallHistoryBetBuilderService;
  let coreToolsService: CoreToolsService;
  let betHistoryBet: IBetHistoryBet;
  let env;
  let windowRef;
  let cmsService;
  let vanillaApiService;

  const ycBetStatuses: IYourCallBetStatuses = betHistoryConstants.ycBetStatuses;

  let
    betHistoryEachWayTerms,
    market,
    dateRangeObject,
    outcomeResult,
    detailedBetObject,
    betHistoryOutcome,
    betHistoryHandicap,
    price,
    betHistoryPart,
    betHistoryLeg,
    accountHistoryResponse,
    sportsConfigHelperService;

  const iniData = function() {
    env = environment as any;
    betHistoryEachWayTerms = {
      value: '123',
      eachWayPlaces: '3'
    };

    market = {
      name: 'fooName'
    };

    dateRangeObject = {
      startDate: '',
      endDate: ''
    };

    outcomeResult = {
      confirmed: 'Y',
      value: 'P'
    };

    detailedBetObject = {
      legs: [],
      numLegs: 1
    };

    betHistoryOutcome = {
      id: '1',
      correctPriceType: '',
      correctedOutcomeMeaningMinorCode: 1,
      displayOrder: 1,
      fakeOutcome: true,
      icon: true,
      liveServChannels: '',
      name: 'fooName',
      outcomeMeaningMajorCode: '',
      outcomeMeaningMinorCode: '',
      outcomeStatusCode: '',
      prices: [],
      runnerNumber: '',
      silkName: '',
      racingFormOutcome: null,
      details: '',
      market: market,
      outcomeResult: 'W',
      eventCategory: {id: '123'},
      eventType: {name: 'fooName'},
      eventClass: {name: 'fooName'},
      event: {name: 'fooName', startTime: 'fooTime'},
      result: outcomeResult
    };

    betHistoryHandicap = {
      value: 123,
      type: '',
      raw: '123'
    };

    price = {
      den: 1,
      num: 2,
      priceDecimal: '123.321'
    };

    betHistoryPart = {
      outcome: [betHistoryOutcome],
      name: 'fooName',
      handicap: betHistoryHandicap,
      eachWayTerms: betHistoryEachWayTerms,
      eachWayPlaces: '2',
      outcomeId: '',
      dispResult: '',
      partNo: '',
      description: '',
      result: '',
      price: [price]
    };

    betHistoryLeg = {
      name: 'fooName',
      part: [betHistoryPart],
      poolPart: [betHistoryPart],
      legSort: {code: '--'},
      legType: {code: 'fooType'},
      startTime: 'fooTime'
    };

    betHistoryBet = {
      winnings : [{   value : "10"}]as any,
      potentialPayout :[  { value :"10"}],
      refund : [{   value : "10"}]as any,
      id: 1,
      documentId: '',
      betTypeRef: {id: ''},
      stake: {currencyRef: {id: ''}},
      lines: {number: 1},
      legRef: [{documentId: '', ordering: ''}],
      ycBet: true,
      allSilkNames: [],
      poolLeg: [betHistoryLeg],
      externalRefId: {
        value: '123',
        lotteryDraw:'test'
      },
      data: [{id: '123'}],
      source: 'e'
    };

    accountHistoryResponse = {
      poolBet: [betHistoryBet],
      bet: [betHistoryBet, betHistoryBet]
    };
  };

  const iniServices = function() {
    localeService = jasmine.createSpyObj(['getString']);
    timeService = jasmine.createSpyObj(['dateTimeOfDayInISO', 'getLocalHourMin', 'parseDateTime']);
    filtersService = jasmine.createSpyObj(['date', 'getTimeFromName', 'clearEventName', 'makeHandicapValue',
      'currencyPosition', 'numberWithCurrency']);
    bppService = jasmine.createSpyObj(['send']);
    userService = {
      currencySymbol: jasmine.createSpy('currencySymbol'),
      isInShopUser: jasmine.createSpy('isInShopUser')
    };
    commandService = jasmine.createSpyObj(['executeAsync', 'API']);
    yourCallHistoryBetBuilderService = jasmine.createSpyObj(['extendHistoryBet']);
    coreToolsService = jasmine.createSpyObj(['getOwnDeepProperty']);

    (localeService.getString as jasmine.Spy).and.returnValue('fooString');
    (filtersService.currencyPosition as jasmine.Spy).and.returnValue('fooString');
    (filtersService.date as jasmine.Spy).and.returnValue(dateRangeObject);
    (filtersService.getTimeFromName as jasmine.Spy).and.returnValue('');
    (filtersService.makeHandicapValue as jasmine.Spy).and.returnValue(' (+0.5)');
    (filtersService.numberWithCurrency as jasmine.Spy).and.callFake((num: number) => `$${num}`);
    (bppService.send as jasmine.Spy).and.returnValue(observableOf({
      response: { model: {} }
    }));
    (commandService.executeAsync as jasmine.Spy).and.returnValue(new Promise((resolve) => resolve(betHistoryBet)));
    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(observableOf('sportPath'))
    };

    windowRef = {
      document:{
        getElementsByClassName : jasmine.createSpy().and.returnValue([   {classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')}
        }])
      }
    };
    window.crypto.getRandomValues = jasmine.createSpy().and.returnValue(123);
    vanillaApiService = {
      get: jasmine.createSpy('get').and.returnValue(observableOf([{
        type: 'segmentDefault',
        teasers: [{
            title: 'Test',
            subTitle: 'QA',
            itemId: '{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}',
            backgroundImage: { src: 'abc' }
        }]
      }]))
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!"
        }
      }))
    } as any;

    service = new BetHistoryMainService(
      localeService as any,
      timeService as any,
      filtersService as any,
      bppService as any,
      userService as any,
      commandService as any,
      yourCallHistoryBetBuilderService as any,
      coreToolsService as any,
      sportsConfigHelperService  as any,
      windowRef as any,
      cmsService as any,
      vanillaApiService as any
    );
    serviceHacked = service as any;
  };

  beforeEach(() => {
    iniData();
    iniServices();
  });


  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('YC bet statuses should be equal to constants', () => {
    expect(service.ycBetStatuses).toEqual(betHistoryConstants.ycBetStatuses);
  });

  it('regularResultStatuses should be initialized', () => {
    expect(service.regularResultStatuses).toBeTruthy();
  });

  it('toteResultStatuses should be initialized', () => {
    expect(service.toteResultStatuses).toBeTruthy();
  });

  it('categoriesData should match environment data', () => {
    expect(service.categoriesData).toEqual(env.CATEGORIES_DATA);
  });

  it( 'getHistoryForYear should call getHistory', () => {
    spyOn(service, 'getHistory');
    service.getHistoryForYear('', '');
    expect(service.getHistory).toHaveBeenCalled();
  });

  it( 'getHistoryForYear should call getSettleType', () => {
    spyOn(serviceHacked, 'getSettleType');
    service.getHistoryForYear('', 'fooType');
    expect(serviceHacked.getSettleType).toHaveBeenCalledWith('fooType');
  });

  describe('extendCashoutBets', () => {
    it('should extend bets', () => {
      const bets = [
        {
          id: 1
        },
        {
          betId: 2
        }
      ] as any;
      service.extendCashoutBets(bets);
      expect(bets[0].betId).toEqual(1);
      expect(bets[1].betId).toEqual(2);
    });
  });

  describe('#getBetsCountForYear', () => {
    beforeEach(() => {
      spyOn(service, 'getBetsCount');
      spyOn(serviceHacked, 'getSettleType');
    });
    it('getBetsCountForYear should call getBetsCount', () => {
      service.getBetsCountForYear('', '');
      expect(serviceHacked.getSettleType).toHaveBeenCalledWith('');
    });
    it('getBetsCountForYear should call getBetsCount width params', () => {
      service.getBetsCountForYear('', 'fooType');
      expect(serviceHacked.getSettleType).toHaveBeenCalledWith('fooType');
    });
    afterEach(() => {
      expect(service.getBetsCount).toHaveBeenCalled();
    });
  });

  describe('#getBetsCount', () => {
    let reqObject;

    beforeEach(() => {
      spyOn(serviceHacked, 'filterByParam');
      spyOn(serviceHacked, 'createRequest').and.returnValue(observableOf({}));
      reqObject = {
        fromDate: dateRangeObject,
        toDate: undefined,
        group: 'BET',
        pagingBlockSize: '20'
      };
    });
    it('getBetsCount should call filterByParam and createRequest', () => {
      service.getBetsCount(dateRangeObject, '', '').subscribe();
    });
    it('getBetsCount should call filterByParam and createRequest with settled', () => {
      reqObject = Object.assign({}, reqObject, { settled: 'settled' });
      service.getBetsCount(dateRangeObject, '', 'settled').subscribe();
    });
    afterEach(fakeAsync(() => {
      tick();
      expect(serviceHacked.filterByParam).toHaveBeenCalledWith('filteredToDate');
      expect(serviceHacked.createRequest).toHaveBeenCalledWith(reqObject as IGetBetHistoryRequest, null, '/count');
    }));
  });

  it( 'getHistoryForTimePeriod should call getHistory', () => {
    spyOn(service, 'getHistory');
    service.getHistoryForTimePeriod('', '', {});
    expect(service.getHistory).toHaveBeenCalled();
  });

  it( 'getHistoryForTimePeriod should call getSettleType', () => {
    spyOn(serviceHacked, 'getSettleType');
    service.getHistoryForTimePeriod('', 'fooType', {});
    expect(serviceHacked.getSettleType).toHaveBeenCalledWith('fooType');
  });

  it( 'getHistory should call filterByParam', () => {
    spyOn(serviceHacked, 'filterByParam');
    service.getHistory(dateRangeObject, '', '');
    expect(serviceHacked.filterByParam).toHaveBeenCalledWith('filteredToDate');
  });

  it( 'getHistory should CreateRequest and callback', () => {
    spyOn(serviceHacked, 'filterByParam');
    service['createRequest'] = jasmine.createSpy().and.callFake((p1, cb) => {
      cb({}, true);
      return observableOf(null);
    });

    service.getHistory(dateRangeObject, '', '');
    expect(serviceHacked.filterByParam).toHaveBeenCalledWith('filteredToDate');
  });

  it( 'getHistory should call createRequest', () => {
    spyOn(serviceHacked, 'createRequest');
    service.getHistory(dateRangeObject, '', '');
    expect(serviceHacked.createRequest).toHaveBeenCalled();
  });

  it( 'getBet should call createRequest', () => {
    spyOn(serviceHacked, 'createRequest');
    service.getBet('');
    expect(serviceHacked.createRequest).toHaveBeenCalled();
  });

  it('getHistoryPage should call createRequest', () => {
    spyOn(serviceHacked, 'getEditMyAccaHistory').and.returnValue(observableOf({}));
    serviceHacked.createRequest = () => {
      return observableOf({});
    };
    service.getHistoryPage('', 'open').subscribe();
    expect(serviceHacked.getEditMyAccaHistory).toHaveBeenCalled();
  });

  it('getHistoryPage should call createRequest', () => {
    spyOn(serviceHacked, 'getEditMyAccaHistory').and.returnValue(observableOf({}));
    serviceHacked.createRequest = () => {
      return observableOf({});
    };
    service.getHistoryPage('', 'settled').subscribe();
    expect(serviceHacked.getEditMyAccaHistory).not.toHaveBeenCalled();
  });

  it('#calling showFirstBet without first bet should return', () => {
    windowRef.document = {
      getElementsByClassName: jasmine.createSpy().and.callFake(param => {
        if (param === 'firstBet') {
          return [];
        }
      }),
      body: {
        appendChild: jasmine.createSpy('appendChild'),
        classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')
        }
      }
    };
    service.showFirstBet('bet');
    expect(windowRef.document.body.classList.add).not.toHaveBeenCalledWith('display-none');
    expect(windowRef.document.body.classList.remove).not.toHaveBeenCalledWith('display-none');
  })

  it('#calling showFirstBet with first bet should add class to element', () => {
    const element = document.createElement('div');
    windowRef.document = {
      getElementsByClassName: jasmine.createSpy().and.callFake(param => {
        if (param === 'firstBet') {
          return [element]
        }
      }),
      classList: {
        add: jasmine.createSpy('add'),
        remove: jasmine.createSpy('remove')
      }
    };
    service.showFirstBet('shopBet');
    expect(windowRef.document.classList.remove).not.toHaveBeenCalledWith('display-none');
  })

  it('#calling showFirstBet with filter should remove class from element', () => {
    const element = document.createElement('div');
    element.classList.add('display-none');
    windowRef.document = {
      getElementsByClassName: jasmine.createSpy().and.callFake(param => {
        if (param === 'firstBet') {
          return [element]
        }
      }),
      classList: {
        add: jasmine.createSpy('add'),
        remove: jasmine.createSpy('remove')
      }
    };
    service.showFirstBet('bet');
    expect(windowRef.document.classList.add).not.toHaveBeenCalledWith('display-none');
  })

  describe('getEditMyAccaHistory', () => {
    beforeEach(() => {
      service['createRequest'] = jasmine.createSpy().and.returnValue(
        observableOf({ paging: {} })
      );
      service.addRemovedLegs = jasmine.createSpy();
    });

    it('no page size', () => {
      service.getEditMyAccaHistory({ bets: [{}] } as any);
      expect(service['createRequest']).not.toHaveBeenCalled();
    });

    it('single page response', fakeAsync(() => {
      service.getEditMyAccaHistory({
        bets: [{ betGroupId: 2, betGroupOrder: 2 }, {}, { betGroupId: 5, betGroupOrder: 3}]
      } as any).subscribe();
      tick();

      expect(service['createRequest']).toHaveBeenCalledTimes(1);
      expect(service.addRemovedLegs).toHaveBeenCalledTimes(1);
    }));

    it('multi page response', fakeAsync(() => {
      let pagesCount = 3;
      (service['createRequest'] as any).and.callFake(() => {
        --pagesCount;
        return observableOf({
          paging: { token: pagesCount ? 'sYhfZ' : undefined }
        });
      });

      service.getEditMyAccaHistory({
        bets: [{ betGroupId: 2, betGroupOrder: 2 }, {}, { betGroupId: 5, betGroupOrder: 3}]
      } as any).subscribe();
      tick();

      expect(service['createRequest']).toHaveBeenCalledTimes(3);
      expect(service.addRemovedLegs).toHaveBeenCalledTimes(1);
    }));
  });

  it('addRemovedLegs', () => {
    spyOn(serviceHacked, 'getRemovedLegs').and.returnValue({ '123': [{}, {}, {}] });
    const data = [{ id: 123, leg: [{}, {}] }, { id: 321, leg: [] }] as any;

    service.addRemovedLegs(data, null);
    expect(data[0].leg.length).toEqual(5);
  });

  it('getRemovedLegs', () => {
    const data = [{
      id: '345',
      betGroupOrder: 0,
      betGroupId: '17',
      leg: [{ part: [{ outcome: [{ id: 'a12341'}]}]}]
    }, {
      id: '123',
      betGroupId: '7',
      betGroupOrder: 1,
      leg: [{ part: [{ outcome: [{ id: 'b12345'}]}]}]
    }, {
      id: '213',
      betGroupId: '7',
      betGroupOrder: 0,
      leg: [
        { part: [{ outcome: [{ id: 'a12345'}]}] },
        { part: [{ outcome: [{ id: 'b12345'}]}] },
        { part: [{ outcome: [{ id: 'c12345'}]}] }
      ]
    }] as any;

    expect(serviceHacked.getRemovedLegs(data)).toEqual({ 123: [{
      removedLeg: true,
      resultedBeforeRemoval: false,
      part: [{ outcome: [{ id: 'a12345'}]}]
    }, {
      removedLeg: true,
      resultedBeforeRemoval: false,
      part: [{ outcome: [{ id: 'c12345'}]}]
    }]});
  });

  it('getRemovedLegs(resultedBeforeRemoval)', () => {
    let time = 100;
    timeService.parseDateTime = jasmine.createSpy('parseDateTime').and.callFake(() => {
      time++;
      return time;
    });

    const data = [{
      id: '345',
      betGroupOrder: 0,
      betGroupId: '17',
      leg: [{ part: [{ outcome: [{ id: 'a12341'}]}]}]
    }, {
      id: '123',
      betGroupId: '7',
      betGroupOrder: 1,
      leg: [{ part: [{ outcome: [{ id: 'b12345'}]}]}]
    }, {
      id: '213',
      betGroupId: '7',
      betGroupOrder: 0,
      settledAt: '2019-03-04 11:00:45',
      leg: [
        { part: [{ outcome: [{ id: 'a12345'}]}] },
        { part: [{ outcome: [{ id: 'b12345'}]}] },
        { part: [{ outcome: [{ id: 'c12345', result: { time: '2019-03-04 10:00:45' } }] }] }
      ]
    }] as any;

    expect(serviceHacked.getRemovedLegs(data)).toEqual({
      123: [{
        removedLeg: true,
        resultedBeforeRemoval: true,
        part: [{ outcome: [{ id: 'c12345', result: { time: '2019-03-04 10:00:45' } }] }]
      }, {
        removedLeg: true,
        resultedBeforeRemoval: false,
        part: [{ outcome: [{ id: 'a12345' }] }]
      }]
    });
  });

  describe('isSingleBet', () => {
    it('should return false based on bet type', () => {
      expect(service.isSingleBet({betType: 'DBL'} as any)).toBeFalsy();
    });

    it('should return false if single bet has any removed legs (ex acca bet)', () => {
      expect(service.isSingleBet({betType: 'SGL', leg: [{removedLeg: true}]} as any)).toBeFalsy();
    });

    it('should return true if single bet has no legs', () => {
      expect(service.isSingleBet({betType: 'SGL'} as any)).toBeTruthy();
    });

    it('should return true if single bet has legs that were not removed (eg pools)', () => {
      expect(service.isSingleBet({betType: 'SGL'} as any)).toBeTruthy();
    });
  });

  describe('formToteBetEventName method should ', () => {
    let result: string;

    beforeEach(() => {
      result = service.formToteBetEventName('fooName', 'fooTime');
    });

    it( 'call getTimeFromName', () => {
      expect(filtersService.getTimeFromName).toHaveBeenCalledWith('fooName');
    });

    it( 'call getLocalHourMin', () => {
      expect(timeService.getLocalHourMin).toHaveBeenCalledWith('fooTime');
    });

    it( 'call clearEventName', () => {
      expect(filtersService.clearEventName).toHaveBeenCalledWith('fooName');
    });

    it( 'return non-empty string', () => {
      expect(result).toBeTruthy();
    });
  });
  //getLottoBetStatus
  it('it should call getLottoBetStatus', () => {
    const draws = [{ winnings: { value: '2' } }]
    const result = service.getLottoBetStatus(draws);
    expect(result).toBe('won');
  });
  it('it should call getLottoBetStatus', () => {
    const draws = [{ winnings: { value: '0' } }]
    const result = service.getLottoBetStatus(draws);
    expect(result).toBe('lost');
  });
  describe('getBetStatus method should ', () => {

    it( 'call getYCBetStatus', () => {
      spyOn(serviceHacked, 'getYCBetStatus');
      service.getBetStatus(betHistoryBet);
      expect(serviceHacked.getYCBetStatus).toHaveBeenCalledWith(betHistoryBet);
    });

    it( 'not call getYCBetStatus', () => {
      betHistoryBet.ycBet = false;

      spyOn(serviceHacked, 'getYCBetStatus');
      service.getBetStatus(betHistoryBet);
      expect(serviceHacked.getYCBetStatus).not.toHaveBeenCalled();
    });

    it( 'should handle won EW bet (All chosen runners ' +
      'got place <= than was required) - case - isWonEWPlaceBet', () => {

      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(1);

      const betStatus = service.getBetStatus({
        ycBet: false,
        legType: 'E',
        settled: 'Y',
        leg: [
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'P',
                      places: '3'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 3
                  } as any
                ]
              } as any
            ]
          } as any,
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'P',
                      places: '1'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 2
                  } as any
                ]
              } as any
            ]
          } as any
        ]
      } as any);
      expect(betStatus).toEqual('won');
    });

    it( 'should handle won EW bet (All chosen runners ' +
      'got place <= than was required) - case - winnings', () => {

      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(1);

      const betStatus = service.getBetStatus({
        ycBet: false,
        legType: 'E',
        settled: 'Y',
        winnings: { value: 1 },
        numLinesWin: '1'
      } as any);
      expect(betStatus).toEqual('won');
    });

    it( 'should handle first lost EW bet case (At least one chosen ' +
      'Runner got place > than was required)', () => {

      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(1);

      const betStatus = service.getBetStatus({
        ycBet: false,
        legType: 'E',
        settled: 'Y',
        leg: [
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'P',
                      places: '3'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 3
                  } as any
                ]
              } as any
            ]
          } as any,
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'P',
                      places: '5'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 4
                  } as any
                ]
              } as any
            ]
          } as any
        ]
      } as any);
      expect(betStatus).toEqual('lost');
    });

    it( 'should handle second lost EW bet case (At lease one chosen Runner lost)', () => {

      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(1);

      const betStatus = service.getBetStatus({
        ycBet: false,
        legType: 'E',
        settled: 'Y',
        leg: [
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'P',
                      places: '3'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 3
                  } as any
                ]
              } as any
            ]
          } as any,
          {
            part: [
              {
                outcome: [
                  {
                    result: {
                      value: 'L'
                    }
                  } as any
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 4
                  } as any
                ]
              } as any
            ]
          } as any
        ]
      } as any);
      expect(betStatus).toEqual('lost');
    });

    it( 'should handle edge case (when there is no outcome)', () => {

      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(0);

      const betStatus = service.getBetStatus({
        ycBet: false,
        legType: 'E',
        settled: 'Y',
        leg: [
          {
            part: [
              {
                eachWayTerms: [
                  {
                    eachWayPlaces: 3
                  } as any
                ]
              } as any
            ]
          } as any,
          {
            part: [
              {
                outcome: [
                ],
                eachWayTerms: [
                  {
                    eachWayPlaces: 4
                  } as any
                ]
              } as any
            ]
          } as any
        ]
      } as any);
      expect(betStatus).toEqual('lost');
    });



    it( 'return non-empty string', () => {
      const result = service.getBetStatus(betHistoryBet);

      expect(result).toBeTruthy();
    });
  });

  it('extractBetTypeReturnsParams should return object with undefined props', () => {
    const betHistoryBets ={ winnings: [{value : undefined}]}as any;
    const result = service.extractBetTypeReturnsParams(betHistoryBets);

    expect(result).toEqual({returns: undefined, refund: undefined, estReturn: undefined});
  });

  it('extractBetTypeReturnsParams should return proper data', () => {
    betHistoryBet.poolType = 'foo';
    betHistoryBet.winnings = {value: 1};
    betHistoryBet.refund = {value: 2};
    betHistoryBet.potentialPayout = {value: '3'};

    const expectedResult: IBetReturns = {returns: 1, refund: 2, estReturn: 3};
    const result = service.extractBetTypeReturnsParams(betHistoryBet);

    expect(result).toEqual(expectedResult);
  });

  it( 'getBetReturnsValue should call extractBetTypeReturnsParams', () => {
    spyOn(service, 'extractBetTypeReturnsParams').and.returnValue(betHistoryBet as any);
    service.getBetReturnsValue(betHistoryBet, 'lost');
    expect(service.extractBetTypeReturnsParams).toHaveBeenCalledWith(betHistoryBet);
  });

  it('getBetReturnsValue should return proper data', () => {
    betHistoryBet.poolType = 'foo';
    betHistoryBet.refund = {value: 2};

    const expectedResult: IBetReturnsValue = {value: 2, status: 'refund'};
    const result = service.getBetReturnsValue(betHistoryBet, 'lost');

    expect(result).toEqual(expectedResult);
  });

  it('getBetReturnsValue should return proper default data', () => {
    const bet ={...betHistoryBet};
    bet.potentialPayout=undefined;
    bet.winnings=undefined;    
    const expectedResult: IBetReturnsValue = {value: 'N/A', status: 'none'};
    const result = service.getBetReturnsValue(bet, '');

    expect(result).toEqual(expectedResult);
  });

  it('getPoolType should return "Tote" if not football', () => {
    expect(service.getPoolType('foo')).toBe('Tote');
  });

  it('getPoolType should return "Football" for "Football pool"', () => {
    expect(service.getPoolType('Football pool')).toBe('Football');
  });

  it( 'getPoolName should call getString', () => {
    service.getPoolName('fooName');
    expect(localeService.getString).toHaveBeenCalled();
  });

  it( 'getSortCode should not call getString if empty leg', () => {
    service.getSortCode([]);
    expect(localeService.getString).not.toHaveBeenCalled();
  });

  it('getSortCode should return empty string if empty leg', () => {
    expect(service.getSortCode([])).toBe('');
  });

  it('collectPoolSelections should return empty array passing empty parameter', () => {
    expect(service.collectPoolSelections([])).toEqual([]);
  });

  it('generateBetsMap should return proper map', () => {
    expect(service.generateBetsMap([betHistoryBet])).toEqual({[betHistoryBet.id]: betHistoryBet});
  });

  it('collectTotePoolLegs should call formToteBetEventName method', () => {
    spyOn(service, 'formToteBetEventName');
    serviceHacked.collectTotePoolLegs(
      detailedBetObject,
      {name: 'fooName', startTime: 'this is time string', poolPart: [betHistoryPart]},
      betHistoryOutcome
    );
    expect(service.formToteBetEventName).toHaveBeenCalledWith('fooName', 'this is time string');
  });

  it( 'collectFootballPoolLegs should call setSelection', () => {
    spyOn(serviceHacked, 'setSelection');
    serviceHacked.collectFootballPoolLegs(detailedBetObject, 'fooNameTest', '', '', '');
    expect(serviceHacked.setSelection).toHaveBeenCalledWith('fooNameTest');
  });

  it( 'collectFootballPoolLegs should call setSelection and sort', () => {
    spyOn(serviceHacked, 'setSelection');
    detailedBetObject.legs= [
        {
          name: 'leg1',
          type: ['H','D','A','B','B'],
          startTime: '',
          outcomeResult: '',
        },
        {
          name: 'leg1',
          type: ['H','D','A','B','B'],
          startTime: '',
          outcomeResult: ''
        },
        {
          name: 'leg4',
          type: ['H','D','A'],
          startTime: '',
          outcomeResult: ''
        },
        {
          name: 'leg2',
          type: ['H','D','A'],
          startTime: '',
          outcomeResult: ''
        },
        {
          name: 'leg3',
          type: ['H','D','A'],
          startTime: '',
          outcomeResult: ''
        },
      ]
    
    serviceHacked.collectFootballPoolLegs(detailedBetObject, 'fooNameTest', 'leg5', '', '');
    expect(serviceHacked.setSelection).toHaveBeenCalledWith('fooNameTest');
  });

  describe('collectLegs method should ', () => {
    let result: any;

    beforeEach(() => {
      spyOn(serviceHacked, 'createOutcomeName');
      spyOn(serviceHacked, 'setEwTerms');
      spyOn(serviceHacked, 'setLegResult');

      result = serviceHacked.collectLegs(
        betHistoryOutcome,
        price,
        betHistoryHandicap,
        '',
        betHistoryEachWayTerms
      );
    });

    it( 'call createOutcomeName', () => {
      expect(serviceHacked.createOutcomeName).toHaveBeenCalledWith(betHistoryOutcome, betHistoryHandicap);
    });

    it( 'call setEwTerms', () => {
      expect(serviceHacked.setEwTerms).toHaveBeenCalledWith(betHistoryEachWayTerms);
    });

    it( 'call setLegResult', () => {
      expect(serviceHacked.setLegResult).toHaveBeenCalledWith(outcomeResult);
    });

    it('return data', () => {
      expect(result).toBeTruthy();
    });
  });

  it( 'createOutcomeName should return outcome.name when no handicap provided', () => {
    expect(serviceHacked.createOutcomeName(betHistoryOutcome, null)).toBe('fooName');
  });

  it( 'createOutcomeName should return outcome.name when handicap value null', () => {
   const result = serviceHacked.createOutcomeName(betHistoryOutcome, {value: null});
    expect(result).toBe('fooName');
  });

  it( 'createOutcomeName should return outcome.name when handicap value ', () => {
    const result = serviceHacked.createOutcomeName(betHistoryOutcome, {value: 0.5});
     expect(result).toBe('fooName (+0.5)');
   });

  it( 'setEwTerms should return string', () => {
    expect(serviceHacked.setEwTerms(null)).toBeTruthy();
  });

  it( 'setEwTerms should modify passed object', () => {
    serviceHacked.setEwTerms(betHistoryEachWayTerms);
    expect(betHistoryEachWayTerms.eachWayPlaces).toBe('1,2,3');
  });

  it( 'setSelection should return appropriate selection sign', () => {
    expect(serviceHacked.setSelection(1)).toBe('H');
  });

  it( 'setSelection should return appropriate selection sign', () => {
    expect(serviceHacked.setSelection(3)).toBe('A');
  });

  it( 'setLegResult should return result as a string', () => {
    expect(serviceHacked.setLegResult(outcomeResult)).toBe('placed');
  });

  it( 'setLegResult should return void if not found', () => {
    expect(serviceHacked.setLegResult({confirmed: 'Y', value: 'foo'})).toBe('void');
  });

  it( 'getYCBetStatus should return status of bet', () => {
    expect(serviceHacked.getYCBetStatus(betHistoryBet)).toBe('open');
  });

  it( 'getYCBetStatus should return status of bet', () => {
    betHistoryBet.ycStatus = ycBetStatuses.lost;
    expect(serviceHacked.getYCBetStatus(betHistoryBet)).toBe('lost');
  });

  it( 'getYCBetStatus should return status of bet', () => {
    betHistoryBet.ycStatus = ycBetStatuses.won;
    expect(serviceHacked.getYCBetStatus(betHistoryBet)).toBe('won');
  });

  it( 'getYCBetStatus should return status of bet void1', () => {
    betHistoryBet.ycStatus = ycBetStatuses.void1;
    expect(serviceHacked.getYCBetStatus(betHistoryBet)).toBe('void');
  });

  it( 'getYCBetStatus should return status of bet void2', () => {
    betHistoryBet.ycStatus = ycBetStatuses.void2;
    expect(serviceHacked.getYCBetStatus(betHistoryBet)).toBe('void');
  });

  it( 'getBetReturns should call getBetReturnsValue with same params', () => {
    spyOn(service, 'getBetReturnsValue').and.callThrough();
    serviceHacked.getBetReturns(betHistoryBet, 'sthFoo');
    expect(service.getBetReturnsValue).toHaveBeenCalledWith(betHistoryBet, 'sthFoo');
  });

  it( 'getBetReturns should return expected result', () => {
    const bet ={...betHistoryBet};
    bet.winnings=undefined;
    bet.potentialPayout=undefined;
    expect(serviceHacked.getBetReturns(bet, '')).toEqual({value: 'fooString', status: 'none'});
  });

  it( 'getBetType should call getString', () => {
    serviceHacked.getBetType('foo', '');
    expect(localeService.getString).toHaveBeenCalledWith('W');
  });

  it( 'getBetType should return string value', () => {
    expect(serviceHacked.getBetType('foo', '')).toBeTruthy();
  });

  it( 'getSelectionNames should return array with one selection name', () => {
    const expectedResult = [{
      selectionName: 'fooName',
      selectionPrice: price,
      selectionStartTime: 'fooTime',
      eventName: 'fooName'
    }];

    expect(serviceHacked.getSelectionNames([betHistoryLeg], '')).toEqual(expectedResult);
  });

  it( 'getSelectionNames should return array with two selection names for Scorecast', () => {
    const betHistoryLegCopy = Object.assign({}, betHistoryLeg);
    const expectedResult = [{
      selectionName: 'fooName fooName',
      selectionPrice: price,
      selectionStartTime: 'fooTime',
      eventName: 'fooName'
    }];

    betHistoryLegCopy.legSort = {code: 'SC'};
    betHistoryLegCopy.part = [betHistoryPart, betHistoryPart];

    expect(serviceHacked.getSelectionNames([betHistoryLegCopy], '')).toEqual(expectedResult);
  });

  it( 'extendWithMeaningMinorCode should return extended bets', () => {
    const betHistoryPartCopy = Object.assign(
      {},
      betHistoryPart,
      {outcome: Object.assign({}, betHistoryOutcome, {name: 'unnamed favourite'})}
    );

    const result = serviceHacked.extendWithMeaningMinorCode([
      ({poolLeg: [{poolPart: [betHistoryPartCopy]}]}) as IBetHistoryBet
    ]);

    expect(result).toBeTruthy();
    expect(result[0].poolLeg[0].poolPart[0].outcome.outcomeMeaningMinorCode).toBe('1');
  });

  it( 'normalizeResponse should call extendWithMeaningMinorCode', () => {
    spyOn(serviceHacked, 'extendWithMeaningMinorCode');
    serviceHacked.normalizeResponse(accountHistoryResponse);
    expect(serviceHacked.extendWithMeaningMinorCode).toHaveBeenCalledWith(accountHistoryResponse.poolBet);
  });

  it( 'normalizeResponse should call executeAsync for every bet', () => {
    accountHistoryResponse.poolBet = null;

    expect((commandService.executeAsync as jasmine.Spy).calls.count()).toEqual(0);
    serviceHacked.normalizeResponse(accountHistoryResponse);
    expect((commandService.executeAsync as jasmine.Spy).calls.count()).toEqual(2);
  });

  it('normalizeResponse should exclude edited bets', fakeAsync(() => {
    const data: any = {
      bet: [{}, { settleInfoAttribute: '&lt;is_edited&gt;' }]
    };
    service['normalizeResponse'](data).then(res => {
      tick();
      expect(res.bets.length).toBe(1);
    });
  }));

  it('normalizeResponse should not exclude edited bets', fakeAsync(() => {
    const data: any = {
      bet: [{}, { settleInfoAttribute: '&lt;is_edited&gt;' }]
    };
    service['normalizeResponse'](data, false).then(res => {
      tick();
      expect(res.bets.length).toBe(2);
    });
  }));

  it( 'mapYCBets should call extendHistoryBet for every bet', () => {
    expect((yourCallHistoryBetBuilderService.extendHistoryBet as jasmine.Spy).calls.count()).toEqual(0);
    serviceHacked.mapYCBets(
      ({data: [{id: '123'}]} as IBetHistoryBet),
      ({bets: [betHistoryBet]} as IPageBets)
    );
    expect((yourCallHistoryBetBuilderService.extendHistoryBet as jasmine.Spy).calls.count()).toEqual(1);
  });

  it( 'mapYCBets should not call extendHistoryBet if YCBet not exist', () => {
    const YCBet = { data: [] } as IBetHistoryBet;
    const bets = { bets: [betHistoryBet] } as IPageBets;
    serviceHacked['mapYCBets'](YCBet, bets);
    expect((yourCallHistoryBetBuilderService.extendHistoryBet as jasmine.Spy)).not.toHaveBeenCalled();
  });

  it('getSettleType should return proper value', () => {
    expect(serviceHacked.getSettleType('open')).toBe('N');
    expect(serviceHacked.getSettleType('settled')).toBe('Y');
    expect(serviceHacked.getSettleType('foo')).toBe(null);
  });

  describe('filterByParam method should ', () => {

    beforeEach(() => {
      serviceHacked.filterByParam('twoWeeksAgoDate');
    });

    it( 'call timeService methods', () => {
      expect(timeService.dateTimeOfDayInISO).toHaveBeenCalledWith('tomorrow');
      expect(timeService.dateTimeOfDayInISO).toHaveBeenCalledWith('yesterday');
      expect(timeService.dateTimeOfDayInISO).toHaveBeenCalledWith('weekAgo');
      expect(timeService.dateTimeOfDayInISO).toHaveBeenCalledWith('twoWeeksAgo');
    });

    it( 'call filterService method 4 times', () => {
      expect((filtersService.date as jasmine.Spy).calls.count()).toBe(4);
    });
  });

  it('createRequest should call bppService.send before resolving', (done: DoneFn) => {
    serviceHacked.createRequest().subscribe(() => {
      expect(bppService.send).toHaveBeenCalled();
      done();
    });
  });

  it('createRequest should call bppService.send with url', (done: DoneFn) => {
    (bppService.send as jasmine.Spy).and.returnValue(observableOf({
      response: {}
    }));

    serviceHacked.createRequest({}, null, '/count').subscribe(() => {
      expect(bppService.send).toHaveBeenCalledWith('getBetHistory', {}, '/count');
      done();
    });
  });

  it('createRequest should call bppService.send without url', (done: DoneFn) => {
    serviceHacked.createRequest({}, null).subscribe(() => {
      expect(bppService.send).toHaveBeenCalledWith('getBetHistory', {}, undefined);
      done();
    });
  });

  it('createRequest should call callback and return as stream', (done: DoneFn) => {
    const spyFn = jasmine.createSpy('spyFn').and.returnValue(Promise.resolve(123));

    serviceHacked.createRequest(null, spyFn).subscribe((res) => {
      expect(spyFn).toHaveBeenCalledWith(jasmine.any(Object));
      expect(res).toBe(123);
      done();
    });
  });

  it('createBetObject', () => {
    service.getBetStatus = jasmine.createSpy();
    service['getBetReturns'] = jasmine.createSpy().and.returnValue({});
    service['getBetType'] = jasmine.createSpy();
    service.getPoolType = jasmine.createSpy();
    service.getPoolName = jasmine.createSpy();
    service.getSortCode = jasmine.createSpy();
    service['getSelectionNames'] = jasmine.createSpy();
    service.collectPoolSelections = jasmine.createSpy();

    const betHistory: any = [{
      leg: [{ legType: {} }],
      poolLeg: {},
      poolType: 'PT',
      poolName: 'PN',
      stake: {
        tokenValue: 1,
        poolStake: 1
      }
    }, {
      leg: [{ legType: {} }],
      poolLeg: {},
      stake: {
        tokenValue: 2,
        value: 2
      }
    }];
    const betIds: any = {};

    service.createBetObject(betHistory, betIds);

    expect(service.getBetStatus).toHaveBeenCalledTimes(2);
    expect(service['getBetReturns']).toHaveBeenCalledTimes(2);
    expect(service['getBetType']).toHaveBeenCalledTimes(2);
    expect(service.getPoolType).toHaveBeenCalledTimes(1);
    expect(service.getPoolName).toHaveBeenCalledTimes(1);
    expect(service.getSortCode).toHaveBeenCalledTimes(2);
    expect(service['getSelectionNames']).toHaveBeenCalledTimes(2);
    expect(service.collectPoolSelections).toHaveBeenCalledTimes(2);
  });

  it('getHistoryByBetGroupId', () => {
    service['createRequest'] = jasmine.createSpy().and.callFake((p1, cb) => {
      cb();
      return observableOf(null);
    });
    service['normalizeResponse'] = jasmine.createSpy();

    service.getHistoryByBetGroupId('1').subscribe();

    expect(service['createRequest']).toHaveBeenCalledTimes(1);
    expect(service['normalizeResponse']).toHaveBeenCalledTimes(1);
  });

  describe('calculateTotals', () => {
    it('should return proper calculation for zero params', () => {
      expect(service.calculateTotals(0, 0)).toEqual({
        totalStakes: '$0',
        totalReturns: '$0',
        profit: '$0',
        iconClass: '',
        label: ''});
    });

    it('should return proper calculation for profit', () => {
      expect(service.calculateTotals(1, 3)).toEqual({
        totalStakes: '$1',
        totalReturns: '$3',
        profit: '$2',
        iconClass: 'arrow-right-up',
        label: ''});
    });

    it('should return proper calculation for loss', () => {
      expect(service.calculateTotals(3, 1, 'label')).toEqual({
        totalStakes: '$3',
        totalReturns: '$1',
        profit: '$-2',
        iconClass: 'arrow-left-down',
        label: 'fooString'});
    });
  });

  describe('#buildSwitchers', () => {
    it('should set switchers', () => {
      const switchers = service.buildSwitchers(() => {});
      expect(service.regularType).toBeDefined();
      expect(service.lottoType).toBeDefined();
      expect(service.poolType).toBeDefined();
      expect(switchers).toEqual([
        service.regularType,
        service.lottoType,
        service.poolType
      ]);
    });
  });
  describe('#getSwitcher', () => {
    it('should return requested switcher', () => {
      service.buildSwitchers(() => {});
      const switcher = service.getSwitcher('regularType');
      expect(switcher).toEqual(service.regularType);
    });

    it('should call onСlick callbacks', () => {
      const onClickCb = jasmine.createSpy();
      const switchers = service.buildSwitchers(onClickCb);
      switchers.forEach((switcher) => {
        switcher.onClick();
      });
      expect(onClickCb).toHaveBeenCalledTimes(3);
    });
  });

  describe('getPartsResult', () => {
    let results;
    describe('should return first result code if results list contains', () => {
      it('a single non "LVW-" code', () => { results = ['P']; });
      it('combination of non "LVW-" codes', () => { results = ['P', 'N']; });
      describe('combination of non "LVW-" and "LVW-" codes', () => {
        it('(P,L,-,V,W)', () => { results = ['P', 'L', '-', 'V', 'W']; });
        it('(L,-,V,W,P)', () => { results = ['L', '-', 'V', 'W', 'P']; });
      });
      afterEach(() => { expect(service.getPartsResult(results)).toEqual(results[0]); });
    });

    describe('should return "L" if results list contains', () => {
      it('only L code', () => { results = ['L']; });
      it('several L codes', () => { results = ['L', 'L']; });
      it('L, W, V and - codes', () => { results = ['W', 'L', '-', 'V']; });
      afterEach(() => { expect(service.getPartsResult(results)).toEqual('L'); });
    });

    describe('should return "V" if results list contains', () => {
      it('only V code', () => { results = ['V']; });
      it('several V codes', () => { results = ['V', 'V']; });
      it('W, L and - codes', () => { results = ['W', 'V', '-']; });
      afterEach(() => { expect(service.getPartsResult(results)).toEqual('V'); });
    });

    describe('should return "-" if results list contains', () => {
      it('only - code', () => { results = ['-']; });
      it('only several - codes', () => { results = ['-', '-']; });
      it('W and - codes', () => { results = ['W', '-']; });
      afterEach(() => { expect(service.getPartsResult(results)).toEqual('-'); });
    });

    describe('should return "W" if results list contains', () => {
      it('only W code', () => { results = ['W']; });
      it('only several W codes', () => { results = ['W', 'W']; });
      afterEach(() => { expect(service.getPartsResult(results)).toEqual('W'); });
    });
  });

  it('should makeSafeCall', () => {
    userService.isInShopUser.and.returnValue(true);
    let result;

    const observableWrapperMock: any = {};

    result = service.makeSafeCall(observableWrapperMock);

    expect(result).toBeDefined();
    expect(result.subscribe).toBeDefined();

    userService.isInShopUser.and.returnValue(false);

    result = service.makeSafeCall(observableWrapperMock);

    expect(result).toEqual(observableWrapperMock);
  });

  describe('setBybLegStatus', () => {
    it('shoud set status', () => {
      const bet: any = { source: 'f' };
      const leg: any = { eventEntity: { eventStatusCode: 'A' }, status: 'suspended' };
      service.setBybLegStatus(bet, leg);
      expect(leg.status).toBe('open');
    });

    it('shoud not set status', () => {
      const bet: any = {};
      const leg: any = { eventEntity: { }, status: 'suspended' };
      service.setBybLegStatus(bet, leg);
      expect(leg.status).toBe('suspended');
    });
  });
  describe('#getCelebrationBanner', () => {
    it('getCelebrationBanner with correct values', () => {
      expect(service.getCelebrationBanner()).not.toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
    it('config as null', () => {
      spyOn(service, 'getCelebrationBannerFromSiteCore');
      service.getCelebrationBanner();
      expect(service.getCelebrationBanner()).not.toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
    it('config with CelebratingSuccess as null', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({CelebratingSuccess: null}));
      expect(service.getCelebrationBanner()).toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
    it('getCelebrationBannerFromSiteCore with error response', () => {
      spyOn(service, 'getCelebrationBannerFromSiteCore');
      service.getCelebrationBannerFromSiteCore = jasmine.createSpy('getCelebrationBannerFromSiteCore').and.returnValue(throwError({ status: 404 }));
      expect(service.getCelebrationBanner()).not.toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
    it('getCelebrationBannerFromSiteCore with empty response', () => {
      spyOn(service, 'getCelebrationBannerFromSiteCore');
      service.getCelebrationBannerFromSiteCore = jasmine.createSpy('getCelebrationBannerFromSiteCore').and.returnValue(observableOf([{"teasers": null}]));
      expect(service.getCelebrationBanner()).not.toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
    it('getCelebrationBannerFromSiteCore with null response', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        CelebratingSuccess: {
          cashoutMessage: "YOU HAVE CASHED OUT: {amount}!!",
          celebrationBannerURL: "{6C768A64-74F8-46FE-A380-9DE3E51C2EBA}",
          celebrationMessage: "CONGRATS!",
          displayCelebrationBanner: true,
          duration: 48,
          winningMessage: "YOU HAVE WON: {amount}!!"
        }
      }));
      service.getCelebrationBannerFromSiteCore = jasmine.createSpy('getCelebrationBannerFromSiteCore').and.returnValue(observableOf(null));
      expect(service.getCelebrationBanner()).not.toEqual({
        congratsBannerImage: '',
        displayCelebrationBanner: false,
        celebrationMessage: '',
        winningMessage: '',
        cashoutMessage: '',
        duration: 0
      });
    });
  });
});
