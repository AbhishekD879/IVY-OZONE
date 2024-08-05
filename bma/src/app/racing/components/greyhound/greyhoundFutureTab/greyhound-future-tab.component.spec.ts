import { GreyhoundFutureTabComponent } from '@racing/components/greyhound/greyhoundFutureTab/greyhound-future-tab.component';

describe('GreyhoundFutureTabComponent', () => {
  let component: GreyhoundFutureTabComponent;
  let filterService, routingHelperService, eventService, sessionStorageService, pubSubService, gtmService, deviceService;

  beforeEach(() => {
    filterService = {
      date: jasmine.createSpy()
    };

    routingHelperService = {
      formSportUrl: jasmine.createSpy(),
      formEdpUrl: jasmine.createSpy()
    };
    eventService = {
      isAnyCashoutAvailable: jasmine.createSpy()
    };
    sessionStorageService = {
      set: jasmine.createSpy('set')
    };
    pubSubService = {
      publish: jasmine.createSpy('publish')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };

    deviceService = {};
    component = new GreyhoundFutureTabComponent(filterService, eventService, routingHelperService, sessionStorageService, pubSubService, gtmService, deviceService);
    component.filter = 'by-time';
    component.orderedEvents = [];
    component.orderedEventsByTypeNames = [];
    component.filteredTypeNames = [{
      name: 'A Type',
      isExpanded: true
    }, {
      name: 'B Type',
      isExpanded: false
    }] as any;
    component.racingEvents = [];
    component.isExpanded = true;
  });

  it('ngOnInit', () => {
    component.isEventOverlay =true;
    component.orderedEvents = [{ link: '', date: ''}] as any;
    component['formEdpUrl'] = jasmine.createSpy('formEdpUrl').and.returnValue('edpUrl');
    component['filteredTime'] = jasmine.createSpy('filteredTime').and.returnValue('filteredTime');

    component.ngOnInit();
    expect((component.orderedEvents[0] as any).link).toEqual('edpUrl');
    expect((component.orderedEvents[0] as any).date).toEqual('filteredTime');
    expect(gtmService.push).not.toHaveBeenCalled();
  });

  it('ngOnChanges isEventOverlay true', () => {
    component.isEventOverlay = false;
    component.ngOnChanges({filter: {currentValue : '2321'}} as any);
    expect(gtmService.push).not.toHaveBeenCalled();
  });

  it('should get filteredTime from filterservice', () => {
    const event = { startTime: '1232323525' } as any;
    component['filteredTime'](event);

    expect(filterService.date).toHaveBeenCalledWith(event.startTime, 'dd-MM-yyyy');
  });

  it('should get CacheOut', () => {
    component.checkCacheOut([], 'typeNameMock');

    expect(eventService.isAnyCashoutAvailable).toHaveBeenCalledWith([], [{ cashoutAvail: 'Y' }]);
  });

  it('should test trackById with id', () => {
    const result = component.trackById(1, {
      id: 111
    });

    expect(result).toEqual(111);
  });

  it('should test trackById with groupFlag', () => {
    const result = component.trackById(1, {
      groupFlag: 22
    });

    expect(result).toEqual(22);
  });

  it('should build URL from Event object', () => {
    const eventMock: any = {};

    component['formEdpUrl'](eventMock);

    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(eventMock);
  });
  
  it('should call toggleByMeetingAccordion', () => {
    component.isExpanded = false;
    component['toggleByMeetingAccordion'](0,'Events');

    expect(gtmService.push).toHaveBeenCalled();
  });

  it('should call toggleByMeetingAccordion by classname', () => {
    component.filteredTypeNames[0].isExpanded = true;
    component['toggleByMeetingAccordion'](0,'Vitural races');

    expect(gtmService.push).toHaveBeenCalled();
  });
  
  it('should call toggleByMeetingAccordion with device desktop', () => {
    component.isEventOverlay = true;
    deviceService.isDesktop = true;
    component['toggleByMeetingAccordion'](1,'Vitural races');
    expect(component.filteredTypeNames[1].isExpanded).toBe(true);
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('should call overlayContentHandler', () => {
    component.filter = 'uk and irish races';
    component['overlayContentHandler']({filter:'uk', eventId:'12123213'}, {id:'1212', categoryId: '1213213'});

    expect(gtmService.push).toHaveBeenCalled();
  });
});
