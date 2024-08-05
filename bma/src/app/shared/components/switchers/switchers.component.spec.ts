import { fakeAsync } from '@angular/core/testing';

import { SwitchersComponent } from '@shared/components/switchers/switchers.component';
import { of } from 'rxjs';
import { GA_TRACKING } from '../../constants/channel.constant';

describe('SwitchersComponent', () => {
  let component: SwitchersComponent;

  let locale;
  let router;
  let gtmTrackingService;
  let navigationService;
  let switchers;
  let tab, tabsArray;
  let mouseEvent;
  let gtmService,filtersService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('getString').and.returnValue('label.')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    gtmTrackingService = {
      setLocation: jasmine.createSpy(),
      clearLocation: jasmine.createSpy(),
    };
    navigationService = {
      openUrl: jasmine.createSpy('openUrl')
    };
    tabsArray = [{
      disabled: false, hidden: false, id: 1, label: 'Tab label', name: 'Tab name', selected: true, title: 'Tab title', url: '/some/url', viewByFilters: 1
    },
    { disabled: false, hidden: false, id: 2, label: 'Tab label', name: 'Tab name', selected: false, title: 'Tab title', url: '/some/url', viewByFilters: 2 }
    ];
    tab = tabsArray[0];
    filtersService = {
      filterLinkforRSS: jasmine.createSpy('filterLinkforRSS').and.returnValue((of('promotion/details/exclusion'))),
    };
    switchers = tabsArray;
    mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new SwitchersComponent(
      locale,
      router,
      gtmTrackingService,
      navigationService,
      gtmService,filtersService
    );

    component.switchers = switchers;
    component.activeTab = tab;
    component.detectGTMLocation = '';
    component.GATrackingModule = 'moduleribbon'; // 'moduleribbon' or 'sportsribbon'
    component.GTMTrackingObj = {
      isHomePage: true,
      event: GA_TRACKING.event,
      GATracking: {
        eventAction: GA_TRACKING.eventAction,
        eventCategory: GA_TRACKING.moduleRibbon.eventCategory,
        eventLabel: ""
      }
    }
  });

  describe('gtmTrackTabName:', () => {
    beforeEach(() => {
      component.detectGTMLocation = 'location';
      spyOn<any>(component, 'gtmTrackTabName');
    });

    it('should track location onInit', () => {
      component.ngOnInit();
      expect(component['gtmTrackTabName']).toHaveBeenCalled();
    });

    it('should track location onChanges', () => {
      const changes: any = {
      };
      component.ngOnChanges(changes as any);
      expect(component['gtmTrackTabName']).toHaveBeenCalled();
    });

    it('should not call for golf gtm', () => {
      const changes: any = {
        activeTab : {
          currentValue : {
            id:  'golf'}
        }
      };
      component.sportName = 'golf';
      component.ngOnChanges(changes as any);
      expect(component['gtmTrackTabName']).toHaveBeenCalled();
      changes.activeTab = {};
      component.ngOnChanges(changes as any);
    });

    it('should call for golf gtm', () => {
      const changes: any = {
        activeTab : {
          currentValue : {
            id:  'golf'},
          previousValue : {
            id:  'cricket'}
        }
      };
      component.sportName = 'golf';
      component.ngOnChanges(changes as any);
      expect(component['gtmTrackTabName']).toHaveBeenCalled();
      changes.activeTab = {};
      component.ngOnChanges(changes as any);
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

  it('should not set location after detecting active tab', () => {
    component.isOverlay = true;
    component.detectActiveTab(tab);
    expect(gtmTrackingService.setLocation).not.toHaveBeenCalled();
  });

  it('should not set location after detecting active tab', () => {
    component.isOverlay = true;
    component.detectActiveTab(tabsArray[1]);
    expect(gtmTrackingService.setLocation).not.toHaveBeenCalled();
  });

  it('should set location after detecting active tab', () => {
    component.detectGTMLocation = 'location';
    spyOn(component, 'getTabName').and.returnValue(jasmine.any(String) as any);
    component.detectActiveTab(tab);
    expect(component.getTabName).toHaveBeenCalledWith(tab);
    expect(gtmTrackingService.setLocation).toHaveBeenCalledWith(jasmine.any(String), component.detectGTMLocation);
  });

  describe('clickFunction', () => {
    it('should invoke "onClick" handler', () => {
      const _tab: any = { title: 'tab1', onClick: jasmine.createSpy('onClick') };
      component.clickFunction(_tab, mouseEvent, 1);
      expect(_tab.onClick).toHaveBeenCalledTimes(1);
    });

    it('should stop url navigation', () => {
      component.preventReload = true;
      component.detectActiveTab = jasmine.createSpy('detectActiveTab').and.callThrough();
      component.activeTab = { id: 'tab-featured' };
      component.clickFunction({ title: 'tab1', url: '/', id: 'tab-featured' } as any, mouseEvent, 1);
      expect(component.detectActiveTab).not.toHaveBeenCalled();
    });

    it('should stop url navigation when filter is available and activetab is null', () => {
      component.preventReload = true;
      component.filter = 0;
      component.switchers = tabsArray;
      component.detectActiveTab = jasmine.createSpy('detectActiveTab').and.callThrough();
      component.activeTab = null;
      component.clickFunction({ title: 'tab1', url: '/some/url', id: 'tab-featured' } as any, mouseEvent, 1);
      expect(component.detectActiveTab).not.toHaveBeenCalled();
    });
    it('should delegate opening to navigationService', () => {
      component.clickFunction({ title: 'tab1', url: '/' } as any, mouseEvent, 1);

      expect(navigationService.openUrl).toHaveBeenCalledTimes(1);
    });

    it('should not navigate by url (prevent route change)', fakeAsync(() => {
      component.preventRouteChange = true;
      component.clickFunction({ title: 'tab1', url: '/' } as any, mouseEvent, 1);
      expect(router.navigate).not.toHaveBeenCalledTimes(1);
    }));

    it('should emit switch action', () => {
      component.switchAction.observers = [{}] as any;
      component.switchAction.emit = jasmine.createSpy('emit');
      component.clickFunction({ title: 'tab1' } as any, mouseEvent, 1);
      expect(component.switchAction.emit).toHaveBeenCalledTimes(1);
    });

    it('should trigger gtmTracker method', () => {
      component.gtmTracker = jasmine.createSpy('gtmTracker');
      component.clickFunction({ title: 'tab1' } as any, mouseEvent, 1);
      expect(component.gtmTracker).toHaveBeenCalled();
    })
    it('should not trigger gtmTracker method', () => {
      component.gtmTracker = jasmine.createSpy('gtmTracker');
      component.GATrackingModule = 'carousel';
      component.clickFunction({ title: 'tab1' } as any, mouseEvent, 1);
      expect(component.gtmTracker).not.toHaveBeenCalled();
    })
  });

  it('should call gtmTracker with switcher data', () => {
    component.gtmTracker({ title: '', url: '/moduleribbon', position: 1 });
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('should trackByLabel', () => {
    const result = component.trackByLabel(1, {
      label: 'testLabel'
    } as any);

    expect(result).toEqual('testLabel');
  });

  describe('@getTabName', () => {
    let result;

    it('should return tab.title', () => {
      result = component.getTabName(tab);

      expect(locale.getString).not.toHaveBeenCalled();
      expect(result).toEqual(tab.title);
    });

    it('should return tab.label', () => {
      tab.title = '';
      result = component.getTabName(tab);

      expect(locale.getString).not.toHaveBeenCalled();
      expect(result).toEqual(tab.label);
    });

    it('should return tab.name', () => {
      tab.title = '';
      tab.label = '';
      result = component.getTabName(tab);

      expect(locale.getString).not.toHaveBeenCalled();
      expect(result).toEqual(tab.name);
    });

    it('should return tab.label and call locale.getString', () => {
      tab.title = '';
      tab.label = 'label.';
      result = component.getTabName(tab);

      expect(locale.getString).toHaveBeenCalledWith(tab.label);
      expect(result).toEqual(tab.label);
    });
  });

  describe('@isActive', () => {
    let result;

    it('should return true', () => {
      component.filter = null;
      result = component.isActive(tab);

      expect(result).toEqual(true);
    });

    it('should return false', () => {
      component.activeTab = { id: 2 } as any;
      component.filter = null;
      result = component.isActive(tab);

      expect(result).toEqual(false);
    });

    it('should return true', () => {
      component.filter = 1;
      result = component.isActive(tab);

      expect(result).toEqual(true);
    });

    it('should return false', () => {
      component.filter = 0;
      result = component.isActive(tab, 1);

      expect(result).toEqual(false);
    });
  });

  describe('@isAutoSizable', () => {
    it('should return false', () => {
      const result = component.isAutoSizable();

      expect(result).toEqual(false);
    });
  });

  describe('@gtmTrackTabName', () => {
    beforeEach(() => {
      component.detectActiveTab = jasmine.createSpy('detectActiveTab').and.callThrough();
      component.isActive = jasmine.createSpy('isActive').and.returnValue(tab);
      component.detectGTMLocation = 'detectGTMLocation';
    });

    it('should not call detectActiveTab', () => {
      component.detectGTMLocation = '';
      component['gtmTrackTabName']();
      expect(component.detectActiveTab).not.toHaveBeenCalled();
      expect(component.isActive).not.toHaveBeenCalled();
    });

    it('should call detectActiveTab with tab', () => {
      component.type = 'links';
      component['gtmTrackTabName']();

      expect(component.detectActiveTab).toHaveBeenCalledWith(tab);
      expect(component.isActive).not.toHaveBeenCalled();
    });

    it('should call detectActiveTab with null', () => {
      component.filter = 2;
      component.type = 'links';
      component['gtmTrackTabName']();

      expect(component.detectActiveTab).toHaveBeenCalledWith(null);
      expect(component.isActive).not.toHaveBeenCalled();
    });

    it('should call detectActiveTab and isActive', () => {
      component.type = '';
      component['gtmTrackTabName']();

      expect(component.isActive).toHaveBeenCalledWith(tab, 0);
      expect(component.detectActiveTab).toHaveBeenCalledWith(tab);
    });
    it('should call filterLinks', () => {
      component.switchers = [{
        disabled: false, hidden: false, id: 1, label: 'Tab label', name: 'Tab name', selected: true, title: 'Tab title', url: '/some/racingsuperseries', viewByFilters: 1
      }];
      (filtersService['filterLinkforRSS']as any).and.returnValue(of('promotion/details/exclusion'));
      component['filterLinks']();
      expect(component.switchers[0].url).toBe('promotion/details/exclusion')
    });
  });
});
