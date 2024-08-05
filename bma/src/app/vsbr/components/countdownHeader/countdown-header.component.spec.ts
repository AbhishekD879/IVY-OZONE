import { CountdownHeaderComponent } from './countdown-header.component';

describe('CountdownHeaderComponent', () => {
  let component;
  let changeDetectorRef;
  let virtualSportsService;
  let events;
  let timeService;

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };
    virtualSportsService = {
      time: {
        subscribe: jasmine.createSpy('subscribe'),
      }
    };
    jasmine.clock().mockDate(new Date(Date.now()));
    events = {
      startsInHour: {
        name: 'Event starts in hour',
        startTimeUnix: Date.now() + 1000 * 60 * 60,
      },
      startsInTwoHours: {
        name: 'Event starts in two hours',
        startTimeUnix: Date.now() + 1000 * 60 * 120,
      },
      startsInTenSeconds: {
        name: 'Event starts in 10 sec',
        startTimeUnix: Date.now() + 1000 * 10,
      },
      startedFiveSecondsAgo: {
        name: 'Event started 5 sec ago',
        startTimeUnix: Date.now() - 1000 * 5,
      },
    };
    timeService = {
      min: 60000
    };
    component = new CountdownHeaderComponent(changeDetectorRef, virtualSportsService, timeService);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnChanges', () => {
    let changes;
    beforeEach(() => {
      changes = {
        eventName: {
          currentValue: events.name
        },
        startTimeUnix: {
          currentValue: events.startsInTenSeconds
        }
      };
    });

    it('should not set eventName', () => {
      delete changes.eventName;
      component.ngOnChanges(changes);
      expect(component.eventName).toBeUndefined();
    });

    it('should not set startTimeUnix', () => {
      delete changes.startTimeUnix;
      component.ngOnChanges(changes);
      expect(component.startTimeUnix).toBeUndefined();
    });

    it('should set eventName', () => {
      component.ngOnChanges(changes);
      expect(component.eventName).toEqual(changes.eventName.currentValue);
    });

    it('should set startTimeUnix', () => {
      component.ngOnChanges(changes);
      expect(component.startTimeUnix).toEqual(changes.startTimeUnix.currentValue);
    });

    it('should create timer', () => {
      virtualSportsService.time = {
        subscribe: jasmine.createSpy('subscribe').and.callFake((callback) => callback()),
      };
      component.ngOnChanges(changes);
      expect(component.timeLeft).toBeDefined();
      expect(component.fillDeg).toBeDefined();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('fillStroke', () => {
    describe('should return', () => {
      it('0 if event starts in more than 30 sec', () => {
        component.startTimeUnix = events.startsInTwoHours.startTimeUnix;
        expect(component.fillStroke(Date.now())).toEqual(0);
      });

      it('a value in range 0 to 180 to fill the countdown rgadually', () => {
        component.startTimeUnix = events.startsInTenSeconds.startTimeUnix;
        expect(component.fillStroke(Date.now())).toBeGreaterThanOrEqual(0);
        expect(component.fillStroke(Date.now())).toBeLessThanOrEqual(180);
      });

      it('a value (180) to fill the countdown fully', () => {
        component.startTimeUnix = events.startedFiveSecondsAgo.startTimeUnix;
        expect(component.fillStroke(Date.now())).toEqual(180);
      });
    });
  });

  describe('getTimeLeft', () => {
    describe('should return', () => {
      it('formatted date if event has not started', () => {
        component.startTimeUnix = events.startsInTenSeconds.startTimeUnix;
        const result = component.getTimeLeft(Date.now());
        expect(result).not.toEqual('LIVE');
      });

      it('LIVE string if event has already started', () => {
        component.startTimeUnix = events.startedFiveSecondsAgo.startTimeUnix;
        expect(component.getTimeLeft(Date.now())).toEqual('LIVE');
      });
    });
    it('should add hours to minutes', () => {
      component.startTimeUnix = events.startsInTwoHours.startTimeUnix;
      const result = component.getTimeLeft(Date.now());
      expect(result).not.toEqual('LIVE');
    });
  });

  describe('ngOnDestroy', () => {
    it('should clear interval', () => {
      component.timerSubscription = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component.timerSubscription.unsubscribe).toHaveBeenCalledTimes(1);
    });
    it('should not do anything', () => {
      component.timerSubscription = null;
      expect(() => {
        component.ngOnDestroy();
      }).not.toThrow();
    });
  });
});
