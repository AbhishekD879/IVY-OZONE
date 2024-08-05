import { of as observableOf, throwError } from 'rxjs';

import { cashoutConstants } from '../../constants/cashout.constant';

import { CashOutLiveUpdatesSubscribeService } from './cashOutLiveUpdatesSubscribeService';
import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { CashOutSetDefaultStateService } from '@app/betHistory/services/cashoutSetDefaultStateService/cashout-set-default-state-service';
import {
  HandleLiveServeUpdatesService
} from '@core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { CashOutLiveServeUpdatesService } from '@app/betHistory/services/cashOutLiveServeUpdatesService/cashOutLiveServeUpdatesService';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ChannelService } from '@core/services/liveServ/channel.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('CashOutLiveUpdatesSubscribeService -', () => {
  let service: CashOutLiveUpdatesSubscribeService;
  let serviceHacked: any;
  let cashOutMapIndexService: CashoutMapIndexService;
  let cashOutSetDefaultStateService: CashOutSetDefaultStateService;
  let cashOutLiveServeHandleUpdatesService: HandleLiveServeUpdatesService;
  let cashOutLiveServeUpdatesService: CashOutLiveServeUpdatesService;
  let pubSubService: PubSubService;
  let channelService: ChannelService;

  let typesAndIds: any;
  let cashOutCtrl: any;

  beforeEach(() => {
    typesAndIds = {outcome: [], event: [], market: []};
    cashOutCtrl = {ctrlName: 'foo', isDestroyed: true};

    cashOutMapIndexService = jasmine.createSpyObj(['getItems']);
    cashOutSetDefaultStateService = jasmine.createSpyObj(['extendMapWithEvents']);
    cashOutLiveServeHandleUpdatesService = jasmine.createSpyObj(['subscribe', 'unsubscribe']);
    cashOutLiveServeUpdatesService = {
      betsMap: {},
      updateCashOutValue: jasmine.createSpy('updateCashOutValue')
    } as any;
    channelService = jasmine.createSpyObj(['formChannel']);

    (cashOutSetDefaultStateService.extendMapWithEvents as jasmine.Spy).and.returnValue(
      observableOf(null)
    );

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
        if (b === 'CASHOUT_CTRL_STATUS' || b === 'UNSUBSCRIBE_LS_UPDATES_MS') {
          cb && cb(cashOutCtrl);
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    } as any;

    service = new CashOutLiveUpdatesSubscribeService(
      cashOutMapIndexService as any,
      cashOutSetDefaultStateService as any,
      cashOutLiveServeHandleUpdatesService as any,
      cashOutLiveServeUpdatesService as any,
      pubSubService as any,
      channelService as any,
    );
    serviceHacked = service as any;
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should be a copy', () => {
    expect(serviceHacked).toEqual(service);
  });

  it('destroyedCashOutCtrls to be modified within constructor call', () => {
    expect(serviceHacked.destroyedCashOutCtrls).toEqual([cashOutCtrl]);
  });

  it('cashout constants should be initialized', () => {
    expect(serviceHacked.CASH_OUT).toEqual(cashoutConstants);
  });

  it('channels should be empty on initialization', () => {
    expect(serviceHacked.channels).toEqual([]);
  });

  describe('addWatch method should',  () => {

    beforeEach(() => {
      serviceHacked.channels = ['foo1', 'foo2'];
      spyOn(serviceHacked, 'getIds').and.returnValue(typesAndIds);
    });

    it('call unsubscribe', () => {
      const channels = serviceHacked.channels;

      service.addWatch(null);
      expect(cashOutLiveServeHandleUpdatesService.unsubscribe).toHaveBeenCalledWith(channels);
    });

    it('call getIds', () => {
      service.addWatch(null);
      expect(serviceHacked.getIds).toHaveBeenCalled();
    });

    it('erase channels', () => {
      service.addWatch(null);
      expect(serviceHacked.channels).toEqual([]);
    });

    it('not call extendMapWithEvents if no outcomes', () => {
      service.addWatch(null);
      expect(cashOutSetDefaultStateService.extendMapWithEvents).not.toHaveBeenCalled();
    });

    it('should update cashOutLiveServeUpdatesService.betsMap', () => {
      service.addWatch({ betId: { betTitle: 'bet' } } as any);
      expect(cashOutLiveServeUpdatesService.betsMap).toEqual({ betId: { betTitle: 'bet' } } as any );
    });
  });

  describe('addWatch method should',  () => {

    beforeEach(() => {
      typesAndIds.outcome = ['foo'];
      spyOn(serviceHacked, 'getIds').and.returnValue(typesAndIds);
    });

    it('call extendMapWithEvents if outcomes present', () => {
      service.addWatch(null);
      expect(cashOutSetDefaultStateService.extendMapWithEvents).toHaveBeenCalledWith(typesAndIds.outcome, null);
    });

    it('should call extendMapWithEvents with error', () => {
      cashOutSetDefaultStateService.extendMapWithEvents = jasmine.createSpy('extendMapWithEvents').and.returnValue(throwError('error'));
      service.addWatch(null);

      expect(cashOutSetDefaultStateService.extendMapWithEvents).toHaveBeenCalledWith(typesAndIds.outcome, null);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('call extendChannelsAndSubscribe within extendMapWithEvents subscriber', (done: DoneFn) => {
      spyOn(serviceHacked, 'extendChannelsAndSubscribe');

      service.addWatch(null);

      cashOutSetDefaultStateService
        .extendMapWithEvents(null, null)
        .subscribe(() => {
          expect(serviceHacked.extendChannelsAndSubscribe).toHaveBeenCalledWith(typesAndIds);
          expect(pubSubService.publish).toHaveBeenCalledWith('BET_EVENTENTITY_UPDATED');
          done();
        });
    });
  });

  describe('addWatchForPlacedEventsOnly method should',  () => {

    beforeEach(() => {
      serviceHacked.channels = ['foo1', 'foo2'];
      spyOn(serviceHacked, 'getIds').and.returnValue(typesAndIds);
    });

    it('call unsubscribe', () => {
      const channels = serviceHacked.channels;

      service.addWatchForPlacedEventsOnly(null);
      expect(cashOutLiveServeHandleUpdatesService.unsubscribe).toHaveBeenCalledWith(channels);
    });

    it('get different getIds', () => {
      service.addWatchForPlacedEventsOnly(null);
      expect(serviceHacked.getIds.calls.count()).toBe(2);
    });

    it('erase channels', () => {
      spyOn(serviceHacked, 'extendChannelsAndSubscribe').and.callFake(() => {});

      service.addWatchForPlacedEventsOnly(null);
      expect(serviceHacked.channels).toEqual([]);
    });

    it('call extendMapWithEvents', () => {
      service.addWatchForPlacedEventsOnly(null);
      expect(cashOutSetDefaultStateService.extendMapWithEvents).toHaveBeenCalledWith(typesAndIds.outcome, null);
    });

    it('call extendChannelsAndSubscribe within extendMapWithEvents subscriber', (done: DoneFn) => {
      spyOn(serviceHacked, 'extendChannelsAndSubscribe');

      service.addWatchForPlacedEventsOnly(null);

      cashOutSetDefaultStateService
        .extendMapWithEvents(null, null)
        .subscribe(() => {
          expect(serviceHacked.extendChannelsAndSubscribe).toHaveBeenCalledWith(typesAndIds);
          expect(pubSubService.publish).toHaveBeenCalledWith('BET_EVENTENTITY_UPDATED');
          done();
        });
    });

    it('should call extendMapWithEvents with error', () => {
      cashOutSetDefaultStateService.extendMapWithEvents = jasmine.createSpy('extendMapWithEvents').and.returnValue(throwError('error'));
      service.addWatchForPlacedEventsOnly(null);
      expect(cashOutSetDefaultStateService.extendMapWithEvents).toHaveBeenCalledWith(typesAndIds.outcome, null);
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  describe('addWatchForRegularBets method should',() => {
    beforeEach(() => {
      spyOn(service, 'addWatchForPlacedEventsOnly');
    });
    it('call addWatchForPlacedEventsOnly with same data', () => {
      service.addWatchForRegularBets({}, ['1'] as any);
      expect(service.addWatchForPlacedEventsOnly).toHaveBeenCalledWith({}, ['1'] as any);
    });

    it('call addWatchForPlacedEventsOnly with same data and null as second default arg', () => {
      service.addWatchForRegularBets({});
      expect(service.addWatchForPlacedEventsOnly).toHaveBeenCalledWith({}, null);
    });
  });

  it('unsubscribeFromLiveUpdates method should call unsubscribe with appropriate data', () => {
    const channels = serviceHacked.channels = ['foo1', 'foo2'];

    service.unsubscribeFromLiveUpdates();
    expect(cashOutLiveServeHandleUpdatesService.unsubscribe).toHaveBeenCalledWith(channels);
  });

  it('registerCashOutControllerEvent method should sync for "CASHOUT_CTRL_STATUS" method', () => {
    serviceHacked.registerCashOutControllerEvent();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'CashOutLiveUpdatesSubscribeService', 'CASHOUT_CTRL_STATUS', jasmine.any(Function)
    );
  });

  it('sync callback within registerCashOutControllerEvent method should update destroyed controllers', () => {
    serviceHacked.destroyedCashOutCtrls = [];

    serviceHacked.registerCashOutControllerEvent();
    expect(serviceHacked.destroyedCashOutCtrls).toEqual([cashOutCtrl]);
  });

  describe('extendChannelsAndSubscribe method should', () => {

    beforeEach(() => {
      spyOn(serviceHacked, 'getEventChannels');
      spyOn(serviceHacked, 'getMarketChannels');
      spyOn(serviceHacked, 'getOutcomeChannels');
      spyOn(serviceHacked, 'registerLiveServEvents');
    });

    it('only call registerLiveServEvents', () => {
      serviceHacked.extendChannelsAndSubscribe(typesAndIds);

      expect(serviceHacked.getEventChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getMarketChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getOutcomeChannels).not.toHaveBeenCalled();
      expect(serviceHacked.registerLiveServEvents).toHaveBeenCalled();
    });

    it('call getEventChannels and registerLiveServEvents', () => {
      typesAndIds.event = ['foo'];
      serviceHacked.extendChannelsAndSubscribe(typesAndIds);

      expect(serviceHacked.getEventChannels).toHaveBeenCalledWith(typesAndIds.event);
      expect(serviceHacked.getMarketChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getOutcomeChannels).not.toHaveBeenCalled();
      expect(serviceHacked.registerLiveServEvents).toHaveBeenCalled();
    });

    it('call getMarketChannels and registerLiveServEvents', () => {
      typesAndIds.market = ['foo'];
      serviceHacked.extendChannelsAndSubscribe(typesAndIds);

      expect(serviceHacked.getEventChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getMarketChannels).toHaveBeenCalledWith(typesAndIds.market);
      expect(serviceHacked.getOutcomeChannels).not.toHaveBeenCalled();
      expect(serviceHacked.registerLiveServEvents).toHaveBeenCalled();
    });

    it('call getMarketChannels and registerLiveServEvents', () => {
      typesAndIds.outcome = ['foo'];
      serviceHacked.extendChannelsAndSubscribe(typesAndIds);

      expect(serviceHacked.getEventChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getMarketChannels).not.toHaveBeenCalled();
      expect(serviceHacked.getOutcomeChannels).toHaveBeenCalledWith(typesAndIds.outcome);
      expect(serviceHacked.registerLiveServEvents).toHaveBeenCalled();
    });
  });

  it('registerLiveServEvents method should sync for "UNSUBSCRIBE_LS_UPDATES_MS" method', () => {
    serviceHacked.registerLiveServEvents();
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  it('sync callback within registerLiveServEvents method should get specific channels and unsubscribe them', () => {
    spyOn(serviceHacked, 'getSpecificChannelsToUnsubscribe').and.callFake( data => data);

    serviceHacked.registerLiveServEvents();
    expect(serviceHacked.getSpecificChannelsToUnsubscribe).toHaveBeenCalledWith(cashOutCtrl);
    expect(cashOutLiveServeHandleUpdatesService.unsubscribe).toHaveBeenCalledWith(cashOutCtrl);
  });

  it('getSpecificChannelsToUnsubscribe method should get data from 3 other methods', () => {
    spyOn(serviceHacked, 'getEventChannels').and.returnValue([]);
    spyOn(serviceHacked, 'getMarketChannels').and.returnValue([]);
    spyOn(serviceHacked, 'getOutcomeChannels').and.returnValue([]);

    serviceHacked.getSpecificChannelsToUnsubscribe(typesAndIds);
    expect(serviceHacked.getEventChannels).toHaveBeenCalled();
    expect(serviceHacked.getMarketChannels).toHaveBeenCalled();
    expect(serviceHacked.getOutcomeChannels).toHaveBeenCalled();
  });

  it('getChannels method should form channel for every list member', () => {
    serviceHacked.getChannels(new Array(4));
    expect(channelService.formChannel['calls'].count()).toBe(4);
  });

  it('getEventChannels method should get data for 3 different channel types', () => {
    spyOn(serviceHacked, 'getChannels').and.returnValue([]);

    serviceHacked.getEventChannels([]);
    expect(serviceHacked.getChannels.calls.count()).toBe(3);
  });

  it('getMarketChannels method should get data for market', () => {
    spyOn(serviceHacked, 'getChannels').and.returnValue([]);

    serviceHacked.getMarketChannels([]);
    expect(serviceHacked.getChannels).toHaveBeenCalledWith([], cashoutConstants.channelName.market);
  });

  it('getOutcomeChannels method should get data for selection', () => {
    spyOn(serviceHacked, 'getChannels').and.returnValue([]);

    serviceHacked.getOutcomeChannels([]);
    expect(serviceHacked.getChannels).toHaveBeenCalledWith([], cashoutConstants.channelName.selection);
  });

  it('getIds method should get data from cashOutMapIndexService with proper data for outcome', () => {
    serviceHacked.getIds();
    expect(cashOutMapIndexService.getItems['calls'].argsFor(0)).toEqual([cashoutConstants.keyProperties.outcome, false]);
  });

  it('getIds method should get data from cashOutMapIndexService with proper data for market and event', () => {
    serviceHacked.getIds(true);
    expect(cashOutMapIndexService.getItems['calls'].argsFor(1)).toEqual([cashoutConstants.keyProperties.market, true]);
    expect(cashOutMapIndexService.getItems['calls'].argsFor(2)).toEqual([cashoutConstants.keyProperties.event, true]);
  });

  it('getIds method should return data from cashOutMapIndexService', () => {
    (cashOutMapIndexService.getItems as jasmine.Spy).and.returnValue({});

    const expectedResult = serviceHacked.getIds(true);
    expect(cashOutMapIndexService.getItems['calls'].count()).toBe(3);
    expect(expectedResult).toEqual({
      outcome: {},
      market: {},
      event: {}
    });
  });
});
