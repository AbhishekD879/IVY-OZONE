import { InplayHelperService } from './inplay-helper.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplayHelperService', () => {
  let service: InplayHelperService;

  let coreToolsService;
  let pubSubService;
  let wsUpdateEventService;
  let commentsService;
  let cacheEventsService;
  let inplayConnectionService;
  let inPlayStorageService;

  beforeEach(() => {
    coreToolsService = {};
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };
    wsUpdateEventService = {
      subscribe: () => {},
    };
    commentsService = {};
    cacheEventsService = {};
    inplayConnectionService = {
      disconnectComponent: jasmine.createSpy('disconnectComponent')
    };
    inPlayStorageService = {};

    service = new InplayHelperService(
      coreToolsService,
      pubSubService,
      wsUpdateEventService,
      commentsService,
      cacheEventsService,
      inplayConnectionService,
      inPlayStorageService
    );
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('subscribeForSportCompetitionChanges', () => {
    it('added competition to collection', () => {
      const data = {
        added: [
          '123', '121'
        ],
        removed: []
      };
      service['addEventListener'] = jasmine.createSpy().and.callFake((str, cb) => {
        cb(data);
      });
      service.subscribeForSportCompetitionChanges('sportId', 'topLevelType');
      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_LS_COMPETITION_ADDED', data);
    });

    it('removed competition from collection', () => {
      const data = {
        removed: [
          '123'
        ],
        added: []
      };
      service['addEventListener'] = jasmine.createSpy().and.callFake((str, cb) => {
        cb(data);
      });
      service.subscribeForSportCompetitionChanges('sportId', 'topLevelType');
      expect(pubSubService.publish).toHaveBeenCalledWith('INPLAY_LS_COMPETITION_REMOVED', data);
    });
  });

  it('shoul call disconect component in helper service', () => {
    service.disconnect();

    expect(inplayConnectionService.disconnectComponent).toHaveBeenCalled();
  });
});
