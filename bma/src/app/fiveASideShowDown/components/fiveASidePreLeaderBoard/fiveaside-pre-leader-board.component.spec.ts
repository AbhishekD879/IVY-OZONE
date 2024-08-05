import { of, throwError } from 'rxjs';
import {
  FiveASidePreLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import {
  CONTEST_DTO_NULL,
  USER_SHOWDOWN_DATA, USER_SHOWDOWN_DATA_NULL, USER_SHOWDOWN_DATA_NO_DISPLAY
} from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.mock';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { TEAM_COLOR } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveasdie-crest-image.mock';
import { welcome_mock } from '../fiveASideWelcomeOverlay/fiveaside-welcome-overlay.mock';

describe('FiveASidePreLeaderBoardComponent', () => {
  let component: FiveASidePreLeaderBoardComponent;
  let userService, route, leaderBoardService, timeService, localeService, fiveASidePreHeaderService, pubSubService,
  cmsService, windowRef, subscriberService, liveServeService, navigationService;

  beforeEach(() => {
    timeService = {
      countDownTimerForHours: jasmine.createSpy('countDownTimerForHours').and.returnValue({ value: '10:30' } as any),
      getDateTimeFormat: jasmine.createSpy('getDateTimeFormat').and.returnValue('10:30 10th March 2021'),
      getFullDateTimeFormatSufx: jasmine.createSpy('getFullDateTimeForciematSufx').and.returnValue('10:30 10 Mar')
    };
    fiveASidePreHeaderService = {
      checkForMatchDay: jasmine.createSpy('checkForMatchDay').and.returnValue(true),
      getTimeDifference: jasmine.createSpy('getTimeDifference').and.returnValue(1000)
    };
    route = {
      params: of({ id: '602f52152c05212d1b9336bc' }),
      snapshot: {
        params: {
          id: '602f52152c05212d1b9336bc'
        }
      }
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('#flag_round_england')
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: pubSubApi
    };
    userService = {
      status: true,
      username: 'username',
      bppToken: 'bppToken'
    };
    leaderBoardService = {
      getContestInformationById: jasmine.createSpy('getContestInformationById').and.returnValue(of({contest: USER_SHOWDOWN_DATA})),
      hasImageForHomeAway: jasmine.createSpy('hasImageForHomeAway').and.returnValue(true),
      setDefaultTeamColors: jasmine.createSpy('setDefaultTeamColors')
    };
    windowRef = {
      document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({
              parentNode: {}
          } as any),
          getElementById: jasmine.createSpy('querySelector').and.returnValue({
              parentNode: {}
          } as any),
    },
    nativeWindow : {
      localStorage: {
          clear: jasmine.createSpy('clear'),
          setItem: jasmine.createSpy('setItem'),
          getItem: jasmine.createSpy('getItem').and.returnValue(true)
      }
    }};
    subscriberService = {
      createChannels: jasmine.createSpy().and.returnValue(['sCLOCK012345678', 'sEVENT012345678']),
      openLiveServeConnectionForUpdates: jasmine.createSpy('openLiveServeConnectionForUpdates'),
      unSubscribeLiveServeConnection: jasmine.createSpy().and.returnValue(['sCLOCK012345678', 'sEVENT012345678'])
    };
    cmsService = {
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of([TEAM_COLOR])),
      getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of(welcome_mock))
    };
    liveServeService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({}))
    };
    navigationService = {
      openRouterUrl: jasmine.createSpy()
    };
    component = new FiveASidePreLeaderBoardComponent(timeService,
      route, pubSubService, fiveASidePreHeaderService, userService, leaderBoardService, localeService,
      cmsService, windowRef, subscriberService, liveServeService, navigationService);
  });

  describe('constructor', () => {
    it('should create component Instance', () => {
      expect(component).toBeTruthy();
    });
  });

  describe('should call correct methods', () => {
    it('should call correct methods', () => {
      component.ngOnInit = jasmine.createSpy();
      component.ngOnDestroy = jasmine.createSpy();
      component.showSpinner = jasmine.createSpy();
      component['reloadComponent']();
      expect(component.ngOnInit).toHaveBeenCalled();
      expect(component.ngOnDestroy).toHaveBeenCalled();
      expect(component.showSpinner).toHaveBeenCalled();
    });
  });

  it('postLoginTrigger', () => {
    pubSubService.subscribe.and.callFake((a, method, cb) => {
      if (method === 'SUCCESSFUL_LOGIN') {
        spyOn(component as any, 'getContestInformation');
        cb();
        expect(component['getContestInformation']).toHaveBeenCalled();
      }
    });
    component['postLoginTrigger']();
  });
  describe('#ngOnInit', () => {
    it('should call fetch prizepool data  function on init', () => {
      component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
      spyOn(component as any, 'getContestInformation');
      spyOn(component as any, 'postLoginTrigger');
      spyOn(component as any, 'getWelcomeOverlayCMS');
      spyOn(component as any, 'reloadComponentData');
      spyOn(component as any, 'checkForDisplayed').and.returnValue(true);
      component.ngOnInit();
      expect(component['decodeInitialData']).toHaveBeenCalled();
      expect(component['getWelcomeOverlayCMS']).toHaveBeenCalled();
      expect(component['checkForDisplayed']).toHaveBeenCalled();
      expect(component['routeSubscriber']).toBeDefined();
    });

    it('should call fetch prizepool data  function on init visited scenario', () => {
      component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
      spyOn(component as any, 'getContestInformation');
      spyOn(component as any, 'postLoginTrigger');
      spyOn(component as any, 'getWelcomeOverlayCMS');
      spyOn(component as any, 'reloadComponentData');
      spyOn(component as any, 'checkForDisplayed').and.returnValue(false);
      component.ngOnInit();
      expect(component['decodeInitialData']).toHaveBeenCalled();
      expect(component['getWelcomeOverlayCMS']).toHaveBeenCalled();
      expect(component['checkForDisplayed']).toHaveBeenCalled();
      expect(component['routeSubscriber']).toBeDefined();
    });

    it('#ngOnInit', () => {
      route = {
        params: of({})
      };
      pubSubService.subscribe.and.callFake((a, method, cb) => {
        cb(345);
      });
      component['route'] = route;
      spyOn(component as any, 'getContestInformation');
      spyOn(component as any, 'postLoginTrigger');
      spyOn(component as any, 'reloadComponentData');
      component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
      component['eventEntity'] = {id: 123} as any;
      component.ngOnInit();
      expect(component['decodeInitialData']).not.toHaveBeenCalled();
      expect(component['routeSubscriber']).toBeDefined();
    });

    it('should call fetch contest data function on init', () => {
      component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
      pubSubService.subscribe.and.callFake((a, method, cb) => {
          cb(123);
      });
      spyOn(component as any, 'postLoginTrigger');
      spyOn(component as any, 'getWelcomeOverlayCMS');
      spyOn(component as any, 'reloadComponentData');
      spyOn(component as any, 'checkForDisplayed').and.returnValue(true);
      component['eventEntity'] = {id: 123} as any;
      component.ngOnInit();
      expect(component['decodeInitialData']).toHaveBeenCalled();
      expect(component['getWelcomeOverlayCMS']).toHaveBeenCalled();
      expect(component['checkForDisplayed']).toHaveBeenCalled();
      expect(component['routeSubscriber']).toBeDefined();
    });

    it('#ngOnInit page foundations', () => {
      route = {
        params: of({})
      };
      pubSubService.subscribe.and.callFake((a, method, cb) => {
        cb();
      });
      component['route'] = route;
      spyOn(component as any, 'getContestInformation');
      spyOn(component as any, 'postLoginTrigger');
      spyOn(component as any, 'reloadComponentData');
      component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
      component['eventEntity'] = {id: 123} as any;
      component.ngOnInit();
      expect(component['decodeInitialData']).not.toHaveBeenCalled();
      expect(component['routeSubscriber']).toBeDefined();
    });
  });

  describe('#fetchInitialData Scenario', () => {
    beforeEach(() => {
      component.showDown = JSON.parse(JSON.stringify(USER_SHOWDOWN_DATA));
    });
    it('should check the Match Day false', () => {
      fiveASidePreHeaderService.checkForMatchDay.and.returnValue(false);
      component['fetchInitialData']();
      expect(component.dateTime).toEqual('10:30 10th March 2021');
    });
    it('should check the Match Day true', () => {
      fiveASidePreHeaderService.checkForMatchDay.and.returnValue(true);
      spyOn(component as any, 'focusListner');
      component['fetchInitialData']();
      expect(component['focusListner']).toHaveBeenCalled();
      expect(component.clockTime).toEqual({ value: '10:30' } as any);
    });
  });

  describe('#focusHandler Scenario', () => {
    beforeEach(() => {
      component.showDown = JSON.parse(JSON.stringify(USER_SHOWDOWN_DATA));
      windowRef = {
        document: {
            querySelector: jasmine.createSpy('querySelector').and.returnValue({
                parentNode: {}
            } as any),
            getElementById: jasmine.createSpy('querySelector').and.returnValue({
                parentNode: {}
            } as any),
      },
      nativeWindow : {
        localStorage: {
            clear: jasmine.createSpy('clear'),
            setItem: jasmine.createSpy('setItem'),
            getItem: jasmine.createSpy('getItem').and.returnValue('2021-05-21T06:00:00Z')
        }
      }};
    });
    it('should check the Match Day false', () => {
      component['eventEntity'] = USER_SHOWDOWN_DATA.eventDetails;
      fiveASidePreHeaderService.checkForMatchDay.and.returnValue(false);
      component['focusHandler']();
    });
    it('should check the Match Day true', () => {
      component['eventEntity'] = USER_SHOWDOWN_DATA.eventDetails;
      fiveASidePreHeaderService.checkForMatchDay.and.returnValue(true);
      component['focusHandler']();
      expect(component.clockTime).toEqual({ value: '10:30' } as any);
    });
  });

  describe('#fetchInitialData Scenario2', () => {
    beforeEach(() => {
      component.showDown = JSON.parse(JSON.stringify(CONTEST_DTO_NULL));
    });
    it('should check the Match Day false', () => {
      component['fetchInitialData']();
    });
    it('should check the Match Day true', () => {
      component['fetchInitialData']();
    });
  });

  describe('#fetchInitialData Negative Scenario', () => {
    beforeEach(() => {
      component.showDown = JSON.parse(JSON.stringify(USER_SHOWDOWN_DATA_NULL));
    });
    it('should check the negative scenario for contest info', () => {
      component['fetchInitialData']();
    });
  });

  it('should navigate to lobby if display false (Case4: no display)', () => {
    component.showDown = USER_SHOWDOWN_DATA_NO_DISPLAY;
    component['contestId'] = '602f52152c05212d1b9336bc';
    component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
    leaderBoardService.getContestInformationById.and.returnValue(of(USER_SHOWDOWN_DATA_NO_DISPLAY));
    component['getContestInformation']();
    expect(leaderBoardService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component.showDown).not.toBeNull();
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  describe('#ngOnDestroy', () => {
    it('#ngOnDestroy', () => {
      component['routeSubscriber'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['prizesSubscriber'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['contestSubscriber'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['eventEntity'] = {
        id: '123',
      } as any;
      spyOn(component as any, 'removeFocusListner');
      component.ngOnDestroy();
      expect(component['routeSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(component['prizesSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(component['contestSubscriber'].unsubscribe).toHaveBeenCalled();
      expect(component['channels']).toEqual(['sCLOCK012345678', 'sEVENT012345678']);
      expect(component['removeFocusListner']).toHaveBeenCalled();
    });
  });

  it('should get contest information in ngOnInit (Case: LoggedOut)', () => {
    component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
    spyOn(component as any, 'postLoginTrigger');
    spyOn(component as any, 'getWelcomeOverlayCMS');
    spyOn(component as any, 'reloadComponentData');
    spyOn(component as any, 'checkForDisplayed').and.returnValue(true);
    component.ngOnInit();
    expect(component['getWelcomeOverlayCMS']).toHaveBeenCalled();
    expect(component['checkForDisplayed']).toHaveBeenCalled();
    expect(component.showDown).not.toBeNull();
  });

  it('should get contest information in ngOnInit (Case: LogIn) and error', () => {
    component['decodeInitialData'] = jasmine.createSpy('decodeInitialData');
    leaderBoardService.getContestInformationById.and.returnValue(throwError('error'));
    userService.username = undefined;
    userService.bppToken = undefined;
    spyOn(component as any, 'postLoginTrigger');
    spyOn(component as any, 'getWelcomeOverlayCMS');
    spyOn(component as any, 'reloadComponentData');
    spyOn(component as any, 'checkForDisplayed').and.returnValue(true);
    component.ngOnInit();
    expect(component['getWelcomeOverlayCMS']).toHaveBeenCalled();
    expect(component['checkForDisplayed']).toHaveBeenCalled();
    expect(component.showDown).toBeUndefined();
  });

  describe('#getWelcomeOverlayCMS', () => {
    it('should map cms data, if you get response', () => {
      component['getWelcomeOverlayCMS']();
      expect(component.preEventData).not.toBeNull();
    });
    it('should not map cms data, if you get actual response', () => {
      cmsService.getWelcomeOverlay.and.returnValue(of(welcome_mock));
      component['getWelcomeOverlayCMS']();
      expect(component.preEventData).toEqual(welcome_mock);
    });
    it('should not map cms data, if you get no response', () => {
      cmsService.getWelcomeOverlay.and.returnValue(of(null));
      component['getWelcomeOverlayCMS']();
      expect(component.preEventData).toEqual(null);
    });
    it('should not map cms data, if you get error', () => {
      cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
      component['getWelcomeOverlayCMS']();
      expect(component.preEventData).toBeUndefined();
    });
  });

describe('#checkForDisplayed', () => {
  beforeEach(() => {
    windowRef = {
      nativeWindow : {
        localStorage: {
            getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    component = new FiveASidePreLeaderBoardComponent(timeService,
      route, pubSubService, fiveASidePreHeaderService, userService, leaderBoardService, localeService,
      cmsService, windowRef, subscriberService, liveServeService, navigationService);
  });
  it('should showdown true preevent false', () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(true);
      component['checkForDisplayed']();
  });

  it('should showdown true preevent false', () => {
    windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(false);
    component['checkForDisplayed']();
});
});

describe('#checkForWelcome', () => {
  beforeEach(() => {
    windowRef = {
      nativeWindow : {
        localStorage: {
            getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    component = new FiveASidePreLeaderBoardComponent(timeService,
      route, pubSubService, fiveASidePreHeaderService, userService, leaderBoardService, localeService,
      cmsService, windowRef, subscriberService, liveServeService, navigationService);
  });
  it('should showdown true preevent false', () => {
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(true);
      component['checkForWelcome']();
  });

  it('should showdown true preevent false', () => {
    windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(false);
    component['checkForWelcome']();
});
});

describe('focusListner', () => {
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
          addEventListener: jasmine.createSpy('addEventListener')
      }
    };
    component = new FiveASidePreLeaderBoardComponent(timeService,
      route, pubSubService, fiveASidePreHeaderService, userService, leaderBoardService, localeService,
      cmsService, windowRef, subscriberService, liveServeService, navigationService);
  });
  it('should call focusListner method', ()=> {
    component['focusListner']();
    expect(windowRef.nativeWindow.addEventListener).toHaveBeenCalled();
  });
});

describe('removeFocusListner', () => {
  beforeEach(() => {
    windowRef = {
      nativeWindow: {
          removeEventListener: jasmine.createSpy('removeEventListener')
      }
    };
    component = new FiveASidePreLeaderBoardComponent(timeService,
      route, pubSubService, fiveASidePreHeaderService, userService, leaderBoardService, localeService,
      cmsService, windowRef, subscriberService, liveServeService, navigationService);
  });
  it('should call removeListeners method present in the ngOnDestroy ', ()=> {
    component['removeFocusListner']();
    expect(windowRef.nativeWindow.removeEventListener).toHaveBeenCalled();
  });
});
  describe('#reloadComponentData', () => {
    it('should reload component whenever page is left idle', () => {
      pubSubService.subscribe.and.callFake((a, b, c) => {
        c();
      });
      spyOn(component as any ,'showSpinner');
      spyOn(component as any ,'ngOnInit');
      spyOn(component as any ,'ngOnDestroy');
      component['reloadComponentData']();
      expect(component.showSpinner).toHaveBeenCalled();
    });
  });
  describe('decodeInitialData', () => {
    it('decodeInitialData with my entries', () => {
      component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.showDown = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component['contestId'] = '602f52152c05212d1b9336bc';
      component.prizePoolData = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
      component['eventEntity'] = {id: 123} as any;
      component.homeName = 'arsenal';
      component.awayName = 'madrid';
      spyOn(component as any, 'fetchInitialData');
      component['decodeInitialData']();
      expect(component.showDown).not.toBeNull();
      expect(component['fetchInitialData']).toHaveBeenCalled();
      expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['arsenal','madrid'],'16');
    });

    it('decodeInitialData with null scenario', () => {
      component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component.showDown = USER_SHOWDOWN_DATA_NO_DISPLAY;
      component['contestId'] = '602f52152c05212d1b9336bc';
      component.prizePoolData = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
      component['eventEntity'] = {id: 123} as any;
      component.homeName = 'arsenal';
      component.awayName = 'madrid';
      spyOn(component as any, 'fetchInitialData');
      spyOn(component as any, 'showError');
      cmsService.getTeamsColors.and.returnValue(throwError('error'));
      component['decodeInitialData']();
      expect(component.showError).toHaveBeenCalled();
    });
  });
});

