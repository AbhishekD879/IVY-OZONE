import { of as observableOf } from 'rxjs';

import { TabsPanelComponent } from '@shared/components/tabsPanel/tabs-panel.component';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

describe('TabsPanelComponent', () => {
  let component: TabsPanelComponent;
  let elementRef;
  let locale;
  let router;
  let gtmTrackingService;
  let navigationService;
  let tab;
  let changes;
  let mouseEvent;
  let casinoMyBetsIntegratedService;

  beforeEach(() => {
    elementRef = { nativeElement: {} };
    router = {
      navigate: jasmine.createSpy('navigate').and.returnValue({
        then: jasmine.createSpy()
      }),
      events: observableOf({})
    };
    locale = jasmine.createSpyObj('locale', ['getString']);
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    gtmTrackingService = jasmine.createSpyObj('gtmService', ['setLocation', 'clearLocation']);
    casinoMyBetsIntegratedService = {
      bmaInit: jasmine.createSpy('bmaInit'),
      getOpenBetTabActiveStatus: null
    };
    mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
    tab = {
      title: 'title',
      url: '/tab-url',
      disabled: false,
      hidden: false,
      id: 1,
      label: 'Tab label',
      name: 'Tab name',
      selected: true,
      marketName: 'build-your-bet'
    } as ITab;
    changes = {
      tpTabs: [tab],
      tpActiveTab: tab
    };

    component = new TabsPanelComponent(
      elementRef,
      locale,
      router,
      gtmTrackingService,
      casinoMyBetsIntegratedService,
      navigationService      
    );
  });

  describe('clickFunction', () => {
    beforeEach(() => {
      component.routerLinkDisable = true;
      spyOn(component, 'detectActiveTab');
      component.tpFunction.emit = jasmine.createSpy('emit');
    });

    it('should prevent default click', () => {
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).not.toHaveBeenCalled();
    });

    it('should detect active tab on click by tab', () => {
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).not.toHaveBeenCalled();
    });

    it('should not redirect if tab has no url or routerLinkDisable is true', () => {
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).not.toHaveBeenCalled();

      tab.url = '';
      component.routerLinkDisable = false;
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).not.toHaveBeenCalled();
    });

    it('should redirect if tab has url and routerLinkDisable is false', () => {
      component.routerLinkDisable = false;
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).toHaveBeenCalledWith(tab.url, true, true);
      expect(component.tpFunction.emit).not.toHaveBeenCalled();
    });

    it('should not emit value', () => {
      component.tpFunction.observers = [];
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).not.toHaveBeenCalled();
    });

    it('should emit value', () => {
      component.tpFuncArr = 'title';
      component.tpFunction.observers = [{}] as any;
      component.clickFunction(tab, mouseEvent);

      expect(navigationService.openUrl).not.toHaveBeenCalled();
      expect(component.tpFunction.emit).toHaveBeenCalledWith({ id: 'title', tab });
    });

    afterEach(() => {
      expect(mouseEvent.preventDefault).toHaveBeenCalled();
      expect(component.detectActiveTab).toHaveBeenCalledWith(tab);
    });
  });

  describe('gtmTrackTabName:', () => {
    beforeEach(() => {
      component.detectGTMLocation = 'location';
      spyOn(component as any, 'gtmTrackTabName').and.callThrough();
    });

    it('should track location onInit', () => {
      component.tpTabs = [tab];
      component.ngOnInit();
      expect((component as any).gtmTrackTabName).toHaveBeenCalled();
    });

    it('should do nothing if tpTabs is undefined', () => {
      component.tpTabs = undefined;
      component.ngOnInit();
      expect((component as any).gtmTrackTabName).not.toHaveBeenCalled();

    });
    it('should track location onChanges', () => {
      component.tpTabs = [tab];
      component.ngOnChanges(changes);

      expect((component as any).gtmTrackTabName).toHaveBeenCalled();
    });

    it('should not track location onChanges', () => {
      changes.tpTabs.firstChange = true;

      component.ngOnChanges(changes);

      expect(component['gtmTrackTabName']).not.toHaveBeenCalled();
    });
  });

  describe('GtmTrackingService:clearLocation', () => {
    it('should not clear location', () => {
      component.ngOnDestroy();
      expect(gtmTrackingService.clearLocation).not.toHaveBeenCalled();
    });

    it('should clear location', () => {
      component.detectGTMLocation = 'location';
      component.ngOnDestroy();
      expect(gtmTrackingService.clearLocation).toHaveBeenCalledWith(component.detectGTMLocation);
    });
  });

  describe('@is5ASideTab', () => {
    let result;

    it('should return false', () => {
      result = component.is5ASideTab(tab);

      expect(result).toEqual(false);
    });

    it('should return true', () => {
      tab.marketName = '5-a-side';
      result = component.is5ASideTab(tab);

      expect(result).toEqual(true);
    });
  });

  describe('@detectActiveTab', () => {
    it('should not set location after detecting active tab', () => {
      component.detectActiveTab(tab);

      expect(gtmTrackingService.setLocation).not.toHaveBeenCalled();
    });

    it('should set location after detecting active tab with tab.title', () => {
      component.detectGTMLocation = 'location';
      component.detectActiveTab(tab);

      expect(gtmTrackingService.setLocation).toHaveBeenCalledWith(tab.title, component.detectGTMLocation);
    });

    it('should set location after detecting active tab with tab.label', () => {
      tab.title = '';
      component.detectGTMLocation = 'location';

      component.detectActiveTab(tab);

      expect(gtmTrackingService.setLocation).toHaveBeenCalledWith(tab.label, component.detectGTMLocation);
    });

    it('should set location after detecting active tab with tab.name', () => {
      tab.title = '';
      tab.label = '';
      component.detectGTMLocation = 'location';

      component.detectActiveTab(tab);

      expect(gtmTrackingService.setLocation).toHaveBeenCalledWith(tab.name, component.detectGTMLocation);
    });
  });

  describe('@setActiveClass', () => {
    let result;

    it('should return true', () => {
      result = component.setActiveClass(tab);

      expect(result).toEqual(true);
    });

    it('should return true', () => {
      component['tpActiveTab'] = { id: 1 } as any;
      result = component.setActiveClass(tab);

      expect(result).toEqual(true);
    });

    it('should return false', () => {
      component['tpActiveTab'] = { id: 2 } as any;
      result = component.setActiveClass(tab);

      expect(result).toEqual(false);
    });
  });

  describe('@getTabsWithTitle', () => {
    let result,
      tabs;

    it('sould return []', () => {
      tabs = [];
      result = component['getTabsWithTitle'](tabs);

      expect(result).toEqual(tabs);
    });

    it('should get tabs list with translated title property', () => {
      tabs = [ tab ];
      result = component['getTabsWithTitle'](tabs);

      expect(result).toEqual(tabs);
    });

    it('should get tabs list with translated label property', () => {
      tabs = [ tab ];
      tabs[0].title = '';
      tabs[0].label = 'label.';
      result = component['getTabsWithTitle'](tabs);

      expect(result).toEqual(tabs);
      expect(locale.getString).toHaveBeenCalledWith(tabs[0].label);
    });

    it('sould return sliced array according to maxElementsToDisplay', () => {
      tabs = [tab,tab,tab,tab, tab];
      component.maxElementsToDisplay = 3;
      result = component['getTabsWithTitle'](tabs);
      expect(result.length).toEqual(component.maxElementsToDisplay);
    });
  });

  it('@gtmTrackTabName', () => {
    spyOn(component, 'detectActiveTab').and.callThrough();
    spyOn(component, 'setActiveClass').and.callThrough();
    component.tpTabs = [tab];

    component['gtmTrackTabName']();

    expect(component.setActiveClass).toHaveBeenCalledWith(tab);
    expect(component.detectActiveTab).toHaveBeenCalledWith(tab);
  });

  it('@ngOnInit should call getTabsWithTitle, set tpTabs, call setActiveTabAsTpTabs and gtmTrackTabName methods', () => {
    const testArr = [1, 2, 3] as any,
      tpActiveTabMock = { id: 1 } as any,
      tpTabsMock = [{ id: 2 }, { id: 3 }] as any;

    component['tpActiveTab'] = tpActiveTabMock;
    component['tpTabs'] = tpTabsMock;
    component['getTabsWithTitle'] = jasmine.createSpy('getTabsWithTitle').and.returnValue(testArr);
    component['setActiveTabAsTpTabs'] = jasmine.createSpy('setActiveTabAsTpTabs');
    component['gtmTrackTabName'] = jasmine.createSpy('gtmTrackTabName');

    component.ngOnInit();

    expect(component['tpTabs']).toEqual(testArr);
    expect(component['getTabsWithTitle']).toHaveBeenCalledWith(tpTabsMock);
    expect(component['setActiveTabAsTpTabs']).toHaveBeenCalledWith(tpActiveTabMock);
    expect(component['gtmTrackTabName']).toHaveBeenCalled();
  });

  it('@ngOnInit should not do anything, if tpTabs is not defined', () => {
    component.tpTabs = undefined;
    spyOn(component as any, 'getTabsWithTitle');
    spyOn(component as any, 'setActiveTabAsTpTabs');
    spyOn(component as any, 'gtmTrackTabName');
    component.ngOnInit();

    expect(component.tpTabs).toEqual(undefined);
    expect((component as any).getTabsWithTitle).not.toHaveBeenCalled();
    expect((component as any).setActiveTabAsTpTabs).not.toHaveBeenCalled();
    expect((component as any).gtmTrackTabName).not.toHaveBeenCalled();
  });

  it('@ngOnChanges should set tpTabs, call getTabsWithTitle, gtmTrackTabName', () => {
    const testArr = [1, 2, 3] as any,
      tpActiveTabMock = { id: 1 } as any,
      tpTabsMock = [{ id: 2 }, { id: 3 }] as any;

    component['tpActiveTab'] = tpActiveTabMock;
    component['tpTabs'] = tpTabsMock;
    component['gtmTrackTabName'] = jasmine.createSpy('gtmTrackTabName');
    component['setActiveTabAsTpTabs'] = jasmine.createSpy('setActiveTabAsTpTabs');
    component['getTabsWithTitle'] = jasmine.createSpy('getTabsWithTitle').and.returnValue(testArr);

    component.ngOnChanges(changes);

    expect(component['tpTabs']).toEqual(testArr);
    expect(component['getTabsWithTitle']).toHaveBeenCalledWith(tpTabsMock);
    expect(component['gtmTrackTabName']).toHaveBeenCalled();
    expect(component['setActiveTabAsTpTabs']).toHaveBeenCalledWith(tpActiveTabMock);
  });

  describe('@ngOnChanges should do nothing', () => {
    beforeEach(() => {
      component.tpTabs = undefined;
      spyOn(component as any, 'getTabsWithTitle');
      spyOn(component as any, 'setActiveTabAsTpTabs');
      spyOn(component as any, 'gtmTrackTabName');
    });

    it('when no tpTabs or tpActiveTab data in changes object', () => {
      component.ngOnChanges({ });
    });
    it('when first change of tpTabs or tpActiveTab', () => {
      component.ngOnChanges({ tpTabs: { firstChange: true }, tpActiveTab: { firstChange: true } } as any);
    });

    afterEach(() => {
      expect(component.tpTabs).not.toBeDefined();
      expect((component as any).setActiveTabAsTpTabs).not.toHaveBeenCalled();
      expect((component as any).getTabsWithTitle).not.toHaveBeenCalled();
      expect((component as any).gtmTrackTabName).not.toHaveBeenCalled();
    });
  });

  describe('@setActiveTabAsTpTabs', () => {
    it('should set tpTabs to tpActiveTab if only 1 tab is being displayed', () => {
      const tpActiveTabMock = { id: 1 } as any,
        tpTabsMock = [{ id: 2 }] as any;

      component['tpActiveTab'] = tpActiveTabMock;
      component['tpTabs'] = tpTabsMock;

      component['setActiveTabAsTpTabs'](tpActiveTabMock);

      expect(component['tpTabs']).toEqual([tpActiveTabMock]);
    });

    it('should NOT set tpTabs to tpActiveTab if more than 1 tab is being displayed', () => {
      const tpActiveTabMock = { id: 1 } as any,
        tpTabsMock = [{ id: 2 }, { id: 3 }] as any;

      component['tpActiveTab'] = tpActiveTabMock;
      component['tpTabs'] = tpTabsMock;

      component['setActiveTabAsTpTabs'](tpActiveTabMock);

      expect(component['tpTabs']).toEqual(tpTabsMock);
    });

    it('should NOT set tpTabs to tpActiveTab if tpActiveTab is undefined', () => {
      const tpActiveTabMock = undefined,
        tpTabsMock = [{ id: 2 }, { id: 3 }] as any;

      component['tpActiveTab'] = tpActiveTabMock;
      component['tpTabs'] = tpTabsMock;

      component['setActiveTabAsTpTabs'](tpActiveTabMock);

      expect(component['tpTabs']).toEqual(tpTabsMock);
    });
  });

  describe('@ngAfterViewInit', () => {
    it('isMyBetsInCasino is true, setActiveTabForCasino is true and tab title is Open Bets', () => {
      component['casinoMyBetsIntegratedService'].isMyBetsInCasino = true;
      spyOn(component['casinoMyBetsIntegratedService'], 'getOpenBetTabActiveStatus').and.returnValue(true);
      tab.selected = false;
      tab.title = 'Open Bets';
      component.tpTabs = [tab];
      component.ngAfterViewInit();
      expect(component['casinoMyBetsIntegratedService'].bmaInit).toHaveBeenCalled();
      expect(component.tpTabs[0].selected).toBe(true);
    });

    it('isMyBetsInCasino is true, setActiveTabForCasino is true and tab title is sometitle', () => {
      component['casinoMyBetsIntegratedService'].isMyBetsInCasino = true;
      spyOn(component['casinoMyBetsIntegratedService'], 'getOpenBetTabActiveStatus').and.returnValue(true);
      tab.selected = false;
      tab.title = 'sometitle';
      component.tpTabs = [tab];
      component.ngAfterViewInit();
      expect(component['casinoMyBetsIntegratedService'].bmaInit).toHaveBeenCalled();
      expect(component.tpTabs[0].selected).toBe(false);
    });

    it('isMyBetsInCasino is true, setActiveTabForCasino is FALSE and tab title is Open Bets', () => {
      component['casinoMyBetsIntegratedService'].isMyBetsInCasino = true;
      spyOn(component['casinoMyBetsIntegratedService'], 'getOpenBetTabActiveStatus').and.returnValue(false);
      tab.selected = false;
      tab.title = 'Open Bets';
      component.tpTabs = [tab];
      component.ngAfterViewInit();
      expect(component['casinoMyBetsIntegratedService'].bmaInit).toHaveBeenCalled();
      expect(component.tpTabs[0].selected).toBe(false);
    });

    it('isMyBetsInCasino is false', () => {
      component['casinoMyBetsIntegratedService'].isMyBetsInCasino = false;
      component.ngAfterViewInit();
      expect(component['casinoMyBetsIntegratedService'].bmaInit).not.toHaveBeenCalled();
    });
  });
});
