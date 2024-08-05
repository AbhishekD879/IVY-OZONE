import { FiveASidePostLeaderBoardComponent } from './fiveaside-post-leader-board.component';
import {
  eventDetails, USER_SHOWDOWN_DATA, USER_SHOWDOWN_DATA_NO_DISPLAY
} from '@app/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.mock';
import { of as observableOf, of, throwError } from 'rxjs';
import { TEAM_COLOR } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveasdie-crest-image.mock';
import { LEADERBOARD_ENTRIES_TOP500, MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import { IHeaderArea } from '@app/fiveASideShowDown/models/entry-information';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('FiveASidePostLeaderBoardComponent', () => {
  let component: FiveASidePostLeaderBoardComponent;
  let windowRefService, route, userService, navigationService,
    showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService;
  beforeEach(() => {
    userService = {
      status: true,
      username: 'username',
      bppToken: 'bppToken'
    };
    deviceService = { isMobile: true };
    windowRefService = {
      nativeWindow: {
        document: {
          querySelector: jasmine.createSpy('querySelector'),
          addEventListener: jasmine.createSpy('addEventListener')
        }
      }
    };
    rendererService = {
      renderer: jasmine.createSpy('renderer')
    };
    showDownService = {
      getContestInformationById: jasmine.createSpy('getContestInformationById').and.returnValue(observableOf({contest: USER_SHOWDOWN_DATA})),
      hasImageForHomeAway: jasmine.createSpy('hasImageForHomeAway').and.returnValue(true),
      setDefaultTeamColors: jasmine.createSpy('setDefaultTeamColors'),
      formFlagName: jasmine.createSpy('formFlagName').and.returnValue('flag_round_scotland'),
      getContestPrizeById: jasmine.createSpy('getContestPrizeById').and.returnValue(observableOf({} as any))
    };
    navigationService = {
      openRouterUrl: jasmine.createSpy()
    };

    route = {
      snapshot: {
        params: {
          id: '602f52152c05212d1b9336bc'
        }
      }
    };

    fiveASideShowDownLobbyService = {
      addScoresAndClockForEvents: jasmine.createSpy('addScoresAndClockForEvents')
    };

    cmsService = {
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(observableOf([TEAM_COLOR]))
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
      showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
      navigationService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnDestroy', () => {
    it('should call removeScrollListeners method present in the ngOnDestroy ', () => {
      spyOn(component as any, 'removeScrollListeners');
      component['routeSubscriber'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();
      expect(component['removeScrollListeners']).toHaveBeenCalled();
      expect(component['routeSubscriber'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('#initScoresFromEventComments', () => {
    it('should call all required methods1', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { score: '1', name: 'Arsenal' }, away: { score: '2', name: 'Manchester' }
      } as any;
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toEqual('1');
      expect(component.headerAreaInfo.awayScore).toEqual('2');
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods1', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { score: '1', name: 'Arsenal' }, away: { score: '2', name: 'Manchester' }
      } as any;
      component.headerAreaInfo = {
      } as any;
      component.event.name = null;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Arsenal');
      expect(component.headerAreaInfo.awayName).toEqual('Manchester');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toEqual('1');
      expect(component.headerAreaInfo.awayScore).toEqual('2');
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods2', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { }, away: { }
      } as any;
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toBeUndefined();
      expect(component.headerAreaInfo.awayScore).toBeUndefined();
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods3', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { score: '', name: '' }, away: { score: '', name: '' }
      } as any;
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toBe('');
      expect(component.headerAreaInfo.awayScore).toBe('');
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods4', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { score: '', name: '' }, away: { score: '', name: '' }
      } as any;
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toBe('');
      expect(component.headerAreaInfo.awayScore).toBe('');
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods5', () => {
      component.event = { ...eventDetails } as any;
      component.event['scores'] = {
        home: { score: '1', name:'Arsenal' }, away: { score: '2', name:'Manchester' }
    } as any;
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toEqual('1');
      expect(component.headerAreaInfo.awayScore).toEqual('2');
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
    it('should call all required methods6', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = { home: {}, away: {}};
      component.headerAreaInfo = {
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.headerAreaInfo.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.headerAreaInfo.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.headerAreaInfo.homeScore).toBeUndefined();
      expect(component.headerAreaInfo.awayScore).toBeUndefined();
      expect(showDownService.formFlagName).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.headerAreaInfo.isScoresAvailable).toBeTruthy();
    });
  });

  it('initContestDetails with checkCommentaryToBeCalledForEvent false', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(false);
    component.postcontestInfo = USER_SHOWDOWN_DATA;
    component.headerAreaInfo = {} as any;
    component['initContestDetails']();
    expect(component.event).toEqual(component['events']);
    expect(component['events']).toEqual(component.postcontestInfo.eventDetails);
  });

  it('initContestDetails with checkCommentaryToBeCalledForEvent true', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(true);
    spyOn(component as any, 'initScoresFromEventComments');
    component.postcontestInfo = USER_SHOWDOWN_DATA;
    component['initContestDetails']();
    expect(component.event).toEqual(component['events']);
    expect(component['events']).toEqual(component.postcontestInfo.eventDetails);
  });

  it(' isMatchCompletedAndResulted0', () => {
    const events = {};
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.isResulted).toBeUndefined();
    expect(component.event.regularTimeFinished).toBeUndefined();
  });

  it(' isMatchCompletedAndResulted1', () => {
    const events = {'regularTimeFinished': true };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.regularTimeFinished).toBeTruthy();
  });
  it(' isMatchCompletedAndResulted2', () => {
    const events = { 'isResulted': true, 'regularTimeFinished': false };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.regularTimeFinished).toBeFalsy();
  });
  it(' isMatchCompletedAndResulted3', () => {
    const events = { 'isResulted': false, 'regularTimeFinished': true };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.regularTimeFinished).toBeTruthy();
  });
  it(' isMatchCompletedAndResulted4', () => {
    const events = { 'isResulted': false, 'regularTimeFinished': false };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.regularTimeFinished).toBeFalsy();
  });

  it(' isTeamScoresAvailable', () => {
    const homescore = '1';
    const awayscore = '1';
    component.headerAreaInfo = {
    } as any;
    component.headerAreaInfo.homeScore = homescore;
    component.headerAreaInfo.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(true);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = '1';
    const awayscore = null;
    component.headerAreaInfo = {
    } as any;
    component.headerAreaInfo.homeScore = homescore;
    component.headerAreaInfo.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = null;
    const awayscore = '1';
    component.headerAreaInfo = {
    } as any;
    component.headerAreaInfo.homeScore = homescore;
    component.headerAreaInfo.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = null;
    const awayscore = null;
    component.headerAreaInfo = {
    } as any;
    component.headerAreaInfo.homeScore = homescore;
    component.headerAreaInfo.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });

  it('should get contest information in ngOnInit (Case1: LoggedOut)', () => {
    spyOn(component as any, 'showSpinner');
    spyOn(component as any, 'decodeInitialData');
    component['contestId'] = '602f52152c05212d1b9336bc';
    component.headerAreaInfo = {} as any;
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component.postcontestInfo).not.toBeNull();
    expect(component.showSpinner).toHaveBeenCalled();
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  describe('scrollHandler', () => {
    beforeEach(() => {
      windowRefService = {
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({}),
        },
        nativeWindow: {
          pageYOffset: 200,
        }
      };
      component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
        showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
        navigationService);
    });
    it('scroll only for mobile only', () => {
      deviceService.isMobile = false;
      component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
        showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
        navigationService);
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });
    it('scroll Handler when pageYOffset is 200', () => {
      windowRefService.nativeWindow.pageYOffset = 200;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('scroll Handler when pageYOffset is 100', () => {
      windowRefService.nativeWindow.pageYOffset = 200;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('scroll Handler when pageYOffset is 80', () => {
      windowRefService.nativeWindow.pageYOffset = 80;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(2);
    });
    it('scroll Handler when pageYOffset is 70', () => {
      windowRefService.nativeWindow.pageYOffset = 70;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(2);
    });
    it('scroll Handler when pageYOffset is 70', () => {
      windowRefService.nativeWindow.pageYOffset = 40;
      component.offSetPValue = 20;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('headerareascorll should not be shown when the pageYoffset is greater than the over-all-height element', () => {
      windowRefService = {
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({ offsetHeight: 50 }),
        },
        nativeWindow: {
          pageYOffset: 1020,
        }
      };
      component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
        showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
        navigationService);
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.offSetPValue = 20;
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).toHaveBeenCalled();
    });
    it('should not call setstyle if slideconent', () => {
      windowRefService.nativeWindow.pageYOffset = 120;
      component.offSetPValue = 20;
      component.slideContent = { offsetHeight: 1020 } as any;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalledTimes(1);
    });
  });

  describe('#checkCommentaryToBeCalledForEvent', () => {
    it('should return false when clock is null and rest are present', () => {
      const event = { clock: null, comments: {} } as any;
      component.isNoCommentaryAvailable = true;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });
    it('should return false when comments is null and rest are present', () => {
      const event = { clock: {}, comments: null } as any;
      component.isNoCommentaryAvailable = true;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });

    it('should return false when clock is null and rest are present', () => {
      const event = { clock: null, comments: {} } as any;
      component.isNoCommentaryAvailable = false;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });

    it('should return false when comments is null and rest are present', () => {
      const event = { clock: {}, comments: null } as any;
      component.isNoCommentaryAvailable = false;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });
    it('should return false when isNoCommentaryAvailable is false', () => {
      const event = { clock: {}, comments: {} } as any;
      component.isNoCommentaryAvailable = false;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });

    it('should return false when isNoCommentaryAvailable is true', () => {
      const event = { clock: {}, comments: {} } as any;
      component.isNoCommentaryAvailable = true;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });

    it('should return false when clock is null and rest are present', () => {
      const event = { clock: null, comments: null } as any;
      component.isNoCommentaryAvailable = false;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeTruthy();
    });

    it('should return false when clock is null and isNoCommentaryAvailable is true', () => {
      const event = { clock: null, comments: null } as any;
      component.isNoCommentaryAvailable = true;
      const result = component['checkCommentaryToBeCalledForEvent'](event);
      expect(result).toBeFalsy();
    });
  });

  describe('addScorllListner', () => {
    beforeEach(() => {
      windowRefService = {
        nativeWindow: {
          document: {
            addEventListener: jasmine.createSpy('addEventListener')
          }
        }
      };
      component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
        showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
        navigationService);
    });
    it('should call setScrollListeners method present in the ngOnDestroy ', () => {
      component['setScrollListeners']();
      expect(windowRefService.nativeWindow.document.addEventListener).toHaveBeenCalled();
    });
  });

  describe('removeScrollListeners', () => {
    beforeEach(() => {
      windowRefService = {
        nativeWindow: {
          document: {
            removeEventListener: jasmine.createSpy('removeEventListener')
          }
        }
      };
      component = new FiveASidePostLeaderBoardComponent(windowRefService, route, userService,
        showDownService, fiveASideShowDownLobbyService, rendererService, cmsService, deviceService, gtmService, pubSubService,
        navigationService);
    });
    it('should call removeListeners method present in the ngOnDestroy ', () => {
      component['removeScrollListeners']();
      expect(windowRefService.nativeWindow.document.removeEventListener).toHaveBeenCalled();
    });
  });

  it('showOverlayFunction', () => {
    component.showOverlay = true;
    component.showOverlayFunction();
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('prizePool', () => {
    it('prizePool', () => {
      component.prizePool();
      expect(component.prize).not.toBeUndefined();
    });
  });

  describe('initialLbrEntries', () => {
    it('initialLbrEntries with user entries', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      spyOn(component as any, 'validateLeaderBoardRecords');
      windowRefService.nativeWindow.clearInterval = jasmine.createSpy('clearInterval');
      component.leaderboardEntires = MY_ENTRIES_LIST;
      component.initialLbrEntries(LEADERBOARD_ENTRIES_TOP500.leaderboardEntries as any);
      expect(component.leaderboardEntires.length).not.toBe(0);
    });
    it('initialLbrEntries without user entries', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component.leaderboardEntires = [];
      component.initialLbrEntries([]);
      expect(component.leaderboardEntires.length).toBe(0);
    });
  });
  describe('validateLeaderBoardRecords', () => {
    it('should set length of intial data for more than 100', () => {
      expect(component['validateLeaderBoardRecords'](100)).toEqual('100');
    });
    it('should set length of intial data for less than 100', () => {
      expect(component['validateLeaderBoardRecords'](2)).toEqual('2');
    });
    it('when intial data is empty', () => {
      expect(component['validateLeaderBoardRecords'](0)).toEqual('0');
    });
  });
  it('ngOnInit', () => {
    component.headerAreaInfo = {} as IHeaderArea;
    spyOn(component as any, 'setScrollListeners');
    spyOn(component as any, 'prizePool');
    spyOn(component as any, 'postLoginTrigger');
    spyOn(component as any, 'decodeInitialData');
    component.ngOnInit();
    expect(component['setScrollListeners']).toHaveBeenCalled();
    expect(component['decodeInitialData']).toHaveBeenCalled();
    expect(component['contestId']).toEqual('602f52152c05212d1b9336bc');
    expect(component['postLoginTrigger']).toHaveBeenCalled();
  });

  it('should navigate to lobby if display false (Case4: no display)', () => {
    component['contestId'] = '602f52152c05212d1b9336bc';
    component.postcontestInfo = USER_SHOWDOWN_DATA_NO_DISPLAY;
    showDownService.getContestInformationById.and.returnValue(of(USER_SHOWDOWN_DATA_NO_DISPLAY));
    spyOn(component as any, 'decodeInitialData');
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component.postcontestInfo).not.toBeNull();
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  it('postLoginTrigger', () => {
    pubSubService.subscribe.and.callFake((a, method, cb) => {
      if (method === 'SUCCESSFUL_LOGIN') {
        spyOn(component as any, 'fetchInitialDataOfEvent');
        cb();
        expect(component['fetchInitialDataOfEvent']).toHaveBeenCalled();
      }
    });
    component['postLoginTrigger']();
  });

  describe('decodeInitialData', () => {
    it('decodeInitialData with my entries', () => {
      component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.postcontestInfo = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.prize = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
      component.myEntriesList = MY_ENTRIES_LIST;
      component.leaderboardEntires = MY_ENTRIES_LIST;
      component.headerAreaInfo = {} as any;
      component.headerAreaInfo.homeName = 'arsenal';
      component.headerAreaInfo.awayName = 'madrid';
      spyOn(component as any, 'initialLbrEntries');
      spyOn(component as any, 'initContestDetails');
      component['decodeInitialData']();
      expect(component.postcontestInfo).not.toBeNull();
      expect(component.initialLbrEntries).toHaveBeenCalled();
      expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['arsenal','madrid'],'16');
    });

    it('decodeInitialData with error in cms call', () => {
      component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.postcontestInfo = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.prize = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
      component.myEntriesList = MY_ENTRIES_LIST;
      component.leaderboardEntires = MY_ENTRIES_LIST;
      component.headerAreaInfo = {} as any;
      component.headerAreaInfo.homeName = null;
      component.headerAreaInfo.awayName = null;
      cmsService.getTeamsColors.and.returnValue(throwError('error'));
      spyOn(component as any, 'initialLbrEntries');
      spyOn(component as any, 'initContestDetails');
      spyOn(component as any, 'showError');
      component['decodeInitialData']();
      expect(component.showError).toHaveBeenCalled();
    });
  });
});
