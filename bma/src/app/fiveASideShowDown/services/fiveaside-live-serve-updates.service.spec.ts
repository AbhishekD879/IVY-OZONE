import LiveEventClock from '@app/shared/components/liveClock/live-event-clock.class';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates.service';
import { eventDetails, sCLOCKUpdate, sEVENTUpdate, sSCBRDUpdate } from '@app/fiveASideShowDown/services/show-down-cards.mock';

describe('FiveasideLiveServeUpdatesService', () => {
  let service: FiveAsideLiveServeUpdatesService;
  let fiveASideShowDownLobbyService;
  let eventMock, clockUpdate, scoreUpdate, eventUpdate, clockObj,
  commentsService, scoreParserService, sportEventHelperService;
  const serverTimeDelta = null;
  const clockData = null;

  beforeEach(() => {
    fiveASideShowDownLobbyService = {
      eventCommentsUpdate: jasmine.createSpy(),
      setEventStateByStartDate: jasmine.createSpy()
    };
    commentsService = {
      footballUpdateExtend: jasmine.createSpy(),
    };
    scoreParserService = {
      getScoreType: jasmine.createSpy('getScoreType'),
    };
    sportEventHelperService = {
      isTennis: jasmine.createSpy('isTennis')
    };
    fiveASideShowDownLobbyService = {
      eventCommentsUpdate: jasmine.createSpy(),
      setEventStateByStartDate: jasmine.createSpy()
    };
    clockObj = new LiveEventClock(serverTimeDelta, clockData);
    eventMock = eventDetails;
    clockUpdate = sCLOCKUpdate;
    scoreUpdate = sSCBRDUpdate;
    eventUpdate = sEVENTUpdate;
    service = new FiveAsideLiveServeUpdatesService(fiveASideShowDownLobbyService, commentsService,
      scoreParserService, sportEventHelperService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#updateEventComments', () => {
    it('#updateEventComments method should be called with event object and update', () => {
      service.updateEventComments(eventMock, scoreUpdate);
      expect(fiveASideShowDownLobbyService.eventCommentsUpdate).not.toHaveBeenCalledWith(scoreUpdate.payload, eventMock);
    });
  });

  describe('#createEventScoreComments', () => {
    it('should not call updateSportScores when extender is undefined', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['createEventScoreComments']({} as any, { categoryCode: 'other', comments: {}, categoryId: '1' } as any);
      expect(commentsService.updateSportScores).not.toHaveBeenCalled();
    });

    it('should call updateSportScores when comments are undefined', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['createEventScoreComments']({} as any, { categoryCode: 'football' } as any);
      expect(commentsService.updateSportScores).toHaveBeenCalledWith(
        { teams: { home: { eventId: undefined }, away: { eventId: undefined } } },
        {}
      );
    });
    it('should call updateSportScores when isTennis is false', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      sportEventHelperService.isTennis.and.returnValue(false);
      service['createEventScoreComments']({} as any, { categoryCode: 'football' } as any);
      expect(commentsService.updateSportScores).toHaveBeenCalled();
    });
    it('should call updateSportScores when isTennis is true', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue('Simple');
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      sportEventHelperService.isTennis.and.returnValue(true);
      service['createEventScoreComments']({} as any, { categoryCode: 'football' } as any);
      expect(commentsService.updateSportScores).toHaveBeenCalled();
    });
    it('should not call updateSportScores when scoreType is undefined', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue(null);
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['createEventScoreComments']({} as any, { categoryCode: 'other', comments: {}, categoryId: '1' } as any);
      expect(commentsService.updateSportScores).not.toHaveBeenCalled();
    });
    it('should not call updateSportScores when scoreType is undefined', () => {
      scoreParserService.getScoreType = jasmine.createSpy('getScoreType').and.returnValue(null);
      commentsService.updateSportScores = jasmine.createSpy('updateSportScores');
      service['createEventScoreComments']({} as any, { categoryCode: 'football', comments: {}, categoryId: '1' } as any);
      expect(commentsService.updateSportScores).not.toHaveBeenCalled();
    });
  });

  describe('#eventClockUpdate', () => {
    it('#eventClockUpdate method should be called with event object and update', () => {
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.eventClockUpdate(clockUpdate.payload, eventMock);
      expect(eventMock.clock.refresh).toHaveBeenCalledWith(clockUpdate.payload);
    });

    it('#eventClockUpdate method should not be called with event object and update is null', () => {
      const payload = null;
      const event = {id : 1} as any;
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.eventClockUpdate(payload, event);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });

    it('#eventClockUpdate method should not be called when event and update id are different', () => {
      const payload = {id : '1'} as any;
      const event = {id :  2, clock : {}} as any;
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.eventClockUpdate(payload, event);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });

    it('#eventClockUpdate method should not be called when event and update id are different', () => {
      const payload = {id : '1'} as any;
      const event = {id :  1, clock : null} as any;
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.eventClockUpdate(payload, event);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });
  });

  it('#updateEventLiveData method should be called with event object and update', () => {
    service.updateEventLiveData(eventMock, eventUpdate);
    expect(eventMock.isResulted).toEqual(eventUpdate.payload.regular_time_finished);
    expect(fiveASideShowDownLobbyService.setEventStateByStartDate).toHaveBeenCalledWith(eventMock);
  });
  describe('#updateClock', () => {
    it('should not be called with event object and update is null', () => {
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.updateClock(null, { payload: null} as any);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });
    it('should not be called when event and update id are different', () => {
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      const update = {
        payload: {ev_id : '1'}
      } as any;
      const event = {id :  2, clock : {}} as any;
      service.updateClock(event, update);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });
    it('should not be called when event and update id are different', () => {
      const update = {
        payload: {ev_id : '1'}
      } as any;
      const event = {id :  1, clock : null} as any;
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.updateClock(event, update);
      expect(eventMock.clock.refresh).not.toHaveBeenCalled();
    });
    it('should call clock refresh if data satisfies', () => {
      eventMock['clock'] = clockObj;
      spyOn(eventMock.clock, 'refresh');
      service.updateClock(eventMock, clockUpdate);
      expect(eventMock.clock.refresh).toHaveBeenCalledWith(clockUpdate.payload);
    });
  });
});
