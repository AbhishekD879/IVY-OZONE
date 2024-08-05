import { HorseRaceGridComponent } from './horse-race-grid.component';

import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';

describe('HorseRaceGridComponent ', () => {
  let component: HorseRaceGridComponent,
    locale,
    lpAvailabilityService,
    racingGaService,
    routingHelperService,
    racingService,
    pubsub,
    gtmService,
    deviceService;
  const racingGroup1 = [{
    startTime: '1550751407661',
    correctedDay: 'racing.dayMonday',
    correctedDayValue: 'racing.today'
  }, {
    startTime: '1550837769000',
    correctedDay: 'racing.dayFriday',
    correctedDayValue: 'racing.tomorrow'
  }, {
    startTime: '1550837769000',
    correctedDay: 'racing.daySunday',
    correctedDayValue: 'racing.daySunday'
  }] as any;

  const racingGroup4 = [{
    startTime: '1550751407661',
    correctedDayValue: 'racing.today'
  }, {
    startTime: '1550837769000',
    correctedDayValue: 'racing.tomorrow'
  }, {
    startTime: '1550837769000',
    correctedDayValue: 'racing.daySunday'
  }] as any;

  const racingGroup3 = [{
    typeName: 'Roscommon',
    name: 'Roscommon',
    startTime: 1550751407661,
    correctedDay: 'racing.dayMonday',
    correctedDayValue: 'racing.today',
    liveStreamAvailable: true,
    cashoutAvail: 'Y',
    isFinished: 'false',
    markets: [{
      ...(<IMarket>{}),
      isGpAvailable: true
    }]
  }, {
    typeName: 'Saas',
    name: 'Saas',
    startTime: 1550837769000,
    correctedDay: 'racing.dayMonday',
    correctedDayValue: 'racing.today',
    isFinished: 'false',
    markets: [{
      ...(<IMarket>{}),
      isGpAvailable: true
    }]
  }, {
    typeName: 'Saas',
    name: 'Saas',
    startTime: 1550837769000,
    correctedDay: 'racing.dayMonday',
    correctedDayValue: 'racing.today',
    isFinished: 'false',
    markets: [{
      ...(<IMarket>{}),
      isGpAvailable: true
    }]
  }, {
    typeName: 'Mauquenchy',
    name: 'Saas',
    startTime: 1550837769000 - (10 * 60 * 1000),
    correctedDay: 'racing.dayMonday',
    correctedDayValue: 'racing.today',
    isFinished: 'false',
    markets: [{
      ...(<IMarket>{}),
      isGpAvailable: true
    }]
  }] as any;

  beforeEach(() => {
    locale = {};
    lpAvailabilityService = {};
    racingGaService = {
      trackEvent: jasmine.createSpy()
    };
    racingService = {
      getFirstActiveEventFromGroup: jasmine.createSpy().and.returnValue({ id: 2 }),
      validateRacesForToday: jasmine.createSpy('validateRacesForToday')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy().and.returnValue('test_edp_url')
    };
    pubsub = {
      publish: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    deviceService = {
      isMobile: true,
      isDesktop: false
    }
    component = new HorseRaceGridComponent(
      locale,
      lpAvailabilityService,
      racingGaService,
      routingHelperService,
      racingService,
      pubsub,
      gtmService,
      deviceService
    );
    component.racingGroupFlag = 'UK';
    component.eventsData = {
      events: [{ markets: [{ outcomes: [{ name: '' }] }] }],
      classesTypeNames: {
        UK: [{
          name: 'Event 1'
        }],
        IE: [{
          name: 'Event 1'
        }],
        VR: [{
          name: 'Event 1'
        }]
      }
    } as any;
    component.racingGroup = racingGroup1;
  });

  describe('#ngOnInit', () => {
    it('should create switchers for Virtual Racing', () => {
      component.raceType = 'horseracing';
      component.racingGroupFlag = 'VR';
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();
      expect(component.filter).toBe('racing.today');
      expect(component.isHR).toBe(true);
      expect(component.switchers).toEqual([{
        name: 'racing.today',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.today'
      }, {
        name: 'racing.tomorrow',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.tomorrow'
      }]);
    });

    it('should create switchers for Default Racing', () => {
      component.raceType = 'greyhounds';
      component.racingGroupFlag = 'UK';
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();
      expect(component.filter).toBe('racing.today');
      expect(component.isHR).toBe(false);
      expect(component.switchers).toEqual([{
        name: 'racing.today',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.today'
      }, {
        name: 'racing.tomorrow',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.tomorrow'
      }, {
        name: 'racing.daySunday',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.daySunday'
      }]);
    });

    it('should update filter with custom value', () => {
      component.filterDay = 'racing.tomorrow';
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();
      expect(component.filter).toEqual(component.filterDay);
    })
  });

  describe('#createSwitchers', () => {
    it('should create switcher', () => {
      component.racingGroup = racingGroup4;
      component['selectDay'] = jasmine.createSpy('selectDay');
      component['createSwitchers']();
      expect(component.switchers).toEqual([{
        name: 'racing.today',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.today'
      }, {
        name: 'racing.tomorrow',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.tomorrow'
      }, {
        name: 'racing.daySunday',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.daySunday'
      }]);
    });

    it('should call selectDay on onClick method', () => {
      component.racingGroup = racingGroup4;
      component['selectDay'] = jasmine.createSpy('selectDay');

      component['createSwitchers']();
      component.switchers[0].onClick();

      expect(component['selectDay']).toHaveBeenCalledWith('racing.today');
    });

    it('should create switcher', () => {
      component.racingGroup = racingGroup1;
      component['createSwitchers']();
      expect(component.switchers).toEqual([{
        name: 'racing.today',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.today'
      }, {
        name: 'racing.tomorrow',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.tomorrow'
      }, {
        name: 'racing.daySunday',
        onClick: jasmine.any(Function),
        viewByFilters: 'racing.daySunday'
      }]);
    });
  });

  it('genEventDetailsUrl', () => {
    const result = component.genEventDetailsUrl({id: 1} as ISportEvent);
    expect(routingHelperService.formEdpUrl).toHaveBeenCalled();

    expect(result).toBe('test_edp_url');
  });

  it('trackSwitchDayEvent', () => {
    locale.getString = jasmine.createSpy().and.returnValues('UK & IRE', 'Wednesday');
    component.racingGroupFlag = 'UK';
    component.sportName = 'horse racing';
    component.trackSwitchDayEvent('Wednesday');
    const gtmObject = {
      eventCategory: 'horse racing',
      eventAction: 'UK & IRE',
      eventLabel: 'Wednesday'
    };

    expect(racingGaService.trackEvent).toHaveBeenCalledWith(gtmObject);
  });

  describe('isBogPresented', () => {
    let eventEntity: ISportEvent[];
    beforeEach(() => {
      eventEntity = [
        {
          ...(<ISportEvent>{}),
          id: 1,
          markets: [],
        }, {
          ...(<ISportEvent>{}),
          id: 2,
          markets: [{
            ...(<IMarket>{}),
            isGpAvailable: true
          }],
          raceStage: '0',
          rawIsOffCode: 'N'
        }
      ];
      component['getFilteredRacesGroup'] =  jasmine.createSpy('getFilteredRacesGroup').and.returnValue(eventEntity);
    });

    it('should call isBogPresented() when isGpAvailable: true', () => {
      component['getRacesForDay'](component.eventsData);
      eventEntity[1].effectiveGpStartTime = new Date(new Date().getTime() - 86400000);
      component['isBogPresented'](eventEntity);

      expect(component['isBogPresented'](eventEntity)).toBe(true);
    });

    it('should create switchers for Horse Racing', () => {
      component.raceType = 'horseracing';
      component.racingGroupFlag = 'UK';
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();

      expect(component.filter).toBe('racing.today');
      expect(component.isHR).toBe(true);
    });

    it('should call isBogPresented() when isGpAvailable: false', () => {
      component['getRacesForDay'](component.eventsData);
      eventEntity[1].markets[0].isGpAvailable = false;
      component['isBogPresented'](eventEntity);

      expect(component['isBogPresented'](eventEntity)).toBe(false);
    });
  });

  describe('filterResultedEvents', () => {
    beforeEach(() => {
      component['sortEvents'] = jasmine.createSpy('sortEvents');
    });

    it('should invoke sortEvents method if groupedRaces array contains more than 1 elem', () => {
      const groupedRaces = [
        {
          groupName: '',
          cashoutAvailable: false,
          liveStreamAvailable: false,
          events: []
        },
        {
          groupName: '',
          cashoutAvailable: false,
          liveStreamAvailable: false,
          events: []
        }
      ];
      component.groupedRaces = groupedRaces as any;
      component['getIndexesOfResultedEvents'] = jasmine.createSpy('getIndexesOfResultedEvents').and.returnValue([0, 1]);
      component['filterResultedEvents']();
      expect(component['getIndexesOfResultedEvents']).toHaveBeenCalled();
      expect(component['sortEvents']).toHaveBeenCalled();
    });

    it('should NOT invoke sortEvents method if groupedRaces array contains more than 1 elem', () => {
      const groupedRaces = [
        {
          groupName: '',
          cashoutAvailable: false,
          liveStreamAvailable: false,
          events: []
        }
      ];
      component.groupedRaces = groupedRaces as any;
      component['getIndexesOfResultedEvents'] = jasmine.createSpy('getIndexesOfResultedEvents').and.returnValue([0, 1]);
      component['filterResultedEvents']();
      expect(component['getIndexesOfResultedEvents']).toHaveBeenCalled();
      expect(component['sortEvents']).not.toHaveBeenCalled();
    });

    it('should not invoke sortEvents method if no resulted event exists', () => {
      component['getIndexesOfResultedEvents'] = jasmine.createSpy('getIndexesOfResultedEvents').and.returnValue([]);
      component['filterResultedEvents']();
      expect(component['getIndexesOfResultedEvents']).toHaveBeenCalled();
      expect(component['sortEvents']).not.toHaveBeenCalled();
    });
  });

  describe('getIndexesOfResultedEvents', () => {
    beforeEach(() => {
      component['sortEvents'] = jasmine.createSpy('sortEvents');
      const groupedRaces = [
        {
          groupName: '',
          cashoutAvailable: false,
          liveStreamAvailable: false,
          events: []
        }
      ];
      component.groupedRaces = groupedRaces as any;
    });

    it('should return array with indexes of resulted events', () => {
      component['checkIfEventIsResulted'] = jasmine.createSpy('checkIfEventIsResulted').and.returnValue(0);
      const result = component['getIndexesOfResultedEvents']();
      expect(result).toEqual([0]);
    });

    it('should return empty array when no resulted events exist', () => {
      component['checkIfEventIsResulted'] = jasmine.createSpy('checkIfEventIsResulted').and.returnValue(null);
      const result = component['getIndexesOfResultedEvents']();
      expect(result).toEqual([]);
    });
  });

  describe('sortEvents', () => {
    it('should move 1 array elem to the end of array', () => {
      const arr = [1, 2, 3, 4] as any;

      component['sortEvents'](arr, [1]);
      expect(arr).toEqual([1, 3, 4, 2]);
    });

    it('should move few array elemes to the end of array (keeping proper order)', () => {
      const arr = [1, 2, 3, 4] as any;

      component['sortEvents'](arr, [1, 2]);
      expect(arr).toEqual([1, 4, 2, 3]);
    });
  });

  describe('checkIfEventIsResulted', () => {
    beforeEach(() => {
      component.groupedRaces = [
        {
          groupName: '',
          events: [
            {
              id: 1,
              isResulted: true
            },
            {
              id: 2,
              isResulted: true
            }
          ]
        },
        {
          groupName: '',
          events: [
            {
              id: 3,
              isResulted: false
            },
            {
              id: 4,
              isResulted: true
            }
          ]
        }
      ] as any;
    });

    it('should return index of fully resulted event', () => {
      const singleElem = component.groupedRaces[0],
        result = component['checkIfEventIsResulted'](singleElem as any);

      expect(result).toBe(0);
    });

    it('should return null if event is not fully resulted', () => {
      const singleElem = component.groupedRaces[1],
        result = component['checkIfEventIsResulted'](singleElem as any);

      expect(result).toBe(null);
    });
  });

  it('should call methods and assign argument to filter variable when selectDay method is called', () => {
    const day = 'Monday';
    component['getRacesForDay'] = jasmine.createSpy('getRacesForDay');
    component['filterResultedEvents'] = jasmine.createSpy('filterResultedEvents');
    component['trackSwitchDayEvent'] = jasmine.createSpy('trackSwitchDayEvent');
    component['scrollToStart'] = jasmine.createSpy('scrollToStart');

    component['selectDay'](day);

    expect(component.filter).toBe(day);
    expect(component['getRacesForDay']).toHaveBeenCalled();
    expect(component['filterResultedEvents']).toHaveBeenCalled();
    expect(component['trackSwitchDayEvent']).toHaveBeenCalledWith(day);
  });

  it('should trackByGroupName', () => {
    expect(component.trackByGroupName(1, {
      groupName: 'groupName',
      events: [{
        id: 0
      }]
    } as any)).toEqual('1groupName0');
  });

  describe('isLpAvailable', () => {
    it('should return true if live price is available', () => {
      lpAvailabilityService.check = jasmine.createSpy('lpAvailabilityService.check').and.returnValue(true);

      expect(component.isLpAvailable('event' as any)).toEqual(true);
    });

    it('should return false if live price is available', () => {
      lpAvailabilityService.check = jasmine.createSpy('lpAvailabilityService.check').and.returnValue(false);

      expect(component.isLpAvailable('event' as any)).toEqual(false);
    });
  });

  describe('showUKToteIndicators', () => {
    it('should return true if racingGroupFlag is equal to UK', () => {
      component.racingGroupFlag = 'UK';

      expect(component.showUKToteIndicators()).toEqual(true);
    });

    it('should return false if racingGroupFlag is NOT equal to UK', () => {
      component.racingGroupFlag = 'test';

      expect(component.showUKToteIndicators()).toEqual(false);
    });
  });

  it('trackById should return event id', () => {
    expect(component.trackById(1, { id: 2 } as any)).toEqual(2);
  });

  it('getFilteredRacesGroup should return group of filtered events', () => {
    const meeting = { name: 'test' } as any;
    component.filter = 'day';
    component.racingGroup = [
      {
        typeName: 'test',
        correctedDayValue: 'day'
      },
      {
        typeName: 'test1',
        correctedDayValue: 'day1'
      },
      {
        typeName: 'test',
        correctedDayValue: 'day'
      },
      {
        typeName: 'test1',
        correctedDayValue: 'day'
      },
      {
        typeName: 'test',
        correctedDayValue: 'day1'
      }
    ] as any;

    expect(component['getFilteredRacesGroup'](meeting)).toEqual([
      {
        typeName: 'test',
        correctedDayValue: 'day'
      },
      {
        typeName: 'test',
        correctedDayValue: 'day'
      }
    ] as any);
  });

  describe('sortRacesGroup', () => {
    it('should sort racing group by name', () => {
      component.eventsOrder = ['name'];
      const arr = [
        {
          id: 3,
          name: 'b'
        },
        {
          id: 1,
          name: 'c'
        },
        {
          id: 2,
          name: 'a'
        }
      ] as any;

      expect(component['sortRacesGroup'](arr)).toEqual([
        {
          id: 2,
          name: 'a'
        },
        {
          id: 3,
          name: 'b'
        },
        {
          id: 1,
          name: 'c'
        }
      ] as any);
    });

    it('should sort racing group by id', () => {
      component.eventsOrder = ['id'];
      const arr = [
        {
          id: 3,
          name: 'b'
        },
        {
          id: 1,
          name: 'c'
        },
        {
          id: 2,
          name: 'a'
        }
      ] as any;

      expect(component['sortRacesGroup'](arr)).toEqual([
        {
          id: 1,
          name: 'c'
        },
        {
          id: 2,
          name: 'a'
        },
        {
          id: 3,
          name: 'b'
        }
      ] as any);
    });
  });

  it('should sort based on displayOrder', () => {
    const eventsData = [
      {
        groupName: 'FR',
        typeDisplayOrder: 3
      }, {
        groupName: 'ZA',
        typeDisplayOrder: 4
      }, {
        groupName: 'UK',
        typeDisplayOrder: 4
      }, {
        groupName: 'AU',
        typeDisplayOrder: 2
      }
    ] as any;
    const response = component['sortMeetings'](eventsData);
    expect(response[0].groupName).toBe('AU');
  });

  describe('getFirstActiveEventFromGroup', () => {
    const eventsMock = {
      events: [{ markets: [{ outcomes: [{ name: '' }] }] }],
      classesTypeNames: {
        UK: [{
          name: 'Roscommon',
          typeDisplayOrder: 100
        },
        {
          name: 'Saas',
          typeDisplayOrder: 102
        },
        {
          name: 'Saas',
          typeDisplayOrder: 102
        },
        {
          name: 'Mauquenchy',
          typeDisplayOrder: 101
        }],
        IE: [{
          name: 'Event 1',
          typeDisplayOrder: 102
        }]
      }
    } as any;
    beforeEach(() => {
      component.filter = 'racing.today';
      component.racingGroupFlag = 'UK';
    });

    it('should sort the group based on active events(false|true)', () => {
      component.raceType = 'horseracing';
      component.racingGroup = [{
        typeName: 'Roscommon',
        name: 'Roscommon',
        startTime: 1550751407661,
        correctedDay: 'racing.dayMonday',
        correctedDayValue: 'racing.today',
        liveStreamAvailable: true,
        cashoutAvail: 'Y',
        isFinished: 'true',
        markets: [{
          ...(<IMarket>{}),
          isGpAvailable: true
        }]
      }] as any;
      racingService.getFirstActiveEventFromGroup = jasmine.createSpy('getFirstActiveEventFromGroup').and
      .returnValue(null);
      component['getRacesForDay'](eventsMock);
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('should sort the group based on active events (true|false)', () => {
      component.raceType = 'horseracing';
      component.racingGroup = [{
        typeName: 'Roscommon',
        name: 'Roscommon',
        startTime: new Date().getTime() + (12 * 60 * 1000),
        correctedDay: 'racing.dayMonday',
        correctedDayValue: 'racing.today',
        liveStreamAvailable: true,
        cashoutAvail: 'Y',
        isFinished: 'false',
        markets: [{
          ...(<IMarket>{}),
          isGpAvailable: true
        }]
      }] as any;
      racingService.getFirstActiveEventFromGroup = jasmine.createSpy('getFirstActiveEventFromGroup').and
      .returnValue(null);
      component['getRacesForDay'](eventsMock);
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('should sort the group based on active events (false|false)', () => {
      component.raceType = 'horseracing';
      component.racingGroup = [{
        typeName: 'Roscommon',
        name: 'Roscommon',
        startTime: new Date().getTime() + (12 * 60 * 1000),
        correctedDay: 'racing.dayMonday',
        correctedDayValue: 'racing.today',
        liveStreamAvailable: true,
        cashoutAvail: 'Y',
        isFinished: 'true',
        markets: [{
          ...(<IMarket>{}),
          isGpAvailable: true
        }]
      }] as any;
      racingService.getFirstActiveEventFromGroup = jasmine.createSpy('getFirstActiveEventFromGroup').and
      .returnValue(null);
      component['getRacesForDay'](eventsMock);
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('should sort the group based on active events(Active events)', () => {
      component.raceType = 'horseracing';
      component.racingGroup = racingGroup3;
      component['getRacesForDay'](eventsMock);
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('should return length 0, if there is no events data', () => {
      component.raceType = 'horseracing';
      const eventsMock1 = {
        events: [{ markets: [{ outcomes: [{ name: '' }] }] }],
        classesTypeNames: {
          UK: [],
          IE: []
        }
      } as any;
      component.racingGroup = [];
      component['getRacesForDay'](eventsMock1);
      expect(component.groupedRaces.length).toBe(0);
    });

    it('should sort the group based on active events(No Active events)', () => {
      component.raceType = 'horseracing';
      component.racingGroup = [{
        typeName: 'Roscommon',
        name: 'Roscommon',
        startTime: new Date().getTime() + 11 * 60 * 1000,
        correctedDay: 'racing.dayMonday',
        correctedDayValue: 'racing.today',
        liveStreamAvailable: true,
        cashoutAvail: 'Y',
        markets: [{
          ...(<IMarket>{}),
          isGpAvailable: true
        }]
      }, {
        typeName: 'Saas',
        name: 'Saas',
        startTime: new Date().getTime() + 12 * 60 * 1000,
        correctedDay: 'racing.dayMonday',
        correctedDayValue: 'racing.today',
        markets: [{
          ...(<IMarket>{}),
          isGpAvailable: true
        }]
      }] as any;
      component['getRacesForDay'](eventsMock);
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('should sort the group based on active events(Active events) in ngOninit', () => {
      component.raceType = 'horseracing';
      component.racingGroup = racingGroup3;
      component.eventsData = eventsMock;
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });
    it('should sort the group based on active events(Active events) in ngOninit (greyhound)', () => {
      component.raceType = 'greyhounds';
      component.racingGroup = racingGroup3;
      component.eventsData = eventsMock;
      spyOn(component as any, 'validateRacesForToday');
      component.ngOnInit();
      expect(component.groupedRaces[0].groupName).toBe('Roscommon');
    });

    it('ngOnChanges', () => {
      const changes = <any>{
        eventsData: {
          currentValue: eventsMock
        }
      };
      component.eventsData = <any>{};
      component.raceType = 'horseracing';
      component.racingGroup = racingGroup3;

      component.ngOnChanges(changes);
      expect(component.eventsData).toEqual(eventsMock);
    });

    it('ngOnChanges no eventsData', () => {
      const changes = <any>{
        eventsData: {}
      };
      component.eventsData = <any>{};
      component.raceType = 'horseracing';
      component.racingGroup = racingGroup3;

      component.ngOnChanges(changes);
      expect(component.eventsData).not.toEqual(eventsMock);
    });
  });

  describe('sortActiveGroupedRaces', () => {
    it('should sort active groups based on name and display order', () => {
      const racingGroup = [{
        groupName: 'Roscommon',
        typeDisplayOrder: 2
      }, {
        groupName: 'Saas',
        typeDisplayOrder: 4
      }, {
        groupName: 'Saas',
        typeDisplayOrder: 4
      }, {
        groupName: 'Mauquenchy',
        typeDisplayOrder: 3
      }] as any;
      const response = component['sortActiveGroupedRaces'](racingGroup);
      expect(response[0].groupName).toBe('Roscommon');
    });
    it('should not return anything if array is empty', () => {
      const racingGroup = [] as any;
      const response = component['sortActiveGroupedRaces'](racingGroup);
      expect(response.length).toBe(0);
    });
  });

  it('isBIRSignpostPresented with null drilldownTagNames', () => {
    const sortedGroupedRaces = [{
      drilldownTagNames: null
    }] as any;

    const isBIRSignpostPresented = component['isBIRSignpostPresented'](sortedGroupedRaces);

    expect(isBIRSignpostPresented).toBeFalse();
  });

  it('isBIRSignpostPresented with undefined drilldownTagNames', () => {
    const sortedGroupedRaces = [{
      dummy: ''
    }] as any;

    const isBIRSignpostPresented = component['isBIRSignpostPresented'](sortedGroupedRaces);

    expect(isBIRSignpostPresented).toBeFalse();
  });

  it('isBIRSignpostPresented with BIR drilldownTagNames', () => {
    const sortedGroupedRaces = [{
      drilldownTagNames: `${DRILLDOWNTAGNAMES.HR_BIR},Tag2,Tag3,`
    }] as any;

    const isBIRSignpostPresented = component['isBIRSignpostPresented'](sortedGroupedRaces);

    expect(isBIRSignpostPresented).toBeTrue();
  });

  it('isBIRSignpostPresented with BIR drilldownTagNames', () => {
    const sortedGroupedRaces = [{
      drilldownTagNames: `Tag2,Tag3,`
    }] as any;

    const isBIRSignpostPresented = component['isBIRSignpostPresented'](sortedGroupedRaces);

    expect(isBIRSignpostPresented).toBeFalse();
  });
  it('should call hasResult', () => {
    component.raceType = 'horseracing';
    let events: any = [{
      correctedDayValue: 'racing.today',
      isResulted: false,
      isStarted: false,
      rawIsOffCode: 'N',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    let hasResult = component['hasResult'](events);
    expect(hasResult).toEqual(false);
    events  = [{
      correctedDayValue: 'racing.today',
      isResulted: false,
      isStarted: false,
      rawIsOffCode: 'Y',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    expect(component['hasResult'](events)).toEqual(true);
    events = [{
      correctedDayValue: 'racing.today',
      isResulted: true,
      isStarted: false,
      rawIsOffCode: 'Y',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    hasResult = component['hasResult'](events);
    expect(hasResult).toEqual(true);
  });

  it('should call earlySignPostTitle', () => {
    locale.getString = jasmine.createSpy('getString').and.returnValue('Early Prices Available');
    expect(component.earlySignPostTitle()).toEqual('Early Prices Available');
  });

  describe("should call isEarlyPricesAvailable", () => {
    it('should check is early price available', () => {
      component.raceType = 'horseracing';
      const events: any = [{
       correctedDayValue : 'racing.today',
       isResulted: false,
       isStarted: false,
       rawIsOffCode: 'N',
       markets : [
         {isLpAvailable: true}
       ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(false);
     });
     it('should check is early price not available', () => {
      component.raceType = 'horseracing';
      const events: any = [{
       correctedDayValue : 'racing.today',
       isStarted: false,
       isLiveNowEvent: false,
       isResulted: false,
       rawIsOffCode: "Y",
       markets : [
         {isLpAvailable: true}
       ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(false);
     });
    it('should check is early price available greyhound today', () => {
      component.raceType = 'greyhound';
      const events: any = [{
       correctedDayValue : 'racing.tomorrow',
       correctedDay : 'sb.today',
       isResulted: false,
       isStarted: false,
       rawIsOffCode: 'N',
       markets : [
         {isLpAvailable: true}
       ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
       expect(isEarlyPricesAvailable).toEqual(true);
     });
    it('should check is early price available greyhound tomorrow', () => {
      component.raceType = 'greyhound';
      const events: any = [{
       correctedDayValue : 'racing.tomorrow',
       correctedDay : 'sb.tomorrow',
       isResulted: false,
       isStarted: false,
       rawIsOffCode: 'N',
       markets : [
         {isLpAvailable: true}
       ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
       expect(isEarlyPricesAvailable).toEqual(true);
     });
  });
  

   

  describe('setGroupedRacesByType', () => {
    it('should set grouped races based on type( horseRacing)', () => {
      component.raceType = 'horseracing';
      const sortedGroupedRaces = [{
        groupName: 'Roscommon',
        typeDisplayOrder: 2
      }, {
        groupName: 'Saas',
        typeDisplayOrder: 4
      }, {
        groupName: 'Saas',
        typeDisplayOrder: 4
      }, {
        groupName: 'Mauquenchy',
        typeDisplayOrder: 3
      }] as any;
      const activeGroupedRaces = [{
        groupName: 'Roscommon',
        typeDisplayOrder: 2
      }] as any;
      const response = component['setGroupedRacesByType'](sortedGroupedRaces, activeGroupedRaces);
      expect(response.length).not.toBe(0);
    });
    it('should set grouped races based on type( greyhounds)', () => {
      component.raceType = 'greyhounds';
      const sortedGroupedRaces = [{
        groupName: 'Roscommon',
        typeDisplayOrder: 2
      }, {
        groupName: 'Saas',
        typeDisplayOrder: 4
      }] as any;
      const activeGroupedRaces = [] as any;
      const response = component['setGroupedRacesByType'](sortedGroupedRaces, activeGroupedRaces);
      expect(response.length).not.toBe(0);
    });
    it('should set groupedraces when array is empty', () => {
      component.raceType = 'greyhounds';
      const sortedGroupedRaces = [] as any;
      const activeGroupedRaces = [] as any;
      const response = component['setGroupedRacesByType'](sortedGroupedRaces, activeGroupedRaces);
      expect(response.length).toBe(0);
    });
  });
  
  describe('OverlayLogic', () => {
    it('should not trigger pubsub publish method', () => {
      const event = {
        categoryId: '21',
        typeId: 223,
        id: 2193204823
      };
      component.showSwitcher = true;
      component.overlayMenuClose(event);
      expect(pubsub.publish).not.toHaveBeenCalled();
    });

    it('should trigger pubsub publish method with empty event', () => {
      const event = null;
      component.showSwitcher = false;
      component.overlayMenuClose(event);
      expect(pubsub.publish).toHaveBeenCalled();
    });


    it('should trigger pubsub publish method', () => {
      const event = {
        categoryId: '21',
        typeId: 223,
        id: 2193204823
      };
      component.showSwitcher = false;
      component.groupFlagText = 'france';
      component.overlayMenuClose(event);
      const expectedObj = {
        eventAction: 'meetings',
        eventCategory: 'horse racing',
        eventLabel: `navigation – ${component.groupFlagText.toLowerCase()}`,
        categoryID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      };
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', expectedObj);
      expect(pubsub.publish).toHaveBeenCalled();
    });

    it('should trigger gtmService push with GH', () => {
      const event = {
        categoryId: '16',
        typeId: 223,
        id: 2193204823
      };
      component.showSwitcher = false;
      component.groupFlagText = 'france';
      component.overlayMenuClose(event);
      const expectedObj = {
        eventAction: 'meetings',
        eventCategory: 'greyhounds',
        eventLabel: `navigation – ${component.groupFlagText.toLowerCase()}`,
        categoryID: event.categoryId,
        typeID: event.typeId,
        eventID: event.id
      };
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', expectedObj);
    });
  });
});
