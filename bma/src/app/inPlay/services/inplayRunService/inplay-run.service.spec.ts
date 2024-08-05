import { InplayRunService } from './inplay-run.service';
import { InplayDataService } from '@app/inPlay/services/inplayData/inplay-data.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { of as observableOf } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';


describe('InplayRunService', () => {
  let service: InplayRunService;
  let commandsMap;
  let commandService;
  let injector;
  let inPlaySubscriptionManager;
  let inPlayDataService;

  beforeEach(() => {
    commandsMap = {};
    commandService = {
      register: jasmine.createSpy('register').and.callFake((key, fn) => {
        commandsMap[key] = fn;
      }),
      API: {
        LOAD_COMPETITION_EVENTS: 'LOAD_COMPETITION_EVENTS',
        SUBSCRIBE_FOR_LIVE_UPDATES: 'SUBSCRIBE_FOR_LIVE_UPDATES',
        UNSUBSCRIBE_FOR_LIVE_UPDATES: 'UNSUBSCRIBE_FOR_LIVE_UPDATES'
      }
    };

    injector = {
      get(type) {
        if (type === InplayDataService) {
          return inPlayDataService;
        } else
        if (type === InplaySubscriptionManagerService) {
          return inPlaySubscriptionManager;
        }
      }
    };

    inPlaySubscriptionManager = {
      subscribeForLiveUpdates: jasmine.createSpy('subscribeForLiveUpdates'),
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    };

    inPlayDataService = {
      loadData: jasmine.createSpy('loadData').and.returnValue(observableOf())
    };

    service = new InplayRunService(
      commandService,
      injector
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('run', () => {
    service.run();
    expect(commandService.register).toHaveBeenCalledWith(
      'LOAD_COMPETITION_EVENTS', jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      'SUBSCRIBE_FOR_LIVE_UPDATES', jasmine.any(Function)
    );
    expect(commandService.register).toHaveBeenCalledWith(
      'UNSUBSCRIBE_FOR_LIVE_UPDATES', jasmine.any(Function)
    );
  });

  it('run LOAD_COMPETITION_EVENTS', fakeAsync( () => {
    service.run();
    commandsMap[commandService.API.LOAD_COMPETITION_EVENTS]();
    tick();
    expect(inPlayDataService.loadData).toHaveBeenCalled();
  }));

  it('run SUBSCRIBE_FOR_LIVE_UPDATES', fakeAsync( () => {
    service.run();
    commandsMap[commandService.API.SUBSCRIBE_FOR_LIVE_UPDATES]();
    tick();
    expect(inPlaySubscriptionManager.subscribeForLiveUpdates).toHaveBeenCalled();
  }));

  it('run UNSUBSCRIBE_FOR_LIVE_UPDATES', fakeAsync( () => {
    service.run();
    commandsMap[commandService.API.UNSUBSCRIBE_FOR_LIVE_UPDATES]();
    tick();
    expect(inPlaySubscriptionManager.unsubscribeForLiveUpdates).toHaveBeenCalled();
  }));

});
