import { of, throwError } from 'rxjs';
import { fakeAsync, flush } from '@angular/core/testing';

import { ToteTabsResultsComponent } from './tote-tabs-results.component';

describe('ToteTabsResultsComponent', () => {
  let component: ToteTabsResultsComponent;
  let userService,
    raceOutcomeDetailsServiceStub,
    toteServiceStub,
    locationService,
    filterServiceStub,
    routerStub,
    activatedRouteStub,
    pubSubService,
    navigationService;

  beforeEach(() => {
    userService = {
      oddsFormat: 'testOddsFormat'
    };

    raceOutcomeDetailsServiceStub = {
      isGenericSilk: jasmine.createSpy('isGenericSilk'),
      isNumberNeeded: jasmine.createSpy('isNumberNeeded'),
      isValidSilkName: jasmine.createSpy('isValidSilkName')
    };

    toteServiceStub = {
      getToteResults: jasmine.createSpy('getToteResults').and.returnValue(of({
        events: [{}, {}],
        typeNamesArray: []
      }))
    };

    locationService = jasmine.createSpyObj(['path']);

    filterServiceStub = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };

    activatedRouteStub = { params: of({}) };

    routerStub = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      }
    };
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };

    component = new ToteTabsResultsComponent(
      raceOutcomeDetailsServiceStub,
      toteServiceStub,
      locationService,
      filterServiceStub,
      routerStub,
      activatedRouteStub,
      userService,
      pubSubService,
      navigationService
    );
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it(`should subscribe on 'pubSubService' if ngOnInit`, fakeAsync(() => {
    component.init = jasmine.createSpy();
    component.ngOnInit();

    expect(pubSubService.subscribe)
      .toHaveBeenCalledWith('toteResults', 'RELOAD_COMPONENTS', jasmine.any(Function));
    expect(component.init).toHaveBeenCalled();

    flush();
  }));

  it(`should run 'init' method if ngOnInit`, () => {
    component.init = jasmine.createSpy();
    component.ngOnInit();
    expect(component.init).toHaveBeenCalled();
  });

  it(`should call 'goToFilter' when switcher clicked`, () => {
    component['goToFilter'] = jasmine.createSpy('goToFilter');
    component.ngOnInit();
    component.switchers.forEach(s => s.onClick());
    expect(component['goToFilter']).toHaveBeenCalledTimes(2);
  });

  it(`should unsubscribe from 'pubSubService' if destroy component`, fakeAsync(() => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('toteResults');

    flush();
  }));

  it(`'areEventsAvailable' method should return false if racing is empty`, () => {
    expect(component.areEventsAvailable()).toBeFalsy();
  });

  it(`'areEventsAvailable' method should return false if racing.events is empty`, () => {
    component.racing = { events: [] };
    expect(component.areEventsAvailable()).toBeFalsy();
  });

  it(`'areEventsAvailable' method should return true if racing has events`, () => {
    component.racing = { events: [{}] };
    expect(component.areEventsAvailable()).toBeTruthy();
  });

  describe('goToFilter', () => {
    it('should delegate navigation (without scroll) to service', () => {
      component.goToFilter('some');

      expect(navigationService.openUrl).toHaveBeenCalledWith(`/tote/results/some`, true, true);
    });

    it('should not proceed with navigation if location if same', () => {
      locationService.path.and.returnValue('/tote/results/some');
      component.goToFilter('some');

      expect(navigationService.openUrl).not.toHaveBeenCalled();
    });
  });

  describe('init', () => {
    it('should navigate to results tab', fakeAsync(() => {
      activatedRouteStub.params = of({ filter: '' });
      component.init();
      flush();
      expect(routerStub.navigateByUrl).toHaveBeenCalled();
    }));

    it('should load tote results', fakeAsync(() => {
      activatedRouteStub.params = of({ filter: 'by-meetings' });
      component.init();
      flush();
      expect(toteServiceStub.getToteResults).toHaveBeenCalled();
    }));

    it('should show error', fakeAsync(() => {
      activatedRouteStub.params = throwError(null);
      component.showError = jasmine.createSpy('showError');
      component.init();
      flush();
      expect(component.showError).toHaveBeenCalled();
    }));
  });

  it('reloadResults', () => {
    component['showSpinner'] = jasmine.createSpy('showSpinner');
    component['init'] = jasmine.createSpy('init');
    component.reloadResults();
    expect(component['showSpinner']).toHaveBeenCalled();
    expect(component['init']).toHaveBeenCalled();
  });

  it('sortEventsByTimeAscending', () => {
    const events = [{ startTime: 2 }, { startTime: 1 }];
    component.sortEventsByTimeAscending(events);
    expect(events).toEqual([{ startTime: 1 }, { startTime: 2 }]);
  });

  it('getSortedPrizePlaces', () => {
    const outcomes = [
      { results: { outcomePosition: 2 } },
      { results: {} },
      { results: { outcomePosition: 1 } }
    ];
    expect( component.getSortedPrizePlaces(outcomes) ).toEqual([
      { results: { outcomePosition: 1 } },
      { results: { outcomePosition: 2 } }
    ]);
  });

  it('byTimeContainerHeader', () => {
    const event: any = { localTime: '[time]', typeName: '[type]', country: '[country]' };
    expect(component.byTimeContainerHeader(event)).toBe('[time] [type] [country]');
  });

  it('getJockeyAndTrainer', () => {
    const outcome: any = {
      racingFormOutcome: { jockey: '[jockey]', trainer: '[trainer]' }
    };
    expect(component.getJockeyAndTrainer(outcome)).toBe('[jockey] / [trainer]');
  });

  it('imgSrc', () => {
    component.images = '/images';
    expect(component.imgSrc('silk1.png')).toBe('/images/silk1.png');
  });

  it('removeLineSymbol', () => {
    component.removeLineSymbol('tst');
    expect(filterServiceStub.removeLineSymbol).toHaveBeenCalledWith('tst');
  });

  it('isLatestResults', () => {
    expect(component.isLatestResults('by-latest-results')).toBeTruthy();
    expect(component.isLatestResults('by-meetings')).toBeFalsy();
  });

  it('isByMeetings', () => {
    expect(component.isByMeetings('by-meetings')).toBeTruthy();
    expect(component.isByMeetings('by-latest-results')).toBeFalsy();
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(1)).toBe(1);
  });

  it('isGenericSilk', () => {
    component.isGenericSilk({} as any, {} as any);
    expect(raceOutcomeDetailsServiceStub.isGenericSilk).toHaveBeenCalled();
  });

  it('isNumberNeeded', () => {
    component.isNumberNeeded({} as any, {} as any);
    expect(raceOutcomeDetailsServiceStub.isNumberNeeded).toHaveBeenCalled();
  });

  it('isValidSilkName', () => {
    component.isValidSilkName({} as any);
    expect(raceOutcomeDetailsServiceStub.isValidSilkName).toHaveBeenCalled();
  });
});
