import { RaceListComponent } from '@shared/components/raceList/race-list.component';

describe('RaceListComponent', () => {
  let component: RaceListComponent;

  let timeService;
  let lpAvailability;
  let routingHelperService;

  beforeEach(() => {
    timeService = {
      formatHours: jasmine.createSpy('formatHours')
    };
    lpAvailability = {
      check: jasmine.createSpy('check').and.returnValue(true)
    };
    routingHelperService = {
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl').and.returnValue('resultedURL')
    };

    component = new RaceListComponent(lpAvailability, routingHelperService, timeService);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });
  it('should initialize properties', () => {
    expect((component as any).PAGE_LIMIT).toEqual(9999);
  });

  describe('ngOnInit', () => {
    it('should call orderedEvents and set limit', () => {
      spyOn(component as any, 'orderEvents').and.returnValue([{ id: 2 }, { id: 1 }] as any);
      component.events = [{ id: 1 }, { id: 2 }] as any;
      component.limit = 100;
      component.ngOnInit();
      expect(component.limited).toEqual(100);
      expect((component as any).orderEvents).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }] as any);
      expect(component.orderedEvents).toEqual([{ id: 2 }, { id: 1 }] as any);
    });
  });

  it('isLpAvailable should return lpAvailability.check for event', () => {
    expect(component.isLpAvailable({ id: 1 } as any)).toEqual(true);
    expect(lpAvailability.check).toHaveBeenCalledWith({ id: 1 });
  });

  describe('getLink', () => {
    it('should return resulted EDP URL for non-tote event', () => {
      expect(component.getLink('non-tote', { id: 1, isResulted: true } as any)).toEqual('resultedURL');
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith({ id: 1, isResulted: true });
    });
    it('should return resulted URL for tote event', () => {
      expect(component.getLink('tote', { id: 1, isResulted: true } as any)).toEqual('/tote/results');
      expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
    });
    it('should return non-resulted URL for tote event', () => {
      expect(component.getLink('tote', { id: 1, isResulted: false } as any)).toEqual('/tote/event/1');
      expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
    });
  });

  describe('showMore', () => {
    it('should increase limited value and update orderedEvents', () => {
      spyOn(component as any, 'orderEvents').and.returnValue([{ id: 2 }, { id: 1 }] as any);
      component.events = [{ id: 1 }, { id: 2 }] as any;
      component.limited = 10;
      component.limit = 5;
      component.showMore();
      expect(component.limited).toEqual(15);
      expect((component as any).orderEvents).toHaveBeenCalledWith([{ id: 1 }, { id: 2 }] as any);
      expect(component.orderedEvents).toEqual([{ id: 2 }, { id: 1 }] as any);
    });
  });

  describe('getIconName', () => {
    it('should return #greyhound-icon', () => {
      component.sportName = 'greyhound';
      expect(component.getIconName()).toEqual('#greyhound-icon');
    });
    it('should return #horseracing-icon', () => {
      component.sportName = 'non-greyhound';
      expect(component.getIconName()).toEqual('#horseracing-icon');
    });
  });

  describe('getRaceTime', () => {
    it('should return time string', () => {
      expect(component.getRaceTime({ localTime: '10:00', typeName: 'TypeName'} as any)).toEqual('10:00 TypeName');
    });
  });

  describe('orderEvents', () => {
    let events;

    beforeEach(() => {
      events = ['A', 'B', 'C', 'D', 'E'];
      component.limited = 2;
      (component as any).PAGE_LIMIT = 4;
      spyOn(component as any, 'getSortFields').and.returnValues('2', '5', '3', '4', '1');
    });
    it('should return sorted events, limited by limit value', () => {
      expect((component as any).orderEvents(events)).toEqual(['E', 'A']);
    });
    it('should return sorted events, limited by default limit value', () => {
      component.limited = null;
      expect((component as any).orderEvents(events)).toEqual(['E', 'A', 'C', 'D']);
    });
    afterEach(() => {
      expect((component as any).getSortFields.calls.allArgs()).toEqual([['A'], ['B'], ['C'], ['D'], ['E']]);
    });
  });

  describe('getSortFields should create combined string for sorting', () => {
    let event;

    beforeEach(() => {
      event = { name: 'Name', localTime: '3:30', foo: 12 };
      component.eventsOrder = ['name', 'localTime', 'foo'];
      timeService.formatHours.and.returnValue('formattedTime');
    });

    it('with localTime entry', () => {
      expect((component as any).getSortFields(event as any))
        .toEqual('_Name_formattedTime_12');
      expect(timeService.formatHours).toHaveBeenCalledWith('3:30');
    });

    it('without localTime entry', () => {
      delete event.localTime;
      expect(component['getSortFields'](event as any))
        .toEqual('_Name_undefined_12');
      expect(timeService.formatHours).not.toHaveBeenCalled();
    });
  });
});
