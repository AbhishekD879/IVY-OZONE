import { BybHomeComponent } from '@yourcall/components/bybHome/byb-home.component';
import { fakeAsync, tick, flush } from '@angular/core/testing';

describe('BybHomeComponent', () => {
  let component;
  let bybHomeService;
  let changeDetectorRef;

  beforeEach(() => {
    bybHomeService = {
      getLeagues: jasmine.createSpy('getLeagues').and.returnValue(Promise.all([])),
      leaguesStatuses: {
        1: true
      },
      todayLeagues: [{
        obTypeId: 1,
        expaned: false
      }, {
        expaned: false,
        obTypeId: 2
      },
      {
        expaned: false,
        obTypeId: 3
      }]
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new BybHomeComponent(bybHomeService, changeDetectorRef);

  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.state.loading).toBe(true);
    expect(component.state.error).toBe(false);
    expect(component.isUsedFromWidget).toBe(false);
    expect(component.switchers).toEqual(null);
    expect(component.filter).toEqual(null);
    expect(component.displayData).toEqual(null);
    expect(component.loaded).toEqual(false);
    expect(component.viewByFilters).toEqual([
      'today',
      'upcoming'
    ]);
  });

  describe('#ngOnInit', () => {
    it('should call ngOnInit when switchers are presen and generate proper switchers', fakeAsync(() => {
      component.ngOnInit();
      expect(component.state.loading).toBe(true);
      tick(100);

      expect(bybHomeService.getLeagues).toHaveBeenCalled();
      expect(component.switchers).toEqual([{ name: 'yourcall.today', onClick: jasmine.any(Function), viewByFilters: 'today' }]);
      component.contentReady = true;
      component.initialPageLoad = true;
      component.switchers[0].onClick();
      expect(component.contentReady).toBeFalsy();
      expect(component.initialPageLoad).toBeFalsy();
      expect(component.state.loading).toBe(false);
    }));

    it('should call ngOnInit when no switchers', fakeAsync(() => {
      component['createSwitchers'] = jasmine.createSpy('createSwitchers');
      component.ngOnInit();
      tick(100);

      expect(bybHomeService.getLeagues).toHaveBeenCalled();
      expect(component.switchers).toEqual(null);
    }));

    it('handle error on failure', fakeAsync(() => {
      bybHomeService.getLeagues.and.returnValue(Promise.reject(''));
      component.ngOnInit();
      flush();

      expect(component.state.error).toBe(true);
    }));
  });


  describe('#ngOnDestroy', () => {
    it('should call ngOnDestroy when no displayData', () => {
      component.displayData = null;
      component.ngOnDestroy();
    });

    it('should call ngOnDestroy when displayData are present', () => {
      component.displayData = [{ expaned: true}] as any;
      component.ngOnDestroy();
      expect(component.displayData).toEqual([{ expaned: false }]);
    });
  });

  describe('#trackByLeague', () => {
    it('should call trackByLeague method', () => {
      const result = component.trackByLeague(1, {status: 'active', title: 'EPL', obTypeId: '223'});

      expect(result).toEqual('1activeEPL223');
    });
  });

  describe('#showSwitchers', () => {
    it('should call showSwitchers method whith swithers', () => {
      component.switchers = [{
        name: 'today',
        viewByFilters: [],
        onClick: () => { }
      }];
      const result = component.showSwitchers();

      expect(result).toEqual(true);
    });

    it('should call showSwitchers method when no switchers', () => {
      const result = component.showSwitchers();

      expect(result).toEqual(null);
    });
  });

  describe('#getTitle', () => {
    it('should call getTitle method when league not normilized', () => {
      const result = component.getTitle({ normilized: false, title: 'title'} as any);

      expect(result).toEqual('title');
    });

    it('should call getTitle method when league is normilized', () => {
      const result = component.getTitle(
        {
          normilized: true,
          title: 'title',
          categoryName: 'categoryName',
          className: 'className',
          typeName: 'typeName'
        } as any
      );

      expect(result).toEqual('categoryName - className - typeName');
    });
  });

  describe('#trackExpandCollapse', () => {
    it('should call trackExpandCollapse', () => {
      const league = { expaned: false } as any;
      component.trackExpandCollapse(league);

      expect(league.expaned).toEqual(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#shouldCreateSwitcher', () => {
    it('should call shouldCreateSwitcher returns true', () => {
      const league = { obTypeId: 1 } as any;
      const result = component['shouldCreateSwitcher']([league, { obTypeId: 2}]);

      expect(result).toEqual(true);
    });

    it('should call shouldCreateSwitcher returns false', () => {
      const league = { obTypeId: 2 } as any;
      const result = component['shouldCreateSwitcher']([league, { obTypeId: 2 }]);

      expect(result).toEqual(false);
    });
  });

  describe('#selectSwitcher', () => {
    it('should call selectSwitcher', () => {
      component.leaguesStatuses = {
        1: true,
        2: false,
        3: true
      };
      expect(component.displayData).toEqual(null);

      component['selectSwitcher']('today');

      expect(component.filter).toEqual('today');
      expect(component.displayData).toEqual([{
        obTypeId: 1,
        expaned: true,
        initiallyExpanded: true,
        eventsLoaded: false
      }, {
        expaned: false,
        obTypeId: 2
      }, {
        obTypeId: 3,
        expaned: true,
        initiallyExpanded: true,
        eventsLoaded: false
      }]);
    });
  });
  describe('handleEventsLoaded', () => {
    it('should return false if displayData is undefined', () => {
      expect(component.contentReady).toBeFalsy();
      component['displayData'] = undefined as any;
      component['handleEventsLoaded']();
      expect(component.contentReady).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should return false if opened sections not initialized yet', () => {
      component.displayData = [
        {
          initiallyExpanded: true,
          eventsLoaded: false,
          obTypeId: 1
        },
        {
          initiallyExpanded: false,
          eventsLoaded: false,
          obTypeId: 2
        }
      ] as any;
      component.leaguesStatuses = {
        1: true,
        2: false
      };
      component['handleEventsLoaded']();
      expect(component['contentReady']).toBeFalsy();
    });
    it('should return true if opened sections already initialized', () => {
      component.displayData = [
        {
          initiallyExpanded: true,
          eventsLoaded: true
        },
        {
          initiallyExpanded: false,
          eventsLoaded: false
        }
      ] as any;
      component['handleEventsLoaded']();
      expect(component['contentReady']).toBeTruthy();
    });
    it('should return false if league status is true but events are not loaded', () => {
      expect(component.contentReady).toBeFalsy();
      component.displayData = [
        {
          initiallyExpanded: true,
          eventsLoaded: false,
          obTypeId: 1
        }
      ] as any;
      component.leaguesStatuses = {
        1: true
      };

      component['handleEventsLoaded']();
      expect(component.contentReady).toBeFalsy();
    });
  });
  describe('getLeagues', () => {
    it('should handle error case for getLeagues', fakeAsync(() => {
      bybHomeService.getLeagues = jasmine.createSpy().and.returnValue(Promise.reject());

      component.getLeagues();
      tick();

      expect(component.loaded).toBeTruthy();
      expect(component.contentReady).toBeTruthy();
    }));

    it('should handle content loaded state', fakeAsync(() => {
      component.switchers = [];

      component.getLeagues();
      tick();

      expect(component.loaded).toBeTruthy();
      expect(component.contentReady).toBeTruthy();
    }));
  });
});
