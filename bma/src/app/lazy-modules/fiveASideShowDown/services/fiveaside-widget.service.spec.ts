import { FiveasideWidgetService } from './fiveaside-widget.service';

describe('FiveasideWidgetService', () => {
  let service: FiveasideWidgetService;
  let lobbyService,
  pubSub,
  rulesService,
  timeSyncService,
  liveEventClockProviderService,
  fiveAsideLiveServeUpdatesService;

  beforeEach(() => {
    fiveAsideLiveServeUpdatesService = {
      createEventScoreComments: jasmine.createSpy(),
      eventClockUpdate: jasmine.createSpy()
    };
    timeSyncService = {
      getTimeDelta: jasmine.createSpy()
    };
    liveEventClockProviderService = {
      create: jasmine.createSpy().and.returnValue({})
    };
    lobbyService = {
      getTeamNameFromEventComments: jasmine.createSpy('getTeamNameFromEventComments').and.returnValue({
        homeTeam: 'england',
        awayTeam: 'scotland'
      } as any),
      addScoresAndClockForEvents: jasmine.createSpy('addScoresAndClockForEvents')
    };
    rulesService = {
      formFlagName: jasmine.createSpy('formFlagName').and.returnValue('#flag_round_england')
    };
    pubSub = {
      publish: jasmine.createSpy('publish'),
      API: {
        SHOWDOWN_LIVE_EVENT_RESULTED: 'SHOWDOWN_LIVE_EVENT_RESULTED'
      }
    };
    service = new FiveasideWidgetService(lobbyService, rulesService, pubSub, timeSyncService, liveEventClockProviderService,
      fiveAsideLiveServeUpdatesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getEventLiveStatus', () => {
    it('should set isLive false, if first condition is false', () => {
      const event = { started: false, id: 123} as any;
      const widget = {} as any;
      service.getEventLiveStatus(event, widget);
      expect(widget.isLive).toBe(false);
    });
    it('should set isLive false, if first condition is true and 2nd is false', () => {
      const event = { started: true, regularTimeFinished: true, id: 123 } as any;
      const widget = {} as any;
      service.getEventLiveStatus(event, widget);
      expect(widget.isLive).toBe(false);
      expect(pubSub.publish).toHaveBeenCalled();
    });
    it('should set isLive false, if first condition is true and 2nd is true', () => {
      const event = { started: true, regularTimeFinished: false, id: 123 } as any;
      const widget = {} as any;
      service.getEventLiveStatus(event, widget);
      expect(widget.isLive).toBe(true);
      expect(pubSub.publish).not.toHaveBeenCalled();
    });
  });
  describe('#setScoresFromEventComments', () => {
    it('should set data from comments', () => {
      spyOn(service as any, 'clockUpdate');
      const event = {
        isFinished: true, regularTimeFinished: true,
        scores: { home: { score: '1' }, away: { score: '2' } }
      } as any;
      const widget = {} as any;
      service.setScoresFromEventComments(event, widget);
      expect(widget.awayScore).toEqual('2');
    });
    it('should call createEventScoreComments when update is passed', () => {
      spyOn(service as any, 'clockUpdate');
      const event = {
        isFinished: true, isResulted: true,regularTimeFinished: true,
        scores : { home: { score: '1' }, away: { score: '2' } } 
      } as any;
      const widget = {} as any;
      service.setScoresFromEventComments(event, widget, { payload: {} } as any);
      expect(fiveAsideLiveServeUpdatesService.createEventScoreComments).toHaveBeenCalled();
    });
  });
  describe('#setScoresFromOptaUpdate', () => {
    it('should call setScoresFromOptaUpdate when update is passed', () => {
      spyOn(service as any, 'clockUpdate');
      const event = {
        isFinished: true, isResulted: true,regularTimeFinished: true,
        scores : { home: { score: '1' }, away: { score: '2' } } 
      } as any;
      const widget = {} as any;
      service.setScoresFromOptaUpdate(event, widget, { payload: { scores: { home: { score: '1' }, away: { score: '2' } } } } as any);
      expect(widget.homeScore).toEqual('1');
      expect(widget.awayScore).toEqual('2');
    });
  });
  describe('#createClockForEventEntity', () => {
    it('should create clock when clock is null', () => {
      const event = {
        started: true
      } as any;
      const widget = {} as any;
      service['createClockForEventEntity'](event as any, {} as any);
      expect(liveEventClockProviderService.create).toHaveBeenCalled();
    });
    it('should not create clock when started is false', () => {
      const event = {
        started: false
      } as any;
      const widget = {} as any;
      service['createClockForEventEntity'](event as any, {} as any);
      expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });
    it('should not create clock when clock is present', () => {
      const event = {
        clock : {},
        started: false
      } as any;
      service['createClockForEventEntity'](event as any, {} as any);
      expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });
  });
  describe('#liveServeUpdatetoClockDataMapper', () => {
    it('should return ILiveClock object', () => {
      const update = {payload : {ev_id : 1}} as any;
      service['liveServeUpdatetoClockDataMapper'](update);
      expect(service['liveServeUpdatetoClockDataMapper'](update)).not.toBeNull();
    });
    it('should return null', () => {
      const update = {} as any;
      service['liveServeUpdatetoClockDataMapper'](update);
      expect(service['liveServeUpdatetoClockDataMapper'](update)).toBeNull();
    });
  });
  describe('#buildLeaderBoardData', () => {
    it('should not update leaderBoards, if no events in widget', () => {
      const leaderBoards = [{}] as any;
      const events = [];
      service.buildLeaderBoardData(leaderBoards, events);
      expect(events.length).toEqual(0);
    });
    it('should not update leaderBoards, if events length is 0', () => {
      const leaderBoards = [{ eventDetails: {}}] as any;
      const events = [];
      service.buildLeaderBoardData(leaderBoards, events);
      expect(events.length).toEqual(0);
    });
    it('should update leaderBoards, if data is available', () => {
      const leaderBoards = [{ eventDetails: {id: 123, clockData: {}}}] as any;
      const events = [];
      service.buildLeaderBoardData(leaderBoards, events);
      expect(events.length).toEqual(1);
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).toHaveBeenCalled();
    });
    it('should update leaderBoards, if clockData is not available', () => {
      const leaderBoards = [{ eventDetails: {id: 123, clockData: null}}] as any;
      const events = [];
      service.buildLeaderBoardData(leaderBoards, events);
      expect(events.length).toEqual(1);
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
    });
  });
  describe('#clockUpdate', () => {
    it('should not update clock, if eventclock is not available', () => {
      const eventEntity = {} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget);
      expect(widget.isHalfTime).toBeUndefined();
    });
    it('should update clock, if eventclock is available(not HT/FT)', () => {
      const eventEntity = { clock: { matchTime: '1:00'}} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget);
      expect(widget.isHalfTime).toBe(false);
      expect(widget.isHalfTime).toBe(false);
    });
    it('should update clock, if eventclock is available(HT)', () => {
      const eventEntity = { clock: { matchTime: 'HT'}} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget);
      expect(widget.isHalfTime).toBe(true);
      expect(widget.isFullTime).toBe(false);
    });
    it('should update clock, if eventclock is available(FT)', () => {
      const eventEntity = { clock: { matchTime: 'FT'}} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget);
      expect(widget.isHalfTime).toBe(false);
      expect(widget.isFullTime).toBe(true);
    });
    it('should call createClockForEventEntity method when update is present', () => {
      spyOn(service as any, 'createClockForEventEntity');
      const eventEntity = { clock: { matchTime: 'FT'}} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget, {} as any);
      expect(service['createClockForEventEntity']).toHaveBeenCalled();
    });
    it('should not call createClockForEventEntity method when update is present', () => {
      spyOn(service as any, 'createClockForEventEntity');
      const eventEntity = { clock: { matchTime: 'FT'}} as any;
      const widget = {} as any;
      service.clockUpdate(eventEntity, widget, null);
      expect(service['createClockForEventEntity']).not.toHaveBeenCalled();
    });
  });
  describe('#getEventResultedStatus', () => {
    it('should get resulted status false, if none satifies', () => {
      const response = service['getEventResultedStatus']({regularTimeFinished: false} as any);
      expect(response).toBe(false);
    });
  });
  describe('#hasTeamScores', () => {
    it('should return false if no homeScore', () => {
      const response = service['hasTeamScores'](null, null);
      expect(response).toBe(false);
    });
    it('should return false if no awayScore', () => {
      const response = service['hasTeamScores']('1', null);
      expect(response).toBe(false);
    });
  });
  describe('#getTeamScore', () => {
    it('should return null, if no comments', () => {
      const event = {} as any;
      const response = service['getTeamScore'](event, 'home');
      expect(response).toBe(null);
    });
    it('should return null, if no teams', () => {
      const event = { comments: {}} as any;
      const response = service['getTeamScore'](event, 'home');
      expect(response).toBe(null);
    });
    it('should return null, if no home', () => {
      const event = { comments: { teams: {}}} as any;
      const response = service['getTeamScore'](event, 'home');
      expect(response).toBe(null);
    });
    it('should not return null, if data is available', () => {
      const event = { scores : { home: { score: '1'}}} as any;
      const response = service['getTeamScore'](event, 'home');
      expect(response).toEqual('1');
    });
  });
  describe('#setActiveWidget', () => {
    it('should return false', () => {
      const response = service['setActiveWidget'](1);
      expect(response).toBe(false);
    });
    it('should return true', () => {
      const response = service['setActiveWidget'](0);
      expect(response).toBe(true);
    });
  });
  describe('#createClockWithClockData', () => {
    it('should add the clock to event', () => {
      const event = { clock: undefined, started: true } as any;
      service['createClockWithClockData'](event);
      expect(event.clock).not.toBeUndefined();
    });
    it('should not add the clock to the event', () => {
      const event = { clock: undefined, started: false } as any;
      service['createClockWithClockData'](event);
      expect(event.clock).toBeUndefined();
    });
    it('should not call liveEventClockProviderService', () => {
      const event = { clock: {}, started: true } as any;
      service['createClockWithClockData'](event);
      expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });
  });
});
