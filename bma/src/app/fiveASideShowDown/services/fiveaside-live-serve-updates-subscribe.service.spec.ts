import {
  FiveAsideLiveServeUpdatesSubscribeService
} from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { CARDS_MOCK, CLOCKUpdate, SCBRDUpdate, sEVENTUpdate } from '@app/fiveASideShowDown/services/show-down-cards.mock';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';

describe('FiveasideLiveServeUpdatesSubscribeService', () => {
  let service: FiveAsideLiveServeUpdatesSubscribeService;
  let channelService;
  let pubSubService;
  let showDownLiveServeHandleUpdatesService;
  let handledShowDownService;
  let channels, contests, liveServeEventUpdate, clockUpdate, scoreUpdate;
  beforeEach(() => {
    channelService = new ChannelService();
    pubSubService = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };
    handledShowDownService = {
      showDownSubscribe: jasmine.createSpy('showDownSubscribe'),
      addEventListner: jasmine.createSpy('addEventListner'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      removeEventAllListner: jasmine.createSpy('removeEventAllListner')
    };
    showDownLiveServeHandleUpdatesService = jasmine.createSpyObj(['subscribe', 'unsubscribe']);
    channels = ['sEVENT1', 'sSCBRD0000000003', 'sEVENT2', 'sSCBRD0000000345'];
    liveServeEventUpdate = sEVENTUpdate;
    clockUpdate = CLOCKUpdate;
    scoreUpdate = SCBRDUpdate;
    contests = CARDS_MOCK;
    service = new FiveAsideLiveServeUpdatesSubscribeService(channelService, pubSubService,
      showDownLiveServeHandleUpdatesService, handledShowDownService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#openLiveServeConnectionForUpdates method should be called with paramters', () => {
    service.openLiveServeConnectionForUpdates(channels);
    expect(showDownLiveServeHandleUpdatesService.subscribe).toHaveBeenCalledWith(channels, jasmine.any(Function), true);
  });

  it('#unSubscribeLiveServeConnection method should be called with paramters', () => {
    const channelsMock = ['sEVENT1', 'sSCBRD0000000003', 'sEVENT2', 'sSCBRD0000000345'];
    service.channelsList = ['sEVENT1', 'sEVENT1', 'sEVENT2', 'sSCBRD0000000003', 'sEVENT2', 'sSCBRD0000000345'];
    service.unSubscribeLiveServeConnection(channelsMock);
    expect(showDownLiveServeHandleUpdatesService.unsubscribe).toHaveBeenCalled();
  });

  describe('#createLiveServeChannels', () => {
    it('#createLiveServeChannels - should return liveserve channel names in array', () => {
      const result = service.createLiveServeChannels(contests);
      const expectedChannels =
        ['CLOCK::232215271', 'CLOCK::232300717', 'SCORE::232215271', 'SCORE::232300717',
          'EVENT::232215271', 'EVENT::232300717'];
      expect(result).toEqual(expectedChannels);
    });
    it('#createLiveServeChannels - should return empty array', () => {
      const result = service.createLiveServeChannels([]);
      expect(result).toEqual([]);
    });
    it('#createLiveServeChannels - should return empty array', () => {
      const result = service.createLiveServeChannels(null);
      expect(result).toEqual([]);
    });
  });

  describe('#createChannels', () => {
    it('#createChannels - should return liveserve channel names in array', () => {
      const events = ['232215271'] as any;
      const result = service.createChannels(events);
      const expectedChannels =
        ['EVENT::232215271', 'SCORE::232215271',
          'CLOCK::232215271'];
      expect(result).toEqual(expectedChannels);
    });
    it('#createChannels - should return empty array', () => {
      const result = service.createChannels([]);
      expect(result).toEqual([]);
    });
  });

  it('#getChannels return channel names based on eventId and type', () => {
    const result = service['getChannels'](['232215271', '232300717'], 'sCLOCK');
    expect(result).toEqual(['sCLOCK232215271', 'sCLOCK232300717']);
  });

  it('#getChannels should not return channel names based on eventId and type', () => {
    const result = service['getChannels']([] as any, '');
    expect(result).toEqual([]);
  });

  it('#getEventIdsToBeSubscribed method should return eventIds which are eligible for live updates', () => {
    const result = service['getEventIdsToBeSubscribed'](contests);
    expect(result).toEqual(['232215271', '232300717']);
  });

  it('#getEventIdsToBeSubscribed method should return empty when contests are empty', () => {
    const result = service['getEventIdsToBeSubscribed']([]);
    expect(result).toEqual([]);
  });

  it('#getEventIdsToBeSubscribed method should return empty when contests are null', () => {
    const result = service['getEventIdsToBeSubscribed'](null);
    expect(result).toEqual([]);
  });

  describe('#filterOnlyLiveEvents', () => {
    it('method should return eventIds which are eligible for live updates', () => {
      const result = service['filterOnlyLiveEvents'](contests[0].contests);
      expect(result).toEqual(['232215271']);
    });

    it('method when contests are empty', () => {
      const contestDetail = [{ eventDetails: {} }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contests are null', () => {
      const contestDetail = [{ events: null }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contest is null', () => {
      const contestDetail = [null] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contests are null', () => {
      const contestDetail = [{ eventDetails: null }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contest is null', () => {
      const contestDetail = [null] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when event as isFinished true', () => {
      const contestDetail = [{ eventDetails: { isFinished: true }, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when event as isFinished true', () => {
      const contestDetail = [{ eventDetails: {}, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contests as isFinished false', () => {
      const contestDetail = [{ eventDetails: { regularTimeFinished: false }, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contests are not present', () => {
      const contestDetail = [] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when showRoleContest not present', () => {
      const contestDetail = [{ eventDetails: null, showRoleContest: false }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when showRoleContest and events are null', () => {
      const contestDetail = [{ eventDetails: null, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });

    it('method when contests as isFinished and showRoleContest is true', () => {
      const contestDetail = [{ eventDetails: { regularTimeFinished: true }, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual([]);
    });
    it('method when contests as regularTimeFinished false and showRoleContest is true', () => {
      const contestDetail = [{ eventDetails: { id: 1, regularTimeFinished: false }, showRoleContest: true }] as any;
      const result = service['filterOnlyLiveEvents'](contestDetail);
      expect(result).toEqual(['1']);
    });
  });

  describe('#liveServeShowdownUpdatesListener publish update based on update type', () => {
    it('#liveServeShowdownUpdatesListener method sCLOCK', () => {
      const update = Object.assign({}, clockUpdate);
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE, update);
    });

    it('#liveServeShowdownUpdatesListener method sSCBRD', () => {
      const update = Object.assign({}, scoreUpdate);
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE, update);
    });

    it('#liveServeShowdownUpdatesListener method sEVENT - should not publish if event is not started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'EVENT';
      update.payload.started = 'N';
      update.payload.status = 'S';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, update);
      expect(service['publishEventStarted']).toHaveBeenCalledWith(update);
    });

    it('#liveServeShowdownUpdatesListener method sEVENT - should publish if event is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'EVENT';
      update.payload.started = 'Y';
      update.payload.status = 'A';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, update);
      expect(service['publishEventStarted']).toHaveBeenCalledWith(update);
    });

    it('#liveServeShowdownUpdatesListener method sEVENT - should publish if event is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'EVENT';
      update.payload.started = 'Y';
      update.payload.status = 'A';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE, update);
      expect(service['publishEventStarted']).toHaveBeenCalledWith(update);
    });

    it('#liveServeShowdownUpdatesListener method sEVMKT - should not publish if event is not started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload.started = 'N';
      update.payload.status = 'S';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(service['publishEventStarted']).toHaveBeenCalledWith(update);
    });

    it('#liveServeShowdownUpdatesListener method sEVMKT - should publish if event is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload.started = 'Y';
      update.payload.status = 'A';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(service['publishEventStarted']).toHaveBeenCalledWith(update);
    });

    it('#liveServeShowdownUpdatesListener method default case', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'RANDOM';
      update.payload.started = 'Y';
      update.payload.status = 'A';
      spyOn(service as any, 'publishEventStarted');
      service['liveServeShowdownUpdatesListener'](update);
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(service['publishEventStarted']).not.toHaveBeenCalled();
    });
  });

  describe('#publishEventStarted', () => {
    it('should not publish if event not is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload = null;
      service['publishEventStarted'](update);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_EVENT_STARTED, update.id.toString());
    });

    it('should publish if event is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload.started = true;
      service['publishEventStarted'](update);
      expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_EVENT_STARTED, update.id.toString());
    });

    it('should not publish if event not is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload.started = false;
      service['publishEventStarted'](update);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_EVENT_STARTED, update.id.toString());
    });

    it('should not publish if event not is started', () => {
      const update = Object.assign({}, liveServeEventUpdate);
      update.type = 'sEVMKT';
      update.payload.started = false;
      service['publishEventStarted'](update);
      expect(pubSubService.publish).not.toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_EVENT_STARTED, update.id.toString());
    });
  });
  describe('getInitialLegs', () => {
    it('getInitialLegs', () => {
      service['getInitialLegs']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('openLiveServeInitialDataEntryInformation', () => {
    it('openLiveServeInitialDataEntryInformation', () => {
      service['openLiveServeInitialDataEntryInformation']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('userEntryUpdates', () => {
    it('userEntryUpdates', () => {
      service['userEntryUpdates']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('legsUpdateSubscribe', () => {
    it('legsUpdateSubscribe', () => {
      service['legsUpdateSubscribe'](['channel'], () => { });
      expect(handledShowDownService.addEventListner).toHaveBeenCalled();
    });
  });
  describe('unSubscribeShowDownChannels', () => {
    it('unSubscribeShowDownChannels', () => {
      service['unSubscribeShowDownChannels'](['channel'], () => { });
      expect(handledShowDownService.unsubscribe).toHaveBeenCalled();
    });
  });
  describe('removeAllEventListneres', () => {
    it('removeAllEventListneres', () => {
      service['removeAllEventListneres'](['channel']);
      expect(handledShowDownService.removeEventAllListner).toHaveBeenCalled();
    });
  });
  describe('addEventListneres', () => {
    it('addEventListneres', () => {
      service['addEventListneres'](['channel'], () => { });
      expect(handledShowDownService.addEventListner).toHaveBeenCalled();
    });
  });
  describe('getInitialLegs', () => {
    it('getInitialLegs', () => {
      service['getInitialLegs']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('openLiveServeInitialDataEntryInformation', () => {
    it('openLiveServeInitialDataEntryInformation', () => {
      service['openLiveServeInitialDataEntryInformation']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('userEntryUpdates', () => {
    it('userEntryUpdates', () => {
      service['userEntryUpdates']('channel', () => { }, 'emit');
      expect(handledShowDownService.showDownSubscribe).toHaveBeenCalled();
    });
  });
  describe('legsUpdateSubscribe', () => {
    it('legsUpdateSubscribe', () => {
      service['legsUpdateSubscribe'](['channel'], () => { });
      expect(handledShowDownService.addEventListner).toHaveBeenCalled();
    });
  });
  describe('unSubscribeShowDownChannels', () => {
    it('unSubscribeShowDownChannels', () => {
      service['unSubscribeShowDownChannels'](['channel'], () => { });
      expect(handledShowDownService.unsubscribe).toHaveBeenCalled();
    });
  });
  describe('removeAllEventListneres', () => {
    it('removeAllEventListneres', () => {
      service['removeAllEventListneres'](['channel']);
      expect(handledShowDownService.removeEventAllListner).toHaveBeenCalled();
    });
  });
  describe('addEventListneres', () => {
    it('addEventListneres', () => {
      service['addEventListneres'](['channel'], () => { });
      expect(handledShowDownService.addEventListner).toHaveBeenCalled();
    });
  });
});
