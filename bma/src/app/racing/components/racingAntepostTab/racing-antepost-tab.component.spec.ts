import { RacingAntepostTabComponent } from './racing-antepost-tab.component';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { RACING_CONFIG } from '@app/core/services/sport/config/racing.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('RacingAntepostTabComponent', () => {
  let component: RacingAntepostTabComponent;

  let filterService,
    locale,
    racingService,
    routingHelperService,
    sessionStorageService,
    pubSubService,
    gtm, deviceService;

  beforeEach(() => {
    filterService = {
      date: jasmine.createSpy()
    };
    locale = {
      getString: jasmine.createSpy().and.returnValue('RACING')
    };
    racingService = {
      ANTEPOST_SWITCHER_KEYS: RACING_CONFIG.ANTEPOST_SWITCHER_KEYS
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    sessionStorageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue('EVFLAG_FT')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish'),
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((fileName, method, callback) => {
        if (method == pubSubService.API.ACTIVE_FUTURE_TAB) {
            callback(true);
        }
      })
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    deviceService = { isDesktop: true };
    component = new RacingAntepostTabComponent(
      filterService,
      locale,
      racingService,
      routingHelperService,
      sessionStorageService,
      pubSubService,
      gtm,
      deviceService
    );
    component.eventsMap = { 'EVFLAG_FT' : {
      "events": [
          {
            "displayOrder": 0,
            "categoryDisplayOrder": "-11010",
            "typeDisplayOrder": -30890,
            "cashoutAvail": "N",
          }
      ],
      "typeNames": [
          {
              "typeName": "Doncaster",
              "typeNameEvents": [
                  {
                    "displayOrder": 0,
                    "categoryDisplayOrder": "-11010",
                    "className": "Horse Racing - Live",
                    "typeName": "Doncaster",
                    "typeDisplayOrder": -32767,
                    "cashoutAvail": "N"
                  }
              ],
              "displayOrder": -32767,
              "cashoutAvail": "N"
          }]
        }
    } as any;
        
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.switchers = [
        {
          name: 'myTab',
          viewByFilters: 'myFilter'
        },
        {
          name: 'myTab1',
          viewByFilters: 'myFilter1'
        },
        {
          name: 'myTab2',
          viewByFilters: 'EVFLAG_FT'
        }
      ] as any;
      component.racing = { events: [] };
    });
    it('should set filter if configured in CMS', () => {
      component.defaultAntepostTab = 'myTab1';
      component.racing = {
        events: [{ id: 1, name: 'testName', drilldownTagNames: 'TEST_TAG' }]
      } as any;
      component.ngOnInit();
      expect(component.filter).toBe('myFilter1');
    });

    it('should set filter with overlay', () => {
      component.defaultAntepostTab = 'myTab1';
      component.isFromOverlay = true;
      component.racing = {
        events: [{ id: 1, name: 'testName', drilldownTagNames: 'TEST_TAG' }]
      } as any;
      component.ngOnInit();
      expect(component.filter).toBe('EVFLAG_FT');
    });
    it('should set first filter if not configured in CMS', () => {
      component.defaultAntepostTab = null;
      component.racing = {
        events: [{ id: 1, name: 'testName', drilldownTagNames: 'TEST_TAG' }]
      } as any;
      component.ngOnInit();
      expect(component.filter).toBe('myFilter');
    });
    it('should not set filter if there are no events', () => {
      spyOn(component, 'getAntepostEventsFlags').and.callThrough();
      spyOn<any>(component, 'setDefaultTab').and.callThrough();

      component.ngOnInit();

      expect(component.getAntepostEventsFlags).not.toHaveBeenCalled();
      expect(component['setDefaultTab']).not.toHaveBeenCalled();
    });
  });
  it('getDate', () => {
    component['getDate'](<any>{ startTime: '1232323525' });
    expect(filterService.date).toHaveBeenCalledWith('1232323525', 'dd-MM-yyyy | HH:mm');
  });


  it('trackById', () => {
    const checkedValue = {id: 5};
    expect(component.trackById(0, checkedValue)).toEqual(5);

    const otherCheckedValue = {typeNameEvents: [{id: 6}]};
    expect(component.trackById(0, otherCheckedValue)).toEqual(6);

  });

  it('formEdpUrl', () => {
    const sportEvent: ISportEvent = {id: 123} as ISportEvent;
    component['formEdpUrl'](sportEvent);

    expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
  });

  it('selectEventList', () => {
    component.isExpanded = [true];
    component.selectEventList('test');

    expect(component.filter).toEqual('test');
    expect(component.isExpanded).toEqual([true]);
  });

  it('selectEventList is overlay gtm data track', () => {
    component.switchers = [
      {
        name: 'Flat races',
        viewByFilters: 'EVFLAG_FT'
      }
    ] as any;
    component.isExpanded = [true];
    component.isFromOverlay = true;
    component.selectEventList('EVFLAG_FT',true);

    expect(component.filter).toEqual('EVFLAG_FT');
    expect(component.isExpanded).toEqual([true]);
    expect(gtm.push).toHaveBeenCalled();
  });


  it('', () => {
    const events = [
      {
        startTime: '1',
        drilldownTagNames: 'EVFLAG_FT'
      },
      {
        startTime: '2',
        drilldownTagNames: 'EVFLAG_FT'
      },
      {
        startTime: '3',
        drilldownTagNames: 'EVFLAG_FT'
      }
    ];

    component.getAntepostEventsFlags(events as ISportEvent[]);
  });

  it('accordionHandler call', () => {
    component.isExpanded = [true, false];
    component.isFromOverlay = true;
    component.accordionHandler(0, {typeName: 'test'} as any);
    expect(gtm.push).toHaveBeenCalled();
  });

  it('accordionHandler with overlay false', () => {
    component.isExpanded = [true, false];
    component.isFromOverlay = false;
    component.accordionHandler(1, {typeName: 'test'} as any);
    expect(gtm.push).not.toHaveBeenCalled();
  });
  
  it('accordionHandler with overlay', () => {
    component.isExpanded = [true, false];
    component.isFromOverlay = true;
    component.accordionHandler(1, {typeName: 'test'} as any);
    expect(gtm.push).toHaveBeenCalled();
  });
  
  it('call closeOverlay false', () => {
    component.isFromOverlay = false;
    component.closeOverlay({} as any);
    expect(gtm.push).not.toHaveBeenCalled();
  });

  it('call closeOverlay true', () => {
    component.isExpanded = [true, false];
    component.isFromOverlay = true;
    component.switchers = [
      {
        name: 'Flat races',
        viewByFilters: 'EVFLAG_FT'
      }
    ] as any;
    component.filter ='EVFLAG_FT';
    component.closeOverlay({categoryId:'19',typeId:'1212',id:'121233'} as any);
    expect(gtm.push).toHaveBeenCalled();
  });
});
