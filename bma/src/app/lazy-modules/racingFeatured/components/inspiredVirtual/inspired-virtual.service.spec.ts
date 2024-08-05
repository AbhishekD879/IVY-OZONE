import { fakeAsync, tick } from '@angular/core/testing';
import { inspiredVirtualConfig } from './inspired-virtual.constant';
import { InspiredVirtualService } from './inspired-virtual.service';

describe('InspiredVirtualService', () => {
  let service: InspiredVirtualService,
    siteServerService,
    timeService,
    cacheEventsService,
    gtmService,
    eventsMock,
    eventsMockPromise,
    timerMock;

  beforeEach(() => {
    timerMock = {
      stop: jasmine.createSpy()
    };
    eventsMock = [{
      id: '1',
      name: 'abc',
      startTime: '3',
      liveServChannels: '111',
      countdownTimer: timerMock,
      liveTimer: timerMock,
      markets: [{
        name: 'testMarket',
      }],
    }, {
      id: '2',
      startTime: '2',
      liveServChannels: '222',
      countdownTimer: timerMock,
      liveTimer: timerMock,
      markets: [{
        name: 'testMarket'
      }]
    }];

    gtmService = {
      push: jasmine.createSpy()
    };
    timeService = {
      apiDataCacheInterval: {},
      selectTimeRangeStart: jasmine.createSpy().and.returnValue('testTimeStart'),
      selectTimeRangeEnd: jasmine.createSpy().and.returnValue('testTimeEnd'),
      getLocalHourMinInMilitary: jasmine.createSpy().and.returnValue('testStartTime')
    };
    cacheEventsService = {
      storedData: {},
      stored: () => { },
      async: jasmine.createSpy().and.returnValue(Promise.resolve(eventsMock)),
      store: jasmine.createSpy().and.returnValue(Promise.resolve(eventsMock))
    };

    siteServerService = {
      getInspiredVirtualEvents: jasmine.createSpy()
    };

    eventsMockPromise = () => Promise.resolve(eventsMock);

    service = new InspiredVirtualService(siteServerService,
      timeService,
      cacheEventsService,
      gtmService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service.config).toEqual(inspiredVirtualConfig);
    expect(timeService.apiDataCacheInterval.inspiredVirtualEventsHR).toEqual(inspiredVirtualConfig.cacheInterval);
    expect(cacheEventsService.storedData.inspiredVirtualEventsHR).toEqual({});
  });

  it('sendGTMOnFirstTimeCollapse', () => {
    service.sendGTMOnFirstTimeCollapse('greyhounds');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'greyhound racing',
      eventAction: 'virtual greyhound racing'
    }));
  });

  it('sendGTMOnGoToLiveEvent', () => {
    service.sendGTMOnGoToLiveEvent('horseracing');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
      eventCategory: 'horse racing',
      eventAction: 'virtual horse racing'
    }));
  });

  it('getStartTime', () => {
    expect(service.getStartTime(111)).toEqual('testStartTime');
    expect(timeService.getLocalHourMinInMilitary).toHaveBeenCalledWith(111);
  });

  describe('destroyTimers', () => {
    it('should NOT delete timer if object does not contain property equal to timers name', () => {
      service.config.eventsCount = 2;
      service.data = [{ id: 1 }];
      service.destroyTimers();

      expect(service.data).toEqual([{ id: 1 }]);
    });

    it('should be unlimited', () => {
      service.data = undefined;
      service.destroyTimers();
      expect(service.data).toBeUndefined();
    });

    it('should be limited', () => {
      service.config.eventsCount = 5;
      service.data = eventsMock;
      service.destroyTimers();

      expect(service.data[0].countdownTimer).toBeFalsy();
      expect(service.data[0].liveTimer).toBeFalsy();

      expect(service.data[1].countdownTimer).toBeFalsy();
      expect(service.data[1].liveTimer).toBeFalsy();
    });

    it('should do nothing if no data on destroyTimers', () => {
      service.config.eventsCount = 1;
      service.destroyTimers();
    });

    it('destroyTimers limited', () => {
      service.config.eventsCount = 5;
      service.data = eventsMock;
      service.destroyTimers();
    });
  });

  it('getEvents', () => {
    spyOn<any>(service, 'cachedEvents').and.returnValue(eventsMockPromise);
    spyOn<any>(service, 'validEvents').and.returnValue(Promise.resolve(eventsMock));
    spyOn<any>(service, 'addTimers').and.returnValue(Promise.resolve(eventsMock));

    service.getEvents().then(result => {
        expect(result).toEqual(eventsMock.reverse());
        expect(service.data.length).toEqual(eventsMock.length);
    });
  });

  it('getEvents when no data in AddTimers', () => {
    spyOn<any>(service, 'cachedEvents').and.returnValue(eventsMockPromise);
    spyOn<any>(service, 'validEvents').and.returnValue(eventsMockPromise);
    spyOn<any>(service, 'addTimers').and.returnValue(null);

    service.getEvents().then((result: any) => {
      expect(result).toEqual([]);
    });
  });

  it('setupEvents', () => {
    const events = [
      { startTime: new Date(new Date().setFullYear(new Date().getFullYear() + 5)).toISOString() },
      { startTime: new Date(new Date().setFullYear(new Date().getFullYear() + 10)).toISOString() }
    ];
    expect(service.setupEvents(events).length).toEqual(2);
    expect(service.data.length).toEqual(2);
  });

  it('setupEvents no events', () => {
    const events = [
      { startTime: '2019-08-03T10:11:12.198Z' },
    ];
    expect(service.setupEvents(events).length).toEqual(0);
    expect(service.data.length).toEqual(0);
  });

  it('setupEvents no events2', () => {
    const events = [];
    expect(service.setupEvents(events).length).toEqual(0);
    expect(service.data.length).toEqual(0);
  });

  it('cachedEvents case 1', fakeAsync(() => {
    spyOn(cacheEventsService, 'stored').and.returnValue(eventsMockPromise);
    service['cachedEvents'](() => {
    }, 'test')('test').then(result => {
      expect(cacheEventsService.async).toHaveBeenCalled();
      expect(result).toEqual(eventsMock);
    });
  }));

  it('cachedEvents case 2', fakeAsync(() => {
    spyOn(cacheEventsService, 'stored').and.returnValue(false);
    const mockFunction = () => Promise.resolve(eventsMock);
    service['cachedEvents'](mockFunction, 'test')('test').then(result => {
      expect(cacheEventsService.async).not.toHaveBeenCalled();
      expect(result).toEqual(eventsMock);
    });
  }));

  it('validEvents', () => {
    eventsMock[0].isFinished = true;
    eventsMock[1].startTime = Date.now() - 20000;
    expect(service['validEvents'](eventsMock)).toEqual([eventsMock[1]]);
  });

  it('addTimers unlimited', () => {
    spyOn<any>(service, 'addTimer');
    expect(service['addTimers'](eventsMock)).toEqual(eventsMock);
    expect(service['addTimer']).toHaveBeenCalledTimes(2);
  });

  it('addTimers limited', () => {
    service.config.eventsCount = 1;
    spyOn<any>(service, 'addTimer');
    expect(service['addTimers'](eventsMock)).toEqual(eventsMock);
    expect(service['addTimer']).toHaveBeenCalledWith(eventsMock[0]);
  });

  it('addTimer', () => {
    spyOn<any>(service, 'chooseTimer').and.returnValue({ call: () => { } });
    service['addTimer'](eventsMock[0]);
    expect(service['chooseTimer']).toHaveBeenCalledWith(eventsMock[0]);
  });

  it('chooseTimer', () => {
    eventsMock[0].startTime = Date.now();
    eventsMock[1].startTime = Date.now() + 90000;
    expect(service['chooseTimer'](eventsMock[0])).toEqual(service['eventLiveTimerFunction']);
    expect(service['chooseTimer'](eventsMock[1])).toEqual(service['beforeEventLiveTimerFunction']);
  });

  describe('beforeEventLiveTimerFunction', () => {
    it('should create countdown timer', fakeAsync(() => {
      const date = Date.now();
      spyOn(Date, 'now').and.returnValue(date);
      spyOn<any>(service, 'addTimer');
      eventsMock[0].startTime = date + 100000;
      service['beforeEventLiveTimerFunction'](eventsMock[0]);
      tick(1000);
      expect(eventsMock[0].countdownTimer).toEqual({
        startTime: eventsMock[0].startTime,
        timeLeft: 19,
        timer: jasmine.any(Number),
        hours: '00',
        minutes: '00',
        seconds: '19',
        start: jasmine.any(Function),
        stop: jasmine.any(Function),
        postUpdate: jasmine.any(Function),
        update: jasmine.any(Function)
      });
      tick(19000);
      expect(eventsMock[0].countdownTimer).toBeUndefined();
      expect(service['addTimer']).toHaveBeenCalled();
    }));

    it('shoud handle 10 and more hours', fakeAsync(() => {
      const date = Date.now();
      spyOn(Date, 'now').and.returnValue(date);
      const event: any = {
        startTime: date + service.config.countdownTimerInterval + 36001000
      };

      service['beforeEventLiveTimerFunction'](event);
      tick(1000);
      event.countdownTimer.stop();

      expect(event.countdownTimer.hours).toEqual('10');
    }));
  });

  it('eventLiveTimerFunction', fakeAsync(() => {
    const date = Date.now();
    const testData = ['test1', 'test2'];
    spyOn(Date, 'now').and.returnValue(date);
    spyOn<any>(service, 'addTimer');
    service.data = testData;
    eventsMock[0].startTime = date + 65000;
    service['eventLiveTimerFunction'](eventsMock[0]);
    tick(1000);
    expect(eventsMock[0].liveTimer).toEqual({
      startTime: eventsMock[0].startTime,
      timeLeft: jasmine.anything(),
      timer: jasmine.anything(),
      start: jasmine.any(Function),
      stop: jasmine.any(Function),
      postUpdate: jasmine.any(Function),
      update: jasmine.any(Function)
    });
    tick(190000);
    expect(eventsMock[0].liveTimer).toBeUndefined();
    expect(service['addTimer']).toHaveBeenCalled();
    expect(service.data).toEqual([testData[0]]);
  }));

  it('eventLiveTimerFunction no events', fakeAsync(() => {
    const date = Date.now();
    const testData = ['test1'];
    spyOn(Date, 'now').and.returnValue(date);
    spyOn<any>(service, 'addTimer');
    service.data = testData;
    eventsMock[0].startTime = date + 65000;
    service['eventLiveTimerFunction'](eventsMock[0]);
    tick(1000);
    expect(eventsMock[0].liveTimer).toEqual({
      startTime: eventsMock[0].startTime,
      timeLeft: jasmine.anything(),
      timer: jasmine.anything(),
      start: jasmine.any(Function),
      stop: jasmine.any(Function),
      postUpdate: jasmine.any(Function),
      update: jasmine.any(Function)
    });
    tick(190000);
    expect(service['addTimer']).not.toHaveBeenCalled();
    expect(service.data.length).toEqual(0);
  }));

  it('requestParams', () => {
    const requestMock = {
      siteChannels: 'M',
      excludeTypeIdCodes: '3048,3049,3123',
      startTime: 'testTimeStart',
      endTime: 'testTimeEnd',
      classId: 285,
      categoryId: 39
    };
    expect(service['requestParams']()).toEqual(requestMock);
  });

  it('should call virtualsGTMEventTracker gtmService.push with the correct data', () => {
    const event = eventsMock[0];
    const url = 'virtuals/sports/next-events'
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'virtuals sports',
      'component.LabelEvent': 'next events',
      'component.ActionEvent': 'click',
      'component.PositionEvent': event?.name,
      'component.LocationEvent': 'next events',
      'component.EventDetails': 'bet now cta',
      'component.URLclicked': url,
    }
    service.virtualsGTMEventTracker(url,event)
    expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
  });

  
  it('should call virtualsGTMEventTracker gtmService not push with the incorrect data', () => {
    const event = undefined;
    const url = 'virtuals/sports/next-events'
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'virtuals sports',
      'component.LabelEvent': 'next events',
      'component.ActionEvent': 'click',
      'component.PositionEvent': event?.name,
      'component.LocationEvent': 'next events',
      'component.EventDetails': 'bet now cta',
      'component.URLclicked': url,
    }
    service.virtualsGTMEventTracker(url,event)
    expect(gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
  });
});
