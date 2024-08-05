import { RaceGridComponent } from '@shared/components/raceGrid/race-grid';

describe('RaceGridComponent', () => {
  let component: RaceGridComponent;

  let timeService;
  let localeService;
  let lpAvailability;
  let datePipe;
  let routingHelperService;

  beforeEach(() => {
    timeService = {
      formatHours: jasmine.createSpy('formatHours'),
      getDayI18nValue: jasmine.createSpy('getDayI18nValue'),
      getMonthI18nValue: jasmine.createSpy('getMonthI18nValue')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    lpAvailability = {
      check: jasmine.createSpy('check').and.returnValue(true)
    };
    datePipe = {
      transform: jasmine.createSpy('transform')
    };
    routingHelperService = {
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };

    component = new RaceGridComponent(timeService, localeService, lpAvailability, datePipe, routingHelperService);
    component.eventsData = {
      events: [],
      groupedRacing: [],
      selectedTab: '',
      classesTypeNames: {},
      modules: {}
    } as any;
    component.racingGroupFlag = 'UK';
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      spyOn(component as any, 'sortAndFillMeetings');
    });
    it('should check race type => "tote"', () => {
      component.raceType = 'tote';
      component.ngOnInit();
      expect(component['isTote']).toBe(true);
    });

    it('should check race type => ""', () => {
      component.raceType = '';
      component.ngOnInit();
      expect(component['isTote']).toBe(false);
    });
    afterEach(() => {
      expect((component as any).sortAndFillMeetings).toHaveBeenCalled();
    });
  });

  describe('getFullDate should get formatted date string', () => {
    let date;
    beforeEach(() => {
      date = {
        date: Symbol('date'),
        toString: jasmine.createSpy('toString').and.returnValue('Date')
      };
      spyOn(window as any, 'Date').and.returnValue(date);
      datePipe.transform.and.returnValues(15, 'Monday', 'Jun');
      component.isTote = false;
    });

    it('for non-Tote event', () => {
      localeService.getString.and.returnValues('Tuesday', 'July');
      timeService.getDayI18nValue.and.returnValue('Tue');
      timeService.getMonthI18nValue.and.returnValue('Jul');

      expect(component.getFullDate()).toEqual('Tuesday 15 / July');
      expect(datePipe.transform.calls.allArgs()).toEqual([[date, 'd']]);
      expect(localeService.getString.calls.allArgs()).toEqual([['Tue'], ['Jul']]);
      expect(date.toString).toHaveBeenCalled();
      expect(timeService.getDayI18nValue).toHaveBeenCalledWith('Date');
      expect(timeService.getMonthI18nValue).toHaveBeenCalledWith(date, false);
    });
    it('for Tote event', () => {
      component.isTote = true;
      expect(component.getFullDate()).toEqual('Monday 15 / Jun');
      expect(datePipe.transform.calls.allArgs()).toEqual([[date, 'd'], [date, 'EEEE'], [date, 'MMM']]);
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(timeService.getDayI18nValue).not.toHaveBeenCalled();
      expect(timeService.getMonthI18nValue).not.toHaveBeenCalled();
    });
  });

  describe('raceTypeIcon should return id-string', () => {
    let event;
    beforeEach(() => {
      event = { categoryId: '19' };
      component.isTote = false;
      (component as any).eventsData = [{ events: [event] }];
    });
    describe('for Tote event -', () => {
      beforeEach(() => {
        component.isTote = true;
      });
      it('greyhound', () => {
        expect(component.raceTypeIcon()).toEqual('#greyhound-icon');
      });
      it('non-greyhound (i.e. horseracing)', () => {
        event.categoryId = '123';
        expect(component.raceTypeIcon()).toEqual('#horseracing-icon');
      });
    });

    describe('for non-Tote event -', () => {
      beforeEach(() => {
        component.isTote = false;
        (component as any).eventsData = { events: [event] };
      });
      it('greyhound', () => {
        expect(component.raceTypeIcon()).toEqual('#greyhound-icon');
      });
      it('non-greyhound (i.e. horseracing)', () => {
        event.categoryId = '123';
        expect(component.raceTypeIcon()).toEqual('#horseracing-icon');
      });
      it('without events', () => {
        (component as any).eventsData.events = [];
        expect(component.raceTypeIcon()).toEqual('#horseracing-icon');
      });
    });
  });

  it('isLpAvailable should return lpAvailability.check for event', () => {
    const event = Symbol('event');
    expect(component.isLpAvailable(event as any)).toEqual(true);
    expect(lpAvailability.check).toHaveBeenCalledWith(event as any);
  });

  describe('genEventDetailsUrl', () => {
    let event;
    beforeEach(() => {
      event = { isResulted: false, id: 123 };
      component.isTote = false;
    });
    it('should return URL string for common event', () => {
      routingHelperService.formResultedEdpUrl.and.returnValue('formed-resulted-edp-url');
      expect(component.genEventDetailsUrl(event)).toEqual('formed-resulted-edp-url');
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith(event);
    });
    describe('should return URL string for Tote event', () => {
      beforeEach(() => {
        component.isTote = true;
      });
      it('(not resulted)', () => {
        expect(component.genEventDetailsUrl(event)).toEqual('/tote/event/123');
      });
      it('(resulted)', () => {
        event.isResulted = true;
        expect(component.genEventDetailsUrl(event)).toEqual('/tote/results');
      });
      afterEach(() => {
        expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
      });
    });

  });

  describe('trackById', () => {
    it('should trackById if id is exist', () => {
      expect(component.trackById(1, { id: '234234'} as any)).toBe('1234234');
    });

    it('should trackById if id is not exist', () => {
      expect(component.trackById(1, {} as any)).toBe('1');
    });
  });

  describe('orderEvents', () => {
    const orderedData = Symbol('ordered data');
    let meeting;

    beforeEach(() => {
      meeting = { events: [{ id: '1' }, { id: '2' }], name: 'name1' };
      component.racingGroup = [
        { id: '1', typeName: 'name2' },
        { id: '2', typeName: 'name1' },
        { id: '3', typeName: 'name1' }
      ] as any;
      component.eventsOrder = ['1', '2', '3'];
      component.isTote = false;
      spyOn(component as any, 'orderData').and.returnValue(orderedData as any);
    });
    it('should order data for Tote event', () => {
      component.isTote = true;
      expect(component.orderEvents(meeting)).toEqual(orderedData as any);
      expect((component as any).orderData).toHaveBeenCalledWith([{ id: '1' }, { id: '2' }], ['1', '2', '3']);
    });
    it('should order data for non-Tote event', () => {
      expect(component.orderEvents(meeting)).toEqual(orderedData as any);
      expect((component as any).orderData)
        .toHaveBeenCalledWith([{ id: '2', typeName: 'name1' }, { id: '3', typeName: 'name1' }], ['1', '2', '3']);
    });
  });

  describe('sortAndFillMeetings', () => {
    const orderedData = Symbol('ordered data');
    let eventsData, meetingsOrder;

    beforeEach(() => {
      spyOn(component as any, 'orderData').and.returnValue(orderedData);
      eventsData = {
        classesTypeNames: {
          'F': [{ name: 'name2' }, { name: 'name1' }],
          'U': [{ name: 'name4' }, { name: 'name3' }]
        }
      };
      meetingsOrder = [];

      component.isTote = false;
      component.eventsData = eventsData;
      component.meetingsOrder = meetingsOrder;
      component.racingGroupFlag = 'F';
    });
    it('should sort non-Tote meetings', () => {
      (component as any).sortAndFillMeetings();
      expect(component.meetings).toEqual([{ name: 'name1' }, { name: 'name2' }] as any);
      expect((component as any).orderData).not.toHaveBeenCalled();
    });
    it('should sort Tote meetings', () => {
      component.isTote = true;
      (component as any).sortAndFillMeetings();
      expect((component as any).orderData).toHaveBeenCalledWith(eventsData, meetingsOrder);
      expect(component.meetings).toEqual(orderedData as any);
    });
  });

  it('orderData should sort each item by params', () => {
    spyOn(component as any, 'getSortFields').and.returnValues('1', '3', '4', '2');
    expect((component as any).orderData(['A', 'B', 'C', 'D'] as any, ['x', 'y'])).toEqual(['A', 'D', 'B', 'C']);
    expect((component as any).getSortFields.calls.allArgs()).toEqual([
      ['A', ['x', 'y']],
      ['B', ['x', 'y']],
      ['C', ['x', 'y']],
      ['D', ['x', 'y']]
    ]);
  });

  describe('getSortFields should create combined string for sorting', () => {
    let event;
    beforeEach(() => {
      event = { name: 'Name', localTime: '3:30', foo: 12 };
      timeService.formatHours.and.returnValue('formattedTime');
    });

    it('with localTime entry', () => {
      expect((component as any).getSortFields(event as any, ['name', 'localTime', 'foo']))
        .toEqual('_Name_formattedTime_12');
      expect(timeService.formatHours).toHaveBeenCalledWith('3:30');
    });

    it('without localTime entry', () => {
      delete event.localTime;
      expect(component['getSortFields'](event as any, ['foo', 'name', 'localTime']))
        .toEqual('_12_Name_undefined');
      expect(timeService.formatHours).not.toHaveBeenCalled();
    });
  });
});
