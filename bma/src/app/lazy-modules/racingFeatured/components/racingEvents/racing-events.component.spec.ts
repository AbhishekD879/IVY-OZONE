
import { RacingEventsComponent } from './racing-events.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { BehaviorSubject } from 'rxjs';

describe('RacingEventsComponent', () => {
  let component;
  let locale;
  let storage;
  let racingService;
  let windowRef, gtm, deviceService, vEPService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('France translated')
    };
    storage = {
      get: jasmine.createSpy('get').and.returnValue(true),
      set: jasmine.createSpy('set'),
    };
    racingService = {
      filterRacingGroup: jasmine.createSpy('filterRacingGroup')
    };
    windowRef = {
      nativeWindow: {
        scrollTo: jasmine.createSpy('scrollTo')      
      }
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
      lastBannerEnabled: {subscribe : (cb) => cb()},
      accorditionNumber: {subscribe : (cb) => cb()},
      lastRacingModuleIndex: 0
    };
    deviceService = {isDesktop: true};
    component = new RacingEventsComponent(locale, storage, racingService, windowRef, gtm, deviceService, vEPService);
  });

  it('ngOnChanges set editable title', () => {
    storage.get.and.returnValue(true);
    component.racing = {
      groupedRacing: [{
        flag: 'UK',
        data: []
      }]
    };

    component.quickNavigationTitles = {'UK': 'UK / Ireland'};
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}});

    expect(component.accordionsState['UK']).toBeTruthy();
    expect(component.titleMap['UK']).toBe('UK / Ireland');

    component.quickNavigationTitles = null;
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}});

  });

  it('ngOnChanges set predefined title', () => {
    component.sectionTitle = {'FR' : 'France'};
    component.moduleTitle = 'UK / Ireland';
    component.racing = {
      groupedRacing: [{
        flag: 'FR',
        data: []
      }]
    };
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}});

    expect(component.titleMap['FR']).toBe('France translated');
    component.ngOnChanges({});
    expect(component.titleMap['FR']).toBe('France translated');
  });

  it(`ngOnChanges show switcher false and storage get true`, () => {
    storage.get = jasmine.createSpy('get').and.returnValue(true),
    component.showSwitcher = false;
    component.racing = {
      groupedRacing: [{
        flag: 'UK',
        data: []
      }]}
    component.quickNavigationTitles = {
      'UK': 'UK / Ireland'
    }
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}, racing: component.racing});

    expect(component.titleMap['UK']).toEqual('UK / Ireland');
    expect(component.overlayAccordionHandler)
    
  })

  it(`ngOnChanges show switcher false and storage get undefined`, () => {
    storage.get = jasmine.createSpy('get').and.returnValue(undefined),
    component.showSwitcher = false;
    component.racing = {
      groupedRacing: [{
        flag: 'UK',
        data: []
      }]}
    component.quickNavigationTitles = {
      'UK': 'UK / Ireland'
    }
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}, racing: component.racing});

    expect(component.titleMap['UK']).toEqual('UK / Ireland');
    expect(component.overlayAccordionHandler)
    
  })

  it(`ngOnChanges show switcher false and isEventOverlay`, () => {
    storage.get = jasmine.createSpy('get').and.returnValue(undefined),
    component.showSwitcher = false;
    component.racing = {
      groupedRacing: [{
        flag: 'UK',
        data: []
      }]}
    component.quickNavigationTitles = {
      'UK': 'UK / Ireland'
    }
    component.isEventOverlay = true;
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}, racing: component.racing});

    expect(component.titleMap['UK']).toEqual('UK / Ireland');
    expect(component.overlayAccordionHandler)
    
  })
 
  it(`ngOnChanges show switcher true and storage get undefined`, () => {
    storage.get = jasmine.createSpy('get').and.returnValue(undefined),
    component.showSwitcher = true;
    component.racing = {
      groupedRacing: [{
        flag: 'UK',
        data: []
      }]}
    component.quickNavigationTitles = {
      'UK': 'UK / Ireland'
    }
    component.sportName = 'greyhound';
    component.filter = false;
    component.isEventOverlay = true;
    component.ngOnChanges({moduleTitle: {currentValue: 'UK / Ireland'}, racing: component.racing});

    expect(component.titleMap['UK']).toEqual('UK / Ireland');
    expect(component.overlayAccordionHandler)
    
  })


  it('trackModule', () => {
    component.sectionTitle = {'UK': 'sb.UKIRRaces'};
    component.accordionsState['UK'] = true;
    component.gaTracking.emit = jasmine.createSpy('gaTrakcing.emit');
    component.trackModule('UK', 'horseracing');

    expect(storage.set).toHaveBeenCalledWith('UK', false);
    expect(component.gaTracking.emit).toHaveBeenCalledWith(['sb.UKIRRaces', 'horseracing']);
  });

  it('trackModule', () => {
    component.sectionTitle = {'UK': 'sb.UKIRRaces'};
    component.showSwitcher = false
    component.accordionsState['UK'] = true;
    component.sportName = 'horseracing';
    component.gaTracking.emit = jasmine.createSpy('gaTrakcing.emit');
    component.trackModule('UK', 'horseracing');

    expect(storage.set).toHaveBeenCalledWith('overlay-horseracing-UK', false);
    expect(component.gaTracking.emit).toHaveBeenCalledWith(['sb.UKIRRaces', 'horseracing']);
  });

  it('trackModule with eventOverlay', () => {
    component.sectionTitle = {'UK': 'sb.UKIRRaces'};
    component.showSwitcher = false
    component.accordionsState = {'UK': true,'FR': false};
    component.isEventOverlay = true;
    component.sportName = 'horseracing';
    component.gaTracking.emit = jasmine.createSpy('gaTrakcing.emit');
    component.trackModule('UK', 'horseracing');

    expect(storage.set).toHaveBeenCalledWith('overlay-horseracing-UK', false);
    expect(component.gaTracking.emit).toHaveBeenCalledWith(['horse racing', { UK: false, FR: false }, 'UK', {}]);
  });

  it('trackModule with eventOverlay greyhound', () => {
    component.sectionTitle = {'UK': 'sb.UKIRRaces'};
    component.showSwitcher = false
    component.accordionsState = {'UK': true,'FR': false};
    component.isEventOverlay = true;
    component.sportName = 'greyhound';
    component.gaTracking.emit = jasmine.createSpy('gaTrakcing.emit');
    component.trackModule('UK', 'greyhound');

    expect(storage.set).toHaveBeenCalledWith('overlay-greyhound-UK', false);
    expect(component.gaTracking.emit).toHaveBeenCalledWith(['greyhounds', { UK: false, FR: false }, 'UK', {}]);
  });

  describe('#ngOnChanges', () => {
    const racingChange = {
      racing: {}
    } as any;
    it('should not call filter racing, if racing is null', () => {
      component.racing = null;
      component.ngOnChanges(racingChange);
      expect(racingService.filterRacingGroup).not.toHaveBeenCalled();
    });
    it('should call filter racing, if groupedracing is null', () => {
      component.racing = {
        groupedRacing: [{
          data: []
        }]
      } as any;
      component.ngOnChanges(racingChange);
      expect(racingService.filterRacingGroup).toHaveBeenCalled();
    });
  });

  it('should check when banner above the accorition enabled',()=>
  {
    component.bannerBeforeAccorditionHeader='virtual';
    expect(component.isDisplayBanner('virtual')).toBeTruthy();
    expect(component.isDisplayBanner('nextRaces')).toBeFalsy();
    expect(component.isDisplayBanner(null)).toBeFalsy();
    component.bannerBeforeAccorditionHeader=undefined;
    expect(component.isDisplayBanner('virtual')).toBeFalsy();
    
  })

  describe('ngOnInit', () => {
    it('ngOnInit', fakeAsync(() => {
      component.ngOnInit();
      tick()
      expect(component.bannerBeforeAccorditionHeader).toBe('bannerBeforeAccorditionHeader')
    }))

    it('ngOnInit', fakeAsync(() => {
      vEPService.lastRacingModuleIndex = 1;
      component.racingIndex = 1
      component.ngOnInit();
      tick()
      expect(component.bannerBeforeAccorditionHeader).toBe('bannerBeforeAccorditionHeader')
    }))

    it('isDisplayBanner name undefined', () => {
      component.bannerBeforeAccorditionHeader = null
      const retVal = component.isDisplayBanner(null);
      expect(retVal).toBeTruthy();
    })
  });

  it('lastBanner', () => {
    component.racingIndex = 1;
    vEPService.lastRacingModuleIndex = 2;
    component.lastBanner();
    expect(component.lastBannerEnabled).toBe(false)
  });

});