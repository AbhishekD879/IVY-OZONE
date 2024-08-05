import { fakeAsync, tick } from '@angular/core/testing';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import {
  CARDS_MOCK, CONTEST_MOCK, eventDetails, EVENTS_DETAILS, EVENT_BUILDER_DETAILS, sSCBRDUpdate
} from '@app/fiveASideShowDown/services/show-down-cards.mock';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { of as observableOf, of } from 'rxjs';
import * as fs from '@app/lazy-modules/locale/translations/en-US/fiveaside.lang';
import { SHOWDOWN_CARDS } from '@app/fiveASideShowDown/constants/constants';
import environment from '@environment/oxygenEnvConfig';
import { LobbyData } from '../models/showdown-lobby-contest.model';

describe('ShowDownLobbyService', () => {
  let service: FiveASideShowDownLobbyService;
  let loadByPortionsService;
  let ssRequestHelperService;
  let commentsService;
  let localeService;
  let coreToolsService;
  let buildUtility;
  let timeService;
  let buildEventsWithScoresAndClockBsService;
  let eventsMock;
  let scoreUpdate, http;
  beforeEach(() => {
    http = {
      get: jasmine.createSpy().and.returnValue(
        observableOf({
          body: CARDS_MOCK,
        })
      ),
      post: jasmine.createSpy('post').and.returnValue(of())
    };
    buildUtility = {
      eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue(EVENT_BUILDER_DETAILS)
    };
    buildEventsWithScoresAndClockBsService = {
      build: jasmine.createSpy('build')
    };
    ssRequestHelperService = {
      getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve([{ x: 1 }]))
    } as any;
    loadByPortionsService = {
      get: jasmine.createSpy().and.returnValue(Promise.resolve([{
        event: {
          id: 1,
          children: [{ eventPeriodId: 2 }]
        }
      }]))
    } as any;
    scoreUpdate = sSCBRDUpdate;
    commentsService = {
      footballUpdateExtend: jasmine.createSpy(),
      extendWithScoreType: jasmine.createSpy()
    };
    timeService = {
      countDownTimerForHours: jasmine.createSpy(),
      formatByPattern: jasmine.createSpy(),
      getOnlyFullDateFormatSuffix: jasmine.createSpy()
    };
    coreToolsService = new CoreToolsService();
    localeService = new LocaleService(coreToolsService);
    localeService.setLangData(fs);
    service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
      buildEventsWithScoresAndClockBsService, localeService, http);
  });

  it('service should be created', () => {
    expect(service).toBeTruthy();
  });

  it('get loadAnimation', () => {
    service['loadAnimation'] = true;
    expect(service.loadAnimation).toEqual(true);
  });

  it('set loadAnimation', () => {
    service.loadAnimation = true;
    expect(service['loadAnimation']).toBe(true);
  });

  it('#addScoresAndClockForEvents -Build event and add scores', () => {
    eventsMock = EVENTS_DETAILS;
    service.addScoresAndClockForEvents(eventsMock);
    expect(eventsMock[0].originalName).toEqual(EVENT_BUILDER_DETAILS.originalName);
    expect(buildEventsWithScoresAndClockBsService.build).toHaveBeenCalled();
  });

  it('#getCommentaryFromEvent -Build commentary from event', () => {
    eventsMock = EVENTS_DETAILS;
    spyOn(service as any, 'buildEventMapFromArray');
    service['getCommentaryFromEvent'](eventsMock);
    expect(service['buildEventMapFromArray']).toHaveBeenCalled();
  });

  it('#removeNullKeysFromEvent - Remove id key', () => {
    const children = [{ id: null, event: 123 }];
    service['removeNullKeysFromEvent'](children);
    expect(Object.keys(children[0])).not.toContain('id');
  });

  it('#removeNullKeysFromEvent - Do not remove id key', () => {
    const children = [{ id: 1, event: 123 }];
    service['removeNullKeysFromEvent'](children);
    expect(Object.keys(children[0])).toContain('id');
  });

  it('#buildEventMapFromArray - Convert array entries to object', () => {
    eventsMock = EVENTS_DETAILS;
    const events = [['1', [{ 'a': 1 }]], ['2', [{ 'a': 2 }]]];
    const result = { '1': [{ 'a': 1 }], '2': [{ 'a': 2 }] };
    expect(service['buildEventMapFromArray'](events)).toEqual(result);
  });

  it('#buildEventMapFromArray - Convert array entries to object when events data passed empty', () => {
    const events = [[undefined, [undefined]]];
    expect(service['buildEventMapFromArray'](events)).toEqual({});
  });

  it('#buildEventMapFromArray - Convert array entries to object when passed empty', () => {
    const events = [undefined, undefined];
    expect(service['buildEventMapFromArray'](events)).toEqual({});
  });

  it('#buildEventMapFromArray - Convert array entries to object when non array passed', () => {
    const events = {} as any;
    expect(service['buildEventMapFromArray'](events)).toEqual({});
  });

  describe('#getCommentsByEventsIds', () => {
    it('should return observable of event and comments', fakeAsync(() => {
      spyOn<any>(service, 'getCommentsByEventIds').and.callThrough();
      buildUtility = {
        eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue({ id: 1, name: 'Event' })
      };
      service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
        buildEventsWithScoresAndClockBsService, localeService, http);
      service['getCommentsByEventIds']([1]).subscribe((response) => {
        expect(response.events.length).not.toBe(0);
      });
      expect(loadByPortionsService.get).toHaveBeenCalled();
      tick();
    }));

    it('should return observable of event and comments when no comments are present', fakeAsync(() => {
      spyOn<any>(service, 'getCommentsByEventIds').and.callThrough();
      ssRequestHelperService = {
        getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve([{ x: 1 }]))
      } as any;
      buildUtility = {
        eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue({ id: 1 })
      };
      loadByPortionsService = {
        get: jasmine.createSpy().and.returnValue(Promise.resolve([{
          event: {
            id: 1
          }
        }]))
      } as any;
      service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
        buildEventsWithScoresAndClockBsService, localeService, http);
      service['getCommentsByEventIds']([1]).subscribe((response: any) => {
        expect(response.events.length).not.toBe(0);
        expect(response.events[0]).toEqual({ id: 1 });
        expect(response.comments).toEqual({});
      });
      expect(loadByPortionsService.get).toHaveBeenCalled();
      tick();
    }));

    it('should return observable of event and comments when no data present', fakeAsync(() => {
      spyOn<any>(service, 'getCommentsByEventIds').and.callThrough();
      ssRequestHelperService = {
        getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve([{ x: 1 }]))
      } as any;
      buildUtility = {
        eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue({ id: 1 })
      };
      loadByPortionsService = {
        get: jasmine.createSpy().and.returnValue(Promise.resolve([]))
      } as any;
      service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
        buildEventsWithScoresAndClockBsService, localeService, http);
      service['getCommentsByEventIds']([1]).subscribe((response: any) => {
        expect(response.events.length).toBe(0);
        expect(response.comments).toEqual({});
      });
      expect(loadByPortionsService.get).toHaveBeenCalled();
      tick();
    }));

    it('should return observable of event and comments when no id present', fakeAsync(() => {
      spyOn<any>(service, 'getCommentsByEventIds').and.callThrough();
      ssRequestHelperService = {
        getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve([{ x: 1 }]))
      } as any;
      buildUtility = {
        eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue(null)
      };
      loadByPortionsService = {
        get: jasmine.createSpy().and.returnValue(Promise.resolve([{
          event: { children: [{ eventPeriodId: 2 }] }
        }]))
      } as any;
      service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
        buildEventsWithScoresAndClockBsService, localeService, http);
      service['getCommentsByEventIds']([1]).subscribe((response: any) => {
        expect(response.events.length).toBe(1);
        expect(response.comments).toBeDefined();
        expect(response.events[0]).toBeNull();
      });
      expect(loadByPortionsService.get).toHaveBeenCalled();
      tick();
    }));

    it('should return observable of event and comments when no id and comments present', fakeAsync(() => {
      spyOn<any>(service, 'getCommentsByEventIds').and.callThrough();
      ssRequestHelperService = {
        getCommentsByEventsIds: jasmine.createSpy().and.returnValue(Promise.resolve([{ x: 1 }]))
      } as any;
      buildUtility = {
        eventBuilder: jasmine.createSpy('eventBuilder').and.returnValue(null)
      };
      loadByPortionsService = {
        get: jasmine.createSpy().and.returnValue(Promise.resolve(null))
      } as any;
      service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
        buildEventsWithScoresAndClockBsService, localeService, http);
      service['getCommentsByEventIds']([1]).subscribe((response: any) => {
        expect(response.events).toBeNull();
        expect(response.comments).toBeNull();
        expect(response.events).toBeNull();
      });
      expect(loadByPortionsService.get).toHaveBeenCalled();
      tick();
    }));
  });

  it('#addScoresAndClock - should get events with commentary and build scores and clock', fakeAsync(() => {
    loadByPortionsService = {
      get: jasmine.createSpy().and.returnValue(Promise.resolve([{
        event: {
          id: 1,
          children: [{ eventPeriodId: 2 }]
        }
      }]))
    } as any;
    buildEventsWithScoresAndClockBsService = {
      build: jasmine.createSpy('build').and.returnValue([{
        event: {
          id: 1,
          children: [{ eventPeriodId: 2 }]
        }
      }, {
        event: {
          id: 2,
          children: [{ eventPeriodId: 2 }]
        }
      }])
    };
    service = new FiveASideShowDownLobbyService(loadByPortionsService, ssRequestHelperService, commentsService, buildUtility, timeService,
      buildEventsWithScoresAndClockBsService, localeService, http);
    service['addScoresAndClock']([1]).subscribe((response) => {
      expect(buildEventsWithScoresAndClockBsService.build).toHaveBeenCalled();
      expect(response.length).not.toBe(0);
    });
    tick();
  }));

  it('#eventCommentsUpdate - should update event comments with liveserve update', () => {
    const update = Object.assign({}, scoreUpdate);
    eventsMock = { ...eventDetails };
    eventsMock['comments'] = {
      teams: {
        scores: {
          home: 'oldHome',
          away: 'oldAway'
        }
      }
    };
    service.eventCommentsUpdate(update.payload, eventsMock);
    expect(commentsService.footballUpdateExtend).toHaveBeenCalled();
    expect(commentsService.extendWithScoreType).toHaveBeenCalledWith(eventsMock, eventsMock.categoryCode);
  });

  it('#eventCommentsUpdate - should not update event comments with liveserve update', () => {
    const update = Object.assign({}, scoreUpdate);
    eventsMock = { ...eventDetails } as any;
    delete eventsMock['comments'];
    service.eventCommentsUpdate(update.payload, eventsMock);
    expect(commentsService.footballUpdateExtend).not.toHaveBeenCalled();
    expect(commentsService.extendWithScoreType).not.toHaveBeenCalledWith(eventsMock, eventsMock.categoryCode);
  });

  describe('#signPostingsPriority', () => {
    it('#signPostingsPriority - should return showdown card signpostings object', () => {
      service['checkSignPostingExistsInContest'] = jasmine.createSpy().and.returnValue(true);
      const contest = { ...CARDS_MOCK[0].contests[0] };
      const result = service.signPostingsPriority(contest as any);
      expect(result.size).toBeTruthy();
      expect(result.totalPrizes).toBeTruthy();
      expect(result.teams).toBeFalsy();
      expect(result.summary).toBeTruthy();
      expect(result.firstPlace).toBeFalsy();
      expect(result.vouchers).toBeFalsy();
      expect(result.tickets).toBeFalsy();
      expect(result.freeBets).toBeFalsy();
    });

    it('#signPostingsPriority - should return showdown card signpostings object as false', () => {
      service['checkSignPostingExistsInContest'] = jasmine.createSpy().and.returnValue(false);
      const contest = { ...CARDS_MOCK[0].contests[0] };
      const result = service.signPostingsPriority(contest as any);
      expect(result.size).toBeFalsy();
      expect(result.totalPrizes).toBeFalsy();
      expect(result.teams).toBeFalsy();
      expect(result.summary).toBeFalsy();
      expect(result.firstPlace).toBeFalsy();
      expect(result.vouchers).toBeFalsy();
      expect(result.tickets).toBeFalsy();
      expect(result.freeBets).toBeFalsy();
    });

    it('#signPostingsPriority - should return all signpostings as false when contest is null', () => {
      service['checkSignPostingExistsInContest'] = jasmine.createSpy().and.returnValue(false);
      const contest = null;
      const result = service.signPostingsPriority(contest as any);
      expect(result.size).toBeFalsy();
      expect(result.totalPrizes).toBeFalsy();
      expect(result.teams).toBeFalsy();
      expect(result.summary).toBeFalsy();
      expect(result.firstPlace).toBeFalsy();
      expect(result.vouchers).toBeFalsy();
      expect(result.tickets).toBeFalsy();
      expect(result.freeBets).toBeFalsy();
    });

    it('#signPostingsPriority - should return all signpostings as false when contest in empty', () => {
      service['checkSignPostingExistsInContest'] = jasmine.createSpy().and.returnValue(false);
      const contest = {};
      const result = service.signPostingsPriority(contest as any);
      expect(result.size).toBeFalsy();
      expect(result.totalPrizes).toBeFalsy();
      expect(result.teams).toBeFalsy();
      expect(result.summary).toBeFalsy();
      expect(result.firstPlace).toBeFalsy();
      expect(result.vouchers).toBeFalsy();
      expect(result.tickets).toBeFalsy();
      expect(result.freeBets).toBeFalsy();
    });
  });

  describe('#checkSignPostingExistsInContest', () => {
    it('should return true when contest and signPost passed', () => {
      const contest = { ...CARDS_MOCK[0].contests[0] } as any;
      const signPost = 'size';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeTruthy();
    });

    it('should return true when contest freeBets object passed', () => {
      const contest = { prizePool: { freeBets: 23 } } as any;
      const signPost = 'freeBets';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeTruthy();
    });

    it('should return false when freeBets and contest object passed', () => {
      const contest = { prizePool: {} } as any;
      const signPost = 'freeBets';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });

    it('should return false when size and contest object passed', () => {
      const contest = { prizePool: {} } as any;
      const signPost = 'size';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });

    it('should return false when size and contest empty object passed', () => {
      const contest = {} as any;
      const signPost = 'size';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });

    it('should return false when contest empty object passed', () => {
      const contest = {} as any;
      const signPost = 'freeBets';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });

    it('should return false when contest empty object passed', () => {
      const contest = {} as any;
      const signPost = '';
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });

    it('should return false when contest null passed', () => {
      const contest = null as any;
      const signPost = null;
      expect(service['checkSignPostingExistsInContest'](contest, signPost)).toBeFalsy();
    });
  });

  describe('#setEventStateByStartDate - should update time and countdown timer in event', () => {
    beforeEach(() => {
      eventsMock = { ...eventDetails };
    });
    it('update time in event when diff seconds are negative', () => {
      eventsMock['started'] = false;
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });

    it('update time in event when diff seconds are positive', () => {
      eventsMock['started'] = false;
      const today = new Date();
      const tomorrowDate = new Date(today);
      tomorrowDate.setDate(tomorrowDate.getDate() + 1);
      eventsMock['startTime'] = tomorrowDate.toISOString();
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.formatByPattern).toHaveBeenCalled();
    });

    it('should not update countdowner in event when diff seconds are positive', () => {
      eventsMock['started'] = false;
      const today = new Date();
      const yesterdayDate = new Date(today);
      yesterdayDate.setDate(yesterdayDate.getDate() - 1);
      eventsMock['startTime'] = yesterdayDate.toISOString();
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });

    it('update time and countdown timer in event', () => {
      eventsMock['started'] = false;
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      eventsMock['startTime'] = tomorrow.toISOString();
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.formatByPattern).toHaveBeenCalled();
    });

    it('update time for finished and resulted event', () => {
      eventsMock['regularTimeFinished'] = true;
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.getOnlyFullDateFormatSuffix).toHaveBeenCalledWith(new Date(eventsMock.startTime));
    });

    it('update time for else condition', () => {
      eventsMock['regularTimeFinished'] = false;
      eventsMock['started'] = true;
      service.setEventStateByStartDate(eventsMock);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });

    it('should not update countDowntimer/dateTime when event or startTime is not present', () => {
      const event = { dateTime: '', countDowntimer: '' } as any;
      service.setEventStateByStartDate(event);
      expect(timeService.formatByPattern).not.toHaveBeenCalled();
      expect(event.dateTime).toEqual('');
      expect(event.countDowntimer).toEqual('');
    });

    it('update time in required format when category is Last 7 Days', () => {
      eventsMock['regularTimeFinished'] = false;
      service.setEventStateByStartDate(eventsMock, 'Last 7 Days', true);
      expect(timeService.getOnlyFullDateFormatSuffix).toHaveBeenCalledWith(new Date(eventsMock.startTime));
    });

    it('update time in required format when category is Last 7 Days but not full time', () => {
      eventsMock['regularTimeFinished'] = false;
      service.setEventStateByStartDate(eventsMock, 'Last 7 Days', false);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });

    it('update time in required format when category is not Last 7 Days', () => {
      eventsMock['regularTimeFinished'] = false;
      service.setEventStateByStartDate(eventsMock, 'My Showdowns', true);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });

    it('update time in required format when category is not Last 7 Days and match is not full time', () => {
      eventsMock['regularTimeFinished'] = false;
      service.setEventStateByStartDate(eventsMock, 'My Showdowns', false);
      expect(timeService.formatByPattern).toHaveBeenCalledWith(new Date(eventsMock.startTime), 'HH:mm');
    });
  });

  describe('#setContestSignPosting - should update display contest details object', () => {
    it('should update display contest details object when data present', () => {
      const contest = CONTEST_MOCK;
      const result = service.setContestSignPosting(contest as any);
      expect(result.entryStake).toEqual('£6+');
      expect(result.totalPrizes).toEqual('£24');
      expect(result.prizePoolSummary).toEqual('12345');
      expect(result.contestSize).toEqual('1000 Total Entries');
      expect(result.prizePoolTotalPrizes).toEqual('234 Total Prizes');
      expect(result.teamsEntries).toEqual('Max 5 entries per user');
      expect(result.firstPlace).toEqual('£10320 To First');
      expect(result.vouchers).toEqual('20 Vouchers');
      expect(result.tickets).toEqual('20 Tickets');
      expect(result.freeBets).toEqual('23 Free Bets');
    });

    it('should update display contest details object when data not present', () => {
      const contest = {
        team: null, size: '', 'prizePool': {
          'cash': null,
          'firstPlace': null,
          'freeBets': null,
          'vouchers': null,
          'summary': null,
          'tickets': null,
          'totalPrizes': null
        },
      };
      const result = service.setContestSignPosting(contest as any);
      expect(result.entryStake).toEqual('');
      expect(result.totalPrizes).toEqual('');
      expect(result.prizePoolSummary).toEqual('');
      expect(result.contestSize).toEqual('');
      expect(result.prizePoolTotalPrizes).toEqual('');
      expect(result.teamsEntries).toEqual('');
      expect(result.firstPlace).toEqual('');
      expect(result.vouchers).toEqual('');
      expect(result.tickets).toEqual('');
      expect(result.freeBets).toEqual('');
    });

    it('should update display contest details object when data present for entriesSize', () => {
      const contest = CONTEST_MOCK as any;
      contest.contestSize = 500;
      const result = service.setContestSignPosting(contest as any);
      expect(result.contestSize).toEqual('500/1000 Entries');
    });
    it('should update display contest details object when data is null for entriesSize', () => {
      const contest = CONTEST_MOCK as any;
      contest.contestSize = null;
      const result = service.setContestSignPosting(contest as any);
      expect(result.contestSize).toEqual('1000 Total Entries');
    });
  });

  describe('#getPrizePoolProperty', () => {
    it('should return empty string when prizePool is null', () => {
      const prizePool = null;
      expect(service['getPrizePoolProperty'](prizePool, 'totalPrizes', 'POUND')).toEqual('');
    });

    it('should return empty string when prizePool property is null', () => {
      const prizePool = {} as any;
      expect(service['getPrizePoolProperty'](prizePool, 'totalPrizes', 'POUND')).toEqual('');
    });
  });

  describe('#getContestProperty', () => {
    it('should return empty string when contestData property is null', () => {
      const contestData = {} as any;
      expect(service['getContestProperty'](contestData, 'teams', 'ENTRIES')).toEqual('');
    });
  });

  describe('#removeResultedContestsFromCategory', () => {
    it('should remove event from My Showdowns by EventId', () => {
      spyOn(service as any, 'pushContestToLast7days');
      const contests = [{
        category: 'MY_SHOWDOWNS',
        contests: [{ eventDetails: { id:'12345' } }]
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(service['pushContestToLast7days']).toHaveBeenCalled();
    });

    it('should remove single event from My Showdowns by EventId', () => {
      const contests = [{
        category: 'MY_SHOWDOWNS',
        categoryName: '',
        contests: [{ eventDetails:{ id:'12345'} }, { eventDetails:{ id:'34567'} }]
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(contests[0].categoryName).toEqual('MY LEADERBOARDS (1)');
      expect(contests[0].contests.length).toEqual(1);
    });

    it('should remove single event from Today by EventId', () => {
      const contests = [{
        category: 'Today',
        categoryName: 'Today',
        contests: [{ eventDetails:{ id:'12345'} }, { eventDetails:{ id:'34567'} }]
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(contests[0].categoryName).toEqual('Today');
    });

    it('should remove event from Today by EventId', () => {
      const contests = [{
        categoryName: 'Today',
        contests: [{ eventDetails:{ id:'12345'} }]
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(contests[0].contests.length).toEqual(0);
    });

    it('should not remove event from 7 days list by EventId', () => {
      const contests = [{
        category: '2021-04-10',
        contests: [{ eventDetails: { id: '12345'} }]
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(contests[0].contests.length).toEqual(1);
    });

    it('should not remove event from 7 days list by EventId', () => {
      spyOn(service as any, 'pushContestToLast7days');
      const contests = [{
        category: '2021-04-10',
        contests: null
      }];
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(service['pushContestToLast7days']).not.toHaveBeenCalled();
      expect(contests[0].contests).toBeNull();
    });

    it('should not call removeResultedContestsFromCategory when contests are null', () => {
      const contests = null;
      spyOn(service as any, 'pushContestToLast7days');
      service.removeResultedContestsFromCategory(contests as any, 12345);
      expect(service['pushContestToLast7days']).not.toHaveBeenCalled();
      expect(contests).toEqual(null);
    });
  });

  describe('#pushContestToLast7days', () => {
    it('should push event to last 7 days list', () => {
      const contestEvents = [{ eventDetails: { id: '12345'} }, { eventDetails: { id:'34567'} }];
      const displayContests = [{
        category: SHOWDOWN_CARDS.LAST7DAYS,
        contests: [{ eventDetails:{ id:'46288' } }]
      }];
      service['pushContestToLast7days'](contestEvents as any, displayContests as any, 12345);
      expect(displayContests[0].contests.length).toEqual(2);
    });

    it('should not push event in last 7 days when event is not found in contests', () => {
      const contestEvents =[{ eventDetails: { id: '12345'} }, { eventDetails: { id:'34567'} }];
      const displayContests = [{
        category: SHOWDOWN_CARDS.LAST7DAYS,
        contests: [{ eventDetails: { id:'46288'} }]
      }];
      service['pushContestToLast7days'](contestEvents as any, displayContests as any, 23848);
      expect(displayContests[0].contests.length).toEqual(1);
    });

    it('should not push event in last 7 days when 7 days section is not present', () => {
      const contestEvents = [{ eventDetails: { id: '12345'} }, { eventDetails: { id:'34567'} }];
      const displayContests = [{
        category: 'Today',
        contests: [{ eventDetails:{id:'46288'}}]
      }];
      service['pushContestToLast7days'](contestEvents as any, displayContests as any, 23848);
      expect(displayContests[0].contests.length).toEqual(1);
    });

    it('should not push event in last 7 days when 7 days section is not present', () => {
      const contestEvents = [{ eventDetails:{id:'12345'} }, { eventDetails:{id:'23848'} }];
      const displayContests = [{
        category: SHOWDOWN_CARDS.LAST7DAYS,
        contests: [{ eventDetails:{id:'46288'} }, { eventDetails: {id:'23848'} }]
      }];
      service['pushContestToLast7days'](contestEvents as any, displayContests as any, 23848);
      expect(displayContests[0].contests.length).toEqual(2);
    });
  });
  describe('#getTeamNameFromEventComments', () => {
    it('should return empty, if no event', () => {
      const event = null;
      const response = service['getTeamNameFromEventComments'](event);
      expect(response).toEqual({ homeTeam: undefined, awayTeam: undefined });
    });
    it('should return empty, if no name in event', () => {
      const event = {} as any;
      const response = service['getTeamNameFromEventComments'](event);
      expect(response).toEqual({ homeTeam: undefined, awayTeam: undefined });
    });
    it('should not return empty, if has event', () => {
      const event = { name:"England vs Scotland",scores: {home: {name: 'England'}, away:{ name:'Scotland' } }} as any;
      const response = service['getTeamNameFromEventComments'](event);
      expect(response).toEqual({ homeTeam: 'England', awayTeam: 'Scotland' });
    });
  });

  describe('#isValidValue', () => {
    it('should return true when value is number', () => {
      expect(service.isValidValue(1)).toEqual(true);
    });
    it('should return true when value is string', () => {
      expect(service.isValidValue('1')).toEqual(true);
    });
    it('should return false when value is undefined', () => {
      expect(service.isValidValue(undefined)).toEqual(false);
    });
    it('should return false when value is null', () => {
      expect(service.isValidValue(null)).toEqual(false);
    });
    it('should return false when value is empty', () => {
      expect(service.isValidValue('')).toEqual(false);
    });
  });

  describe('#getAllShowdownContests', () => {
    it('should call http and return observable', () => {
      const brand = environment.brand;
      const lobbyObj: LobbyData = {
        brand: brand,
        userId: 'M8sha',
        offSet: 240,
        token: 'bppToken'
      };
    service.getAllShowdownContests(brand, 'M8sha', 'bppToken');
    expect(http.post).toHaveBeenCalled();
    });
  });
});
