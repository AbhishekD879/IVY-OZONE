import { SpecialsSportTabComponent } from '@app/lazy-modules/specialsSportTab/components/specials-sport-tab.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('SpecialsSportTabComponent', () => {
  let component: SpecialsSportTabComponent;
  let sportTabsService: any;
  let pubSubService: any;
  let sport: any;

  beforeEach(() => {
    sportTabsService = {
      deleteEvent: jasmine.createSpy(),
      eventsBySections: jasmine.createSpy()
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, callback) => {
        callback(1);
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      }
    };

    component = new SpecialsSportTabComponent(sportTabsService, pubSubService);

    sport = {
      getByTab: jasmine.createSpy().and.returnValue(of([])),
      subscribeLPForUpdates: jasmine.createSpy(),
      unSubscribeLPForUpdates: jasmine.createSpy()
    };
    component.display = 'specials';
    component.sport = sport;
  });

  it('ngOnInit should call methods', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
    expect(sportTabsService.deleteEvent).toHaveBeenCalledTimes(1);
    expect(sportTabsService.deleteEvent).toHaveBeenCalledWith(1, []);
    expect(sport.getByTab).toHaveBeenCalledWith('specials');
    expect(sport.subscribeLPForUpdates).toHaveBeenCalledTimes(1);
  });

  it('ngOnDestroy should call methods', () => {
    component.ngOnInit();
    component.ngOnDestroy();
    expect(sport.unSubscribeLPForUpdates).toHaveBeenCalledTimes(1);
    expect(component['loadSubscription'].closed).toBeTruthy();
  });

  describe('isEnhancedMultiplesSection', () => {
    let data: any;

    beforeEach(() => {
      data = {events: {length: 1}, typeName: 'Enhanced Multiples'};
    });

    it('should return correct value if length is more than 0', () => {
      expect(component.isEnhancedMultiplesSection(data)).toBeTruthy();
    });

    it('should return correct value if length is equal 0', () => {
      data.events.length = 0;
      expect(component.isEnhancedMultiplesSection(data)).toBeFalsy();
    });

    it('should return correct value if typeName is incorrect', () => {
      data.typeName = 'some type';
      expect(component.isEnhancedMultiplesSection(data)).toBeFalsy();
    });
  });

  it('trackByTypeId should return correct id', () => {
    expect(component.trackByTypeId(1, {typeId: 'some id'} as any)).toEqual('some id');
  });

  it('trackById should return correct id', () => {
    expect(component.trackById(1, {id: 2} as any)).toEqual(2);
  });

  it('trackByIndex should return correct id', () => {
    expect(component.trackByIndex(2)).toEqual(2);
  });

  describe('loadSpecialsData', () => {
    let data;

    beforeEach(() => {
      data = {
        length: 5
      };
    });

    it('should set properties and call then after promise resolve', fakeAsync(() => {
      (component.sport.getByTab as any).and.returnValue(of(data));

      component['loadSpecialsData']();

      tick();

      expect(sportTabsService.eventsBySections).toHaveBeenCalled();
      expect(sport.subscribeLPForUpdates).toHaveBeenCalled();
    }));

    it('should set properties and call then after promise resolve with null', fakeAsync(() => {
      (component.sport.getByTab as any).and.returnValue(of(null));

      component['loadSpecialsData']();

      tick();

      expect(sportTabsService.eventsBySections).not.toHaveBeenCalled();
    }));

    it('should set properties and call then after promise reject', fakeAsync(() => {
      spyOn(console, 'warn');
      (component.sport.getByTab as any).and.returnValue(throwError(null));

      component['loadSpecialsData']();

      tick();

      expect(component.isLoaded).toBeTruthy();
      expect(component.isResponseError).toBeTruthy();
      expect(console.warn).toHaveBeenCalledWith('Specials Data:', null);
    }));

    it('should warn with given error', fakeAsync(() => {
      spyOn(console, 'warn');
      (component.sport.getByTab as any).and.returnValue(throwError({ error: 'error' }));

      component['loadSpecialsData']();

      tick();

      expect(component.isLoaded).toBeTruthy();
      expect(component.isResponseError).toBeTruthy();
      expect(console.warn).toHaveBeenCalledWith('Specials Data:', 'error');
    }));
  });
});
