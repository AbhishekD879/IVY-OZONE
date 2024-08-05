import { CashoutPanelComponent } from './cashout-panel.component';
import { of as observableOf } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { IBetHistoryPart } from '../../models/bet-history.model';
import { CASHOUT_SUSPENDED } from '../cashOutMessaging/cash-out-message.constants';
import { cashoutConstants } from '../../constants/cashout.constant';

describe('CashoutPanelComponent', () => {
  let component: CashoutPanelComponent;
  let cashoutPanelService;
  let pubsub;
  let timeService,cmsService;

  const betLocation: string = 'betLocation';
  const bet: any = {
    eventSource: {
      partialCashOutPercentage: 5,
      leg: [{ 'eventEntity': { 'eventIsLive': true } }],
      cashoutValue: 'CASHOUT_SELN_NO_CASHOUT'
    },
    location: 'location'
  };
  const data: any[] = [
    {
      eventSource: {
        errorDictionary: 'errorDictionary',
        partialCashOutPercentage: 4,
        partialCashoutAvailable: 'partialCashoutAvailable',
        isCashOutUnavailable: false
      },
      location: 'location'
    }
  ];

  beforeEach(() => {
    cashoutPanelService = {
      isButtonShown: jasmine.createSpy(),
      isCashOutSuspendedValue: jasmine.createSpy(),
      isPartialAvailable: jasmine.createSpy(),
      getButtonState: jasmine.createSpy(),
      getStateConfig: jasmine.createSpy(),
      doCashOut: jasmine.createSpy(),
      setPartialState: jasmine.createSpy()
    };
    pubsub = {
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        CASHOUT_COUNTDOWN_TIMER: 'CASHOUT_COUNTDOWN_TIMER',
        IS_LIVE: 'IS_LIVE'
      }
    };
    timeService = jasmine.createSpyObj(['countDownTimer']);
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        cashOutMessaging: {
          enable: true
        },
        HorseRacingBIR: {
          marketsEnabled: ['win or each Way']
        }
      }))
    };

    component = new CashoutPanelComponent(
      cashoutPanelService,
      pubsub,
      timeService,
      cmsService
    );

    component.bet = bet;
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('isButtonShown', () => {
    component.betLocation = betLocation;
    // eslint-disable-next-line
    const isButtonShownInit = component.isButtonShown;

    expect(cashoutPanelService.isButtonShown).toHaveBeenCalledWith(component.bet.eventSource, component.betLocation);
  });

  it('isPartialAvailable', () => {
    // eslint-disable-next-line
    const isPartialAvailableInit = component.isPartialAvailable;

    expect(cashoutPanelService.isPartialAvailable).toHaveBeenCalledWith(component.bet.eventSource);
  });

  it('buttonState', () => {
    // eslint-disable-next-line
    const buttonStateInit = component.buttonState;

    expect(cashoutPanelService.getButtonState).toHaveBeenCalledWith(component.bet.eventSource);
  });

  it('stateConfig', () => {
    // eslint-disable-next-line
    const stateConfigInit = component.stateConfig;

    expect(cashoutPanelService.getStateConfig).toHaveBeenCalledWith(component.bet.eventSource);
  });

  it('doCashOut', () => {
    component.data = data;
    component.doCashOut('type');

    expect(cashoutPanelService.doCashOut).toHaveBeenCalledWith(component.data, component.bet.location, component.bet.eventSource, 'type');
    expect(pubsub.publish).toHaveBeenCalled();
  });

  it('doCashOut should start timer if "confirm" action', () => {
    spyOn(component as any, 'iniTimer');
    component.doCashOut('type');
    expect(component['iniTimer']).not.toHaveBeenCalled();

    component.doCashOut();
    expect(component['iniTimer']).toHaveBeenCalled();
  });

  it('should start timer defining subscription name', () => {
    expect(component.subscriberName).not.toBeDefined();

    component.doCashOut();

    expect(component.subscriberName).toBeDefined();
  });

  it('should start timer triggering countdown once', () => {
    pubsub.subscribe.and.callFake((a, b, cb) => cb(3));
    timeService.countDownTimer.and.returnValue({} as any);

    expect(component.countDownTimer).not.toBeDefined();

    component.doCashOut();

    expect(component.countDownTimer).toBeDefined();
    expect(timeService.countDownTimer).toHaveBeenCalledWith(3);
    expect(timeService.countDownTimer).toHaveBeenCalledTimes(1);
    expect(pubsub.unsubscribe).toHaveBeenCalled();
    expect(component.subscriberName).toBe(null);
  });

  it('should not start timer but cancel subscription', () => {
    pubsub.subscribe.and.callFake((a, b, cb) => cb(null));
    timeService.countDownTimer.and.returnValue({} as any);

    expect(component.countDownTimer).not.toBeDefined();

    component.doCashOut();

    expect(component.countDownTimer).not.toBeDefined();
  });

  it('partialPercentageChange', () => {
    const updatedPercentage: number = 123;
    component.partialPercentageChange(updatedPercentage);

    expect(component.bet.eventSource.partialCashOutPercentage).toEqual(updatedPercentage);
  });

  it('should clean on ngOnDestroy', () => {
    component.subscriberName = 'foo';
    component.countDownTimer = jasmine.createSpyObj(['stop']);
    component.ngOnDestroy();

    expect(pubsub.unsubscribe).toHaveBeenCalledWith('foo');
    expect(component.countDownTimer.stop).toHaveBeenCalled();
  });

  it('#isPartialCashOutAvailable Should update bet.isPartialActive', () => {
    component.isPartialCashOutAvailable = true;
    component.isPartialCashOutAvailable = false;

    expect(cashoutPanelService.setPartialState).toHaveBeenCalledWith(component.bet.eventSource, false);
  });

  it('#isPartialCashOutAvailable Should not update bet.isPartialActive', () => {
    component.isPartialCashOutAvailable = true;
    component.isPartialCashOutAvailable = true;

    expect(cashoutPanelService.setPartialState).not.toHaveBeenCalled();
  });

  describe('isShowCashoutMessaging', () => {

    it('should call isShowCashoutMessaging without bet.eventSource.leg', () => {
      component.bet = { eventSource: {}} as any;
      const val = component.isShowCashoutMessaging();
      expect(val).not.toBeTruthy();
    });

    it('should call isShowCashoutMessaging with bet.eventSource.leg', () => {
      component.bet = { eventSource: { leg: [{ eventEntity: { isDisplayed: true, isActive: true, rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: null}}] }} as any;
      spyOn(component,'updateInit');
      spyOn(component,'enableMarketLevelFlags');
      component.isShowCashoutMessaging();
      expect(component.updateInit).toHaveBeenCalled();
      expect(component.enableMarketLevelFlags).toHaveBeenCalled();
    });

    it('should call isShowCashoutMessaging with isMarketLevelDisabled,isEventLevelDisabled ', () => {
      component.bet = { eventSource: {}} as any;
      component.isMarketLevelDisabled = true;
      component.isEventLevelDisabled = true;
      spyOn(component,'updateInit');
      component.isShowCashoutMessaging();
      expect(component.updateInit).not.toHaveBeenCalled();

    });

    it('should call isShowCashoutMessaging without isMarketLevelDisabled,isEventLevelDisabled with id null ', () => {
      component.bet = { eventSource: { leg: [{ eventEntity: { isDisplayed: true, eventStatusCode: 'S', rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: null}}] }} as any;
      component.isMarketLevelDisabled = false;
      component.isEventLevelDisabled = false;
      spyOn(component,'updateInit');
      component.isShowCashoutMessaging();
      expect(component.updateInit).toHaveBeenCalled();
    });

    it('should call isShowCashoutMessaging without isMarketLevelDisabled,isEventLevelDisabled ', () => {
      component.bet = { eventSource: { leg: [{ eventEntity: { isDisplayed: false, eventStatusCode: 'A', rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: '1'}}] }} as any;
      component.isMarketLevelDisabled = false;
      component.isEventLevelDisabled = false;
      spyOn(component,'updateInit');
      component.isShowCashoutMessaging();
      expect(component.updateInit).toHaveBeenCalled();
    });

    it('should call with bet.eventSource.leg with event and market flags', () => {
      component.bet = { eventSource: { leg: [{ eventEntity: { isDisplayed: true, isActive: true, rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: null}}] }} as any;
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {isDisplayed: true,
          isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component,'updateInit');
      spyOn(component,'enableMarketLevelFlags');
      component.isMarketLevelDisabled = true;
      component.isEventLevelDisabled = true;
      component.isShowCashoutMessaging();
      expect(component.enableMarketLevelFlags).not.toHaveBeenCalled();
    });

    it('should call with bet.eventSource.leg without evententity', () => {
      component.bet = { eventSource: { leg: [{ val: {}}] }} as any;
      spyOn(component,'updateInit');
      spyOn(component,'enableMarketLevelFlags');
      component.isMarketLevelDisabled = false;
      component.isEventLevelDisabled = false;
      component.isShowCashoutMessaging();
      expect(component.enableMarketLevelFlags).not.toHaveBeenCalled();
    });
  });

  describe('updateEventAndMarketFlags', () => {

    it('should call updateEventAndMarketFlags with empty param', () => {
      const update: any =  { id: '1', updatePayload: {displayed: 'N', status: 'S', is_off: 'N'}};
      component.updateEventAndMarketFlags(null);
      expect(component.isShow).not.toBeTruthy();
    });

    it('should not call updateEventAndMarketFlags', () => {
      const update: any =  {
        id: '2', updatePayload: {displayed: 'N', status: 'S', is_off: 'N'}};
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component, 'updateInit');
      component.updateEventAndMarketFlags(update);
      expect(component.updateInit).not.toHaveBeenCalled();
    });

    it('should call updateEventAndMarketFlags', () => {
      const update: any =  {
        id: '1',
        updatePayload: {displayed: 'N', status: 'S', is_off: 'N'}
      };
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: { isDisplayed: true,
          isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      component.updateEventAndMarketFlags(update);
      expect(component.isShow).not.toBeTruthy();
    });

    it('should call updateEventAndMarketFlags with display and status', () => {
      const update: any =  {
        id: '1',
        updatePayload: {displayed: 'Y', status: 'A', is_off: 'N'}
      };
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: { isDisplayed: true,
          isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      component.updateEventAndMarketFlags(update);
      expect(component.isShow).not.toBeTruthy();
    });

    it('should call updateEventAndMarketFlags with eventIDMap', () => {
      const update: any =  {
        id: '1',
        updatePayload: {displayed: 'N', status: 'S', is_off: 'N', ev_id: '1'}
      };
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component as any,'updateInit');
      component.updateEventAndMarketFlags(update);
      expect(component.updateInit).toHaveBeenCalled();
    });

    it('should call updateEventAndMarketFlags with eventIDMap with type as event', () => {
      const update: any =  {
        id: '1',
        type: 'event',
        updatePayload: {displayed: 'N', status: 'S', is_off: 'N', ev_id: '1', names: {en: 'name'}}
      };
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component as any,'updateInit');
      component.updateEventAndMarketFlags(update);
      expect(component.isShow).not.toBeTruthy();
    });

    it('should call updateEventAndMarketFlags with eventIDMap with names', () => {
      const update: any =  { id: '1', updatePayload: {displayed: 'N', status: 'S', is_off: 'N', ev_id: '1', names: {en: 'name'}}};
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component as any,'updateInit');
      component.updateEventAndMarketFlags(update);
      expect(component.isShow).not.toBeTruthy();
    });

    it('should call updateEventAndMarketFlags without updatepayload', () => {
      const update: any =  {
      };
      component.updateEventAndMarketFlags(update);
      expect(component.isShow).not.toBeTruthy();
    });
  });

  describe('enableAllFlags', () => {
    it('should call enableAllFlags with false', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);

      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component, 'isCashoutSuspended').and.returnValue(false);
      spyOn(component, 'setGAstatus');
      component.enableAllFlags();
      expect(component.isShow).not.toBeTruthy();
    });

    it('should call enableAllFlags with true', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true }} as any);

      component.allEventsAndMarkets.set('2',{
        name: 'event2', event_name: 'event2', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true }} as any);
      spyOn(component, 'isCashoutSuspended').and.returnValue(true);
      spyOn(component, 'setGAstatus');
      component.enableAllFlags();
      expect(component.isShow).toBeTruthy();
    });
  });

  describe('isEventActive', () => {
    it('should call isEventActive ', () => {
      const cashout = { isDisplayed: false, isActive: false, rawIsOffCode: 'N', cashoutAvail: 'Y',
      isCashoutMessagingEnabled: false
      };
      component.isEventActive(cashout);
      expect(cashout.isCashoutMessagingEnabled).toBeTruthy();
    });

    it('should call isEventActive ', () => {
      const cashout = { isDisplayed: true, isActive: true, rawIsOffCode: 'Y', cashoutAvail: 'Y',
        isCashoutMessagingEnabled: true
      };
      component.isEventActive(cashout);
      expect(cashout.isCashoutMessagingEnabled).not.toBeTruthy();
    });
  });

  describe('isMarketLevelCashoutMessagingEnabled', () => {
    it('should call isMarketLevelCashoutMessagingEnabled ', () => {
      const marketCashout = { isDisplayed: false, isActive: false, rawIsOffCode: 'N', cashoutAvail: 'Y',
      isCashoutMessagingEnabled: false
      };
      component.isMarketLevelCashoutMessagingEnabled(marketCashout, true);
      expect(marketCashout.isCashoutMessagingEnabled).toBeTruthy();
    });

    it('should call isMarketLevelCashoutMessagingEnabled ', () => {
      const marketCashout = { isDisplayed: true, isActive: false, rawIsOffCode: 'N', cashoutAvail: 'Y',
      isCashoutMessagingEnabled: false
      };
      component.isMarketLevelCashoutMessagingEnabled(marketCashout, true);
      expect(marketCashout.isCashoutMessagingEnabled).not.toBeTruthy();
    });
  });

  describe('isEventActiveForMarket', () => {
    it('should call isEventActiveForMarket to be truthy ', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true}} as any);
      const retVal = component.isEventActiveForMarket('1');
      expect(retVal).toBeTruthy();
    });

    it('should call isEventActiveForMarket to be falsy', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: false, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true }} as any);
      const retVal = component.isEventActiveForMarket('1');
      expect(retVal).not.toBeTruthy();
    });
  });

  describe('updateInit', () => {
    it('should call isEventActiveForMarket and isMarketLevelCashoutMessagingEnabled to be called ', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true }} as any);
      spyOn(component, 'isEventActiveForMarket').and.returnValue(true);
      spyOn(component, 'isMarketLevelCashoutMessagingEnabled');
      spyOn(component, 'enableAllFlags');
      component.updateInit();
      expect(component.isMarketLevelCashoutMessagingEnabled).toHaveBeenCalled();
    });

    it('should call isEventActiveForMarket is false ', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'market', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: false }} as any);
      spyOn(component, 'isEventActiveForMarket').and.returnValue(false);
      spyOn(component, 'isMarketLevelCashoutMessagingEnabled');
      spyOn(component, 'enableAllFlags');
      component.updateInit();
      expect(component.isMarketLevelCashoutMessagingEnabled).not.toHaveBeenCalled();
    });

    it('should call isEventActiveForMarket and isMarketLevelCashoutMessagingEnabled not to be called ', () => {
      component.allEventsAndMarkets.set('1',{
        name: 'event1', event_name: 'event1', event_id: '1', type: 'event', cashoutMessagingFlags: {
          isDisplayed: true, isActive: true, rawIsOffCode:  'Y', cashoutAvail: 'Y', isCashoutMessagingEnabled: true }} as any);
      spyOn(component, 'isEventActive');
      spyOn(component, 'enableAllFlags');
      component.updateInit();
      expect(component.isEventActive).toHaveBeenCalled();
    });
  });

  describe('setGAstatus', () => {
    it('should call setGAstatus ', () => {
      const events = [{ name: 'name', event_name: 'name', event_id: '1', type: 'market',
          cashoutMessagingFlags: { isDisplayed: true, isActive: true, rawIsOffCode: 'Y', cashoutAvail: 'N', isCashoutMessagingEnabled: true
        }}];
      component.setGAstatus(events);
      expect(component.gaTrackDetails.size).toBe(1);
    });
  });

  describe('isCashoutSuspended', () => {
    it('should call isCashoutSuspended ', () => {
      const better: any = {eventSource : {cashoutStatus: 'CASHOUT_SELN_SUSPENDED'}};
      component.bet = better;
      const retVal = component.isCashoutSuspended();
      expect(retVal).toBeTruthy();
    });

    it('should call isCashoutSuspended and return false ', () => {
      const better: any = {eventSource : {cashoutStatus: 'false'}};
      component.bet = better;
      const retVal = component.isCashoutSuspended();
      expect(retVal).not.toBeTruthy();
    });
  });

  describe('ngOnInit', () => {
    it('should call ngOnInit without payload', () => {
      const update = {id: '123'};
      pubsub.subscribe.and.callFake((a, b, cb) => cb(update));
      spyOn(component,'isShowCashoutMessaging');
      spyOn(component,'updateEventAndMarketFlags');
      component.ngOnInit();
      expect(component.updateEventAndMarketFlags).toHaveBeenCalled();
    });
  });

  describe('IS_LIVE E/W cashout', () => {
    const panelMsg = {
      type: cashoutConstants.cashOutAttempt.SUSPENDED
    };
    const eventId = '1234';
    beforeEach(() => {
      component.bet = {
        "eventSource": {
          "partialCashOutPercentage": 5,
          "leg": [
            {
              "eventEntity": {
                "eventIsLive": true
              }
            }
          ],
          "cashoutValue": "CASHOUT_SELN_NO_CASHOUT"
        },
        "location": "location"
      } as any;
      component.bet.eventSource.event = [eventId];
      component.bet.eventSource.leg[0].eventEntity.categoryId = environment.HORSE_RACING_CATEGORY_ID;
      component.bet.eventSource.legType = 'E';
      component.bet.eventSource.leg[0].part = [{eventMarketDesc : "Win or Each Way"}] as IBetHistoryPart[];
      pubsub.subscribe.and.callFake((a, b, cb) => {
        b === pubsub.API.IS_LIVE && cb(eventId);
      });
    });
    it('should call ngOnInit - IS_LIVE with eventId', () => {
      component.bet.eventSource.leg[0].eventEntity.rawIsOffCode = 'Y';
      component.bet.eventSource.leg[0].status = 'open';
      spyOn<any>(component, 'isEWBetSuspend').and.callThrough();

      component.ngOnInit();

      expect(component.bet.eventSource.panelMsg).toEqual(panelMsg);
      expect(component.bet.eventSource.isPartialCashOutAvailable).toBeFalse();
      expect(component.bet.eventSource.cashoutValue).toBe(CASHOUT_SUSPENDED);
      expect(component.bet.eventSource.isCashOutUnavailable).toBeTrue();
      expect(component['isEWBetSuspend']).toHaveBeenCalled();
    });

    it('isLive - bet leg eventEntity null', () => {
      component.bet.eventSource.leg = [{eventEntity: null}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      expect(component['isLive'](component.bet.eventSource)).toBeFalse();
    });

    it('should not disable cashout btn when undefined for - bet event', () => {
      component.bet.eventSource.event = undefined;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when null for - bet event', () => {
      component.bet.eventSource.event = null;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet event is empty', () => {
      component.bet.eventSource.event = [];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet different event ', () => {
      component.bet.eventSource.event = ['1'];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when null for - bet updateEventId ', () => {
      component.bet.eventSource.event = ['1'];
      component.bet.eventSource.cashoutValue = 'ENABLED';
      pubsub.subscribe.and.callFake((a, b, cb) => {
        b === pubsub.API.IS_LIVE && cb(null);
      });

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when undefined for - bet updateEventId ', () => {
      component.bet.eventSource.event = ['1'];
      component.bet.eventSource.cashoutValue = 'ENABLED';
      pubsub.subscribe.and.callFake((a, b, cb) => {
        b === pubsub.API.IS_LIVE && cb();
      });

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when undefined for - bet leg ', () => {
      component.bet.eventSource.leg = undefined;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when null for - bet leg ', () => {
      component.bet.eventSource.leg = null;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg empty', () => {
      component.bet.eventSource.leg = [];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg greater than 2', () => {
      component.bet.eventSource.leg = [1, 2]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg eventEntity null', () => {
      component.bet.eventSource.leg = [{eventEntity: null}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg eventEntity undefined', () => {
      component.bet.eventSource.leg = [{}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg categoryId football', () => {
      component.bet.eventSource.leg = [{eventEntity: {categoryId: 'DUMMYID'}, status : 'open'}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg status - win', () => {
      component.bet.eventSource.leg = [{eventEntity: {categoryId: environment.HORSE_RACING_CATEGORY_ID, rawIsOffCode: 'Y'}, status : 'win'}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg legType undefined', () => {
      delete component.bet.eventSource.legType;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg legType null', () => {
      component.bet.eventSource.legType = null;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg legType code not E/W', () => {
      component.bet.eventSource.legType = 'DUMMY';
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg part undefined', () => {
      component.bet.eventSource.leg[0].part = undefined;
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg part empty', () => {
      component.bet.eventSource.leg[0].part = [];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg part null', () => {
      component.bet.eventSource.leg[0].part = [null];
      component.bet.eventSource.cashoutValue = 'ENABLED';

      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should not disable cashout btn when - bet leg part eventMarketDesc not Win or Each Way', () => {
      component.bet.eventSource.leg[0].part = [{eventMarketDesc: 'DUMMY'}]  as any[];
      component.bet.eventSource.cashoutValue = 'ENABLED';
      
      component.ngOnInit();

      expect(component.bet.eventSource.cashoutValue).toEqual('ENABLED');
    });

    it('should unsubscribe the subscriberNameEW', () => {
      component['subscriberNameEW'] = 'TEST';
      component.ngOnDestroy();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith(component['subscriberNameEW']);
    });

    it('should call getSystemConfig with config - null', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(null))};
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('should call getSystemConfig with config - undefined', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(undefined))};
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('should call getSystemConfig with HorseRacingBIR - null', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: null}))};
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('should call getSystemConfig with HorseRacingBIR - undefined', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))};
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('should call getSystemConfig with marketsEnabled - null', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: {marketsEnabled: null}}))};
      
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      const enabledBIRMarket = emptyComponent['isEnabledBIRMarket'](component.bet.eventSource.leg);
      
      expect(enabledBIRMarket).toBeFalse();
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('should call getSystemConfig with marketsEnabled - undefined', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({HorseRacingBIR: {}}))};
      
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      const enabledBIRMarket = emptyComponent['isEnabledBIRMarket'](component.bet.eventSource.leg);

      expect(enabledBIRMarket).toBeFalse();
      expect(emptyComponent['BIRMarketsEnabled']).toBeFalsy();
    });

    it('isEnabledBIRMarket with undefined BIRMarketsEnabled', () => {

    });

  });

  describe('enableMarketLevelFlags', () => {
    it('should call enableMarketLevelFlags', () => {
      const marketsEntity = {markets: [{  isDisplayed: true, marketStatusCode: 'A', rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: null}]} as any;
      component.enableMarketLevelFlags(marketsEntity);
      expect(component.allEventsAndMarkets.size).not.toBe(0);
    });

    it('should call enableMarketLevelFlags with id and false case', () => {
      const marketsEntity = {id: '2', markets: [{  isDisplayed: false, marketStatusCode: 'S', rawIsOffCode:'Y',
      cashoutAvail: 'Y', name: 'Event A vs B', id: '1'}]} as any;
      component.enableMarketLevelFlags(marketsEntity);
      expect(component.allEventsAndMarkets.size).not.toBe(0);
    });
  });

  describe('constructor', () => {
    it('should call constructor with out config ', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))};
      const emptyComponent = new CashoutPanelComponent(cashoutPanelService, pubsub, timeService, cmsService);
      expect(emptyComponent.enableCashOut).not.toBe(true);
    });
  });
});
