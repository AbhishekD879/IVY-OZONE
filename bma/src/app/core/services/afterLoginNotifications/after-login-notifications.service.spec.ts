import { of, throwError } from 'rxjs';
import { AfterLoginNotificationsService } from './after-login-notifications.service';
import { tick, fakeAsync } from '@angular/core/testing';

describe('AfterLoginNotificationsService', () => {
  let service: AfterLoginNotificationsService;

  let freeBetsService, command, user, iteratorService, pubSubService, cmsService, location, iterator;

  beforeEach(() => {
    freeBetsService = {
      showFreeBetsInfo: jasmine.createSpy('showFreeBetsInfo').and.returnValue(of(null)),
    };
    command = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve(null)),
      API: {
        SHOW_TUTORIAL_OVERLAY: 'SHOW_TUTORIAL_OVERLAY'
      }
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
        LOGIN_POPUPS_END: 'LOGIN_POPUPS_END',
        SHOW_TIMELINE_TUTORIAL: 'SHOW_TIMELINE_TUTORIAL'
      },
      publishSync: jasmine.createSpy(),
      publish: jasmine.createSpy('publish').and.callFake((a, cb) => cb && cb()),
      subscriptions: {},
    
      subscribe: jasmine.createSpy()
    };
    cmsService = {
     getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(of(null)),
      getFanzoneComingBack: jasmine.createSpy(),
      subscribe: jasmine.createSpy()
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
      location,
    );
  });

  it('start', fakeAsync(() => {
    service.start();
    tick();
    expect(iteratorService.create).toHaveBeenCalledTimes(1);
    expect(iterator.start).toHaveBeenCalledTimes(1);
  }));

  it('to have been called with \'notificationDialogs\' ', fakeAsync(() => {
    service.start();
    tick();
    expect(iteratorService.create).toHaveBeenCalledWith(service['notificationDialogs']);
  }));

  describe('#allowedByPath', () => {
    it('should not allow if path 1-2-free', () => {
      location.path.and.returnValue('1-2-free');
      expect(service['allowedByPath']()).toBeFalsy();
    });

    it('should allow if path not 1-2-free', () => {
      location.path.and.returnValue('');
      expect(service['allowedByPath']()).toBeTruthy();
    });
  });

  describe('iterator to be executed', () => {

    it('fanzoneComingBack - if flag is on',  fakeAsync(() => {
      const data = [{fzComingBackPopupDisplay: true}]
      cmsService.getFanzoneComingBack = jasmine.createSpy('').and.returnValue(of(data));
      service.brand = "ladbrokes";
      pubSubService.publish = jasmine.createSpy('publish').and.callFake((event, data) => {
        pubSubService.subscriptions[event] && pubSubService.subscriptions[event](data);
      });
      service['notificationDialogs'][0].run(iterator);
      tick(); 
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.FANZONE_COMING_BACK, data);
    }));

    it('fanzoneComingBack - if flag is off',  fakeAsync(() => {
      const data = [{fzComingBackPopupDisplay: false}]
      cmsService.getFanzoneComingBack = jasmine.createSpy('').and.returnValue(of(data));
      service.brand = "ladbrokes";
      pubSubService.publish = jasmine.createSpy('publish').and.callFake((event, data) => {
        pubSubService.subscriptions[event] && pubSubService.subscriptions[event](data);
      });
      service['notificationDialogs'][0].run(iterator);
      tick(); 
      expect(iterator.next).toHaveBeenCalledTimes(1);
    }));

    it('fanzoneComingBack - if brand is coral',  fakeAsync(() => {
      const data = [{fzComingBackPopupDisplay: false}]
      cmsService.getFanzoneComingBack = jasmine.createSpy('').and.returnValue(of(data));
      service.brand = "coral";
      pubSubService.publish = jasmine.createSpy('publish').and.callFake((event, data) => {
        pubSubService.subscriptions[event] && pubSubService.subscriptions[event](data);
      });
      service['notificationDialogs'][0].run(iterator);
      tick(); 
      expect(iterator.next).toHaveBeenCalledTimes(1);
    }));
    
    it('fanzoneComingBack error scenario',  fakeAsync(() => {
      cmsService.getFanzoneComingBack = jasmine.createSpy('').and.returnValue(throwError({}));
      service.brand = "ladbrokes";
      service['notificationDialogs'][0].run(iterator);
      tick(); 
      expect(iterator.next).toHaveBeenCalledTimes(1);
    }));

    
    it('freeBets', () => {
      service['notificationDialogs'][1].run(iterator);
      expect(freeBetsService.showFreeBetsInfo).toHaveBeenCalledTimes(1);
      expect(iterator.next).toHaveBeenCalledTimes(1);
    });

    it('oddsBoost (boost disabled)', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(of({enabled: false}));

      service['notificationDialogs'][2].run(iterator);
      tick();

      expect(cmsService.getOddsBoost).toHaveBeenCalled();
      expect(command.executeAsync).not.toHaveBeenCalledWith(command.API.ODDS_BOOST_TOKENS_SHOW_POPUP);
      expect(iterator.next).toHaveBeenCalledTimes(1);
    }));

    it('oddsBoost (boost enabled)', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(of({enabled: true}));

      service['notificationDialogs'][2].run(iterator);
      tick();

      expect(cmsService.getOddsBoost).toHaveBeenCalled();
      expect(command.executeAsync).toHaveBeenCalledWith(command.API.ODDS_BOOST_TOKENS_SHOW_POPUP);
      expect(iterator.next).toHaveBeenCalledTimes(1);
    }));

    it('showTimelineSplash', () => {
      service['notificationDialogs'][3].run(iterator);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.SHOW_TIMELINE_TUTORIAL);
      expect(iterator.next).toHaveBeenCalledTimes(1);
    });

    it('showExpiryMessage', () => {
      service['allowedByPath'] = jasmine.createSpy('allowedByPath').and.returnValue(true);
      service['notificationDialogs'][4].run(iterator);
      expect(user.set).toHaveBeenCalledWith({quickDepositTriggered: false, loginPending: false});
      expect(pubSubService.publish).toHaveBeenCalledWith('LOGIN_POPUPS_END');
    });

    it('should not showExpiryMessage', () => {
      service['allowedByPath'] = jasmine.createSpy('allowedByPath').and.returnValue(false);
      service['notificationDialogs'][4].run(iterator);
      expect(user.set).toHaveBeenCalledWith({quickDepositTriggered: false, loginPending: false});
      expect(pubSubService.publish).toHaveBeenCalledWith('LOGIN_POPUPS_END');
    });
  });
});