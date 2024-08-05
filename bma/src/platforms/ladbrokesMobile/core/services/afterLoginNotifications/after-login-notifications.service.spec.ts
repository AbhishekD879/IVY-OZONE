import { of as observableOf, of } from 'rxjs';
import { AfterLoginNotificationsService } from './after-login-notifications.service';
import { commandApi } from '@core/services/communication/command/command-api.constant';

describe('AfterLoginNotificationsService', () => {
  let service: AfterLoginNotificationsService;

  let freeBetsService;
  let command;
  let user;
  let iteratorService;
  let iterator;
  let pubSubService;
  let cmsService;
  let location;

  beforeEach(() => {
    freeBetsService = {
      showFreeBetsInfo: jasmine.createSpy('showFreeBetsInfo').and.returnValue(observableOf(null)),
      showExpiryMessage: jasmine.createSpy('showExpiryMessage')
    };
    command = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve(null)),
      API: commandApi
    };
    user = {
      quickDepositTriggered: false,
      set: jasmine.createSpy(),
    };
    iterator = {
      start: jasmine.createSpy(),
      next: jasmine.createSpy()
    };
    iteratorService = {
      create: jasmine.createSpy().and.returnValue(iterator)
    };
    pubSubService = {
      API: {
        SHOW_TUTORIAL_OVERLAY: 'SHOW_TUTORIAL_OVERLAY',
      },
      publishSync: jasmine.createSpy(),
      publish: jasmine.createSpy('publish').and.callFake((a, cb) => cb && cb()),
      subscribe: jasmine.createSpy()
    };
    cmsService = {
      getFanzoneComingBack: jasmine.createSpy().and.returnValue(of(null)),
      getOddsBoost: jasmine.createSpy()
    };
    location = {
      path: jasmine.createSpy().and.returnValue('')
    } as any;

    service = new AfterLoginNotificationsService(
      freeBetsService,
      command,
      user,
      iteratorService,
      pubSubService,
      cmsService,
      location
    );
  });

  describe('iterator to be executed', () => {
    it('freeBets', () => {        
      service['freeBetInfoShow'](iterator);
      expect(iterator.next).toHaveBeenCalledTimes(1);
    });
  });
});
