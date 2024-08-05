import { CARDS_MOCK, CONTEST_MOCK } from '@app/fiveASideShowDown/services/show-down-cards.mock';
import { of, throwError } from 'rxjs';
import {
  FiveASideShowDownLobbyComponent
} from '@app/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { PUBSUB_API, SHOWDOWN_CARDS } from '@app/fiveASideShowDown/constants/constants';
import { T_AND_C } from '@app/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { welcome_mock } from '../fiveASideWelcomeOverlay/fiveaside-welcome-overlay.mock';

describe('ShowDownLobbyComponent', () => {
  let component: FiveASideShowDownLobbyComponent;
  let fiveASideShowDownLobbyService, fiveAsideLiveServeUpdatesSubscribeService,
    userService, changeDetectorRef = null, cmsService;
  let timeService = null;
  let gtmService, pubSubService, device, liveServeService,bonusSuppression;
  let windowRef = null;

  beforeEach(() => {
    userService = {
      userName: 'test-gvc',
      email: 'test@internalgvc.com'
    };
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi
    };
    device = { isDesktop: true };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    liveServeService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({}))
    };
    bonusSuppression = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false)
    };
    timeService = {
      isTodayDate: jasmine.createSpy().and.returnValue(true),
      getOnlyFullDateFormatSuffix: jasmine.createSpy(),
      getFullDateFormatSuffixWithDay: jasmine.createSpy(),
      determineDay: jasmine.createSpy()
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    windowRef = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake(cb => cb()),
        localStorage: {
          clear: jasmine.createSpy('clear'),
          setItem: jasmine.createSpy('setItem'),
          getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    fiveAsideLiveServeUpdatesSubscribeService = {
      createLiveServeChannels: jasmine.createSpy().and.returnValue(['sCLOCK012345678', 'sEVENT012345678']),
      openLiveServeConnectionForUpdates: jasmine.createSpy(),
      unSubscribeLiveServeConnection: jasmine.createSpy(),
    };
    fiveASideShowDownLobbyService = {
      loadAnimation: true,
      addScoresAndClockForEvents: jasmine.createSpy(),
      removeResultedContestsFromCategory: jasmine.createSpy(),
      getAllShowdownContests: jasmine.createSpy().and.returnValue(of({ showdownCards: CARDS_MOCK }))
    };
    cmsService = {
      getTermsAndConditions: jasmine.createSpy('getTermsAndConditions').and.returnValue(of(T_AND_C)),
      getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of(welcome_mock)),
      getCMSRGYconfigData: jasmine.createSpy().and.returnValue(of({}))
    };
    component = new FiveASideShowDownLobbyComponent(fiveASideShowDownLobbyService,
      fiveAsideLiveServeUpdatesSubscribeService,
      userService, gtmService, windowRef, changeDetectorRef, timeService, cmsService, pubSubService, device,
      liveServeService,bonusSuppression);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('constructor', () => {
    it('should create component instance', () => {
      expect(component).toBeTruthy();
    });
  });

  it('#userStatus should return userService.status', () => {
    expect(component.loadAnimation).toEqual(fiveASideShowDownLobbyService.loadAnimation);
  });

  it('footerGATrack', () => {
    const gtmData = {
      eventCategory: '5-A-Side Showdown',
      eventAction: 'click',
      eventLabel: 'T&C',
      location: 'showDownLobby',
    };
    component.footerGATrack();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
  });

  describe('#ngOnInit', () => {
    it('should call fetchAllShowdownContests during ngOnInit', () => {
      component['fetchAllShowdownContests'] = jasmine.createSpy('fetchAllShowdownContests');
      spyOn(component as any, 'postUserLoginTrigger');
      spyOn(component as any, 'removeResultedContestByEventId');
      spyOn(component as any, 'reloadComponentListener');
      component.ngOnInit();
      expect(component['fetchAllShowdownContests']).toHaveBeenCalled();
      expect(component['postUserLoginTrigger']).toHaveBeenCalled();
      expect(component['removeResultedContestByEventId']).toHaveBeenCalled();
      expect(component.termsConditions).not.toBe(null);
    });
    it('should not map cms data, if you get no response', () => {
      spyOn(component as any, 'postUserLoginTrigger');
      spyOn(component as any, 'reloadComponentListener');
      cmsService.getTermsAndConditions.and.returnValue(of(null));
      component.ngOnInit();
      expect(component.termsConditions).toBe(null);
    });
  });

  describe('#showRoleBasedContests', () => {
    it('should show the contest only to a test user if the contest is eligble for test users', () => {
      const contestdata = CONTEST_MOCK;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should show not the contest only to a test user if the contest is eligble for real users', () => {
      const contestdata = CONTEST_MOCK;
      userService.email = 'test@gmail.com';
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(false);
    });
    it('should show not the contest only to a loggedout  user if the contest is eligble for real users', () => {
      const contestdata = CONTEST_MOCK;
      userService.email = null;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(false);
    });
    it('should show not the contest only to a test user if the contest is eligble for real users', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = false;
      contestdata.realAccount = true;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should should not show the contest only to a real user / loggedout  user if the contest is eligble for real users', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = false;
      contestdata.realAccount = true;
      userService.email = 'test@gmail.com';
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should should not show the contest only to a logged out user / loggedout  user if the contest is eligble for real users', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = false;
      contestdata.realAccount = true;
      userService.email = null;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should show the contest  to all users if the contest is eligble for test users and real users ', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = true;
      contestdata.realAccount = true;
      userService.email = null;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should show the contest  to all users if the contest is eligble for test users and real users ', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = true;
      contestdata.realAccount = true;
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
    it('should show the contest  to all users if the contest is eligble for test users and real users ', () => {
      const contestdata = CONTEST_MOCK;
      contestdata.testAccount = true;
      contestdata.realAccount = true;
      userService.email = 'test@gmail.com';
      expect(component['showRoleBasedContests'](contestdata as any)).toBe(true);
    });
  });

  describe('#isTestOrRealUser', () => {
    it('should test if a user is a test user for coral domain', () => {
      const useremail = 'testgvccl@coral.co.uk';
      const testUser = 'testUser';
      expect(component['isTestOrRealUser'](useremail)).toBe(testUser);
    });
    it('should test if a user is a test user for ladbrokes domain', () => {
      const useremail = 'testgvcld@coral.co.uk';
      const testUser = 'testUser';
      expect(component['isTestOrRealUser'](useremail)).toBe(testUser);
    });
    it('should test if a user is a test user for coral domain', () => {
      const useremail = 'test@internalgvc.com';
      const testUser = 'testUser';
      expect(component['isTestOrRealUser'](useremail)).toBe(testUser);
    });
    it('should test if a user is a real user for coral domain', () => {
      const useremail = 'coral@gmail.com';
      const realUser = 'realUser';
      expect(component['isTestOrRealUser'](useremail)).toBe(realUser);
    });
    it('should test if a user is a real user for ladbrokes domain', () => {
      const useremail = 'ladbrokes@gmail.com';
      const realUser = 'realUser';
      expect(component['isTestOrRealUser'](useremail)).toBe(realUser);
    });
  });

  describe('#fetchAllShowdownContests', () => {
    beforeEach(() => {
      spyOn(component as any, 'showSpinner');
      spyOn(component as any, 'hideSpinner');
      spyOn(component as any, 'initShowdownContestData');
      spyOn(component as any, 'getWelcomeOverlayData');
    });

    it('#fetchAllShowdownContests - should call API and fetch contests', () => {
      component['fetchAllShowdownContests']();
      expect(component['showSpinner']).toHaveBeenCalled();
      expect(component['displayContests'] as any).toEqual(jasmine.arrayContaining(CARDS_MOCK));
      expect(component['showSpinner']).toHaveBeenCalled();
      expect(component['initShowdownContestData']).toHaveBeenCalled();
      expect(component['hideSpinner']).toHaveBeenCalled();
    });

    it('#fetchAllShowdownContests - should call API and fetch contests and not to call addScoresAndClockForEvents', () => {
      component['CARDS_MOCK'] = [{ id: '1ab', children: [{ event: '1', player: '1' }] }] as any;
      component['fetchAllShowdownContests']();
      expect(fiveASideShowDownLobbyService.addScoresAndClockForEvents).not.toHaveBeenCalled();
    });

    it('#fetchAllShowdownContests - should not call API and fetch contests when children is missing', () => {
      component['CARDS_MOCK'] = [{ id: '1ab' }] as any;
      component['fetchAllShowdownContests']();
      expect(fiveASideShowDownLobbyService.addScoresAndClockForEvents).not.toHaveBeenCalled();
    });

    it('#fetchAllShowdownContests - should not call API and fetch contests when contest is missing', () => {
      component['CARDS_MOCK'] = [null] as any;
      component['fetchAllShowdownContests']();
      expect(fiveASideShowDownLobbyService.addScoresAndClockForEvents).not.toHaveBeenCalled();
    });

    it('#fetchAllShowdownContests - should call showError when http returns error', () => {
      component.showError = jasmine.createSpy('showError');
      fiveASideShowDownLobbyService.getAllShowdownContests.and.returnValue(throwError({ status: 404 }));
      component['fetchAllShowdownContests']();
      expect(component.showError).toHaveBeenCalled();
    });

    it('#fetchAllShowdownContests - should call hideSpinner when http returns data as null', () => {
      component.hideSpinner = jasmine.createSpy('hideSpinner');
      fiveASideShowDownLobbyService.getAllShowdownContests.and.returnValue(of(null));
      component['fetchAllShowdownContests']();
      expect(component['initShowdownContestData']).not.toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
    });
  });

  describe('#initShowdownContestData', () => {
    beforeEach(() => {
      spyOn(component as any, 'setTutorialPosition');
    });

    it('should not call addScoresAndClockForEvents when events are null', () => {
      spyOn(component as any, 'setLobbyCategoryNames');
      spyOn(component as any, 'getRoleBasedContestsSize');
      component['displayContests'] = [{ id: '1ab', children: [{ event: '1', player: '1', events: null }] }] as any;
      component['initShowdownContestData']();
      expect(component['setLobbyCategoryNames']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not call addScoresAndClockForEvents when children is empty', () => {
      spyOn(component as any, 'setLobbyCategoryNames');
      spyOn(component as any, 'getRoleBasedContestsSize');
      component['displayContests'] = [{ id: '1ab', children: [] }] as any;
      component['initShowdownContestData']();
      expect(component['setLobbyCategoryNames']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not call addScoresAndClockForEvents when children is missing', () => {
      spyOn(component as any, 'setLobbyCategoryNames');
      spyOn(component as any, 'getRoleBasedContestsSize');
      component['displayContests'] = [{ id: '1ab' }] as any;
      component['initShowdownContestData']();
      expect(component['setLobbyCategoryNames']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should call pubSub LOBBY_DATA_RELOADED_COMPLETED', () => {
      component['displayContests'] = [{ id: '1ab', contests: [{ event: '1', player: '1', eventDetails: [{}] }] },
      { id: '2ab', contests: [{ event: '2', player: '2', eventDetails: [{}] }] }] as any;
      component['initShowdownContestData']();
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });

  describe('#getRoleBasedContestsSize', () => {
    it('should return count of contests based on the showRoleContest flag', () => {
      const contests = [{ showRoleContest: true }, { showRoleContest: false }, { showRoleContest: undefined }] as any;
      expect(component['getRoleBasedContestsSize'](contests)).toEqual(1);
    });

    it('should return 0 whenn array is empty', () => {
      const contests = [] as any;
      expect(component['getRoleBasedContestsSize'](contests)).toEqual(0);
    });
  });

  describe('#setLobbyCategoryNames', () => {
    it('should update category MYSHOWDOWNS', () => {
      timeService.isTodayDate.and.returnValue(false);
      const contest = { category: SHOWDOWN_CARDS.MYSHOWDOWNS, categoryName: '', children: [1, 2, 3], displayCount: 3 } as any;
      component['setLobbyCategoryNames'](contest);
      expect(contest.categoryName).toEqual('MY LEADERBOARDS (3)');
    });

    it('should update category LAST7DAYS', () => {
      timeService.isTodayDate.and.returnValue(false);
      const contest = { category: SHOWDOWN_CARDS.LAST7DAYS, categoryName: '', children: [1, 2, 3] } as any;
      component['setLobbyCategoryNames'](contest);
      expect(contest.categoryName).toEqual(SHOWDOWN_CARDS.LAST_7_DAYS);
    });

    it('should update category when isTodayorTomorrow is true', () => {
      spyOn(component as any, 'checkDateIsTodayOrTomorrow').and.returnValue('today');
      const contest = { category: '', categoryName: '' } as any;
      component['setLobbyCategoryNames'](contest);
      expect(contest.categoryName).toEqual(SHOWDOWN_CARDS.DAYS['today']);
    });

    it('should update category in toCheckCategoryOrValidDate true condition', () => {
      spyOn(component as any, 'checkDateIsTodayOrTomorrow').and.returnValue(null);
      component['toCheckCategoryOrValidDate'] = jasmine.createSpy().and.returnValue(true);
      timeService.getFullDateFormatSuffixWithDay.and.returnValue('Friday 25th January');
      const contest = { category: '', categoryName: '', date: '25-01-2019' } as any;
      component['setLobbyCategoryNames'](contest);
      expect(contest.categoryName).toEqual('Friday 25th January');
    });

    it('should update category in toCheckCategoryOrValidDate false condition', () => {
      timeService.isTodayDate.and.returnValue(false);
      component['toCheckCategoryOrValidDate'] = jasmine.createSpy().and.returnValue(false);
      timeService.getFullDateFormatSuffixWithDay.and.returnValue('Friday 25th January');
      const contest = { category: '', categoryName: '', date: '25-01-2019' } as any;
      component['setLobbyCategoryNames'](contest);
      expect(contest.categoryName).toEqual('');
    });
  });

  describe('#checkDateIsTodayOrTomorrow', () => {
    it('should return null if date string is invalid', () => {
      const date = 'abc';
      expect(component['checkDateIsTodayOrTomorrow'](date)).toEqual(null);
    });

    it('should return today if date is today', () => {
      timeService.determineDay.and.returnValue('today');
      const date = '2021-03-31T04:56:41.000Z';
      expect(component['checkDateIsTodayOrTomorrow'](date)).toEqual('today');
    });

    it('should return tomorrow if date is tomorrow', () => {
      timeService.determineDay.and.returnValue('tomorrow');
      const date = '2021-04-01T04:56:41.000Z';
      expect(component['checkDateIsTodayOrTomorrow'](date)).toEqual('tomorrow');
    });

    it('should return null if it is not today or tomorrow', () => {
      timeService.determineDay.and.returnValue('future');
      const date = '2021-04-01T04:56:41.000Z';
      expect(component['checkDateIsTodayOrTomorrow'](date)).toEqual(null);
    });
  });

  it('#postUserLoginTrigger', () => {
    spyOn(component as any, 'fetchAllShowdownContests');
    component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
      if (ch[0] === pubSubService.API.SUCCESSFUL_LOGIN) {
        fn();
      }
    });
    component['postUserLoginTrigger']();
    expect(component['fetchAllShowdownContests']).toHaveBeenCalled();
  });

  describe('#removeResultedContestByEventId', () => {
    it('should call removeResultedContestsFromCategory method when message published', () => {
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED) {
          fn();
        }
      });
      component['removeResultedContestByEventId']();
      expect(fiveASideShowDownLobbyService.removeResultedContestsFromCategory).toHaveBeenCalled();
    });
  });

  describe('#reloadComponentListener', () => {
    it('should call ngOnInit', () => {
      spyOn(component as any, 'ngOnInit');
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.RELOAD_COMPONENTS) {
          fn();
        }
      });
      component['reloadComponentListener']();
      expect(component.ngOnInit).toHaveBeenCalled();
    });
  });

  describe('#toCheckCategoryOrValidDate', () => {
    it('should return true if string is valid date', () => {
      const date = '2021-03-23';
      expect(component['toCheckCategoryOrValidDate'](date)).toEqual(true);
    });

    it('should return false if string is valid date', () => {
      const date = SHOWDOWN_CARDS.TODAY;
      expect(component['toCheckCategoryOrValidDate'](date)).toEqual(false);
    });
  });

  it('#openLiveServConnection should call LiveServe service with channels list', () => {
    component['openLiveServConnection']();
    expect(fiveAsideLiveServeUpdatesSubscribeService.createLiveServeChannels).toHaveBeenCalled();
    expect(fiveAsideLiveServeUpdatesSubscribeService.openLiveServeConnectionForUpdates)
      .toHaveBeenCalledWith(['sCLOCK012345678', 'sEVENT012345678']);
  });

  it('#unSubscribeLiveServConnection should call unsubscribe LiveServe service with channels list', () => {
    component['unSubscribeLiveServConnection']();
    expect(fiveAsideLiveServeUpdatesSubscribeService.createLiveServeChannels).toHaveBeenCalled();
    expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeLiveServeConnection)
      .toHaveBeenCalledWith(['sCLOCK012345678', 'sEVENT012345678']);
  });

  it('#ngOnDestroy should call methods', () => {
    component['unSubscribeLiveServConnection'] = jasmine.createSpy('unSubscribeLiveServConnection');
    component.ngOnDestroy();
    expect(component['unSubscribeLiveServConnection']).toHaveBeenCalled();
  });

  describe('#triggerLobbyTutorial', () => {
    it('should make showOverlay true', () => {
      component['triggerLobbyTutorial']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.showOverlay).toBe(true);
    });
  });

  describe('captureLeftSlideDoneEvent', () => {
    it('captureLeftSlideDoneEvent when timeout triggers when visible is true', () => {
      const event = {
        disabled: true,
        fromState: false,
        toState: true,
      } as any;
      component['loadOverlay'] = jasmine.createSpy('loadOverlay');
      component.captureLeftSlideDoneEvent(event);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 4000);
      expect(fiveASideShowDownLobbyService.loadAnimation).toBe(true);
    });
  });
  describe('loadOverlay', () => {
    beforeEach(() => {
      spyOn(component as any, 'getWelcomeOverlayData');
    });
    it('loadOverlay when timeout triggers when visible is true', () => {
      const event = {
        disabled: true,
        fromState: false,
        toState: true,
      } as any;

      component['loadOverlay'](event, true);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(fiveASideShowDownLobbyService.loadAnimation).toBe(true);
    });
    it('loadOverlay when timeout triggers when visible is false', () => {
      const event = {
        disabled: true,
        fromState: false,
        toState: true,
      } as any;
      component['loadOverlay'](event, false);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(component.showOverlay).toBe(false);
      expect(fiveASideShowDownLobbyService.loadAnimation).toBe(true);
    });
    it('loadOverlay when timeout triggers when tostate is false', () => {
      const event = {
        disabled: true,
        fromState: false,
        toState: false,
      } as any;
      component['loadOverlay'](event, true);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(component.showOverlay).toBe(false);
      expect(fiveASideShowDownLobbyService.loadAnimation).toBe(true);
    });
    it('loadOverlay when timeout triggers when tostate&visible is false', () => {
      const event = {
        disabled: true,
        fromState: false,
        toState: false,
      } as any;
      component['loadOverlay'](event, false);
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
      expect(component.showOverlay).toBe(false);
    });
  });

  describe('#getWelcomeOverlayData', () => {
    it('should not map cms data, if you get no response', () => {
      component.welcomeCard = { overlayEnabled: true } as any;
      spyOn(component, 'initWelcomeOverlay');
      cmsService.getWelcomeOverlay.and.returnValue(of({ welcomeCard: { overlayEnabled: true } }));
      component['getWelcomeOverlayData']();
      expect(component.welcomeCard).not.toBeNull();
    });
    it('should throw error', () => {
      component.welcomeCard = undefined;
      cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
      component['getWelcomeOverlayData']();
      expect(component.welcomeCard).toBeUndefined();
    });
  });

  describe('#initWelcomeOverlay', () => {
    it('should open triggerLobbyTutorial when isDesktop is true', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = false;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when isDesktop is false and isAnimationLoaded is true', () => {
      component.isDesktop = false;
      component.isAnimationLoaded = true;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = false;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when isDesktop is false and isAnimationLoaded is false', () => {
      component.isDesktop = false;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = false;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when displayContests is null', () => {
      component.isDesktop = false;
      component.isAnimationLoaded = false;
      component.displayContests = null;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when displayContests is empty', () => {
      component.isDesktop = false;
      component.isAnimationLoaded = false;
      component.displayContests = [] as any;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when overlayEnabled is false', () => {
      component.isDesktop = false;
      component.isAnimationLoaded = false;
      component.displayContests = [] as any;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](false);
      expect(component.lobbyManualTutorial).toBeFalsy();
    });

    it('should open triggerLobbyTutorial when welcomeOverlaySeen is false', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = false;
      component.isLobbyOverlaySeen = false;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.showOverlay).toEqual(true);
    });

    it('should open triggerLobbyTutorial when welcomeOverlaySeen is true and isLobbyOverlaySeen is true', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = true;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](false);
      expect(component.showOverlay).toEqual(false);
    });

    it('should open triggerLobbyTutorial when welcomeOverlaySeen and isLobbyOverlaySeen is true', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = true;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.showOverlay).toEqual(false);
    });

    it('should open triggerLobbyTutorial when welcomeOverlaySeen is true and isLobbyOverlaySeen is false', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = false;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.showOverlay).toEqual(true);
    });

    it('should open triggerLobbyTutorial when all true', () => {
      component.isDesktop = true;
      component.isAnimationLoaded = false;
      component.displayContests = [1, 2] as any;
      component.welcomeOverlaySeen = true;
      component.isLobbyOverlaySeen = true;
      spyOn(component, 'triggerLobbyTutorial');
      component['initWelcomeOverlay'](true);
      expect(component.showOverlay).toEqual(false);
    });
  });

  describe('#setLobbyTutorialIndex', () => {
    it('should update showTutorialIndex index', () => {
      component.showTutorialIndex = undefined;
      component['setLobbyTutorialIndex'](1);
      expect(component.showTutorialIndex).toEqual(1);
    });
    it('should update showTutorialIndex index', () => {
      component.showTutorialIndex = 3;
      component['setLobbyTutorialIndex'](2);
      expect(component.showTutorialIndex).toEqual(3);
    });
  });

  describe('#setTutorialPosition', () => {
    it('should call setLobbyTutorialIndex', () => {
      spyOn(component as any, 'setLobbyTutorialIndex');
      component['setTutorialPosition'](1, 1);
      expect(component['setLobbyTutorialIndex']).toHaveBeenCalled();
    });
    it('should not call setLobbyTutorialIndex', () => {
      spyOn(component as any, 'setLobbyTutorialIndex');
      component['setTutorialPosition'](0, 1);
      expect(component['setLobbyTutorialIndex']).not.toHaveBeenCalled();
    });
    it('should not call setLobbyTutorialIndex', () => {
      spyOn(component as any, 'setLobbyTutorialIndex');
      component['setTutorialPosition'](undefined, 1);
      expect(component['setLobbyTutorialIndex']).not.toHaveBeenCalled();
    });
  });
});
