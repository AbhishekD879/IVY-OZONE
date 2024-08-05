import { InplaySubscriptionService } from '@app/bigCompetitions/services/inplaySubscription/inplay-subscription-service';
import { commandApi } from '@core/services/communication/command/command-api.constant';

describe('InplaySubscriptionService', () => {
  let service;
  let commandService;
  let wsUpdateEventService;
  let eventsIds;

  beforeEach(() => {
    eventsIds = ['80498'];
    commandService = {
      API: commandApi,
      executeAsync: jasmine.createSpy('executeAsync')
    };
    wsUpdateEventService = {
      subscribe: jasmine.createSpy('subscribe')
    };
    service = new InplaySubscriptionService(commandService, wsUpdateEventService);
  });

  it('constructor', () => {
    expect(wsUpdateEventService.subscribe).toHaveBeenCalled();
  });

  it('subscribeForLiveUpdates', () => {
    service.subscribeForLiveUpdates(eventsIds);
    expect(commandService.executeAsync).toHaveBeenCalledWith(
      commandService.API.SUBSCRIBE_FOR_LIVE_UPDATES,
      jasmine.arrayContaining([eventsIds])
    );
  });

  it('unsubscribeForLiveUpdates', () => {
    service.unsubscribeForLiveUpdates(eventsIds);
    expect(commandService.executeAsync).toHaveBeenCalledWith(
      commandService.API.UNSUBSCRIBE_FOR_LIVE_UPDATES,
      jasmine.arrayContaining([eventsIds])
    );
  });

  describe('loadCompetitionEvents', () => {
    let eventWithMarkets,
      sportEvents,
      categoryId,
      typeId,
      modifyMainMarkets,
      isLiveNow,
      requestParams;

    beforeEach(() => {
      eventWithMarkets = { markets: [{}] };
      sportEvents = [ {}, { markets: [] }, eventWithMarkets ];
      categoryId = 3243;
      typeId = 8993;
      modifyMainMarkets = false;
      isLiveNow = true;
      requestParams = {
        categoryId: 3243,
        isLiveNowType: true,
        topLevelType: 'LIVE_EVENT',
        typeId: 8993,
        modifyMainMarkets: true
      };

      commandService.executeAsync = jasmine.createSpy().and.returnValue(Promise.resolve(sportEvents));
    });

    it('isLiveNow true, modifyMainMarkets true', () => {
      service.loadCompetitionEvents(isLiveNow, categoryId, typeId).then((result) => {
        expect(result.length).toBe(1);
        expect(result[0]).toBe(eventWithMarkets);
        expect(commandService.executeAsync).toHaveBeenCalledWith(
          commandService.API.LOAD_COMPETITION_EVENTS,
          jasmine.arrayContaining(
            [
              'competition',
              jasmine.objectContaining(requestParams)
            ]
          ),
          jasmine.arrayContaining([])
        );
      });
    });

    it('isLiveNow false, modifyMainMarkets false', () => {
      isLiveNow = false;
      requestParams = {
        categoryId: 3243,
        isLiveNowType: false,
        topLevelType: 'UPCOMING_EVENT',
        typeId: 8993,
        modifyMainMarkets: false
      };

      service.loadCompetitionEvents(isLiveNow, categoryId, typeId, modifyMainMarkets).then((result) => {
        expect(result.length).toBe(1);
        expect(result[0]).toBe(eventWithMarkets);
        expect(commandService.executeAsync).toHaveBeenCalledWith(
          commandService.API.LOAD_COMPETITION_EVENTS,
          jasmine.arrayContaining(
            [
              'competition',
              jasmine.objectContaining(requestParams)
            ]
          ),
          jasmine.arrayContaining([])
        );
      });
    });
  });
});
