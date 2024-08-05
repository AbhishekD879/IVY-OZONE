import { CompetitionFiltersComponent } from './competition-filters.component';
import { of } from 'rxjs';

describe('CompetitionFiltersComponent', () => {
  let component: CompetitionFiltersComponent;
  let activatedRoute;
  let changeDetectorRef;
  let gtmService;

  beforeEach(() => {
    activatedRoute = {
      params: of({})
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new CompetitionFiltersComponent(activatedRoute, changeDetectorRef, gtmService);

    component.filters = [
      { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
      { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
    ];
    component.sportId = '16';
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should call detectChanges', () => {
      activatedRoute.params = of({
        typeName: 'typeName',
        className: 'className'
      });
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: false, name: '3h', type: 'Time', value: 3 }
      ]);
    });

    it('should call detectChanges when tab param is present and equals `today', () => {
      activatedRoute.params = of({ tab: 'today' });
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: false, name: '3h', type: 'Time', value: 3 }
      ]);
    });

    it('should not call detectChanges when tab param is present but differs from `today', () => {
      activatedRoute.params = of({ tab: 'tomorrow' });
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
    });

    it('should not call detectChanges when typeName equals undefined', () => {
      activatedRoute.params = of({ className: 'className' });
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
    });

    it('should not call detectChanges when className equals undefined', () => {
      activatedRoute.params = of({ typeName: 'typeName' });
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
    });

    it('should not call detectChanges when params is undefined', () => {
      component.ngOnInit();

      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
    });
  });

  describe('#ngOnDestroy', () => {
    it('should unsubscribe', () => {
      component['routeSubscription'] = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
      component.ngOnDestroy();

      expect(component['routeSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('#onFilterChange', () => {
    let event;

    beforeEach(() => {
      component.filterChange.emit = jasmine.createSpy('emit');
      event = { id: '1', active: true, name: '1h', type: 'Time', value: 1 };
    });

    it('should emit filter change', () => {
      component.onFilterChange(event);

      expect(component.filterChange.emit).toHaveBeenCalled();
    });

    it('should set active = false', () => {
      component.onFilterChange(event);

      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: false, name: '3h', type: 'Time', value: 3 }
      ]);
      expect(component.filterChange.emit).toHaveBeenCalled();
    });

    it('should not set active = false when filter.type !== event.type', () => {
      event.type = 'League';
      component.onFilterChange(event);

      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
      expect(component.filterChange.emit).toHaveBeenCalled();
    });

    it('should not set active = false when filter.id !== event.id', () => {
      event.id = '5';
      component.onFilterChange(event);

      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: false, name: '3h', type: 'Time', value: 3 }
      ]);
      expect(component.filterChange.emit).toHaveBeenCalled();
    });

    it('should not set active = false when filter.type !== event.type and filter.id !== event.id', () => {
      event.type = 'League';
      event.id = '5';
      component.onFilterChange(event);

      expect(component.filters).toEqual([
        { id: '1', active: false, name: '1h', type: 'Time', value: 1 },
        { id: '2', active: true, name: '3h', type: 'Time', value: 3 }
      ]);
      expect(component.filterChange.emit).toHaveBeenCalled();
    });
    it('should pull data to gtmService with select', () => {
      component.onFilterChange(event);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'time filters',
        eventAction: '1h',
        eventLabel: 'select',
        categoryID: '16'
      });
    });
    it('should pull data to gtmService with deselect', () => {
      event.active = false;
      component.onFilterChange(event);

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        event: 'trackEvent',
        eventCategory: 'time filters',
        eventAction: '1h',
        eventLabel: 'deselect',
        categoryID: '16'
      });
    });
  });

  describe('#trackByIndex', () => {
    it('should return index', () => {
      const result = component.trackByIndex(1);

      expect(result).toEqual(1);
    });
  });
});
