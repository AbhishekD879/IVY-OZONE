import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';
import { flush, fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BetFinderComponent', () => {
  let component: BetFinderComponent;
  let storageService;
  let domToolsService;
  let windowRefService;
  let localeService;
  let gtm;
  let router;
  let betFinderHelperService;
  let pubsub;
  const  elementRef = {
    nativeElement : {
      offsetWidth: '30'
    }
  };

  beforeEach(() => {
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
    };
    domToolsService = {
      toggleClass: jasmine.createSpy('toggleClass'),
      getOuterHeight: jasmine.createSpy('getOuterHeight'),
      getHeight: jasmine.createSpy('getHeight'),
      getScrollTop: jasmine.createSpy('getScrollTop'),
      HeaderEl: {},
      FooterEl: {}
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({})
      },
      nativeWindow: {
        setTimeout: jasmine.createSpy('nativeWindow')
      }
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
      getRacesList: jasmine.createSpy('betFinderHelperService').and.returnValue(of([])),
      filterRunners: jasmine.createSpy('filterRunners').and.returnValue([]),
      setFilters: jasmine.createSpy('setFilters')
    };
    pubsub = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake(() => {}),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    component = new BetFinderComponent(
      storageService,
      domToolsService,
      windowRefService,
      localeService,
      gtm,
      router,
      betFinderHelperService,
      pubsub
    );

    component.filters = {};
    component.selectedCourse = '';
    component.defaultMeeting = {
      courseShort: '',
      course: ''
    };
    component['bfFormContainer']  = elementRef;
  });

  describe('ngOnInit', () => {
    it('should init component', () => {
      const filters: any = { selectionSupercomputer: {} };
      storageService.get.and.returnValue(filters);
      windowRefService.nativeWindow.setTimeout.and.callFake(cb => cb());

      component.ngOnInit();

      expect(component.filters).toBe(filters);
      expect(component.defaultMeeting.courseShort).toBe('All');
      expect(localeService.getString).toHaveBeenCalledWith('bf.allMeetings');
      expect(component.headerElm).toBeDefined();
      expect(component.footerElm).toBeDefined();
    });

    it('should parseResponse', fakeAsync(() => {
      spyOn(component as any, 'parseResponse');
      pubsub.subscribe.and.callFake((a, b, cb) => cb());
      component.ngOnInit();
      flush();
      expect(component['parseResponse']).toHaveBeenCalledTimes(2);
    }));

    it('should not parseResponse', fakeAsync(() => {
      spyOn(component as any, 'parseResponse');
      betFinderHelperService.getRacesList.and.returnValue(throwError('test error'));
      pubsub.subscribe.and.callFake((a, b, cb) => cb());
      component.ngOnInit();
      flush();
      expect(component['parseResponse']).not.toHaveBeenCalled();
    }));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('betFinderComponent');
  });

  it('should trackByIndex', () => {
    expect(component.trackByIndex(1)).toEqual(1);
  });

  describe('selectStar', () => {
    it('should select star', () => {
      component.selectStar(1);
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'star rating',
        eventLabel: '1 star'
      }));
    });

    it('should select star (starSelection)', () => {
      component.filters = {starSelection : 2};
      component.selectStar(2);
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'star rating',
        eventLabel: '0 stars'
      }));
    });
  });

  describe('selectButton', () => {
    it('should select checkbox button', () => {
      component.filters['test'] = true;
      component.selectButton('test');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'form',
        eventLabel: 'deselect - tstsstring'
      }));
    });

    it('should select checkbox button (odds)', () => {
      component.selectButton('oddsBoost');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'odds',
        eventLabel: 'select - tstsstring'
      }));
    });

    it('should select checkbox button (odds)', () => {
      component.selectButton('provenGoing');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'going (ground type)',
        eventLabel: 'select - tstsstring'
      }));
    });
  });

  describe('onSelectChange', () => {
    it('should call filter method and sendGTM on select change', () => {
      component.onSelectChange();
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'meetings',
        eventLabel: 'All meetings'
      }));
    });

    it('should call filter method and sendGTM on select change (meetingShort)', () => {
      component.filters.meetingShort = 'tst';
      component.meetings = [{
        courseShort: 'tst',
        course: 'test'
      }];
      component.onSelectChange();
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'meetings',
        eventLabel: 'test'
      }));
    });
    it('onSelectChange gets meeting', () => {
      const meeting = {
        courseShort: 'tst',
        course: 'test'
      };
      component.onSelectChange(meeting);
      expect(component.isActiveDropDown).toBeFalsy();
      expect(component.filters.meetingShort).toBe(meeting.courseShort);
      expect(component.selectedCourse).toBe(meeting.course);
    });
  });

  it('should set all values to default state', () => {
    component.defaultMeeting = {
      courseShort: 'all',
      course: 'all meetings'
    };
    component.onReset();
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'bet finder',
      eventAction: 'reset',
      eventLabel: ''
    }));
    expect(component.selectedCourse).toEqual('all meetings');
  });

  it('should save selected filters into the LocalStorage', () => {
    component.onSaveSelection();
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'bet finder',
      eventAction: 'save selection',
      eventLabel: ''
    }));
  });

  it('should save selected filters into the LocalStorage and switch to results page', () => {
    component.filters = {
      meetingShort: 'All',
      starSelection: 0,
      runnerName: ''};

    component.onFindBets();
    expect(storageService.set).toHaveBeenCalledWith('betFinderFilters', jasmine.objectContaining({
      meetingShort: 'All',
      starSelection: 0,
      runnerName: ''
    }));
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'bet finder',
      eventAction: 'find bets',
      eventLabel: ''
    }));
  });

  describe('selectButton', () => {
    it('should select Radio Button (deselect)', () => {
      component.selectRadioButton('selectedItem');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'supercomputer filters',
        eventLabel: 'deselect - tstsstring'
      }));
    });

    it('should select Radio Button (swlect)', () => {
      component.computerButtons = ['test1', 'test2'];
      component.selectRadioButton('test1');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        eventCategory: 'bet finder',
        eventAction: 'supercomputer filters',
        eventLabel: 'select - tstsstring'
      }));
    });
  });

  describe('setStickyFooter', () => {
    it('should setStickyFooter onWindowScroll', () => {
      component.headerElm = {} as any;
      component.footerElm = {} as any;
      component.onWindowScroll();
      expect(domToolsService.toggleClass).toHaveBeenCalled();
    });

    it('should not setStickyFooter onWindowScroll', () => {
      component.onWindowScroll();
      expect(domToolsService.toggleClass).not.toHaveBeenCalled();
    });

    it('should call getOuterHeight on cookieElm', () => {
      component.headerElm = {} as any;
      component.footerElm = {} as any;
      component.cookieElm = {id: 'agreements'} as any;
      component['setStickyFooter']();
      expect(domToolsService.getOuterHeight).toHaveBeenCalledWith({id: 'agreements'});
    });

    it('should not call getOuterHeight on cookieElm', () => {
      component.headerElm = {} as any;
      component.footerElm = {} as any;
      component.cookieElm = undefined;
      component['setStickyFooter']();
      expect(domToolsService.getOuterHeight).not.toHaveBeenCalledWith({id: 'agreements'});
    });
  });
  describe('onClickDropDown', () => {
    it('should change isActiveDropDown to true', () => {
      component.isActiveDropDown = false;
      component.onClickDropDown();

      expect(component.isActiveDropDown).toBeTruthy();
    });
    it('should change isActiveDropDown to false', () => {
      component.isActiveDropDown = true;
      component.onClickDropDown();

      expect(component.isActiveDropDown).toBeFalsy();
    });
  });
  describe('parseResponse', () => {
    it('should set initial data to the component after the response is received (cypher)', () => {
      const response = {
        cypher: {
          meetings: [{} as any],
          runners: ''
        }
      };
      component['parseResponse'](response as any);
      expect(component.meetings).toEqual(response.cypher.meetings);
    });

    it('should set initial data to the component after the response is received (no cypher)', () => {
      const response = {};
      component['parseResponse'](response as any);
      expect(betFinderHelperService.filterRunners).toHaveBeenCalled();
    });
  });

  it('should setStickyFooterWidth onWindowScroll', fakeAsync(() => {
    component.onWindowResize();
    tick(501);
    expect(component.bfWidth).toBeDefined();
  }));
  describe('getMeeting', () => {
    it('should get meeting from meetings array', () => {
      const meetings = [
        {
          courseShort: 'courseShort',
          course: 'course'
        },
        {
          courseShort: 'courseShort2',
          course: 'course2'
        }
      ];
      component.filters.meetingShort = 'courseShort';
      const result = component['getMeeting'](meetings);
      expect(result).toEqual(meetings[0]);
    });
    it('should get meeting from defaultMeeting variable', () => {
      const meetings = [
        {
          courseShort: 'courseShort',
          course: 'course'
        }
      ];
      component.defaultMeeting = {
        courseShort: 'courseShort4',
        course: 'course4'
      };
      component.filters.meetingShort = 'courseShort3';
      const result = component['getMeeting'](meetings);
      expect(result).toEqual(component.defaultMeeting);
    });
  });

  it('sendGTM should send event with meeting course', () => {
    component.filters.starSelection = 1;
    component.filters.meetingShort = 'meeting1';
    component.meetings = [{ courseShort: 'meeting1', course: 'meeting1' }];
    component['sendGTM']('', '', true);
    expect(gtm.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      betFinderMeetings: 'meeting1'
    }));
  });

  it('resetButtonValues', () => {
    component['resetButtonValues'](['btn']);
    expect(component.filters['btn']).toBeFalsy();
  });

  it('selectedButtons', () => {
    component.filters['btn1'] = true;
    component['selectedButtons'](['btn1', 'btn2']);
    expect(localeService.getString).toHaveBeenCalledWith('bf.btn1');
    expect(localeService.getString).not.toHaveBeenCalledWith('bf.btn2');
  });

  describe('setSelectionsNumber', () => {
    it('should set no selections message', () => {
      component['setSelectionsNumber'](0);
      expect(localeService.getString).toHaveBeenCalledWith('bf.noselection');
      expect(localeService.getString).toHaveBeenCalledWith('bf.found');
    });

    it('should set selections found message', () => {
      component['setSelectionsNumber'](1);
      expect(localeService.getString).toHaveBeenCalledWith('bf.selection');
      expect(localeService.getString).toHaveBeenCalledWith('bf.found');
    });
  });
});
