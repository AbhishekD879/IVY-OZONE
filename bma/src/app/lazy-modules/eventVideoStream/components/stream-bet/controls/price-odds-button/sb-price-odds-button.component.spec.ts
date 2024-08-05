
import { SbPriceOddsButtonComponent } from './sb-price-odds-button.component';


describe('SbPriceOddsButtonComponent', () => {
  let component: SbPriceOddsButtonComponent;

  let userService, gtmService, pubsubService,
    betSlipSelectionsData, commandService, routingState, gtmTrackingService, sportEventHelperService, localeService, elementRef;

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

    elementRef = {
      nativeElement: {parentNode : {style: {backgroundColor: "#78b200"}}}
    };

    component = new SbPriceOddsButtonComponent(pubsubService, localeService, commandService, sportEventHelperService, elementRef,gtmTrackingService,routingState);
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
      component.isStreamAndBet = true;
      component.onPriceOddsButtonClick(event);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('IS_ADDTOBETSLIP_IN_PROCESS');
    });

    it('should execute async check', () => {
      spyOn(component, 'formSelectionData').and.callThrough();
      commandService.executeAsync.and.returnValue(Promise.resolve(true));
      component.isStreamAndBet = true;
      component.onPriceOddsButtonClick(event);

      expect(event.stopPropagation).toHaveBeenCalled();
      expect(component.formSelectionData).not.toHaveBeenCalled();
      expect(commandService.executeAsync).toHaveBeenCalledWith('IS_ADDTOBETSLIP_IN_PROCESS');
    });
   
  });

  it('should call formSelectionData', () => {
    spyOn<any>(component, 'getCorrectPriceType').and.callThrough();
    gtmTrackingService.detectTracking.and.returnValue({
      location: 'test location',
      module: 'test module'
    });
    component.sbPosition = 10;
    component.outcome = {
      id: 315,
      outcomeMeaningMajorCode: '1',
      prices: [],
      modifiedPrice: {id: 602},
      isFavourite: false
    } as any;
    component.event = {
      id: 523,
      categoryId: '21',
      categoryName: 'horseracing',
      isStarted: true,
      eventIsLive: true,
      name: 'test',
      typeName: 'testNmae',
      typeId: '5123'
    } as any;
    component.market = {
      id: 7,
      name: 'Match Result',
      isLpAvailable: true
    } as any;
    component.formSelectionData();
    expect(component['getCorrectPriceType']).toHaveBeenCalled()
  });

  it('should call formSelectionData - GTM object', () => {
    spyOn<any>(component, 'getCorrectPriceType').and.callThrough();
    gtmTrackingService.detectTracking.and.returnValue({
      location: 'test location',
      module: 'next races'
    });
    component.sbPosition = 10;
    component.outcome = {
      id: 315,
      outcomeMeaningMajorCode: '1',
      prices: [],
      modifiedPrice: {id: 602},
      isFavourite: false
    } as any;
    component.event = {
      id: 523,
      categoryId: '39',
      categoryName: 'horseracing',
      isStarted: true,
      eventIsLive: false,
      name: 'test',
      typeName: 'testNmae',
      typeId: '5123'
    } as any;
    component.market = {
      id: 7,
      name: 'Match Result',
      isLpAvailable: true,
      isSCAvailable: true
    } as any;
    component.formSelectionData();
    expect(component['getCorrectPriceType']).not.toHaveBeenCalled()
  });

  it('should call formSelectionData', () => {
    spyOn<any>(component, 'getCorrectPriceType').and.callThrough();
    component.outcome = {
      id: 315,
      outcomeMeaningMajorCode: '1',
      prices: [{handicapValueDec: '3' }],
      modifiedPrice: {id: 602}
    } as any;
    component.event = {
      id: 523,
      categoryId: '21',
      categoryName: 'horseracing',
      isStarted: true,
      eventIsLive: true,
      name: 'test',
      typeName: 'testNmae',
      typeId: '5123'
    } as any;
    component.market = {
      id: 7,
      name: 'Match Result',
      rawHandicapValue: '3',
      isLpAvailable: true
    } as any;
    component.formSelectionData();
    expect(component['getCorrectPriceType']).toHaveBeenCalled()
  });
 
});
