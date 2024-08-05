import { StatsDropDownComponent } from './stats-drop-down.component';
import { of } from 'rxjs';

describe('StatDropDownComponent', () => {
  let component: StatsDropDownComponent;
  let fiveASideService;
  let gtmService;

  beforeEach(() => {
    fiveASideService = {
      getPlayerStats: jasmine.createSpy('getPlayerStats').and.returnValue([]),
      activeView: 'player-page',
      loadPlayerStats: jasmine.createSpy('loadPlayerStats').and.returnValue(of([] as any))
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new StatsDropDownComponent(fiveASideService, gtmService);
    component.eventEntity = { id: 1 } as any;
    component.player = { id: 2 } as any;
    component.formation = { statId: 3, stat: 'Stat3' } as any;
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(fiveASideService.getPlayerStats)
      .toHaveBeenCalledWith(component.eventEntity.id, component.player.id);
  });

  describe('#ngOnInit', () => {
    it('should call getPlayerStats, if it is player page scenario', () => {
      component.ngOnInit();
      expect(fiveASideService.getPlayerStats)
        .toHaveBeenCalledWith(component.eventEntity.id, component.player.id);
    });
    it('should call loadPlayerStats, if it is players-list scenario', () => {
      fiveASideService.activeView = 'player-list';
      component.ngOnInit();
      expect(fiveASideService.loadPlayerStats)
        .toHaveBeenCalledWith(component.eventEntity.id, component.player.id);
    });
  });

  it('trackByFn', () => {
    expect(component.trackByFn(0, { id: 1 } as any)).toBe(1);
  });

  describe('clickItem', () => {
    beforeEach(() => {
      spyOn(component.statChange, 'emit');
      spyOn(component, 'menuToggle');
    });

    it('should emit item', () => {
      component.clickItem({ id: 4 } as any);
      expect(component.statChange.emit).toHaveBeenCalledWith({ id: 4 } as any);
    });

    it('should not emit item', () => {
      component.clickItem({ id: 3 } as any);
      expect(component.statChange.emit).not.toHaveBeenCalled();
    });
  });

  describe('menuToggle', () => {
    it('should show menu', () => {
      const eventData = {
        eventCategory: '5-A-Side',
        eventAction: 'Show Markets',
        eventLabel: 'Market Dropdown'
      };
      component.menuToggle();
      expect(component.showMenu).toBeTruthy();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', eventData);
    });

    it('should hide menu', () => {
      const eventData = {
        eventCategory: '5-A-Side',
        eventAction: 'Hide Markets',
        eventLabel: 'Market Dropdown'
      };
      component.menuToggle(false);
      expect(component.showMenu).toBeFalsy();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', eventData);
    });
  });

  describe('clickHandler', () => {
    let clickEvent;
    beforeEach(() => {
      clickEvent = { preventDefault: jasmine.createSpy('preventDefault') };
    });

    it('should not prevent default', () => {
      component.clickHandler(clickEvent);
      expect(clickEvent.preventDefault).not.toHaveBeenCalled();
    });

    it('should prevent event and close menu', () => {
      spyOn(component, 'menuToggle');
      clickEvent.cancelable = true;
      component.clickHandler(clickEvent);
      expect(clickEvent.preventDefault).toHaveBeenCalled();
      expect(component.menuToggle).toHaveBeenCalledWith(false);
    });
  });
});
