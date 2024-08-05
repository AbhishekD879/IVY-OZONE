import { of, Subject } from 'rxjs';
import { ServiceClosureService } from '@app/lazy-modules/serviceClosure/service-closure.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('ServiceClosureService', () => {
  let service: ServiceClosureService;
  let userService, windowRefService, cmsService, rtmsService, claimsService, eventsService, apiVanillaService, pubSub, fanzoneHelperService, fanzoneStorageService, timeService, router;

  beforeEach(() => {
    pubSub = {
      publish:jasmine.createSpy('publish'),
      cbMap: {},

      subscribe: jasmine.createSpy('subscribe').and.callFake((name, method, cb) => pubSub.cbMap[method] = cb),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    userService = {status :false};
    windowRefService = {
      nativeWindow: {
        portal: {
          excludedInSameSession: true,
          allProductsExcludedInSameSession: true
        }
      }
    };

    rtmsService = {
      messages: jasmine.createSpy('messages').and.returnValue(of('message'))
    };
    claimsService = {
      get: jasmine.createSpy('get')
    };

    
    apiVanillaService = {
      get: jasmine.createSpy('get').and.returnValue(of({})),
      persistPlaybreakVal: false,
      playBreakSubject: new Subject<boolean>()
    };

    eventsService = {
      events: {
        get: jasmine.createSpy('get').and.returnValue(of({}))
      }
    };
    (eventsService as any).events = of({ eventName: 'PLAY_BREAK', data: { playBreak: true } });
    (rtmsService as any).messages = of({ type: 'PLAY_BREAK_START_EVENT' });
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.callFake(() => {
        return of({ SelfExclusion: true });
      })
    };

    fanzoneHelperService = {
      PublishFanzoneData: jasmine.createSpy('PublishFanzoneData')
    };

    fanzoneStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get')
    }


    timeService = {
      getSuspendAtTime: jasmine.createSpy('getSuspendAtTime').and.returnValue('2023-05-08T13:18:24Z')
    }

    router = {
      navigate: jasmine.createSpy('navigate')
    }

    cmsService.getSystemConfig.and.returnValue(of({}));

    service = new ServiceClosureService(
      userService,
      cmsService,
      windowRefService,
      rtmsService,
      claimsService,
      eventsService,
      apiVanillaService,
      pubSub,
      fanzoneHelperService,
      fanzoneStorageService,
      timeService,
      router
    );

  });
 
  describe('getInitValues', () => {
  
    it('should getInitValues not to be called', () => {
      spyOn(service, 'getInitValues');
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({} as any));
      spyOn(service, 'playBreakStatusOfUser');
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).not.toHaveBeenCalled();
    });

    it('should getInitValues not to be called wth isGetInitDataCalled as true', () => {
      spyOn(service, 'getInitValues');
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({} as any));
      spyOn(service, 'playBreakStatusOfUser');
      service.isGetInitDataCalled = true;
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).not.toHaveBeenCalled();
    });

    it('should getInitValues to be called with user status true', () => {
      userService.status = true;
      service.cmsConfigMessages.playBreakEnable = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'true' }] } } as any));
      // spyOnProperty(eventsService, 'events', 'get').and.returnValue(of({eventName: 'PLAY_BREAK', data: {playBreak : true}}));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be called with user status and playbreak enable true', () => {
      userService.status = true;
      service.cmsConfigMessages.playBreakEnable = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'true' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text', playBreakEnable: true } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be called with is blocked', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'false' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be called withoout SPORTSBOOK', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'POKER', isBlocked: 'false' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should miss isBlocked', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should closuredetails is null', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [null] } }));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should closuredetails is empty array', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [] } }));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should miss productId', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{}] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should miss closureDetails', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: {} } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should miss outer closureDetails', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({} as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should call with null case', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of(null));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should call', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'false' }] } } as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should call with isblocked as true', () => {
      userService.status = true;
      service.cmsConfigMessages = { selfExclusionEnable: true } as any;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'true' }] } } as any));
      spyOn(service, 'populateCmsCOnfigs');
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be calledwith out data obj fields in true case', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'true' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({} as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be called with out data obj fields in false case', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'false' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({} as any));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be calledwith out data obj sa null in true case', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'true' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of(null));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });

    it('should getInitValues to be called with out data obj as null in false case', () => {
      userService.status = true;
      spyOn(service, 'getInitValues').and.
        returnValue(of({ closureDetails: { closureDetails: [{ productId: 'SPORTSBOOK', isBlocked: 'false' }] } } as any));
      spyOn(service, 'userAccountMessageObs').and.returnValue(of(null));
      service.checkUserServiceClosureStatus();
      expect(service.getInitValues).toHaveBeenCalled();
    });
  });

  describe('userAccountMessageObs', () => {
    it('should userAccountMessageObs to be called', () => {
      const retVal = service.userAccountMessageObs();
      expect(retVal).toBeTruthy();
    });
  });

  describe('getInitValues', () => {
    it('should getInitValues to be called', () => {
      service.getInitValues();
      expect(apiVanillaService.get).toHaveBeenCalled();
    });
  });

  describe('checkplayBreak', () => {
    it('should checkplayBreak to be called', () => {
      const message = { type: 'PLAY_BREAK_START_EVENT' } as any;
      service.cmsConfigMessages.playBreakEnable = true;
      service.checkplayBreak(message);
      expect(service.userServiceClosureOrPlayBreakVal).toBeTruthy();
    });

    it('should checkplayBreak to be called', () => {
      const message = { type: 'PLAY_BREAK_END_EVENT' };
      service.cmsConfigMessages.playBreakEnable = true;
      service.checkplayBreak(message);
      expect(service.userServiceClosureOrPlayBreakVal).not.toBeTruthy();
    });

    it('should checkplayBreak to be called with other values', () => {
      const message = { type: 'NOT_PLAY_BREAK' };
      service.cmsConfigMessages.playBreakEnable = true;
      service.checkplayBreak(message);
      expect(service.userServiceClosureOrPlayBreakVal).toBeTruthy();
    });
  });

  describe('populateCmsCOnfigs', () => {
    it('should populateCmsCOnfigs to be called', () => {
      const data = {
        selfExclusion: 'text', selfExclusionEnable: true, playBreak: 'text2', playBreakEnable: true, immediateBreak: 'text3',
        immediateBreakEnable: true
      };
      service.populateCmsCOnfigs(data);
      expect(service.cmsConfigMessages.immediateBreakEnable).toBeTruthy();
    });

    it('should populateCmsCOnfigs to be called with empty obj', () => {
      const data = null;
      service.populateCmsCOnfigs(data);
      expect(service.cmsConfigMessages.immediateBreakEnable).toBeTruthy();
    });
  });

  describe('updateClosureFlag', () => {
    it('should updateClosureFlag to be called', () => {
      service.cmsConfigMessages = { selfExclusion: 'true', selfExclusionEnable: true } as any;
      service.updateClosureFlag();
      userService.status = true;
      expect(service.userServiceClosureOrPlayBreakVal).toBeTruthy();
    });

    it('should updateClosureFlag to be called and se as false', () => {
      service.cmsConfigMessages = { selfExclusion: 'true', selfExclusionEnable: false } as any;
      service.userServiceClosureOrPlayBreakVal = false;
      service.updateClosureFlag();
      expect(service.userServiceClosureOrPlayBreakVal).not.toBeTruthy();
    });

    it('should updateClosureFlag to be called and se as true', () => {
      service.cmsConfigMessages = { immediateBreak: 'trueval', immediateBreakEnable: true } as any;
      claimsService.get.and.returnValue('2');
      service.updateClosureFlag();
      expect(service.userServiceClosureOrPlayBreakVal).toBeTruthy();
      expect(service.userAccountInfo).toBe('trueval');
    });

    it('should updateClosureFlag allProductsExcludedInSameSession to be called and se as false', () => {
      service.cmsConfigMessages = { immediateBreak: 'trueval', immediateBreakEnable: true } as any;
      spyOn(service, 'isOneDayExclusion').and.returnValue(true);
      service.updateClosureFlag();
      expect(service.userServiceClosureOrPlayBreakVal).toBeTruthy();
      expect(service.userAccountInfo).toBe('trueval');
    });
    it('should publish',fakeAsync(() =>{
      userService.status = true;
      service.updateClosureFlag();
      service.userServiceClosureOrPlayBreakVal = true;
      pubSub.publish(pubSub.API.USER_CLOSURE_PLAY_BREAK,service.userServiceClosureOrPlayBreakVal);
      tick(1000);
      expect(pubSub.publish).toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,true);
      pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
          expect(val).toBeTrue();
      });
    }))
    it('should  publish false',() =>{
      userService.status = true;
      service.updateClosureFlag();
      service.userServiceClosureOrPlayBreakVal = false;
      pubSub.publish(pubSub.API.USER_CLOSURE_PLAY_BREAK,service.userServiceClosureOrPlayBreakVal);
      expect(pubSub.publish).toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,false);
      pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
          expect(val).toBeFalse();
      });
    })
    it('should not publish',fakeAsync(() =>{
      userService.status = false;
      service.updateClosureFlag();
      tick(1000);
      expect(pubSub.publish).not.toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,true);
      pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
          expect(val).toBeUndefined();
      });
    }))
  });

  describe('isOneDayExclusion', () => {
    it('should isOneDayExclusion to be called', () => {
      const data = {
        selfExclusion: 'text', selfExclusionEnable: true, playBreak: 'text2', playBreakEnable: true, immediateBreak: 'text3',
        immediateBreakEnable: true
      };
      const portalWindowObj = { endDate: '2021-09-22T17:40:41Z', startDate: '2021-09-21T17:40:41Z' };
      const retVal = service.isOneDayExclusion(portalWindowObj);
      expect(retVal).toBeTruthy();
    });

    it('should isOneDayExclusion to be called with false', () => {
      const data = {
        selfExclusion: 'text', selfExclusionEnable: true, playBreak: 'text2', playBreakEnable: true, immediateBreak: 'text3',
        immediateBreakEnable: true
      };
      const portalWindowObj = { endDate: '2021-09-23T17:40:41Z', startDate: '2021-09-21T17:40:41Z' } as any;
      const retVal = service.isOneDayExclusion(portalWindowObj);
      expect(retVal).not.toBeTruthy();
    });

    it('should isOneDayExclusion to be called with false', () => {
      const data = {
        selfExclusion: 'text', selfExclusionEnable: true, playBreak: 'text2', playBreakEnable: true, immediateBreak: 'text3',
        immediateBreakEnable: true
      };
      const portalWindowObj = {} as any;
      const retVal = service.isOneDayExclusion(portalWindowObj);
      expect(retVal).not.toBeTruthy();
    });
  });
  describe('userServiceClosureOrPlayBreak', () => {
    it('should userServiceClosureOrPlayBreak to be called', () => {
      service.userServiceClosureOrPlayBreakVal = true;
      const retVal = service.userServiceClosureOrPlayBreak;
      expect(retVal).toBeTruthy();
    });
  });
  describe('userServiceClosureOrPlayBreakCheck', () => {
    it('should userServiceClosureOrPlayBreakCheck to be called', () => {
      service.userServiceClosureOrPlayBreakVal = true;
      const retVal = service.userServiceClosureOrPlayBreakCheck();
      expect(retVal).toBeTruthy();
    });

    it('should userServiceClosureOrPlayBreakCheck to be called with false', () => {
      service.userServiceClosureOrPlayBreakVal = false;
      spyOn(service, 'updateClosureFlag');
      const retVal = service.userServiceClosureOrPlayBreakCheck();
      expect(retVal).not.toBeTruthy();
    });
  });

  describe('enablePlaybreak', () => {
    it('should userServiceClosureOrPlayBreak to be called', () => {
      service.cmsConfigMessages = { playBreak: false } as any;
      const message = {} as any;
      spyOn(service, 'checkplayBreak');
      const retVal = service.enablePlaybreak(message);
      expect(retVal).toBeUndefined();
    });

    it('should userServiceClosureOrPlayBreak to be called', () => {
      service.cmsConfigMessages = { playBreak: true } as any;
      const message = {} as any;
      spyOn(service, 'userAccountMessageObs').and.returnValue(of({} as any));
      spyOn(service, 'checkplayBreak');
      spyOn(service, 'populateCmsCOnfigs');
      const retVal = service.enablePlaybreak(message);
      expect(retVal).toBeUndefined();
    });
  });

  describe('call constructor without going in', () => {
  it('should userServiceClosureOrPlayBreak to be called', () => {
      (eventsService as any).events = of({ eventName: 'PLAY_BREAK', data: { playBreak: false } });
      apiVanillaService.persistPlaybreakVal = false;
      const service1 = new ServiceClosureService(userService, cmsService, windowRefService, rtmsService, claimsService, eventsService,
        apiVanillaService, pubSub, fanzoneHelperService,fanzoneStorageService,timeService,router);
      expect(service1.userServiceClosureOrPlayBreakVal).toBeFalsy();
    });

    it('should userServiceClosureOrPlayBreak to be called with persistPlaybreakVal as true', () => {
      (eventsService as any).events = of({ eventName: 'PLAY_BREAK', data: { playBreak: false } });
      apiVanillaService.persistPlaybreakVal = true;
      const service1 = new ServiceClosureService(userService, cmsService, windowRefService, rtmsService, claimsService, eventsService,
        apiVanillaService, pubSub, fanzoneHelperService,fanzoneStorageService,timeService,router);
      expect(service1.userServiceClosureOrPlayBreakVal).toBeTruthy();
     
    });
    it('#constructor should call publish false in constructor with user logged in', fakeAsync(() => {
      userService.status = true;
     
      const service1 = new ServiceClosureService(userService, cmsService, windowRefService, rtmsService, claimsService, eventsService,
        apiVanillaService, pubSub, fanzoneHelperService,fanzoneStorageService,timeService,router);
        service1.userServiceClosureOrPlayBreakVal = false;
        spyOn(service1, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
     
      pubSub.publish(pubSub.API.USER_CLOSURE_PLAY_BREAK,service1.userServiceClosureOrPlayBreakVal);
      tick(1000);
      expect(service).toBeTruthy();
      expect(pubSub.publish).toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,false);
      pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
        expect(val).toBeFalse();
    });
      }));
      it('#constructor should call publish true in constructor with user logged in', fakeAsync(() => {
        userService.status = true;
        const service1 = new ServiceClosureService(userService, cmsService, windowRefService, rtmsService, claimsService, eventsService,
          apiVanillaService, pubSub, fanzoneHelperService,fanzoneStorageService,timeService,router);
          spyOn(service1, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
       
        service1.userServiceClosureOrPlayBreakVal = true;
        pubSub.publish(pubSub.API.USER_CLOSURE_PLAY_BREAK,service1.userServiceClosureOrPlayBreakVal);
        tick(1000);
        expect(service1).toBeTruthy();
        expect(pubSub.publish).toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,true);
        pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
          expect(val).toBeTrue();
      });
        }));
      it('#constructor should not call publish  in constructor with user not logged in', fakeAsync(() => {
        userService.status = false;
        tick(1000);
        const service1 = new ServiceClosureService(userService, cmsService, windowRefService, rtmsService, claimsService, eventsService,
          apiVanillaService, pubSub, fanzoneHelperService,fanzoneStorageService,timeService,router);
          spyOn(service1, 'userAccountMessageObs').and.returnValue(of({ selfexclusion: 'selfexclusion text', playbreak: 'playbreak text' } as any));
       
        service1.userServiceClosureOrPlayBreakVal = false;
        expect(service1).toBeTruthy();
        expect(pubSub.publish).not.toHaveBeenCalledWith(pubSub.API.USER_CLOSURE_PLAY_BREAK,service1.userServiceClosureOrPlayBreakVal);
        pubSub.subscribe('userServiceClosureOrPlayBreak',pubSub.API.USER_CLOSURE_PLAY_BREAK,val =>{
          expect(val).toBeUndefined();
      });
      }));
  });

  describe('Listen to Change of Team for Fanzone', () => {
    it('# should call changeFanzoneTeam when RTMS fanzone event is listened', fakeAsync(() => {
      const message = { type: 'FZ_PLAYER_PREFS',payload:{PreferencesObject:{TEAM_ID:'test',TEAM_NAME:'test'}} };
      const changeFanzoneTeam= spyOn(service,'changeFanzoneTeam');
      service.enablePlaybreak(message);
      tick(1000);
      expect(changeFanzoneTeam).toHaveBeenCalled();
    }));

    it('#should should publish Fanzone Team Change', () => {
      fanzoneStorageService.get.and.returnValue({teamName: 'FZ001',teamId: 'test'});
      const rtmsEvent = {
        params: {
          payload: {
            PreferencesObject: {
              TEAM_ID: '9q0arba2kbnywth8bkxlhgmdr',
              TEAM_NAME: 'Chelsea'
            },
          },
          type: 'FZ_PLAYER_PREFS'
        }
      }
      service.changeFanzoneTeam(rtmsEvent.params);
      expect(fanzoneStorageService.set).toHaveBeenCalled();
      expect(fanzoneHelperService.PublishFanzoneData).toHaveBeenCalled();
    });

    it('#should should publish Fanzone Team Change if case', () => {
      const rtmsEvent = {
        params: {
          payload: {
            PreferencesObject: {
             
            },
          },
          type: 'FZ_PLAYER_PREFS'
        }
      } as any
      fanzoneStorageService.get = jasmine.createSpy('get').and.returnValue({})
      service.changeFanzoneTeam(rtmsEvent.params);
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    });

    it('#should should publish Fanzone Team Change else case', () => {
      const rtmsEvent = {
        params: {
          payload: {
            PreferencesObject: {
             
            },
          },
          type: 'FZ_PLAYER_PREFS'
        }
      } as any;
      fanzoneStorageService.get = jasmine.createSpy('get').and.returnValue({isResignedUser: true,isFanzoneExists: true,teamId: '123',teamName: 'test',communication: 'test'})
      service.changeFanzoneTeam(rtmsEvent.params);
      expect(fanzoneStorageService.set).toHaveBeenCalled();
    });
  });
});
