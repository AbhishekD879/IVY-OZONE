import { InplayMarketSelectorComponent } from '@shared/components/marketSelector/inplayMarketSelector/inplay-market-selector.component';
import { of } from 'rxjs';

describe('InplayMarketSelectorComponent', () => {
  let component: InplayMarketSelectorComponent;
  let marketSelectorConfigService;
  let marketSelectorTrackingService;
  let marketSelectorStorageService;
  let sportsConfigService;
  let activatedRoute;

  beforeEach(() => {
    marketSelectorConfigService = {
      selectorType: [{
        SPORT_ID: 234,
        MARKETS_NAMES: {
          1: '1',
          2: '2',
          3: '3',
          4: '4'
        }
      }]
    };
    marketSelectorTrackingService = {
      pushToGTM: jasmine.createSpy('pushToGTM')
    };
    marketSelectorStorageService = {
      restoreSelectedOption: jasmine.createSpy('restoreSelectedOption').and.returnValue('Match Result'),
      storeSelectedOption: jasmine.createSpy('storeSelectedOption')
    };
    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(of({
        sportConfig: {
          config: {
            request: {
              categoryId: '16'
            }
          }
        }
      }))
    };
    activatedRoute = {
      snapshot: {
          paramMap: {
              get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
          },
          params: of({
            sport: 'golf',
            id: '18',
            display: 'upcoming'
        })
      },
      params: of({
          sport: 'golf',
          id: '18',
          display: 'upcoming'
      })
  };

    component = new InplayMarketSelectorComponent(
      marketSelectorConfigService,
      marketSelectorTrackingService,
      marketSelectorStorageService,
      sportsConfigService,
      activatedRoute
    );
    component.selectorType = 'selectorType';
    component.marketSelectorOptions = ['1', '2', '3', '4'];
    component.resetDropdown = false;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnChanges', () => {
    it('check of market filter and marketFilterText', () => {
      component.SELECTOR_DATA = marketSelectorConfigService.selectorType[0];
      component.selectorType = 'selectorType';
      component.sportId = 234;
      component.selectedMarketName.emit = jasmine.createSpy();
      component.selectOptions = [{ name: '1', text: '1' }, { name: '2', text: '2' }, { name: '3', text: '3' }, { name: '4', text: '4' }];
      const changes = {
        marketSelectorOptions: {
          currentValue: {},
          previousValue: {},
          firstChange: true
        },
        eventDataSection: {
          currentValue: { marketSelector: '2' },
          previousValue: { marketSelector: '1' },
          firstChange: true
        }
      };
      component.ngOnChanges(changes as any);

      expect(component.marketFilter).toEqual('2');
      expect(component.marketFilterText).toEqual('2');
      expect(component.selectedMarketName.emit).toHaveBeenCalledWith('2');
    });
  });

  it('ngOnInit with options', () => {
    component.marketSelectorOptions = ['Match Result', 'Match Betting'];
    component.selectedMarketName.emit = jasmine.createSpy();
    component.sportId = 234;
    marketSelectorStorageService.restoreSelectedOption = jasmine.createSpy().and.returnValue('Match Result');
    component.eventDataSection = {
      categoryId: '16',
      categoryName: 'Football',
      categoryCode: 'FOOTBALL',
      className: 'Football England',
      typeName: 'League One',
      typeId: '440',
      classDisplayOrder: -32767,
      typeDisplayOrder: -32765,
      typeSectionTitleAllSports: 'England - League One',
      typeSectionTitleOneSport: 'England - League One',
      typeSectionTitleConnectApp: 'League One',
      eventCount: 2,
      eventsIds: [
        10593500,
        10593523
      ],
      events : [],
      marketSelector: 'Main Market',
    };
    component.ngOnInit();
    expect(component.selectedMarketName.emit).toHaveBeenCalledWith(component.marketFilter);
    expect(component.marketFilter).toEqual('Match Result');
    expect(component.marketFilterText).toEqual('');
  });
  it('ngOnInit with options with no market available', () => {
    component.marketSelectorOptions = ['Match Betting', 'Match Result'];
    component.selectedMarketName.emit = jasmine.createSpy();
    component.sportId = 234;
    marketSelectorStorageService.restoreSelectedOption = jasmine.createSpy().and.returnValue('Total Points');
    component.eventDataSection = {
      categoryId: '16',
      categoryName: 'Football',
      categoryCode: 'FOOTBALL',
      className: 'Football England',
      typeName: 'League One',
      typeId: '440',
      classDisplayOrder: -32767,
      typeDisplayOrder: -32765,
      typeSectionTitleAllSports: 'England - League One',
      typeSectionTitleOneSport: 'England - League One',
      typeSectionTitleConnectApp: 'League One',
      eventCount: 2,
      eventsIds: [
        10593500,
        10593523
      ],
      events : [],
      marketSelector: 'Main Market',
    };
    component.ngOnInit();
    expect(component.selectedMarketName.emit).toHaveBeenCalledWith(component.marketFilter);
    expect(component.marketFilter).toEqual('Match Betting');
    expect(component.marketFilterText).toEqual('');
  });

  it('should reset the dropdown', ()=> {
    component.selectedMarketName.emit = jasmine.createSpy();
    component.sportId = 234;
    component.eventDataSection = {
      categoryId: '16',
      categoryName: 'Football',
      categoryCode: 'FOOTBALL',
      className: 'Football England',
      typeName: 'League One',
      typeId: '440',
      classDisplayOrder: -32767,
      typeDisplayOrder: -32765,
      typeSectionTitleAllSports: 'England - League One',
      typeSectionTitleOneSport: 'England - League One',
      typeSectionTitleConnectApp: 'League One',
      eventCount: 2,
      eventsIds: [
        10593500,
        10593523
      ],
      events : [],
      marketSelector: 'Main Market',
    };
    component.resetDropdown = true;
    component.selectedMarketName.emit = jasmine.createSpy();
    component.ngOnInit();
    expect(component.resetDropdown).toBeTruthy();
  });

  it('should not reset the dropdown', ()=> {
    component.selectedMarketName.emit = jasmine.createSpy();
    component.sportId = 234;
    component.eventDataSection = {
      categoryId: '16',
      categoryName: 'Football',
      categoryCode: 'FOOTBALL',
      className: 'Football England',
      typeName: 'League One',
      typeId: '440',
      classDisplayOrder: -32767,
      typeDisplayOrder: -32765,
      typeSectionTitleAllSports: 'England - League One',
      typeSectionTitleOneSport: 'England - League One',
      typeSectionTitleConnectApp: 'League One',
      eventCount: 2,
      eventsIds: [
        10593500,
        10593523
      ],
      events : [],
      marketSelector: 'Main Market',
    };
    component.resetDropdown = false;
    component.selectedMarketName.emit = jasmine.createSpy();
    component.ngOnInit();
    expect(component.resetDropdown).toBeFalsy();
  });

  it('ngOnInit without options', () => {
    component.marketSelectorOptions = [];
    component.ngOnInit();

    expect(component.marketFilter).toBeUndefined();
    expect(component.marketFilterText).toEqual('');
  });

  it('selector data should be null', () => {
    component.selectorType = 'footballTest';
    component['createOptionsList'] = jasmine.createSpy('createOptionsList');
    component.ngOnInit();
    expect(component.SELECTOR_DATA).toBe(null);
  });
  describe('filterMarkets', () => {
    it('should emit market name', () => {
      component.SELECTOR_DATA = marketSelectorConfigService.selectorType[0];
      component.selectedMarketName.emit = jasmine.createSpy();
      component.filterMarkets('someMarket');
      expect(component.selectedMarketName.emit).toHaveBeenCalledWith('someMarket');
    });
    it('emit market name from non ngOnInit and update GTM', () => {
      component.SELECTOR_DATA = marketSelectorConfigService.selectorType[0];
      component.sportId = 234;
      component.selectedMarketName.emit = jasmine.createSpy();
      component.filterMarkets('1');
      expect(component.selectedMarketName.emit).toHaveBeenCalledWith('1');
      expect(component['marketSelectorTrackingService'].pushToGTM).toHaveBeenCalledWith('1', component.sportId);
    });
    it('emit market name from ngOnInit and should not update GTM', () => {
      component.SELECTOR_DATA = marketSelectorConfigService.selectorType[0];
      component.sportId = 234;
      component.selectedMarketName.emit = jasmine.createSpy();
      component.filterMarkets('1', true);
      expect(component.selectedMarketName.emit).toHaveBeenCalledWith('1');
      expect(component['marketSelectorTrackingService'].pushToGTM).not.toHaveBeenCalledWith('1', component.sportId);
    });
  });

  describe('initSelectorOptions', () => {
    it('should emit market name', () => {
      component.SELECTOR_DATA = marketSelectorConfigService.selectorType[0];
      component.selectorType = 'selectorType';
      component.sportId = 234;
      component.selectedMarketName.emit = jasmine.createSpy();
      component.marketFilter = 'someMarketFilter';
      component.marketSelectorOptions = ['someDifferentMarketFilter'];
      component['initSelectorOptions']();
      expect(component.selectedMarketName.emit).toHaveBeenCalledWith('someDifferentMarketFilter');
    });
  });
  it('should call isMarketAvailable', () => {
    component.marketFilter = 'Match Betting';
    component.marketSelectorOptions = ['Match Betting'];
    expect(component.isMarketAvailable(component.marketFilter)).toBeTrue();
  });
});
