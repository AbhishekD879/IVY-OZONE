import { NextRacesToBetslipComponent } from './nextraces-to-betslip.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import {
  betPlacedOnHR,
  mainBetSingleMock,
  mostRacingTipsWithOutHorsesMock,
  mostTippedHorsesEventsMock,
  quickBetPlacedOnHR
} from '@app/lazy-modules/racingPostTip/mock/racing-pot-tip-mock';

describe('NextRacesToBetslipComponent', () => {
  let changeDetectorRef,
    routingHelperService,
    router,
    gtmService,
    pubSubService,
    betSlipService,
    locale,
    nextRacesHomeService;

  const isNextRaces = {
    isTipPresent: false,
    nextRaces: mostTippedHorsesEventsMock as any
  };
  const mockString = 'Flat Turf';
  let component: NextRacesToBetslipComponent;
  beforeEach(() => {
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    router = jasmine.createSpyObj(['navigateByUrl']);
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb && cb(isNextRaces)),
      API: pubSubApi
    };
    nextRacesHomeService = {
      trackNextRace: jasmine.createSpy('trackNextRace'),
      isItvEvent: jasmine.createSpy('isItvEvent'),
      getGoing: jasmine.createSpy('getGoing'),
      getDistance: jasmine.createSpy('getDistance')
    };
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue(mockString)
    };
    betSlipService = jasmine.createSpy('betslipService');

    component = new NextRacesToBetslipComponent(
      changeDetectorRef,
      routingHelperService,
      router,
      gtmService,
      pubSubService,
      betSlipService,
      locale,
      nextRacesHomeService
    );
  });
  describe('ngOnInit', () => {
    it('should init component when is tip present is false', () => {
      component['getNextRaces'] = jasmine.createSpy('getNextRaces');
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component['getNextRaces']).toHaveBeenCalled();
    });
    it('should init component when istip present is true', () => {
      component['getNextRaces'] = jasmine.createSpy('getNextRaces');
      const NextRaces = {
        isTipPresent: true,
        nextRaces: mostTippedHorsesEventsMock as any
      };
      pubSubService.subscribe.and.callFake((a, b, cb: Function) => {
        if (b === 'IS_TIP_PRESENT') {
          cb(NextRaces);
        }
      });
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
      expect(component['getNextRaces']).not.toHaveBeenCalled();
    });
  });

  describe('ngOnchanges', () => {
   it('ngOnChanges: should not call getNextraces method', () => {
    component['getNextRaces'] = jasmine.createSpy('getNextRaces');
    component.ngOnChanges({});
    expect(component['getNextRaces']).not.toHaveBeenCalled();
   });

   it('ngOnChanges: should not call getNextraces method with racingpostdata empty', () => {
     component.racingPostData= null;
     component['getNextRaces'] = jasmine.createSpy('getNextRaces');
    component.ngOnChanges({
      isNextRacesData: {
        previousValue:null, 
        firstChange:true, 
        currentValue: true,
        isFirstChange: () => false
      }
    });
    expect(component['getNextRaces']).not.toHaveBeenCalled();
   });

   it('ngOnChanges: should not call getNextraces method with empty arguments', () => {
    component['getNextRaces'] = jasmine.createSpy('getNextRaces');
      component.racingPostData= [];
     component.ngOnChanges(null);
     expect(component['getNextRaces']).not.toHaveBeenCalled();
   });

   it('ngOnChanges: should call getNextraces method', () => {
    component['getNextRaces'] = jasmine.createSpy('getNextRaces');
      component.racingPostData= [];
     component.ngOnChanges({
       isNextRacesData: {
         previousValue:null, 
         firstChange:true, 
         currentValue: true,
         isFirstChange: () => true
       }
     });
     expect(component['getNextRaces']).toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('ngOnDestroy: should unsubscribe from next races', function () {
      component['upCellSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();
      expect(component['upCellSubscription'].unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('isTipPresent');
    });
  });

  describe('getNextRaces', () => {
    it('#getRacingPostTipData it should get racing post data when mainbet when BetPlacedOnHR is true', () => {
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component['trackForNextRaces'] = jasmine.createSpy('trackForNextRaces');
      component.multiReceipts = mostRacingTipsWithOutHorsesMock as any;
      component.mainBetReceipts = mainBetSingleMock as any;
      component.quickBetReceipt = { categoryId: '21', eventId: 1 } as any;
      component['isBetPlacedOnHR'] = true;
      component['getNextRaces'](mostTippedHorsesEventsMock as any);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component['checkForBetsData']).toHaveBeenCalled();
      expect(component['trackForNextRaces']).toHaveBeenCalled();
    });
    it('#getRacingPostTipData it should get racing post data when quickbet when BetPlacedOnHR is true', () => {
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component.quickBetReceipt = quickBetPlacedOnHR as any;
      component['trackForNextRaces'] = jasmine.createSpy('trackForNextRaces');
      component.mainBetReceipts = [];
      component['isBetPlacedOnHR'] = true;
      component.multiReceipts = [];
      component.racingPostData = mostTippedHorsesEventsMock as any;
      component['getNextRaces'](null);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(component['checkForBetsData']).toHaveBeenCalled();
      expect(component['trackForNextRaces']).toHaveBeenCalled();
    });
    it('#getRacingPostTipData it should get racing post data when quickbet when BetPlacedOnHR is false', () => {
      component['checkForBetsData'] = jasmine.createSpy('checkForBetsData');
      component['trackForNextRaces'] = jasmine.createSpy('trackForNextRaces');
      component.quickBetReceipt = quickBetPlacedOnHR as any;
      component['isBetPlacedOnHR'] = false;
      component.multiReceipts = [];
      component['getNextRaces'](mostTippedHorsesEventsMock as any);
      expect(changeDetectorRef.markForCheck).not.toHaveBeenCalled();
      expect(component['trackForNextRaces']).not.toHaveBeenCalled();
      expect(component['checkForBetsData']).toHaveBeenCalled();
    });
  });
  it('trackForNextRaces', () => {
    component['trackForNextRaces']();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'bet receipt',
      eventAction: 'rendered',
      eventLabel: 'next races'
    }));
  });
  it('#getGoing', () => {
    component.getGoing('G');

    expect(nextRacesHomeService.getGoing).toHaveBeenCalledWith('G');
  });

  it('#getDistance', () => {
    component.getDistance('Distance');

    expect(nextRacesHomeService.getDistance).toHaveBeenCalledWith('Distance');
  });
  describe('#getRaceType', () => {
    it('should return race type with going', () => {
      locale.getString.and.returnValue('Flat Turf');
      const result = component.getRaceType('FLT');

      expect(result).toEqual('Flat Turf');
    });

    it('should return epty string when key not found', () => {
      locale.getString.and.returnValue('KEY_NOT_FOUND');
      const result = component.getRaceType('Flat Turf');

      expect(result).toEqual('');
    });
  });
  describe('formEdpUrl', () => {
    it('should create EDP url', () => {
      component.formEdpUrl(({ id: '1' } as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
    });
  });
  it('#trackByEvents', () => {
    const result = component.trackByEvents(1, ({
      id: '12345',
      name: 'name',
      categoryId: '12'
    } as any));

    expect(result).toEqual('1_12345_name_12');
  });
  it('#trackEvent', () => {
    spyOn(component.closeFn, 'emit');
    const entity = { name: '12:00 Southwell' } as any;
    component.trackEvent(entity);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'bet receipt',
      eventAction: 'navigation',
      eventLabel: 'next races'
    }));
    expect(component.closeFn.emit).toHaveBeenCalled();
    expect(router.navigateByUrl).toHaveBeenCalled();
  });
  describe('#checkForBetsData', () => {
    beforeEach(() => {
      component['checkForBetType'] = jasmine.createSpy('checkForBetType');
    });

    it('should set true if betData exists', () => {
      const betData = betPlacedOnHR as any;
      component['checkForBetsData'](betData);
      expect(component['checkForBetType']).toHaveBeenCalled();
    });

    it('should set true if betData is empty', () => {
      const betData = [] as any;
      component['checkForBetsData'](betData);
      expect(component['isBetPlacedOnHR']).toBe(true);
    });
  });
  describe('#checkForBetType', () => {
    it('should check for not tricast and forecast and isbetplaced on hr is true', () => {
      const betData = betPlacedOnHR as any;
      component['checkForBetType'](betData[0]);
      expect(component['isBetPlacedOnHR']).toBe(true);
    });
    it('should check for tricast and isbetplaced on hr is false', () => {
      const betData = betPlacedOnHR as any;
      betData[0].combiType = 'TRICAST';
      component['checkForBetType'](betData[0]);
      expect(component['isBetPlacedOnHR']).toBe(false);
    });
    it('should check for forecast and isbetplaced on hr is false', () => {
      const betData = betPlacedOnHR as any;
      betData[0].combiType = 'FORECAST';
      component['checkForBetType'](betData[0]);
      expect(component['isBetPlacedOnHR']).toBe(false);
    });
  });
});
