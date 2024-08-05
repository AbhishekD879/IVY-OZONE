import { LiveClockComponent } from '@shared/components/liveClock/live-clock.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('LiveClockComponent', () => {
  let component: any;

  let timeSyncService: any;
  let liveEventClockProviderService: any;
  let fakeClock: any;

  beforeEach(() => {
    timeSyncService = {
      getTimeDelta: jasmine.createSpy('getTimeDelta').and.returnValue('timeDelta')
    };

    fakeClock = {
      ev_id: 'test_id',
      update: jasmine.createSpy('update')
    };

    liveEventClockProviderService = {
      create: jasmine.createSpy().and.returnValue(fakeClock)
    };

    component = new LiveClockComponent(
      timeSyncService,
      liveEventClockProviderService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('event input', () => {
    it('should set event', () => {
      component.event = {};
      expect(component.event).toEqual({});
    });

    it('should not set other properties for input event that is not set', () => {
      component.event = undefined;
      expect(component.liveTime).toEqual(null);
    });

    it('should do nothing when no data in event', () => {
      expect(() => {
        component.event = {};
      }).not.toThrow();
      expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });

    it('should create clock and run timer', () => {
      component.event = {
        initClock: {
          ev_id: '23',
        }
      };
      expect(liveEventClockProviderService.create).toHaveBeenCalledWith('timeDelta',
        {
          ev_id: '23'
        });
    });

    it('should start timer for existing clock', fakeAsync(() => {
      const clockUpdatedSpy = spyOn(component.clockUpdated, 'emit');
      component.event = {
        clock: {
          ev_id: '23',
          update: jasmine.createSpy('update')
        }
      };
      expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
      expect(component.liveTime).toBeDefined();
      const subscription = component.liveTime.subscribe();
      tick(2000);
      subscription.unsubscribe();
      expect(clockUpdatedSpy).toHaveBeenCalled();
    }));
  });

});
