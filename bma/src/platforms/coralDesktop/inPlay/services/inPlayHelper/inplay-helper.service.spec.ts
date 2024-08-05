import { InplayHelperService } from './inplay-helper.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

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
    coreToolsService = {
      merge: jasmine.createSpy('merge').and.returnValue({
        socket: {
          ribbon: {
            emit: 'emit message',
            on: 'on message'
          }
        }
      })
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    wsUpdateEventService = {
      subscribe: () => {},
    };
    commentsService = {};
    cacheEventsService = {
      storedData: {
        index: {
          data: [
            {
              id: 10
            }
          ]
        }
      }
    };
    inplayConnectionService = {
      connectComponent: jasmine.createSpy('connectComponent'),
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

  describe('#handleLiveUpdate', () => {
    it('handleLiveUpdate should be called', () => {
      service.cachePrefix = 'index';
      service.handleLiveUpdate('10', 'message');
      expect(pubSubService.publish).toHaveBeenCalledWith('WS_EVENT_UPDATE', { events: [ { id: 10 } ], update: 'message' });
    });
    it('handleLiveUpdate should NOT be called', () => {
      service.cachePrefix = 'index';
      service.handleLiveUpdate('11', 'message');
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  xdescribe('@getRibbonData', () => {
    it('should throw error if no data', () => {
      inplayConnectionService.connectComponent.and.returnValue(of({
        connection: {
          on:  (event, callback) => {
            callback({ items: [] });
          }
        }
      }));

      service.getRibbonData({} as any).subscribe(() => {}, (err) => {
        expect(err).toBe('no data');
      });
    });

    it('should return no response after 3 second', fakeAsync(() => {
      inplayConnectionService.connectComponent.and.returnValue(of({
        connection: {
          on:  () => {},
          emit: jasmine.createSpy('emit')
        }
      }));

      service.getRibbonData({} as any).subscribe(() => {}, (err) => {
        expect(err).toBe('No response after 3 seconds');
      });
      tick(3000);
    }));
  });
});
