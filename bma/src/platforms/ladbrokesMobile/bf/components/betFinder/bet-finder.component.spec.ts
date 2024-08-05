import { Subject } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { LadbrokesMobileBetFinderComponent } from '@ladbrokesMobile/bf/components/betFinder/bet-finder.component';

describe('LadbrokesMobileBetFinderComponent', () => {
  let component;
  let storageService;
  let domToolsService;
  let windowRefService;
  let localeService;
  let gtm;
  let router;
  let betFinderHelperService;
  let pubsub;
  let getRacesListSubj;
  let rendererService;

  beforeEach(() => {
    getRacesListSubj = new Subject();
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      getOuterHeight: jasmine.createSpy('getOuterHeight'),
      getHeight: jasmine.createSpy('getHeight'),
      getScrollTop: jasmine.createSpy('getScrollTop')
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({})
      },
      nativeWindow: {}
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('TstsString')
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    betFinderHelperService = {
      getRacesList: jasmine.createSpy('betFinderHelperService').and.returnValue(getRacesListSubj),
      filterRunners: jasmine.createSpy('filterRunners').and.returnValue([]),
      setFilters: jasmine.createSpy('setFilters')
    };
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    rendererService = {
      renderer: {
        listen: jasmine.createSpy('listen').and.returnValue(() => {
        })
      }
    };

    component = new LadbrokesMobileBetFinderComponent(
      storageService,
      domToolsService,
      windowRefService,
      localeService,
      gtm,
      router,
      betFinderHelperService,
      pubsub,
      rendererService
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('@hideDropdown: should not hide when it is click to open dropdown', () => {
    component.isActiveDropDown = true;
    const event = {
      target: { className: 'meetings-title' }
    };
    component['hideDropdown'](event);

    expect(component.isActiveDropDown).toEqual(true);
  });

  it('@hideDropdown: should not do anything if it is not open', () => {
    windowRefService.document.querySelector = jasmine.createSpy().and.returnValue(undefined);
    component.isActiveDropDown = false;
    const event = {
      target: { className: 'title' }
    };
    component['hideDropdown'](event);

    expect(component.isActiveDropDown).toEqual(false);
  });

  it('@hideDropdown: should hide if it is click outside dropdown', () => {
    component.isActiveDropDown = true;
    const event = {
      target: { className: 'other className' }
    };
    component['hideDropdown'](event);

    expect(component.isActiveDropDown).toEqual(false);
  });
});
