import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';
import { NavigationEnd } from '@angular/router';
import { fakeAsync, tick } from '@angular/core/testing';

describe('StreamTrackingService', () => {
  let service: StreamTrackingService,
    windowRef,
    gtmService,
    liveStreamService,
    rendererListeners,
    rendererUnlisteners,
    rendererService,
    router,
    routerEventsCb,
    routingState,
    eventMock,
    playerAttrs,
    playerMock,
    beforeunload;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListenerSpy').and.callFake((e, handler) => {
          beforeunload = handler;
        }),
        removeEventListener: jasmine.createSpy('removeEventListenerSpy'),
        _QLGoingDown: {}
      }
    };
    gtmService = {
      push: jasmine.createSpy('pushSpy')
    };
    liveStreamService = {
      checkIfRacingEvent: jasmine.createSpy('checkIfRacingEventSpy')
    };
    rendererListeners = {};
    rendererUnlisteners = {};
    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listenSpy').and.callFake((player, eventName, cb) => {
          const key = `${(playerAttrs.id_ || playerAttrs.id)}_${eventName}`;
          rendererListeners[key] = cb;
          rendererUnlisteners[key] = jasmine.createSpy(`${key}-unlisten-spy`);
          return rendererUnlisteners[key];
        })
      }
    };
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribeSpy').and.callFake(cb => {
          routerEventsCb = cb;
          return {
            unsubscribe: jasmine.createSpy('unsubscribe')
          };
        })
      }
    };
    routingState = {
      getCurrentUrl: jasmine.createSpy('getCurrentUrlSpy').and.returnValue('test'),
      getPreviousUrl: jasmine.createSpy('getPreviousUrlSpy').and.returnValue('test1')
    };
    playerAttrs = {
      id_: 'p1',
      id: 'p1'
    };
    playerMock = {
      id: 'p1',
      getAttribute: jasmine.createSpy('getAttributeSpy').and.callFake(s => playerAttrs[s]),
    };
    eventMock = { id: 'i1', target: { id: 'p1' } };
    service = new StreamTrackingService(windowRef, gtmService, liveStreamService, rendererService, router, routingState);
  });

  describe('setTrackingForPlayer method', () => {
    describe('should exit', () => {
      it('if no player element is provided', () => { playerMock = null; });
      it('if no event is provided', () => { eventMock = null; });
      it('if player has id_ property', () => { playerMock.id_ = 'p1'; });

      afterEach(() => {
        service.setTrackingForPlayer(playerMock, eventMock);
        expect(rendererService.renderer.listen).not.toHaveBeenCalled();
        playerMock && expect(playerMock.getAttribute).not.toHaveBeenCalled();
        expect(service['preSimOrLiveSimId']).not.toBeDefined();
      });
    });

    describe('should create event listeners for play, pause and pauseEnded player events', () => {
      it('if player id_ attribute is truthy and is not yet tracked by such key', () => {});
      it('if player id_ attribute is falsy, but player still has "id" attribute and is not yet tracked by such key', () => {
        playerAttrs.id_ = undefined;
      });

      it('if player with another id has been already tracked', () => {
        playerAttrs.id_ = 'p2';
        service.setTrackingForPlayer(playerMock, eventMock);
        rendererService.renderer.listen.calls.reset();
        playerAttrs.id_ = 'p1';
      });

      afterEach(() => {
        service.setTrackingForPlayer(playerMock, eventMock);
        expect(rendererService.renderer.listen.calls.allArgs()).toEqual([
          [playerMock, 'playing', jasmine.any(Function)],
          [playerMock, 'pause', jasmine.any(Function)],
          [playerMock, 'ended', jasmine.any(Function)]
        ]);

        expect((service['trackingVideos'] as any)['p1']).toEqual({
          timeWatched: 0,
          streamingEvent: eventMock,
          isOver30MinutesPlayed: false,
          playerObj: playerMock,
          listeners: {
            play: jasmine.any(Function),
            pause: jasmine.any(Function),
            pauseEnded: jasmine.any(Function)
          }
        });
      });
    });

    describe('should not create event listeners for same player more than once', () => {
      describe('when player has been already tracked by id_', () => {
        beforeEach(() => {
          service.setTrackingForPlayer(playerMock, eventMock);
          rendererService.renderer.listen.calls.reset();
        });
        it('(second is tracked by _id)', () => { });
        it('(second is tracked by id)', () => { playerAttrs.id_ = undefined; });
      });

      describe('when player has been already tracked by id', () => {
        beforeEach(() => {
          playerAttrs.id_ = undefined;
          service.setTrackingForPlayer(playerMock, eventMock);
          rendererService.renderer.listen.calls.reset();
        });
        it('(second is tracked by id)', () => {});
        it('(second is tracked by id_)', () => { playerAttrs.id_ = 'p1'; });
      });

      afterEach(() => {
        service.setTrackingForPlayer(playerMock, eventMock);
        expect(rendererService.renderer.listen).not.toHaveBeenCalled();
      });
    });

    describe('the private preSimOrLiveSimId property', () => {
      describe('should not be updated', () => {
        describe('when window._QLGoingDown.jwplayer.id', () => {
          it('does not exist', () => { windowRef.nativeWindow._QLGoingDown = undefined; });
          it('does not exist', () => {});
          it('does not exist', () => { windowRef.nativeWindow._QLGoingDown = { jwplayer: {} }; });
          it('is not equal to player.id', () => { windowRef.nativeWindow._QLGoingDown = { jwplayer: { id: 'p2' } }; });
        });
        it('when window._QLGoingDown.jwplayer.id equals player.id but current player has been already tracked by id', () => {
          playerAttrs.id_ = undefined;
          service.setTrackingForPlayer(playerMock, eventMock);
          windowRef.nativeWindow._QLGoingDown = { jwplayer: { id: 'p1' } };
        });
        afterEach(() => {
          service.setTrackingForPlayer(playerMock, eventMock);
          expect(service['preSimOrLiveSimId']).not.toBeDefined();
        });
      });
      describe('should be updated when window._QLGoingDown.jwplayer.id equals player.id', () => {
        it('and player has not been tracked yet', () => {});
        it('and player has been tracked by id_', () => {
          service.setTrackingForPlayer(playerMock, eventMock);
        });
        afterEach(() => {
          windowRef.nativeWindow._QLGoingDown = { jwplayer: { id: 'p1' } };
          service.setTrackingForPlayer(playerMock, eventMock);
          expect(service['preSimOrLiveSimId']).toEqual('p1');
        });
      });
    });

    describe('player event listener', () => {
      beforeEach(() => {
        service.setTrackingForPlayer(playerMock, eventMock);
        service['getVideoId'] = jasmine.createSpy('getVideoIdSpy').and.returnValue(playerAttrs.id);
      });

      describe('on tracked playing event', () => {
        it('should call startTimer (private)', () => {
          service['startTimer'] = jasmine.createSpy('startTimerSpy');
          rendererListeners['p1_playing']();
          expect(service['startTimer']).toHaveBeenCalledWith(eventMock);
        });
      });

      describe('on tracked pause event', () => {
        const playerEventMock = {};
        beforeEach(() => {
          service['removeInterval'] = jasmine.createSpy('removeIntervalSpy');
          service['pushToGAPlayerStatus'] = jasmine.createSpy('pushToGAPlayerStatusSpy');
        });
        describe('should call removeInterval and pushToGAPlayerStatus (private)', () => {
          it('when video was not stopped', () => {
            expect(((service['trackingVideos'] as any).p1 as any).wasStopped).not.toBeDefined();
          });
          it('when video entry is not defined)', () => {
            service['getVideoId'] = jasmine.createSpy('getVideoIdSpy').and.returnValue(undefined);
          });
          afterEach(() => {
            rendererListeners['p1_pause'](playerEventMock);
            expect(service['removeInterval']).toHaveBeenCalledWith(playerEventMock as any);
            expect(service['pushToGAPlayerStatus']).toHaveBeenCalledWith(eventMock, 'pause');
          });
        });
        it('should exit when video was stopped', () => {
          ((service['trackingVideos'] as any).p1 as any).wasStopped = true;
          rendererListeners['p1_pause'](playerEventMock);
          expect(service['pushToGAPlayerStatus']).not.toHaveBeenCalled();
          expect(service['removeInterval']).not.toHaveBeenCalled();
        });

        afterEach(() => {
          expect(service['getVideoId']).toHaveBeenCalledWith(eventMock);
        });
      });

      describe('on tracked ended event', () => {
        beforeEach(() => {
          service['resetAllTracking'] = jasmine.createSpy('resetAllTrackingSpy');
          service['pushToGAPlayerStatus'] = jasmine.createSpy('pushToGAPlayerStatusSpy');
        });
        describe('if stream has already been completed', () => {
          it('should exit', () => {
            ((service['trackingVideos'] as any).p1 as any).streamCompleted = true;
            rendererListeners['p1_ended']();
            expect(service['pushToGAPlayerStatus']).not.toHaveBeenCalled();
            expect(service['resetAllTracking']).not.toHaveBeenCalled();
          });
        });
        describe('if stream has not been completed', () => {
          beforeEach(() => {
            expect(((service['trackingVideos'] as any).p1 as any).streamCompleted).not.toBeDefined();
            rendererListeners['p1_ended']();
          });
          it('should set streamCompleted flag to true', () => {
            expect(((service['trackingVideos'] as any).p1 as any).streamCompleted).toEqual(true);
          });
          it('should call pushToGAPlayerStatus (private)', () => {
            expect(service['pushToGAPlayerStatus']).toHaveBeenCalledWith(eventMock, 'complete');
          });
          it('should call resetAllTracking (private)', () => {
            expect(service['resetAllTracking']).toHaveBeenCalledWith();
          });
        });
        afterEach(() => {
          expect(service['getVideoId']).toHaveBeenCalledWith(eventMock);
        });
      });
    });
  });

  describe('resetTimer', () => {
    beforeEach(() => {
      service['getVideoId'] = jasmine.createSpy('getVideoIdSpy').and.returnValue(playerAttrs.id);
      spyOn(window, 'clearInterval');
      service.setTrackingForPlayer(playerMock, eventMock);
      (service['trackingVideos'] as any)['p1'].interval = 1;
      (service['trackingVideos'] as any)['p1'].timeWatched = 3;
    });

    it('should reset the timeWatched counter and clear interval for video based on event id', () => {
      service.resetTimer(eventMock);
      expect(window.clearInterval).toHaveBeenCalledWith(1 as any);
      expect(((service['trackingVideos'] as any).p1 as any).timeWatched).toEqual(0);
    });

    it('should do nothing if no video is tracked', () => {
      service['getVideoId'] = jasmine.createSpy('getVideoIdSpy').and.returnValue(undefined);
      service.resetTimer(eventMock);
      expect(window.clearInterval).not.toHaveBeenCalled();
      expect(((service['trackingVideos'] as any).p1 as any).timeWatched).toEqual(3);
    });

    afterEach(() => {
      expect(service['getVideoId']).toHaveBeenCalledWith(eventMock);
    });
  });

  describe('private getVideoId', () => {
    beforeEach(() => { service['preSimOrLiveSimId'] = 'preSim'; });

    it('should return event.target.id if it is available', () => {
      expect(service['getVideoId'](eventMock)).toEqual('p1');
    });
    describe('if event.target.id is not available', () => {
      beforeEach(() => { delete eventMock.target; });

      describe('and if event.id is defined', () => {
        it('should return preSimOrLiveSimId if QL_video player for current event id is tracked', () => {
          (service['trackingVideos'] as any).QL_video_i1 = {};
          expect(service['getVideoId'](eventMock)).toEqual('preSim');
        });
        it('should return event.id if QL_video player for current event id is not tracked', () => {
          expect(service['getVideoId'](eventMock)).toEqual('i1');
        });
      });

      describe('and if event.id is not defined', () => {
        beforeEach(() => { delete eventMock.id; });
        it('should return preSimOrLiveSimId', () => {
          expect(service['getVideoId'](eventMock)).toEqual('preSim');
        });
      });
    });
  });

  describe('private resetAllTracking', () => {
    beforeEach(() => {
      service.setTrackingForPlayer(playerMock, eventMock);
      playerAttrs.id_ = 'p2';
      service.setTrackingForPlayer(playerMock, eventMock);
      (service['trackingVideos'] as any)['p1'].interval = 1;
      (service['trackingVideos'] as any)['p2'].interval = 2;
      spyOn(window, 'clearInterval');
      service['resetAllTracking']();
    });
    it('should unlisten all tracked events for all players', () => {
      ['p1', 'p2'].forEach(player => {
        ['playing', 'pause', 'ended'].forEach(event => expect(rendererUnlisteners[`${player}_${event}`]).toHaveBeenCalled());
      });
    });
    it('should clear intervals for all players', () => {
      expect((window.clearInterval as any).calls.allArgs()).toEqual([[1], [2]]);
    });
  });

  describe('checkIdForDuplicates', () => {
    it('scheckIdForDuplicates true', () => {
      service['trackedIds'] = <any>{
        test: [1, 2, 3]
      };
      expect(service.checkIdForDuplicates(1, 'test')).toEqual(true);
    });

    it('scheckIdForDuplicates false', () => {
      service['trackedIds'] = <any>{
        test: [11, 2, 3]
      };
      expect(service.checkIdForDuplicates(1, 'test')).toEqual(false);
    });
  });

  describe('startTimer', () => {
    let event;

    beforeEach(() => {
      event = <any>{
        target: {
          id: 10
        }
      };

      service['trackingVideos'] = <any>{
        10: {
          streamCompleted: false,
          streamingEvent: {}
        }
      };
    });

    it('!(streamCompleted)', () => {
      service['startTimer'](event);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'streaming',
        liveStreamProgress: 'start'
      }));
    });

    it('(streamCompleted)', () => {
      service['trackingVideos']['10'].streamCompleted = true;

      service['startTimer'](event);
      expect(gtmService.push).not.toHaveBeenCalled();
    });

    it('startWasTracked', () => {
      service['subscribeForPageUnload'] = jasmine.createSpy('subscribeForPageUnload');
      service['pushToGAPlayerStatus'] = jasmine.createSpy('pushToGAPlayerStatus');
      service['trackingVideos']['10'].startWasTracked = true;

      service['startTimer'](event);

      expect(service['subscribeForPageUnload']).not.toHaveBeenCalled();
      expect(service['pushToGAPlayerStatus']).not.toHaveBeenCalled();
    });

    it('isOver30MinutesPlayed', () => {
      service['updateAndCheckTime'] = jasmine.createSpy('updateAndCheckTime');
      service['trackingVideos']['10'].isOver30MinutesPlayed = true;

      service['startTimer'](event);

      expect(service['updateAndCheckTime']).not.toHaveBeenCalled();
    });
  });

  it('clearURL', () => {
    expect(
      service['clearURL']('https://sherwood3-excalibur.ladbrokes.com/test/url')
    ).toEqual('https://sherwood3-excalibur.ladbrokes.com/test');
  });

  describe('subscribeForPageUnload', () => {
    let event, navEvent;

    beforeEach(() => {
      event = <any>{
        target: {
          id: 10
        }
      };
      navEvent = new NavigationEnd(0 , 'test', 'test1');

      service['pushToGAPlayerStatus'] = jasmine.createSpy('pushToGAPlayerStatus');
      service['trackingVideos'] = <any>{
        10: {
          wasStopped: false,
          streamCompleted: true,
          interval: 1,
          timeWatched: 1,
          listeners: {
            pause: jasmine.createSpy('pause'),
            pauseEnded: jasmine.createSpy('pauseEnded'),
            play: jasmine.createSpy('play')
          }
        }
      };
    });

    it('should subscribe for page unload and hash change events', fakeAsync(() => {
      service['subscribeForPageUnload'](event);
      beforeunload();
      expect(service['pushToGAPlayerStatus']).not.toHaveBeenCalled();
      tick();
      routerEventsCb(navEvent);
    }));

    it('should not send "stop" status to GA on router events when URLs match, but on beforeunload event', fakeAsync(() => {
      service['trackingVideos']['10'].streamCompleted = false;
      routingState.getPreviousUrl = jasmine.createSpy('routingState.getPreviousUrl').and.returnValue('test');
      service['subscribeForPageUnload'](event);
      beforeunload();
      expect(service['pushToGAPlayerStatus']).toHaveBeenCalledWith(event, 'stop');
      tick();
      routerEventsCb(navEvent);
      expect(service['pushToGAPlayerStatus']).toHaveBeenCalledTimes(1);
    }));

    it('should send "stop" status to GA both on router events and on beforeunload event', fakeAsync(() => {
      service['trackingVideos']['10'].streamCompleted = false;
      service['subscribeForPageUnload'](event);
      beforeunload();
      expect(service['pushToGAPlayerStatus']).toHaveBeenCalledWith(event, 'stop');
      tick();
      routerEventsCb(navEvent);
      expect(service['pushToGAPlayerStatus']).toHaveBeenCalledTimes(2);
    }));

    it('should not handle router event if it is not of NavigationEnd type', fakeAsync(() => {
      service['subscribeForPageUnload'](event);
      beforeunload();
      tick();
      navEvent = {} as any;
      routerEventsCb(navEvent);
      expect(routingState.getPreviousUrl).not.toHaveBeenCalled();
      expect(routingState.getCurrentUrl).not.toHaveBeenCalled();
    }));

    afterEach(() => {
      expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalledWith('beforeunload', jasmine.any(Function));
      expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalledWith('beforeunload', jasmine.any(Function));
      navEvent instanceof NavigationEnd && expect(routingState.getPreviousUrl).toHaveBeenCalled();
      navEvent instanceof NavigationEnd && expect(routingState.getCurrentUrl).toHaveBeenCalled();
    });
  });

  describe('getEventAction', () => {
    it('getEventAction (Advert)', () => {
      windowRef.nativeWindow._QLGoingDown.status = 'Advert';
      expect(service['getEventAction']()).toEqual('watch pre sim');
    });

    it('getEventAction (nothing)', () => {
      windowRef.nativeWindow._QLGoingDown.status = 'nothing';
      expect(service['getEventAction']()).toEqual('watch video stream');
    });

    it('getEventAction (nothing)', () => {
      windowRef.nativeWindow._QLGoingDown.status = true;
      expect(service['getEventAction']()).toEqual('watch live sim');
    });
  });

  describe('reformatTime', () => {
    beforeEach(() => {
      service['trackingVideos'] = <any>{
        1: {
          isOver30MinutesPlayed: false
        }
      };
    });

    it('reformatTime (over 30 minutes)', () => {
      const event = <any>{
        id: 1
      };
      expect(service['reformatTime'](1860, event)).toEqual('over 30 minutes');
    });

    it('reformatTime (over 1 minute)', () => {
      const event = <any>{
        id: 1
      };
      expect(service['reformatTime'](61, event)).toEqual('1 minutes');
    });

    it('reformatTime (over 1 minute)', () => {
      const event = <any>{
        id: 1
      };
      expect(service['reformatTime'](59, event)).toEqual('59 seconds');
    });
  });

  describe('updateAndCheckTime', () => {
    it('updateAndCheckTime', () => {
      service['trackingVideos'] = <any>{
        1: {
          isOver30MinutesPlayed: false,
          timeWatched: 4000,
          streamingEvent: {}
        }
      };

      const event = <any>{
        id: 1
      };

      service['updateAndCheckTime'](event);
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('updateAndCheckTime', () => {
      service['trackingVideos'] = <any>{
        1: {
          isOver30MinutesPlayed: false,
          timeWatched: 5000,
          streamingEvent: {}
        }
      };

      const event = <any>{
        id: 1
      };

      service['updateAndCheckTime'](event);
      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });

  it('removeInterval', () => {
    service['trackingVideos'] = <any>{
      1: {
        interval: 10
      }
    };

    const event = <any>{
      id: 1
    };

    service['removeInterval'](event);

    expect(service['trackingVideos'][1]).toEqual({});
  });

  it('addIdToTrackedList', () => {
    service['trackedIds'] = <any>{
      10: []
    };

    service.addIdToTrackedList(12, '10');
    expect(service['trackedIds'][10][0]).toEqual(12);
  });

  it('pushToGAPlayerStatus', () => {
    const event = <any>{
      id: 2
    };

    service['pushToGAPlayerStatus'](event, 'test');
    expect(gtmService.push).not.toHaveBeenCalled();
  });
});
