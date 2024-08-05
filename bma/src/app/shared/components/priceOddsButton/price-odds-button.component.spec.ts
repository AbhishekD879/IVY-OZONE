import { fakeAsync, tick } from '@angular/core/testing';

import { PriceOddsButtonComponent } from './price-odds-button.component';

describe('PriceOddsButtonComponent', () => {
  let component: PriceOddsButtonComponent;

  let userService, gtmService, pubsubService,
    betSlipSelectionsData, commandService, routingState, gtmTrackingService, sportEventHelperService, localeService, scorecastDataService;

  const event = {
    stopPropagation: jasmine.createSpy('stopPropagation')
  } as any;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubsubService = {
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION'
      }
    };
    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { return 'data'},
    }
    betSlipSelectionsData = {
      count: () => 1
    };
    userService = {
      oddsFormat: {}
    };
    commandService = {
      API: {IS_ADDTOBETSLIP_IN_PROCESS: 'IS_ADDTOBETSLIP_IN_PROCESS'},
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(false))
    };
    routingState = jasmine.createSpyObj(['getCurrentSegment']);
    gtmTrackingService = {
      detectTracking: jasmine.createSpy('detectTracking')
    };
    sportEventHelperService = jasmine.createSpyObj(['isOutrightEvent', 'isSpecialEvent']);

    localeService = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('Success')
    };

    component = new PriceOddsButtonComponent(userService, gtmService, pubsubService, commandService,
      betSlipSelectionsData, routingState, gtmTrackingService, sportEventHelperService, localeService,scorecastDataService);
    component.event = {
      id: 523,
      categoryId: '19',
      categoryName: 'football',
      isStarted: true,
      eventIsLive: true,
      name: 'Dynamo vs Liverpool',
      typeName: 'Competition',
      typeId: '5123'
    } as any;
    component.market = {
      id: 7,
      name: 'Match Result',
      rawHandicapValue: '3'
    } as any;
    component.outcome = {
      id: 315,
      outcomeMeaningMajorCode: '1',
      prices: [
        {
          handicapValueDec: '3',
          priceType: 'LP'
        }
      ],
      modifiedPrice: {id: 602}
    } as any;
    component.sbPosition = 1;
  });

  it ('ngOnInit should subscribe and Update Prices', () => {
    component.outcome.prices[0].priceDen = 1;
    component.outcome.prices[0].priceNum = 1;
    component.handicapVal = '1,';
    component.correctName='2';

    pubsubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
      channelFunction({
        priceDen: 100,
        priceNum: 101
      });

      expect(component.outcome.prices[0].priceDen).toEqual(100);
      expect(component.outcome.prices[0].priceNum).toEqual(101);
      expect(component.handicapVal).toEqual('1');
      expect(component.showCorrectScore).toEqual(true);
    });

    component.ngOnInit();
  });

  it ('ngOnInit should subscribe and Update Prices when handicap value is null', () => {
    component.outcome.prices[0].priceDen = 1;
    component.outcome.prices[0].priceNum = 1;
    component.handicapVal = '';

    pubsubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
      channelFunction({
        priceDen: 100,
        priceNum: 101
      });

      expect(component.outcome.prices[0].priceDen).toEqual(100);
      expect(component.outcome.prices[0].priceNum).toEqual(101);
      expect(component.handicapVal).toEqual('');

    });

    component.ngOnInit();
  });

  it ('ngOnInit should subscribe but not Update Prices', () => {
    delete component.outcome.prices;

    pubsubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
      channelFunction({
        priceDen: 100,
        priceNum: 101
      });

      expect(component.outcome.prices).toEqual(undefined);
    });

    component.ngOnInit();
  });

  it ('ngOnInit should subscribe but not Update Prices', () => {
    component.outcome.prices = [];

    pubsubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
      channelFunction({
        priceDen: 100,
        priceNum: 101
      });

      expect(component.outcome.prices).toEqual([]);
    });

    component.ngOnInit();
  });

  it ('ngOnDestroy shoud unsubscribe on destroy', () => {
    component.ngOnDestroy();

    expect(pubsubService.unsubscribe).toHaveBeenCalled();
  });

  it('showOddsPriceValue should be called', () => {
    const showVal = true;
    component['showOddsPriceValue'](showVal);
    expect(component.showSuspendValue).toBe(true);
  });

  describe('@onPriceOddsButtonClick', () => {
    it('should execute async check', () => {
      component.onPriceOddsButtonClick(event);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('IS_ADDTOBETSLIP_IN_PROCESS');
    });

    it('after check should add to betslip if not in progress', fakeAsync(() => {
      component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
      component.onPriceOddsButtonClick(event);
      tick();

      expect(component['addToBetSlip']).toHaveBeenCalledWith(event);
    }));

    it('after check should not add to betslip if still in progress', fakeAsync(() => {
      component['addToBetSlip'] = jasmine.createSpy('addToBetSlip');
      commandService.executeAsync.and.returnValue(Promise.resolve(true));
      component.onPriceOddsButtonClick(event);
      tick();

      expect(component['addToBetSlip']).not.toHaveBeenCalledWith(event);
    }));
  });

  describe('@addToBetSlip', () => {

    beforeEach(() => {
      gtmTrackingService.detectTracking.and.returnValue({
        location: 'test location',
        module: 'test module'
      });
      sportEventHelperService.isOutrightEvent.and.returnValue(true);
      sportEventHelperService.isSpecialEvent.and.returnValue(true);
    });

    it('should add bet to betslip - priceType LP', () => {
      component.market.isLpAvailable = true;
      component.market.isSCAvailable = true;
      component['addToBetSlip'](event);

      const expectedObject = [
        {
          eventIsLive: true,
          outcomes: [{
            id: 315,
            outcomeMeaningMajorCode: '1',
            prices: [{handicapValueDec: '3', priceType: 'LP'}],
            modifiedPrice: {id: 602}
          }],
          typeName: 'Competition',
          price: {handicapValueDec: '3', priceType: 'LP'},
          handicap: {type: '1', raw: '3'},
          goToBetslip: false,
          modifiedPrice: {id: 602},
          eventId: 523,
          isOutright: true,
          isSpecial: true,
          GTMObject: {
            categoryID: '19',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {location: 'test location', module: 'test module'},
            betData: {
              name: 'Dynamo vs Liverpool',
              category: '19',
              variant: '5123',
              brand: 'Match Result',
              dimension60: '523',
              dimension61: 315,
              dimension62: 1,
              dimension63: 0,
              dimension64: 'test location',
              dimension65: 'test module',
              dimension94: component.sbPosition,
              dimension177: 'show',
              dimension180: 'normal'
            }
          },
          details: jasmine.objectContaining({
            isSPLP: false,
            info: jasmine.objectContaining({ isStarted: true })
          }),
          eventName: 'Dynamo vs Liverpool'
        }
      ];

      expect(sportEventHelperService.isOutrightEvent).toHaveBeenCalledWith(jasmine.any(Object));
      expect(sportEventHelperService.isSpecialEvent).toHaveBeenCalledWith(jasmine.any(Object), true);
      expect(pubsubService.publishSync).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
    });

    it('should add bet to betslip - priceType for virtuals', () => {
      component.market.isLpAvailable = true;
      component.market.isSCAvailable = true;
      component.event.categoryId = '39';
      gtmTrackingService.detectTracking.and.returnValue({
        location: 'test location',
        module: 'next races'
      });
      component['addToBetSlip'](event);

      const expectedObject = [
        {
          eventIsLive: true,
          outcomes: [{
            id: 315,
            outcomeMeaningMajorCode: '1',
            prices: [{handicapValueDec: '3', priceType: 'LP'}],
            modifiedPrice: {id: 602}
          }],
          typeName: 'Competition',
          price: {handicapValueDec: '3', priceType: 'LP'},
          handicap: {type: '1', raw: '3'},
          goToBetslip: false,
          modifiedPrice: {id: 602},
          eventId: 523,
          isOutright: true,
          isSpecial: true,
          GTMObject: {
            categoryID: '39',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {location: 'test location', module: 'next races'},
            betData: {
              name: 'Dynamo vs Liverpool',
              category: '39',
              variant: '5123',
              brand: 'Match Result',
              dimension60: '523',
              dimension61: 315,
              dimension62: 1,
              dimension63: 0,
              dimension64: 'test location',
              dimension65: 'next races',
              dimension94: component.sbPosition,
              dimension177: 'show',
              dimension180: 'virtual'
            }
          },
          details: jasmine.objectContaining({
            isSPLP: false,
            info: jasmine.objectContaining({ isStarted: true })
          }),
          eventName: 'Dynamo vs Liverpool'
        }
      ];

      expect(sportEventHelperService.isOutrightEvent).toHaveBeenCalledWith(jasmine.any(Object));
      expect(sportEventHelperService.isSpecialEvent).toHaveBeenCalledWith(jasmine.any(Object), true);
      expect(pubsubService.publishSync).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
    });

    it('should add bet to betslip - priceType SP', () => {
      component.eventQuickSwitch = false;
      component.goToBetslip = true;
      component.market.isSCAvailable = false;
      betSlipSelectionsData.count = () => 0;
      component.market = {
        id: 7,
        name: 'Match Result'
      } as any;
      component.outcome = {
        id: 315,
        outcomeMeaningMajorCode: '1'
      } as any;
      component['addToBetSlip'](event);

      const expectedObject = [
        {
          eventIsLive: true,
          outcomes: [{prices: [], id: 315, outcomeMeaningMajorCode: '1'}],
          typeName: 'Competition',
          price: {priceType: 'SP'},
          handicap: undefined,
          goToBetslip: true,
          modifiedPrice: undefined,
          eventId: 523,
          isOutright: true,
          isSpecial: true,
          GTMObject: {
            categoryID: '19',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {location: 'test location', module: 'test module'},
            betData: {
              name: 'Dynamo vs Liverpool',
              category: '19',
              variant: '5123',
              brand: 'Match Result',
              dimension60: '523',
              dimension61: 315,
              dimension62: 1,
              dimension63: 0,
              dimension64: 'test location',
              dimension65: 'test module',
              dimension94: component.sbPosition,
              dimension177: 'No show',
              dimension180: 'normal'
            }
          },
          details: jasmine.objectContaining({
            isSPLP: false,
            info: jasmine.objectContaining({ isStarted: true })
          }),
          eventName: 'Dynamo vs Liverpool'
        }
      ];

      expect(pubsubService.publishSync).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
    });

    it(`should 'detectTracking' with current segment`, () => {
      routingState.getCurrentSegment.and.returnValue('segment');
      component.gtmModuleTitle = 'ModuleTitle';

      component['addToBetSlip'](event);

      expect(component['gtmTrackingService'].detectTracking)
        .toHaveBeenCalledWith('ModuleTitle', 'segment', component.event, component.market, undefined);
    });

    it('should add bet to betslip - priceType SP with not started, event.originalName, market.marketname', () => {
      component.eventQuickSwitch = false;
      component.goToBetslip = true;
      component.market.isSCAvailable = false;
      component['env'] = {
        BYB_CONFIG: {
          HR_YC_EVENT_TYPE_ID: '5123'
        }
      } as any;
      betSlipSelectionsData.count = () => 0;
      component.event = {
        id: 523,
        categoryId: 19,
        originalName: 'original name',
        isStarted: true,
        eventIsLive: false,
        name: 'Dynamo vs Liverpool',
        typeName: 'Competition',
        typeId: '5123'
      } as any;
      component.market = {
        id: 7,
        marketName: 'market name field',
        name: 'Match Result'
      } as any;
      component.outcome = {
        prices: [],
        id: 315,
        outcomeMeaningMajorCode: '1'
      } as any;
      component['addToBetSlip'](event);

      const expectedObject = [
        {
          eventIsLive: false,
          outcomes: [{prices: [], id: 315, outcomeMeaningMajorCode: '1'}],
          typeName: 'Competition',
          price: {priceType: 'SP'},
          handicap: undefined,
          goToBetslip: true,
          modifiedPrice: undefined,
          eventId: 523,
          isOutright: true,
          isSpecial: true,
          GTMObject: {
            categoryID: '19',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {location: 'test location', module: 'test module'},
            betData: {
              name: 'original name',
              category: '19',
              variant: '5123',
              brand: 'market name field',
              dimension60: '523',
              dimension61: 315,
              dimension62: 0,
              dimension63: 1,
              dimension64: 'test location',
              dimension65: 'test module',
              dimension94: component.sbPosition,
              dimension177: 'No show',
              dimension180: 'normal'
            }
          },
          details: jasmine.objectContaining({
            isSPLP: false,
            info: jasmine.objectContaining({ isStarted: true })
          }),
          eventName: 'original name'
        }
      ];

      expect(pubsubService.publishSync).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
    });
    it('should add bet to betslip - for quick switch', () => {
      component.eventQuickSwitch = true;
      component.goToBetslip = true;
      component.market.isSCAvailable = false;
      component['env'] = {
        BYB_CONFIG: {
          HR_YC_EVENT_TYPE_ID: '5123'
        }
      } as any;
      betSlipSelectionsData.count = () => 0;
      component.event = {
        id: 523,
        categoryId: 19,
        originalName: 'original name',
        isStarted: true,
        eventIsLive: false,
        name: 'Dynamo vs Liverpool',
        typeName: 'Competition',
        typeId: '5123'
      } as any;
      component.market = {
        id: 7,
        marketName: 'market name field',
        name: 'Match Result'
      } as any;
      component.outcome = {
        prices: [],
        id: 315,
        outcomeMeaningMajorCode: '1'
      } as any;
      component['addToBetSlip'](event);


      const expectedObject = [
        {
          eventIsLive: false,
          outcomes: [{ prices: [], id: 315, outcomeMeaningMajorCode: '1' }],
          typeName: 'Competition',
          price: { priceType: 'SP' },
          handicap: undefined,
          goToBetslip: true,
          modifiedPrice: undefined,
          eventId: 523,
          isOutright: true,
          isSpecial: true,
          GTMObject: {
            categoryID: '19',
            typeID: '5123',
            eventID: '523',
            selectionID: '315',
            tracking: {
              location: 'events switcher-test location', module: 'test module'
            },
            betData: {
              name: 'original name',
              category: '19',
              variant: '5123',
              brand: 'market name field',
              dimension60: '523',
              dimension61: 315,
              dimension62: 0,
              dimension63: 1,
              dimension64: 'events switcher-test location',
              dimension65: 'test module',
              dimension94: component.sbPosition,
              dimension177: 'No show',
              dimension180: 'normal'
            }
          },
          details: jasmine.objectContaining({
            isSPLP: false,
            info: jasmine.objectContaining({ isStarted: true })
          }),
          eventName: 'original name'
        }
      ];

      expect(pubsubService.publishSync).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', expectedObject);
    });
  });
});
