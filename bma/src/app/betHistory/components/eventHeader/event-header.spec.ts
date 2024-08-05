import { FiltersService } from '@core/services/filters/filters.service';
import { EventHeaderComponent } from '@app/betHistory/components/eventHeader/event-header.component';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { EventService } from '@sb/services/event/event.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('EventHeaderComponent', () => {

  let component: EventHeaderComponent;

  const today = new Date();
  const future = new Date();
  future.setDate(future.getDate() + 1);

  function fakeCall(time) {
      const formatted = new Date(time);
      /* eslint-disable */
      return time === `${today}` ? `${formatted.getHours()}:${today.getMinutes()}, Today` :
        `${formatted.getHours()}:${formatted.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${formatted.toLocaleString('en-US', { month: 'short' })}`;
      /* eslint-enable */
  }

  const timeServiceStub = {
    getEventTime: jasmine.createSpy().and.callFake(fakeCall),
    animationDelay: 5000,
    formatByPattern: jasmine.createSpy()
  };

  const filterServiceStub: Partial<FiltersService> = {};
  const coreToolsStub: Partial<CoreToolsService> = {
    getDaySuffix: jasmine.createSpy('getDaySuffix').and.returnValue('st')
  };
  const localeStub: Partial<LocaleService> = {
    getString: () => 'test'
  };
  const eventServiceStub: Partial<EventService> = {
    isLiveStreamAvailable: () => {
      return { liveStreamAvailable: false };
    }
  } as any;
  const windowRefStub: Partial<WindowRefService> = {
    nativeWindow: {
      clearTimeout: jasmine.createSpy('clearTimeout'),
      setTimeout: jasmine.createSpy('setTimeout').and.callFake((fn, time) => { fn(); })
    }
  }

  const sessionStorageStub = {
      get: jasmine.createSpy('get').and.returnValue({'123-123-125':{time:'12-2-2023 2:33:33',eventName:'testevent',id:'12345'}}),
      set: jasmine.createSpy('set')
  };

  const eventNamePipeStub = {
    transform: jasmine.createSpy('transform').and.returnValue('test event name')
  };

  beforeEach(() => {
    component = new EventHeaderComponent(
      timeServiceStub as any,
      coreToolsStub as any,
      localeStub as any,
      eventServiceStub as any,
      windowRefStub as any,
      filterServiceStub as any,
      sessionStorageStub as any,
      eventNamePipeStub as any
    );
    component.id = '123';
    component.outcomeId = '125';
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should check correct today event startTime format', fakeAsync(() => {
    component.event = { startTime: today, id:'123' } as any;
    const formatted = `${today.getHours()}:${today.getMinutes()}, Today`;
    component.ngOnInit();
    tick();

    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(`${today}`);
    expect(component.timerLabel).toEqual(formatted);
  }));

  it('should check correct future event startTime format', fakeAsync(() => {
    /* eslint-disable */
    const formatted = `${future.getHours()}:${future.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${future.toLocaleString('en-US', { month: 'short' })}`;
    /* eslint-enable */

    component.event = { startTime: future, id:'123' } as any;
    component.ngOnInit();
    tick();

    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(`${future}`);
    expect(component.timerLabel).toEqual(formatted);
  }));

  it('should check update sesion data with no clock', fakeAsync(() => {
    component.event = { startTime: today, id:'123' } as any;
    component.event.clock = {liveScore:null};
    component.eventName = "test event";
    const formatted = `${today.getHours()}:${today.getMinutes()}, Today`;
    component.ngOnInit();
    tick();

    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(`${today}`);
    expect(component.timerLabel).toEqual(formatted);
    //expect(component.sessionData['123-123-125'].eventName).toEqual('test event name');
  }));

  it('should check update sesion data with clock', fakeAsync(() => {
    component.event = { startTime: today, id:'123' } as any;
    component.event.clock = {liveTime:'12:23'};
    component.eventName = "test event";
    const formatted = `${today.getHours()}:${today.getMinutes()}, Today`;
    component.ngOnInit();
    tick();

    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(`${today}`);
    expect(component.timerLabel).toEqual(formatted);
    expect(component.sessionData['123-123-125'].eventName).toEqual('test event name');
  }));

  it('should check update sesion data without clock', fakeAsync(() => {
    component.event = { startTime: today, id:'123' } as any;
    component.isLabelShown = true;
    component.legType = 'E';
    component.place = '2';
    component.placeWithFormat = "2nd";
    component.eventName = "test event";
    const formatted = `${today.getHours()}:${today.getMinutes()}, Today`;
    component.ngOnInit();
    tick();

    expect(timeServiceStub.getEventTime).toHaveBeenCalledWith(`${today}`);
    expect(component.sessionData['123-123-125'].eventName).toEqual('test event name');
  }));

  describe('setPlaceWithFormat', () => {
    it('when place = 31', () => {
      const place = '31';
      component['setPlaceWithFormat'](place);

      expect(coreToolsStub.getDaySuffix).toHaveBeenCalledWith(place);
      expect(component.placeWithFormat).toEqual(`31st Place`);
    });

    it('when place = 2', () => {
      const place = '2';
      coreToolsStub.getDaySuffix = jasmine.createSpy('getDaySuffix').and.returnValue('nd');
      component['setPlaceWithFormat'](place);

      expect(coreToolsStub.getDaySuffix).toHaveBeenCalledWith(place);
      expect(component.placeWithFormat).toEqual(`2nd Place`);
    });

    it('when place = 3', () => {
      const place = '3';
      coreToolsStub.getDaySuffix = jasmine.createSpy('getDaySuffix').and.returnValue('rd');
      component['setPlaceWithFormat'](place);

      expect(coreToolsStub.getDaySuffix).toHaveBeenCalledWith(place);
      expect(component.placeWithFormat).toEqual(`3rd Place`);
    });

    it('when place = 10', () => {
      const place = '10';
      coreToolsStub.getDaySuffix = jasmine.createSpy('getDaySuffix').and.returnValue('th');
      component['setPlaceWithFormat'](place);

      expect(coreToolsStub.getDaySuffix).toHaveBeenCalledWith(place);
      expect(component.placeWithFormat).toEqual(`10th Place`);
    });
  });

  describe('hasScores', () => {
    describe('football', () => {
      it('falsy 3', () => {
        component.isFootball = true;
        component.event = {} as any;
        expect(component.hasScores).toBeFalsy();
      });

      it('falsy 4', () => {
        component.isFootball = true;
        component.event = {
          comments: {}
        } as any;
        expect(component.hasScores).toBeFalsy();
      });

      it('falsy 5', () => {
        component.isFootball = true;
        component.event = {
          comments: { teams: {} }
        } as any;
        expect(component.hasScores).toBeFalsy();
      });

      it('falsy 6', () => {
        component.isFootball = true;
        component.event = {
          comments: {
            teams: { home: {} }
          }
        } as any;
        expect(component.hasScores).toBeFalsy();
      });

      it('should return false if score is not defined', () => {
        component.isFootball = true;
        component.event = {
          comments: {
            teams: {
              home: { score: undefined }
            }
          }
        } as any;
        expect(component.hasScores).toBeFalsy();
      });

      it('should return true if score is a string', () => {
        component.isFootball = true;
        component.event = {
          comments: {
            teams: {
              home: { score: '0' }
            }
          }
        } as any;
        expect(component.hasScores).toBeTruthy();
      });

      it('should return True if some score is defined', () => {
        component.isFootball = true;
        component.event = {
          comments: {
            teams: {
              home: { score: undefined },
              away: { score: '1' }
            }
          }
        } as any;
        expect(component.hasScores).toBeTruthy();
      });
    });

    it('should return true if score is a number', () => {
      component.isFootball = true;
      component.event = {
        comments: {
          teams: {
            home: { score: 0 }
          }
        }
      } as any;
      expect(component.hasScores).toBeTruthy();
    });
  });

  describe('Cricket', () => {
    beforeEach(() => {
      component.event = {
        comments: {
          teams: {
            home: { score: 'A U21' },
            away: { score: 'A 234/5d' }
          }
        }
      } as any;
    });

    it('should return true if score is a string', () => {
      expect(component.hasScores).toBeTruthy();
    });

    it('should return true if away score is a number', () => {
      delete component.event.comments.teams.home;
      component.event.comments.teams.away.score = 0;
      expect(component.hasScores).toBeTruthy();
    });
  });

  describe('ngOnChanges', () => {
    it('should call updateMatchTimerLabel method', () => {
      spyOn(component, 'updateMatchTimerLabel' as any);
      spyOn(component, 'updateSession' as any);
      component['ngOnChanges']({
        runningSetIndex: {
          firstChange: false
        }
      } as any);
      expect(component['updateMatchTimerLabel']).toHaveBeenCalled();
    });

    it('updateMatchTimerLabel should set timerLabel as HT when result is W', () => {
      component.isFootball = true;
      component.event = {
        comments: {
          teams: { home: {} }
        },
        clock: {
          matchTime: 'HT'
        },
        id:'123'
      } as any;
      component.result = 'W';
      component['updateMatchTimerLabel']();
      expect(component.timerLabel).toBe('HT');
      expect(component.isLiveEvent).toBeTruthy();
    });

    it('updateMatchTimerLabel should set timerLabel as HT when result is -', () => {
      component.isFootball = true;
      component.event = {
        comments: {
          teams: { home: {} }
        },
        clock: {
          matchTime: 'HT'
        },
        id:'123'
      } as any;
      component.result = '-';
      component['updateMatchTimerLabel']();
      expect(component.timerLabel).toBe('HT');
      expect(component.isLiveEvent).toBeTruthy();
    });

    it('should set suspended status true method if status not suspended', () => {
      component['status'] = 'suspended';
      component['ngOnChanges']({
        status: {
          firstChange: false
        }
      } as any);
      expect(component['isSuspendedEvent']).toBeTruthy();
    });
    it('should set suspended status false method if status not suspended', () => {
      component['status'] = 'open';
      component['ngOnChanges']({
        status: {
          firstChange: false
        }
      } as any);
      expect(component['isSuspendedEvent']).toBeFalsy();
    });
  });

  describe('ngOnInit', () => {
    it('should set event name as original name for horse racing event', fakeAsync(() => {
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
      component.event = {
        categoryId: '21',
        localTime: '22:00',
        originalName: '16:25 Nottingham',
        name: 'Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('16:25 Nottingham');
    }));

    it('should set event name as original name for greyhounds event', fakeAsync(() => {
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
      component.event = {
        categoryId: '19',
        localTime: '22:00',
        originalName: '16:25 Nottingham',
        name: 'Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('16:25 Nottingham');
    }));

    it('should set event name as event name with local time for virtual horse racing event', fakeAsync(() => {
      timeServiceStub.formatByPattern.and.returnValue('20:00');
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
      component.event = {
        categoryId: '39',
        classId: 285,
        startTime: 1582747200000,
        localTime: '20:00',
        originalName: '20:00 Nottingham',
        name: 'Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('20:00 Nottingham');
    }));

    it('should set event name as event name without original name for virtual horse racing event', fakeAsync(() => {
      timeServiceStub.formatByPattern.and.returnValue('20:00');
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
      component.event = {
        categoryId: '39',
        classId: 285,
        startTime: 1582747200000,
        name: '20:00 Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('20:00 Nottingham');
    }));

    it('should set event name as event name with local time for virtual greyhounds event', fakeAsync(() => {
      timeServiceStub.formatByPattern.and.returnValue('20:00');
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(true);
      component.event = {
        categoryId: '39',
        classId: 286,
        startTime: 1582747200000,
        localTime: '20:00',
        originalName: '20:00 Nottingham',
        name: 'Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('20:00 Nottingham');
    }));

    it('should set event name as name for greyhounds event if originalName does not exists', fakeAsync(() => {
      component['checkForHorse'] = jasmine.createSpy().and.returnValue(false);
      component.event = {
        categoryId: '19',
        name: 'Nottingham',
        localTime: '22:00', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('Nottingham');
    }));

    it('should set event name as name for horse racing event if originalName does not exists', fakeAsync(() => {
      component.event = {
        categoryId: '21',
        localTime: '22:00',
        name: 'Nottingham', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('Nottingham');
    }));

    it('should set event name as name for all other sports event(not greyhounds or horse racing virtual or not)', fakeAsync(() => {
      component.event = {
        categoryId: '16',
        originalName: 'Arsenal vs Manchester City 2:0',
        name: 'Arsenal vs Manchester City', id:'123'
      } as any;

      component.ngOnInit();
      tick();

      expect(component.eventName).toBe('Arsenal vs Manchester City');
    }));
  });
  describe('checkForHorse', () => {
    it('checkForHorse if event has id', () => {
      const event = {
        categoryId: '1',
        localTime: '22:00',
        name: 'home v away'
      } as any;
      component['checkForHorse'](event);
    });
    it('checkForHorse if event does not have id', () => {
      const event = {
        categoryId: '39',
        localTime: '22:00',
        name: 'home'
      } as any;
      component['checkForHorse'](event);
    });
  });

  it('should call updatesession and session storage as empty', () => {
    sessionStorageStub.get = jasmine.createSpy('get').and.returnValue(null);
    component.updateSession();
    expect(component).toBeTruthy;
  })
});
