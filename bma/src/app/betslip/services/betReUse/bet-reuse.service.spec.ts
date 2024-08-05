import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { BetReuseService } from './bet-reuse.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { betReceiptsMock } from '@betslip/services/betReceipt/bet-receipt.service.mock';
import { commandApi } from '@core/services/communication/command/command-api.constant';

describe('BetReuseService', () => {
  let service: BetReuseService;
  let siteServerService;
  let pubSubService;
  let addToBetslipService;
  let gtmTrackingService;
  let gtmService;
  let mockServiceData, command, device, infoDialogService;
  let gtmOrigin;

  const mockUuid = '123';

  beforeEach(() => {
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve([])),
      getEvent: jasmine.createSpy('getEvent').and.returnValue(observableOf({}))
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback()),
      API: pubSubApi
    };
    addToBetslipService = jasmine.createSpyObj('addToBetslipService', ['addToBetSlip', 'reuseSelections']);
    mockServiceData = JSON.parse(JSON.stringify(betReceiptsMock));
    gtmTrackingService = {
      getBetOrigin: jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule'
      }),
      restoreGtmTracking: jasmine.createSpy(),
      getTracking: jasmine.createSpy()
    };
    gtmService = {
      getSBTrackingData: jasmine.createSpy('getSBTrackingData').and.returnValue([{GTMObject: {betData:{dimension94:1}}, outcomeId:  ['381480']}]),
      removeSBTrackingItem: jasmine.createSpy('removeSBTrackingItem'),
      push: jasmine.createSpy('push'),
      setSBTrackingData: jasmine.createSpy('setSBTrackingData')
    };

    gtmOrigin = {
      location: 'location',
      module: 'module'
    };

    command = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve())
    };

    command.API = commandApi;
    infoDialogService = jasmine.createSpyObj('infoDialogService', ['openConnectionLostPopup']);
    device = jasmine.createSpyObj('device', ['isOnline']);

    spyOn(console, 'warn');

    service = new BetReuseService(
      siteServerService,
      pubSubService,
      addToBetslipService,
      gtmTrackingService,
      gtmService,
      command,
      device,
      infoDialogService
    );
  });

  it('constructor', () => {
    service.location = "";
    expect(pubSubService.subscribe).toHaveBeenCalledWith('reUseBet',
    pubSubService.API.REUSE_LOCATION, jasmine.any(Function));
    expect(service.location).toEqual("");
  });

  describe('#reuse', () => {
    let receiptData;
    let events;
    let location;

    beforeEach(() => {
      events = Object.assign({}, mockServiceData.events);
      receiptData = Object.assign({}, mockServiceData.receiptData);
      siteServerService.getEvent.and.returnValue(Promise.resolve(events));
      location = "mybets- open bets";
    });
    it('reuse (outcomes availalbe)', fakeAsync(() => {
      const outcomesIds = ['1'];
      service['sortByOutcomeIds'] = jasmine.createSpy().and.returnValue(() => null);
      service['removeSuspendedBetReceipts'] = jasmine.createSpy().and.returnValue(() => null);
      service['mergeEventsWithReceipts'] = jasmine.createSpy().and.returnValue(() => null);
      service['markForeCastTricastReceipts'] = jasmine.createSpy().and.returnValue(() => null);
      service['removeLegsWithNoEventInfo'] = jasmine.createSpy().and.returnValue(() => null);


      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve(events));
      addToBetslipService.reuseSelections.and.returnValue(observableOf(null));

      const result = service.reuse(outcomesIds, receiptData, location);
      expect(result).toEqual(jasmine.any(Promise));

      expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith({outcomesIds});
      tick();
      expect(service['sortByOutcomeIds']).toHaveBeenCalledWith(outcomesIds, events);
      expect(service['removeSuspendedBetReceipts']).toHaveBeenCalledWith(outcomesIds, receiptData);
      expect(service['mergeEventsWithReceipts']).toHaveBeenCalledWith(events, receiptData);
      expect(service['markForeCastTricastReceipts']).toHaveBeenCalledWith(receiptData);
      expect(service['removeLegsWithNoEventInfo']).toHaveBeenCalledWith(receiptData);
      expect(addToBetslipService.reuseSelections).toHaveBeenCalledTimes(1);
      expect(gtmTrackingService.restoreGtmTracking).toHaveBeenCalledWith(outcomesIds);
      // expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.REUSE_OUTCOME);
      expect(service.message).toEqual({ type: undefined, msg: undefined });
    }));

    it('reuse (no outcomes)', () => {
      const outcomesIds = [];
      expect(service.reuse(outcomesIds, receiptData, location)).toEqual(jasmine.any(Promise));
      // expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith('REUSE_OUTCOME');
      expect(service.message).toEqual({ type: undefined, msg: undefined });
    });

    it('reuse (warn)', () => {
      const outcomesIdsList = ['1'];
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.reject('error'));
      service.reuse(<any>outcomesIdsList, receiptData, location).then(() => {
      }, () => {
        expect(console.warn).toHaveBeenCalledWith('Error while getEventsByOutcomeIds (BetReuseService.getEventsByOutcomeIds)', 'error');
      });
    });

    it('reuse no location (no outcomes)', () => {
      location = "";
      const outcomesIds = [];
      expect(service.reuse(outcomesIds, receiptData, location)).toEqual(jasmine.any(Promise));
      // expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith('REUSE_OUTCOME');
      expect(service.message).toEqual({ type: undefined, msg: undefined });
    });

  });

  describe('#mergeEventsWithReceipts', () => {
    it('bet type is single and event ID present', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702230',
            event: {categoryName: 'Football'}
          }]
        }]
      }] as any;
      const events= [
        { id: 6702230, name: 'Chelsea v Hull', categoryId: '16', categoryCode: 'FOOTBALL' }
      ] as any;
      service['mergeEventsWithReceipts'](events, receiptData);
      expect(receiptData[0].leg[0].part[0].event).toEqual(events[0]);
    });
    it('bet type is single and event ID is not present', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: {categoryName: 'Football'}
          }]
        }]
      }] as any;
      const events= [
        { id: 6702230, name: 'Chelsea v Hull', categoryId: '16', categoryCode: 'FOOTBALL' }
      ] as any;
      service['mergeEventsWithReceipts'](events, receiptData);
      expect(receiptData[0].leg[0].part[0].event).not.toEqual(events[0]);
    })
  });

  describe('#removeSuspendedBetReceipts', () => {
    it('if any suspended outcome Id is not present', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: {
              categoryName: 'Football'
            }
          }]
        }]
      }] as any;
      const outComeIds = ['449905491'];
      service['removeSuspendedBetReceipts'](outComeIds, receiptData);
      expect(receiptData[0].leg[0].part.length).toEqual(1);
    });
    it('if any suspended outcome Id is present', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905492',
            outcomeId: '449905492',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: {
              categoryName: 'Football'
            }
          }]
        }]
      }] as any;
      const outComeIds = ['449905491'];
      service['removeSuspendedBetReceipts'](outComeIds, receiptData);
      expect(receiptData[0].leg.length).not.toEqual(1);
    });
  })

  describe('#removeLegsWithNoEventInfo', () => {
    it('if any legs with no event', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: undefined
          }]
        }]
      }] as any;
      service['removeLegsWithNoEventInfo'](receiptData);
      expect(receiptData[0].leg.length).toEqual(0);
    });
    it('if any legs with event', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        status: 'A',
        leg: [{
          part: [{
            outcome: '449905492',
            outcomeId: '449905492',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: {
              categoryName: 'Football'
            }
          }]
        }]
      }] as any;
      service['removeLegsWithNoEventInfo'](receiptData);
      expect(receiptData[0].leg.length).toEqual(1);
    });
  });

  describe('#markForeCastTricastReceipts', () => {
    it('if receipt is isFCTC', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        sortType: 'TRICAST',
        status: 'A',
        type: '',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: undefined
          }],
          legSort: {code: 'SF'}
        }]
      }] as any;
      service['markForeCastTricastReceipts'](receiptData);
      expect(receiptData[0].leg[0].legSort).toBe('SF');
      expect(receiptData[0].type).toBe('TRICAST');
    });
    it('if receipt is not isFCTC', () => {
      const receiptData = [{
        betId: '381522',
        stake: '1.00',
        numLegs: '1',
        numLines: '1',
        stakePerLine: '1.00',
        betType: 'SGL',
        potentialPayout: '1.50',
        sortType: 'TRICAST',
        status: 'A',
        type: '',
        leg: [{
          part: [{
            outcome: '449905491',
            outcomeId: '449905491',
            priceNum: '1',
            priceDen: '2',
            handicap: '',
            eventId: '6702231',
            event: undefined
          }],
          legSort: {code: 'SFF'}
        }]
      }] as any;
      service['markForeCastTricastReceipts'](receiptData);
      expect(receiptData[0].leg[0].legSort).not.toBe('SF');
      expect(receiptData[0].type).toBe('');
    });
  })

  describe('#sortByOutcomeIds', () => {
    it('should sort by outcome ID order', () => {
      const outcomesIds = ['1', '2', '3', '4'];
      const data = [
        {
          markets: [{
            outcomes: [
              { id: '2' },
              { id: '1' },
              { id: '3' },
              { id: '4' },
              { id: '5' }]
          }]
        }
      ] as any;
      service['sortByOutcomeIds'](outcomesIds, data);
      expect((data)[0].markets[0].outcomes[0].id).toEqual('1');
      expect((data)[0].markets[0].outcomes[2].id).toEqual('3');
    });
  });

  describe('reuseQuickBet', () => {
    it('should open popup if is not connected', () => {
      const requestData = {} as any;
      service.reuseQuickBet(requestData);
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });

    it('should add to betslip if is connected (manual adding)', () => {
      device.isOnline.and.returnValue(true);
      service['formBetslipSelection'] = jasmine.createSpy();
      service['trackAddBetToQB'] = jasmine.createSpy();
      const selectionData = {disabled: false} as any;
      service.reuseQuickBet(selectionData);

      expect(service['command'].executeAsync).toHaveBeenCalled();
      expect(service['trackAddBetToQB']).toHaveBeenCalledWith(selectionData, true);
      expect(service['formBetslipSelection']).toHaveBeenCalled();
    });

    it('should add selection to BS if not receipt', () => {
      device.isOnline.and.returnValue(true);
      service['trackAddBetToQB'] = jasmine.createSpy();
      service['formBetslipSelection'] = jasmine.createSpy();
      const selectionData = {disabled: false} as any;
      service.reuseQuickBet(selectionData);

      expect(service['command'].executeAsync).toHaveBeenCalled();
      expect(service['trackAddBetToQB']).toHaveBeenCalledWith(selectionData, true);
      expect(service['formBetslipSelection']).toHaveBeenCalled();
    });

    it('should not add selection to BS if not receipt but selection is disabled', () => {
      device.isOnline.and.returnValue(true);
      service['trackAddBetToQB'] = jasmine.createSpy();
      service['formBetslipSelection'] = jasmine.createSpy();
      const selectionData = {
        disabled: true
      } as any;
      service.reuseQuickBet(selectionData);

      expect(service['command'].executeAsync).not.toHaveBeenCalled();
      expect(service['trackAddBetToQB']).not.toHaveBeenCalled();
      expect(service['formBetslipSelection']).not.toHaveBeenCalled();
    });

    it('should not add selection to BS if no data (undisplayed)', () => {
      device.isOnline.and.returnValue(true);
      service['trackAddBetToQB'] = jasmine.createSpy();
      service['formBetslipSelection'] = jasmine.createSpy();
      const selectionData = {} as any;
      service.reuseQuickBet(selectionData);

      expect(service['command'].executeAsync).not.toHaveBeenCalled();
      expect(service['trackAddBetToQB']).not.toHaveBeenCalled();
      expect(service['formBetslipSelection']).not.toHaveBeenCalled();
    });

  });

  describe('formBetslipSelection for selection and GTMObject data', () => {

    it('selection and GTMObject data', () => {
      const selectionData = {
        selectionData: { requestData: { outcomeIds: '23' } },
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: true,
        GTMObject: {},
        stake: '1',
        selectionType: 'type',
        requestData: {outcomeIds: ['12121212']}
      } as any;
      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();
      gtmTrackingService.getTracking.and.returnValue({});
      service['formBetslipSelection'](selectionData);
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(service['isVirtualSport']).toHaveBeenCalledWith(selectionData.categoryName);
    });
  });

  describe('formBetslipSelection', () => {

    it('slip selection without data', () => {
      const selectionData = {
        eventId: 123,
        requestData: {outcomeIds: []}
      } as any;
      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();
      expect(service['formBetslipSelection'](selectionData)).toEqual({
        outcomeId: [],
        userEachWay: undefined,
        userStake: undefined,
        type: undefined,
        price: {priceType: 'SP'},
        isVirtual: undefined,
        eventId: 123,
        isOutright: undefined,
        isSpecial: undefined,
        GTMObject: null,
      });
    });

    it('slip selection with incoming data', () => {
      const selectionData = {
        isLP: true,
        hasSP: true,
        price: {},
        requestData: {outcomeIds: [1]},
        isEachWay: true,
        stake: 'stake',
        selectionType: 'selectionType',
        categoryName: 'Virtual Sports',
        eventId: 123
      } as any;
      gtmTrackingService.getTracking.and.returnValue({});
      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();
      service['formBetslipSelection'](selectionData);
      expect(service['isVirtualSport']).toHaveBeenCalledWith(selectionData.categoryName);
      expect(service['getSelectionType']).toHaveBeenCalledWith(selectionData.selectionType);
    });

    it('slip selection with incoming data negative case', () => {
      const selectionData = {
        eventId: 123,
        isLP: true,
        hasSP: false,
        price: {},
        requestData: {outcomeIds: [1]},
        isEachWay: true,
        stake: 'stake',
        selectionType: 'selectionType',
        categoryName: 'categoryName'
      } as any;
      gtmTrackingService.getTracking.and.returnValue({});
      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();
      service['formBetslipSelection'](selectionData);
      expect(service['isVirtualSport']).toHaveBeenCalledWith(selectionData.categoryName);
      expect(service['getSelectionType']).toHaveBeenCalledWith(selectionData.selectionType);
    });

    it('formBetslipSelection', () => {
      const selectionData = {
        requestData: {outcomeIds: '23'},
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: true,
        GTMObject: {},
        stake: '1',
        selectionType: 'type'
      } as any;

      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();

      expect(service['formBetslipSelection'](selectionData)).toEqual(jasmine.objectContaining({
        userEachWay: selectionData.isEachWay,
        userStake: selectionData.stake
      }));
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(service['isVirtualSport']).toHaveBeenCalledWith(selectionData.categoryName);
    });

    it('@formBetslipSelection else cases', () => {
      gtmTrackingService.getTracking.and.returnValue({key: 'value'} as any);
      const selectionData = {
        requestData: {key: '23'},
        isStarted: false,
        categoryName: 'Football',
        isYourCallBet: true,
        freebetValue: 2,
        isEachWay: true,
        isLP: true,
        hasSP: false,
        GTMObject: {},
        stake: '1',
        selectionType: 'type'
      } as any;
      service['isVirtualSport'] = jasmine.createSpy();
      service['getSelectionType'] = jasmine.createSpy();

      expect(service['formBetslipSelection'](selectionData)).toEqual(jasmine.objectContaining({
        userEachWay: selectionData.isEachWay,
        userStake: selectionData.stake,
        isOutright: undefined,
        isSpecial: undefined,
      }));
      expect(gtmTrackingService.getTracking).toHaveBeenCalled();
      expect(service['isVirtualSport']).toHaveBeenCalledWith(selectionData.categoryName);
    });
  });

  it('getSelectionType', () => {
    expect(service['getSelectionType']('ab')).toBe('ab');
    expect(service['getSelectionType'](1)).toBe('simple');
  });

  it('isVirtualSport', () => {
    expect(service['isVirtualSport']('Virtual Sports')).toBe(true);
    expect(service['isVirtualSport']('Virtual Spor')).toBe(false);
  });



  describe('trackAddBetToQB', () => {
    it('toBetslip arg, live, byb, boost active, streamed', fakeAsync(() => {
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {
        streamID: '12',
        streamActive: true
      }));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      } as any;

      service['trackAddBetToQB'](eventData, true);
      tick();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'reuse selection',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 3,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 1,
              dimension63: 1,
              dimension64: 'quick bet receipt',
              dimension65: '',
              dimension86: 1,
              dimension87: 1,
              dimension88: '12',
              dimension166: 'reuse',
            }]
          }
        }
      });
    }));

    it('toQuickbet arg, not live, not byb, not boost active, not streamed', fakeAsync(() => {
      (command.executeAsync as jasmine.Spy).and.returnValue(Promise.resolve( {}));
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '4'
      } as any;

      service['trackAddBetToQB'](eventData);
      tick();

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'quickbet',
        eventAction: 'reuse selection',
        eventLabel: 'success',
        ecommerce: {
          add: {
            products: [{
              name: 'event name',
              category: '1',
              variant: '11',
              brand: 'mname',
              metric1: 4,
              dimension60: '111',
              dimension61: 1111,
              dimension62: 0,
              dimension63: 0,
              dimension64: 'quick bet receipt',
              dimension65: '',
              dimension86: 0,
              dimension87: 0,
              dimension88: null,
              dimension166: 'reuse'
            }]
          }
        }
      });
    }));

    it('It should call dynamicGtmObj', fakeAsync(() => {
      const eventData = {
        eventName: 'event name',
        marketName: 'mname',
        isStarted: true,
        isYourCallBet: true,
        isBoostActive: true,
        outcomeId: 1111,
        eventId: 111,
        typeId: 11,
        categoryId: 1,
        freebetValue: '3'
      } as any;

      const dummyObj = {
        location: '/',
        module: 'quickbet'
      }

      service['trackAddBetToQB'](eventData, true);
      tick();
      expect(gtmTrackingService.dynamicGtmObj).toBe(undefined);
    }));
   });

});
