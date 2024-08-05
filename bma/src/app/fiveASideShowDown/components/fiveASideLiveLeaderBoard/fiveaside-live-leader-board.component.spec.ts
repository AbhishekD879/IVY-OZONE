import { FiveASideLiveLeaderBoardComponent } from './fiveaside-live-leader-board.component';
import {
  eventDetails, sCLOCKUpdate, sEVENTupdate, USER_SHOWDOWN_DATA, EVENTS_DETAILS_COMMENTS, USER_SHOWDOWN_DATA_NO_DISPLAY
} from '@app/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of, throwError } from 'rxjs';
import { TEAM_COLOR } from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveasdie-crest-image.mock';
import {
  MY_ENTRIES_LIST, LEADERBOARD_MYENTRIES,
  LEADERBOARD_MYENTRIES_MYMOCK_10, LEADERBOARD_MYENTRIES_500_GR, LEADERBOARD_DATA_ALL
} from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import { LIVE_OVERLAY,PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';

describe('FiveASideLiveLeaderBoardComponent', () => {
  let component: FiveASideLiveLeaderBoardComponent;
  let windowRefService, rendererService,
    showDownService, fiveAsideLiveServeUpdatesSubscribeService, router, fiveAsideLiveServeUpdatesService, pubSub, coreToolsService,
    route, fiveASideShowDownLobbyService, userService, localeService, cmsService, gtmService, changeDetectorRef,
    liveServeService, deviceService, awsService, liveEventClockProviderService, timeSyncService, navigationService;
  beforeEach(() => {
    userService = {
      status: true,
      username: 'username',
      bppToken: 'bppToken'
    };
    fiveAsideLiveServeUpdatesSubscribeService = {
      unSubscribeShowDownChannels: jasmine.createSpy('unSubscribeShowDownChannels'),
      openLiveServeInitialDataEntryInformation: jasmine.createSpy('openLiveServeInitialDataEntryInformation'),
      createChannels: jasmine.createSpy().and.returnValue(['sCLOCK012345678', 'sEVENT012345678']),
      openLiveServeConnectionForUpdates: jasmine.createSpy('openLiveServeConnectionForUpdates'),
      unSubscribeLiveServeConnection: jasmine.createSpy().and.returnValue(['sCLOCK012345678', 'sEVENT012345678'])
    };
    windowRefService = {
      nativeWindow: {
        clearInterval: jasmine.createSpy('clearInterval'),
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        document: {
          querySelector: jasmine.createSpy('querySelector'),
          addEventListener: jasmine.createSpy('addEventListener')
        },
        localStorage: {
          clear: jasmine.createSpy('clear'),
          setItem: jasmine.createSpy('setItem'),
          getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy()
    };
    rendererService = {
      renderer: jasmine.createSpy('renderer')
    };
    showDownService = {
      getContestInformationById: jasmine.createSpy('getContestInformationById').and.returnValue(of(USER_SHOWDOWN_DATA)),
      hasImageForHomeAway: jasmine.createSpy('hasImageForHomeAway').and.returnValue(true),
      setDefaultTeamColors: jasmine.createSpy('setDefaultTeamColors')
    };
    router = {
      navigate: jasmine.createSpy('navigate').and.returnValue([]),
    };
    route = {
      snapshot: {
        params: {
          id: '602f52152c05212d1b9336bc'
        }
      }
    };
    fiveAsideLiveServeUpdatesService = {
      updateEventComments: jasmine.createSpy(),
      eventClockUpdate: jasmine.createSpy(),
      updateEventLiveData: jasmine.createSpy(),
      initEventStarted: jasmine.createSpy(),
    };
    fiveASideShowDownLobbyService = {
      addScoresAndClockForEvents: jasmine.createSpy('addScoresAndClockForEvents')
    };
    coreToolsService = {
      uuid: jasmine.createSpy('uuid')
    };
    pubSub = {
      subscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
      API: pubSubApi,
      unsubscribe: jasmine.createSpy()
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('#flag_round_england')
    };
    cmsService = {
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of([TEAM_COLOR])),
      getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of({})),
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
        limit: 10
      } as any))
    };
    liveServeService = {
      connect: jasmine.createSpy('connect').and.returnValue(of({})),
      disconnect: jasmine.createSpy('disconnect'),
      closeConnection: jasmine.createSpy('closeConnection')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    deviceService = { isMobile: true };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    liveEventClockProviderService = {
      create: jasmine.createSpy().and.returnValue({})
    };
    timeSyncService = {
      getTimeDelta: jasmine.createSpy()
    };
    navigationService = {
      openRouterUrl: jasmine.createSpy()
    };
    component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService,
      showDownService, fiveAsideLiveServeUpdatesSubscribeService, pubSub,
      fiveAsideLiveServeUpdatesService, coreToolsService, route, fiveASideShowDownLobbyService,
      userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
       liveEventClockProviderService,timeSyncService, navigationService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOninit', () => {
    it('should call all the methods present in the ngOnInit ', () => {
      spyOn(component as any, 'setScrollListeners');
      spyOn(component as any, 'decodeInitialData');
      spyOn(component as any, 'openLiveServConnection');
      spyOn(component as any, 'getInitialLeaderBoardData');
      spyOn(component as any, 'getInitialLiveOverlayData');
      component['getLiveupdatesubscription'] = jasmine.createSpy('getLiveupdatesubscription');
      component.ngOnInit();
      expect(component['setScrollListeners']).toHaveBeenCalled();
      expect(component['decodeInitialData']).toHaveBeenCalled();
      expect(component['getLiveupdatesubscription']).toHaveBeenCalled();
    });
  });

  describe('#reloadComponent', () => {
    it('should be called for the reloadComponent', () => {
      pubSub.subscribe.and.callFake((a, b, c) => {
        c();
      });
      spyOn(component as any ,'ngOnInit');
      spyOn(component as any ,'ngOnDestroy');
      component['reloadComponent']();
      expect(component.dataLoading).toBe(true);
    });
  });

  describe('initialLbrEntries', () => {
    it('initialLbrEntries with user entries', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      const myEntries = { update: LEADERBOARD_MYENTRIES_MYMOCK_10 };
      pubSub.subscribe.and.callFake((a, method, cb) => {
        spyOn(component as any, 'myEntriesFilter');
        cb(myEntries);
        expect(component['myEntriesFilter']).toHaveBeenCalled();
      });
      spyOn(component as any, 'validateLeaderBoardRecords');
      component['myUserEntries'] = MY_ENTRIES_LIST;
      component.initialLbrEntries(LEADERBOARD_DATA_ALL as any);
      expect(component['myUserEntries'].length).not.toBe(0);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('initialLbrEntries without user entries', () => {
      component['initialAllRecords'] = [];
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component['myUserEntries'] = [];
      component['initialAllRecords'] = [];
      component.initialLbrEntries([] as any);
      expect(component['myUserEntries'].length).toBe(0);
    });
    it('initialLbrEntries with user entries', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      spyOn(component as any, 'myEntriesFilter');
      component['myUserEntries'] = MY_ENTRIES_LIST;
      component.initialLbrEntries(LEADERBOARD_DATA_ALL as any);
      expect(component['myUserEntries'].length).not.toBe(0);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('initialLbrEntries with user entries 0 check', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component['myUserEntries'] = [];
      component.initialLbrEntries(LEADERBOARD_DATA_ALL as any);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('initialLbrEntries - check initialAllRecords has data', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component['myUserEntries'] = [];
      component.initialLbrEntries(LEADERBOARD_DATA_ALL as any);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('initialLbrEntries - check initialAllRecords when empty', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component['myUserEntries'] = [];
      const leaderboardAllData = {...LEADERBOARD_DATA_ALL};
      leaderboardAllData.leaderboard = undefined;
      leaderboardAllData.leaderboardUserEntries = undefined;
      leaderboardAllData.myEntries = undefined;
      component.initialLbrEntries(leaderboardAllData as any);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
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

  describe('initialEntrySummary', () => {
    it('initialEntrySummary', () => {
      component.initialEntrySummary(MY_ENTRIES_LIST);
      expect(component.myEntries.length).not.toBe(0);
    });
    it('initialEntrySummary for non login scenario', () => {
      spyOn(component as any, 'myEntriesFilter');
      component['isLoginUpdate'] = true;
      component.initialEntrySummary(MY_ENTRIES_LIST);
      expect(component['myEntriesFilter']).toHaveBeenCalled();
      expect(component.myEntries.length).not.toBe(0);
    });
  });

  describe('getInitialLeaderBoardData', () => {
    it('getInitialLeaderBoardData logged out scenario', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      spyOn(component as any, 'unSubscribeChannel');
      component['contestId'] = '12342344';
      userService.username = null;
      component.getInitialLeaderBoardData();
      expect(component['leaderboardChannel']).toBe('LDRBRD::602f52152c05212d1b9336bc::0');
      expect(fiveAsideLiveServeUpdatesSubscribeService.openLiveServeInitialDataEntryInformation).toHaveBeenCalled();
    });

    it('getInitialLeaderBoardData', () => {
      userService.username = 'username';
      userService.bppToken = 'bppToken';
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      spyOn(component as any, 'unSubscribeChannel');
      component['contestId'] = '12342344';
      component.getInitialLeaderBoardData();
      expect(component['leaderboardChannel']).toBe('LDRBRD::602f52152c05212d1b9336bc::username::bppToken');
      expect(fiveAsideLiveServeUpdatesSubscribeService.openLiveServeInitialDataEntryInformation).toHaveBeenCalled();
    });
  });

  describe('#leaderboardUpdateHandler', () => {
    const originalMock = [{
      'id': '1',
      'index': 0,
      'contestId': '60520915caf74d3428154ba4',
      'userId': '1',
      'betId': 'O/189716734/0001870',
      'stake': '5',
      'priceNum': '11',
      'priceDen': '1',
      'voided': false,
      'overallProgressPct': 20,
      'winningamount': 10,
      'rank': 1,
      'gifts': 'freebet',
      '_class': 'com.entain.oxygen.showdown.model.Entry',
    }];

    it('should call initialLbrEntries method if initialRecordsCopy has 0 entries', () => {
      const data = LEADERBOARD_DATA_ALL as any;
      component.initialRecordsCopy = [];
      spyOn(component as any, 'initialLbrEntries');
      component.leaderboardUpdateHandler(data);
      expect(component['initialLbrEntries']).toHaveBeenCalled();
    });

    it('should not call shuffle method if initialRecordsCopy is undefined', () => {
      const data = LEADERBOARD_DATA_ALL as any;
      component.initialRecordsCopy = undefined;
      spyOn(component as any, 'initialLbrEntries');
      component.leaderboardUpdateHandler(data);
      expect(component['initialLbrEntries']).toHaveBeenCalled();
    });

    it('should call shuffle method if initialRecordsCopy data present', () => {
      const data = LEADERBOARD_DATA_ALL as any;
      data.ertFlag = true;
      component.initialRecordsCopy = originalMock;
      spyOn(component as any, 'shuffle');
      component.leaderboardUpdateHandler(data);
      expect(component['shuffle']).toHaveBeenCalled();
    });

    it('should call publish when my entries present', () => {
      const data = LEADERBOARD_DATA_ALL as any;
      component.initialRecordsCopy = originalMock;
      spyOn(component as any, 'shuffle');
      component.leaderboardUpdateHandler(data);
      expect(pubSub.publish).toHaveBeenCalled();
    });
    it('should not call publish when my entries are empty', () => {
      const data = {myEntries : []} as any;
      component.initialRecordsCopy = originalMock;
      spyOn(component as any, 'shuffle');
      component.leaderboardUpdateHandler(data);
      expect(pubSub.publish).not.toHaveBeenCalled();
    });
    it('should not call publish when my entries are empty', () => {
      const data = {myEntries : undefined} as any;
      component.initialRecordsCopy = originalMock;
      spyOn(component as any, 'shuffle');
      component.leaderboardUpdateHandler(data);
      expect(pubSub.publish).not.toHaveBeenCalled();
    });
  });

  it('loginTrigger', () => {
    pubSub.subscribe.and.callFake((a, method, cb) => {
      cb();
    });
    spyOn(component as any, 'unSubscribeChannel');
    spyOn(component as any, 'getInitialLeaderBoardData');
    component['contestId'] = '602f52152c05212d1b9336bc';
    component['loginTrigger']();
    expect(pubSub.publish).toHaveBeenCalled();
    expect(component['leaderboardChannel']).toBe('LDRBRD::602f52152c05212d1b9336bc::0');
    expect(component.getInitialLeaderBoardData).toHaveBeenCalled();
  });
  describe('deltaRecordUpdatesCallBack', () => {
    it('should clear set interval when no of repeatitions matched', () => {
      const myEntries = { update: LEADERBOARD_MYENTRIES_MYMOCK_10 };
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component.initialRecordsCopy = LEADERBOARD_DATA_ALL.leaderboard;
      spyOn(component as any, 'checkIfRecordExist');
      component['deltaRecordUpdatesCallBack'](() => { }, 100, 1);
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('should not clear set interval when no of repeatitions matched', () => {
      windowRefService.nativeWindow.setInterval = jasmine.createSpy('setInterval').and.callFake((callback) => {
        callback && callback();
      });
      component['deltaRecordUpdatesCallBack'](() => { }, 100, 5);
      expect(windowRefService.nativeWindow.clearInterval).not.toHaveBeenCalled();
    });
  });

  describe('#myEntriesFilter', () => {
    it('should be called the feature config with data', () => {
      component['myUserEntries'] = LEADERBOARD_MYENTRIES_500_GR;
      component['myEntriesFilter']();
      pubSub.subscribe.and.callFake((a, method, cb) => {
        cb();
      });
      expect(pubSub.publish).toHaveBeenCalled();
    });
  });

  describe('shuffle', () => {
    it('check for id present within 500 records with same index', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      component.componentId = '123456';
      const originalMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      const deltaMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'prizes': []
      }];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      pubSub.subscribe.and.callFake((a, b, cb) => cb({ update: originalMock }));
      component['initialAllRecords'] = originalMock;
      component.initialRecordsCopy = originalMock;
      component.shuffle(LEADERBOARD_DATA_ALL as any);
      expect(component.changeOrder).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('check for id present within 500 records with different indexes', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      component.componentId = '123456';
      const originalMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      const deltaMock = [{
        'id': '1',
        'index': 1,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'prizes':[]
      }];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      pubSub.subscribe.and.callFake((a, b, cb) => cb({ update: originalMock }));
      component.initialRecordsCopy = originalMock;
      component['initialAllRecords'] = originalMock;
      component.shuffle(LEADERBOARD_DATA_ALL as any);
      expect(component.changeOrder).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();

    });
    it('check for id not present within 500 records with same indexes', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      const originalMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      const deltaMock = [{
        'id': '2',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      },
      {
        'id': '2',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '2',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      component.initialRecordsCopy = originalMock;
      component['initialAllRecords'] = originalMock;
      component.shuffle(LEADERBOARD_DATA_ALL as any);
      expect(component.changeOrder).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('check for id not present within 500 records with different indexes', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      const originalMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      const deltaMock = [{
        'id': '2',
        'index': 1,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      },
      {
        'id': '2',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '2',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      component.initialRecordsCopy = originalMock;
      component['initialAllRecords'] = originalMock;
      component.shuffle(LEADERBOARD_DATA_ALL as any);
      expect(component.changeOrder).toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('check for id not present within 500 records with different indexes and index not present', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      const originalMock = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      const deltaMock = [{
        'id': '2',
        'index': undefined,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      },
      {
        'id': '2',
        'index': undefined,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '2',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
        '_class': 'com.entain.oxygen.showdown.model.Entry',
      }];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      const leaderboardAllData = LEADERBOARD_DATA_ALL as any;
      leaderboardAllData.leaderboard = deltaMock;
      component.initialRecordsCopy = originalMock;
      component['initialAllRecords'] = originalMock;
      component.shuffle(leaderboardAllData as any);
      expect(component.changeOrder).not.toHaveBeenCalled();
    });
    it('check for initial records and final delta records length is eaual or not', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      const deltaMock = [];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      component['initialAllRecords'] = [];
      const data = LEADERBOARD_DATA_ALL as any;
      data.ertFlag = true;
      component.shuffle(LEADERBOARD_DATA_ALL as any);
      expect(component.changeOrder).not.toHaveBeenCalled();
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalled();
    });
    it('check for initialization of myentries in updated leaderboard entries list', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      const deltaMock = [];
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      component['initialAllRecords'] = [];
      const data = { ...LEADERBOARD_DATA_ALL } as any;
      data.myEntries = undefined;
      component.shuffle(data as any);
      expect(component['myUserEntries']).toEqual([]);
      expect(component['myEntries']).toEqual([]);
    });
    it('check for initialization of leaderboardUserEntries in updated leaderboard entries list', () => {
      spyOn(component as any, 'changeOrder');
      spyOn(component as any, 'initDeltaTime');
      component['deltaRecordUpdatesCallBack'] = jasmine.createSpy().and.callFake((a, b, c) => {
        a();
      });
      component['initialAllRecords'] = [];
      const data = { ...LEADERBOARD_DATA_ALL } as any;
      data.leaderboardUserEntries = undefined;
      component.shuffle(data as any);
      expect(component['userEntries']).toEqual([]);
    });
  });

  describe('initDeltaTime', () => {
    it('check for initial delta count > 50', () => {
      component['updatedLeaderBoardEntries'].length = 100;
      const deltaTime = component['initDeltaTime']();
      expect(deltaTime).toEqual(100);
    });
  });
    it('check for initial delta count < 50', () => {
      component['updatedLeaderBoardEntries'].length = 40;
      const deltaTime = component['initDeltaTime']();
      expect(deltaTime).toEqual(25);
    });

  describe('changeOrder', () => {
    it('should check for both ids are same', () => {
      const previuosIndex = 0, updatedIndex = 0;
      component.initialRecordsCopy = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }];
      const deltaMock = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }] as any;
      component.changeOrder(previuosIndex, updatedIndex, deltaMock);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.initialRecordsCopy.length).not.toBe(0);
    });
    it('should check for both ids are not same', () => {
      const previuosIndex = 0, updatedIndex = 1;
      component.initialRecordsCopy = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      },
      {
        'id': '2',
        'index': 1,
        'rankedIndex': 1,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }];
      component.changeOrder(previuosIndex, updatedIndex);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
      expect(component.initialRecordsCopy.length).not.toBe(0);
    });
    it('should check for both ids are same and previous index is undefined', () => {
      const previuosIndex = undefined, updatedIndex = 0;
      component.initialRecordsCopy = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }];
      const deltaMock = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }] as any;
      component.changeOrder(previuosIndex, updatedIndex, deltaMock);
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.initialRecordsCopy.length).not.toBe(0);
    });
    it('should check for both ids are same and updated index undefined', () => {
      const previuosIndex = 0, updatedIndex = undefined;
      component.initialRecordsCopy = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }];
      const deltaMock = [{
        'id': '1',
        'index': 0,
        'rankedIndex': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'gifts': 'freebet',
      }] as any;
      component.changeOrder(previuosIndex, updatedIndex, deltaMock);
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
      expect(component.initialRecordsCopy.length).not.toBe(0);
    });
  });

  describe('initialEntrySummary', () => {
    it('initialEntrySummary', () => {
      component.initialEntrySummary(LEADERBOARD_MYENTRIES as any);
      expect(component.myEntries.length).not.toBe(0);
    });
  });


  describe('ngOnDestroy', () => {
    it('should call removeScrollListeners method present in the ngOnDestroy ', () => {
      spyOn(component as any, 'unsubscribeForLiveServeConnection');
    });
    it('should not call unsubscribe if subscription does not exist', () => {
      component['leaderbaordLimitSubscription'] = null;
      component['unsubscribeForLiveServeConnection'] = jasmine.createSpy();
      component['removeScrollListeners'] = jasmine.createSpy();
      component.ngOnDestroy();
      expect(component['unsubscribeForLiveServeConnection']).toHaveBeenCalled();
      expect(component['removeScrollListeners']).toHaveBeenCalled();
      expect(component['leaderbaordLimitSubscription']).toBeNull();
    });
    it('should call unsubscribe if subscription exist', () => {
      component['leaderbaordLimitSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['removeScrollListeners'] = jasmine.createSpy();
      component.ngOnDestroy();
      expect(component['removeScrollListeners']).toHaveBeenCalled();
      expect(component['leaderbaordLimitSubscription'].unsubscribe).toHaveBeenCalled();
    });
    it('should call unsubscribe if subscription exist', () => {
      component['leaderbaordLimitSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      spyOn(component as any, 'ngOnInit');
      component['removeScrollListeners'] = jasmine.createSpy();
      component.ngOnDestroy();
      expect(component['removeScrollListeners']).toHaveBeenCalled();
      expect(component['leaderbaordLimitSubscription'].unsubscribe).toHaveBeenCalled();
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
      component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService,
        showDownService, fiveAsideLiveServeUpdatesSubscribeService, pubSub,
        fiveAsideLiveServeUpdatesService, coreToolsService, route, fiveASideShowDownLobbyService,
        userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
        liveEventClockProviderService,timeSyncService, navigationService);
    });
    it('should call removeListeners method present in the ngOnDestroy ', () => {
      component['removeScrollListeners']();
      expect(windowRefService.nativeWindow.document.removeEventListener).toHaveBeenCalled();
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
      component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService,
        showDownService, fiveAsideLiveServeUpdatesSubscribeService, pubSub,
        fiveAsideLiveServeUpdatesService, coreToolsService, route, fiveASideShowDownLobbyService,
        userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
        liveEventClockProviderService,timeSyncService, navigationService);
    });
    it('should call setScrollListeners method present in the ngOnDestroy ', () => {
      component['setScrollListeners']();
      expect(windowRefService.nativeWindow.document.addEventListener).toHaveBeenCalled();
    });
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
      component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService, showDownService,
        fiveAsideLiveServeUpdatesSubscribeService,
        fiveAsideLiveServeUpdatesService, coreToolsService,
        pubSub, route, fiveASideShowDownLobbyService,
        userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
        liveEventClockProviderService,timeSyncService, navigationService);
    });
    it('scroll only for mobile only',()=> {
      deviceService.isMobile = false ;
      component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService,
        showDownService, fiveAsideLiveServeUpdatesSubscribeService, pubSub,
        fiveAsideLiveServeUpdatesService, coreToolsService, route, fiveASideShowDownLobbyService,
        userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
        liveEventClockProviderService,timeSyncService, navigationService);
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component['scrollHandler']();
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
    });
    it('scroll Handler when pageYOffset is 200', () => {
      windowRefService.nativeWindow.pageYOffset = 200;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('scroll Handler when pageYOffset is 100', () => {
      windowRefService.nativeWindow.pageYOffset = 200;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('scroll Handler when pageYOffset is 80', () => {
      windowRefService.nativeWindow.pageYOffset = 80;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(2);
    });
    it('scroll Handler when pageYOffset is 70', () => {
      windowRefService.nativeWindow.pageYOffset = 70;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(2);
    });
    it('scroll Handler when pageYOffset is 70', () => {
      windowRefService.nativeWindow.pageYOffset = 40;
      component.offSetPValue = 20;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalledTimes(3);
    });
    it('headerareascorll should not be shown when the pageYoffset is greater than the over-all-height element', () => {
      windowRefService = {
        document: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({offsetHeight: 50}),
        },
        nativeWindow: {
          pageYOffset: 1020,
        }
      };
      component = new FiveASideLiveLeaderBoardComponent(windowRefService, rendererService, showDownService,
        fiveAsideLiveServeUpdatesSubscribeService,
        fiveAsideLiveServeUpdatesService, coreToolsService,
        pubSub, route, fiveASideShowDownLobbyService,
        userService, localeService, cmsService, gtmService, changeDetectorRef, liveServeService, deviceService, awsService,
        liveEventClockProviderService,timeSyncService, navigationService);
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.offSetPValue = 20;
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).toHaveBeenCalled();
    });
    it('should not call setstyle if slideconent', () => {
      windowRefService.nativeWindow.pageYOffset = 120;
      component.offSetPValue = 20;
      component.slideContent= { offsetHeight: 1020 } as  any;
      rendererService.renderer.setStyle = jasmine.createSpy('setStyle').and.returnValue({});
      component.scrollHandler();
      expect(rendererService.renderer.setStyle).not.toHaveBeenCalledTimes(1);
    });
  });

  it(' isMatchCompletedAndResulted0', () => {
    const events = {};
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.regularTimeFinished).toBeUndefined();
  });

  describe('#updateEventCommentaryAvailability', () => {
    it('should update isNoCommentaryAvailable as true', () => {
      component.isNoCommentaryAvailable = false;
      const event = { started: true, clock: null, comments: null } as any;
      component['updateEventCommentaryAvailability'](event);
      expect(component.isNoCommentaryAvailable).toBeTruthy();
    });

    it('should update isNoCommentaryAvailable as false', () => {
      component.isNoCommentaryAvailable = false;
      const event = null;
      component['updateEventCommentaryAvailability'](event);
      expect(component.isNoCommentaryAvailable).toBeFalsy();
    });

    it('should update isNoCommentaryAvailable as false', () => {
      component.isNoCommentaryAvailable = false;
      const event = { started: false, clock: null, comments: null } as any;
      component['updateEventCommentaryAvailability'](event);
      expect(component.isNoCommentaryAvailable).toBeFalsy();
    });
    it('should update isNoCommentaryAvailable as false', () => {
      component.isNoCommentaryAvailable = false;
      const event = { started: true, clock: {}, comments: null } as any;
      component['updateEventCommentaryAvailability'](event);
      expect(component.isNoCommentaryAvailable).toBeFalsy();
    });
    it('should update isNoCommentaryAvailable as false', () => {
      component.isNoCommentaryAvailable = false;
      const event = { started: true, clock: {}, comments: {} } as any;
      component['updateEventCommentaryAvailability'](event);
      expect(component.isNoCommentaryAvailable).toBeFalsy();
    });
  });

  it(' isMatchCompletedAndResulted1', () => {
    const events = { 'isResulted': true, 'isFinished': true };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.isResulted).toBeTruthy();
  });
  it(' isMatchCompletedAndResulted2', () => {
    const events = { 'isResulted': true, 'isFinished': false };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.isResulted).toBeTruthy();
  });
  it(' isMatchCompletedAndResulted3', () => {
    const events = { 'isResulted': false, 'isFinished': true };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.isResulted).toBeFalsy();
  });
  it(' isMatchCompletedAndResulted4', () => {
    const events = { 'isResulted': false, 'isFinished': false };
    component.event = events as any;
    component.isMatchCompletedAndResulted();
    expect(component.event.isResulted).toBeFalsy();
  });

  it(' isTeamScoresAvailable', () => {
    const homescore = '1';
    const awayscore = '1';
    component.homeScore = homescore;
    component.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(true);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = '1';
    const awayscore = null;
    component.homeScore = homescore;
    component.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = null;
    const awayscore = '1';
    component.homeScore = homescore;
    component.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });
  it(' isTeamScoresAvailable', () => {
    const homescore = null;
    const awayscore = null;
    component.homeScore = homescore;
    component.awayScore = awayscore;
    const result = component.isTeamScoresAvailable();
    expect(result).toBe(false);
  });

  it(' setEventLiveStatus', () => {
    const events = {};
    component.event = events as any;
    component.setEventLiveStatus();
    expect(component.eventIsLive).toBeFalsy();
  });

  it(' setEventLiveStatus1', () => {
    const events = { 'regularTimeFinished': false, 'started': true };
    component.event = events as any;
    component.setEventLiveStatus();
    expect(component.eventIsLive).toBeTruthy();
  });

  it(' setEventLiveStatus2', () => {
    const events = { 'regularTimeFinished': true, 'started': true };
    component.event = events as any;
    component.setEventLiveStatus();
    expect(component.eventIsLive).toBeFalsy();
  });

  it(' setEventLiveStatus3', () => {
    const events = { 'regularTimeFinished': false, 'started': false };
    component.event = events as any;
    component.setEventLiveStatus();
    expect(component.eventIsLive).toBeFalsy();
  });

  it(' setEventLiveStatus4', () => {
    const events = { 'regularTimeFinished': true, 'started': false };
    component.event = events as any;
    component.setEventLiveStatus();
    expect(component.eventIsLive).toBeFalsy();
  });

  describe('#getLiveupdatesubscription SHOWDOWN_LIVE_SCORE_UPDATE subscription', () => {
    let update;
    beforeEach(() => {
      spyOn(component as any, 'createClockUpdate');
      update = {
        id: 232341790,
        payload: {
          scores: {}
        }
      } as any;
      component.event = { ...eventDetails } as any;
      component['pubSub'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE) {
          fn(update);
        }
      });
    });

    it('should update scores when all conditions are met', () => {
      update = {
        id: 232341790,
        payload: {
          scores: { home: { score: 1 }, away: { score: 2 } }
        }
      } as any;
      spyOn(component as any, 'isTeamScoresAvailable');
      component['getLiveupdatesubscription']();
      expect(component.isTeamScoresAvailable).toHaveBeenCalled();
    });

    it('should not update scores if not the same event', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update.id = 1000;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if payload scores is null', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update.payload = {scores : null};
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if away is not present', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update.payload = {scores : {home : {score : 1 }}};
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if home is not present', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update.payload = {scores : {home : {away : 1 }}};
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if payload is null', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update.payload = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if update is null', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      update = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });

    it('should not update scores if event id is null', () => {
      spyOn(component as any, 'initScoresFromEventComments');
      component.event.id = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
    });
  });

  describe('#getLiveupdatesubscription SHOWDOWN_LIVE_CLOCK_UPDATE subscription', () => {
    let update;
    beforeEach(() => {
      spyOn(component as any, 'createClockUpdate');
      update = { ...sCLOCKUpdate } as any;
      component.event = { ...eventDetails } as any;
      component['pubSub'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE) {
          fn(update);
        }
      });
    });

    it('should update clock when all conditions are met', () => {
      spyOn(component as any, 'onClockUpdate');
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).toHaveBeenCalledWith(update.payload, component.event);
      expect(component.onClockUpdate).toHaveBeenCalled();
      expect(component['createClockUpdate']).toHaveBeenCalled();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should not update clock if not the same event', () => {
      update.id = 1000;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
    });

    it('should not update clock if payload is null', () => {
      update.payload = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
    });

    it('should not update clock if update is null', () => {
      update = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
    });

    it('should not update clock if event id is null', () => {
      component.event.id = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
    });
  });

  describe('#getLiveupdatesubscription SHOWDOWN_LIVE_EVENT_UPDATE subscription', () => {
    let update;
    beforeEach(() => {
      update = sEVENTupdate;
      component.event = { ...eventDetails } as any;
      component['pubSub'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE) {
          fn(update);
        }
      });
    });

    it('should update event when all conditions are met', () => {
      spyOn(component as any, 'onClockUpdate');
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).toHaveBeenCalledWith(component.event, update);
      expect(component.onClockUpdate).toHaveBeenCalled();
    });

    it('should not update event if not the same event', () => {
      update.id = 1000;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
    });

    it('should not update event if payload is null', () => {
      update.payload = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
    });

    it('should not update event if update is null', () => {
      update = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
    });

    it('should not update event if event id is null', () => {
      component.event.id = null;
      component['getLiveupdatesubscription']();
      expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
    });
  });

  it('#ngOnDestroy - should call methods', () => {
    component['unsubscribeForLiveServeConnection'] = jasmine.createSpy();
    component['removeScrollListeners'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(component['unsubscribeForLiveServeConnection']).toHaveBeenCalled();
  });

  it('#openLiveServConnection should call LiveServe service with channels list', () => {
    component['openLiveServConnection']();
    expect(fiveAsideLiveServeUpdatesSubscribeService.createChannels).toHaveBeenCalled();
    expect(fiveAsideLiveServeUpdatesSubscribeService.openLiveServeConnectionForUpdates)
      .toHaveBeenCalledWith(['sCLOCK012345678', 'sEVENT012345678']);
  });

  it('#unSubscribeLiveServConnection should call unsubscribe LiveServe service with channels list', () => {
    component['unsubscribeForLiveServeConnection']();
    expect(fiveAsideLiveServeUpdatesSubscribeService.createChannels).toHaveBeenCalled();
    expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeLiveServeConnection)
      .toHaveBeenCalledWith(['sCLOCK012345678', 'sEVENT012345678']);
  });

  it('onClockUpdate', () => {
    spyOn(component as any, 'isHalftime').and.returnValue(true);
    spyOn(component as any, 'isFulltime').and.returnValue(true);
    component.onClockUpdate();
    expect(component['isHalftime']).toHaveBeenCalledWith(component.event);
    expect(component['isFulltime']).toHaveBeenCalledWith(component.event);
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
  it('formFlagName', () => {
    const name = 'Scotland';
    const result = component['formFlagName'](name);
    expect(result).toBe('#flag_round_england');
  });

  describe('#initScoresFromEventComments', () => {
    it('should call all required methods1', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = {
          home: { score: '1', name: 'Jeonbuk Hyundai Motors' }, away: { score: '2', name: 'Gangwon' }
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods1', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = {
          home: { score: '1', name: 'Jeonbuk Hyundai Motors' }, away: { score: '1', name: 'Gangwon' }
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods2', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = {
          home: {}, away: {}
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component.homeScore).toBe('0');
      expect(component.awayScore).toBe('0');
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods3', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = {
          home: { name: '', score: '' }, away: { name: '', score: '' }
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods4', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores = {
          home: { name: '', score: '' }, away: { name: '', score: '' }
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods5', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores= {
          home: { score: '1', name: 'india' }, away: { score: '2', name: 'england' }
      } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component.homeName).toEqual('Jeonbuk Hyundai Motors');
      expect(component.awayName).toEqual('Gangwon');
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
    it('should call all required methods6', () => {
      component.event = { ...eventDetails } as any;
      component.event.scores= {
        home: { }, away: { }
    } as any;
      component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
      component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
      component['formFlagName'] = jasmine.createSpy().and.returnValue('flag_round_scotland');
      component['isHalftime'] = jasmine.createSpy().and.returnValue(true);
      component['initScoresFromEventComments']();
      expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
      expect(component['formFlagName']).toHaveBeenCalledTimes(2);
      expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
      expect(component.isScoresAvailable).toBeTruthy();
      expect(component['isHalftime']).toHaveBeenCalled();
    });
  });

  it('isHalftime', () => {
    component.event = { clock: { matchTime: 'HT' } } as any;
    const result = component['isHalftime'](component.event);
    expect(result).toEqual(true);
  });

  it('isHalftime', () => {
    component.event = { clock: { matchTime: 'FT' } } as any;
    const result = component['isHalftime'](component.event);
    expect(result).toEqual(false);
  });

  it('isFulltime', () => {
    component.event = { ...EVENTS_DETAILS_COMMENTS } as any;
    const result = component['isFulltime'](component.event);
    expect(result).toEqual(false);
  });

  it('isFulltime', () => {
    component.event = { clock: { matchTime: 'FT' } } as any;
    const result = component['isFulltime'](component.event);
    expect(result).toEqual(true);
  });

  it('should get contest information in ngOnInit (Case1: LoggedOut)', () => {
    spyOn(component as any, 'decodeInitialData');
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'initContestDetails');
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  it('should get contest information in ngOnInit (Case2: LoggedOut)', () => {
    spyOn(component as any, 'decodeInitialData');
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(true);
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  it('should get contest information in ngOnInit (Case3: LoggedOut)', () => {
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'decodeInitialData');
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(false);
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  it('should navigate to lobby if display false (Case4: no display)', () => {
    spyOn(component as any, 'decodeInitialData');
    component.contestInfo = USER_SHOWDOWN_DATA_NO_DISPLAY;
    showDownService.getContestInformationById.and.returnValue(of(USER_SHOWDOWN_DATA_NO_DISPLAY));
    component['fetchInitialDataOfEvent']();
    expect(showDownService.getContestInformationById).toHaveBeenCalledWith('602f52152c05212d1b9336bc', 'username', 'bppToken');
    expect(component.contestInfo).not.toBeNull();
    expect(component['decodeInitialData']).toHaveBeenCalled();
  });

  it('initContestDetails with checkCommentaryToBeCalledForEvent false', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(false);
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'getInitialLeaderBoardData');
    spyOn(component as any, 'getInitialLiveOverlayData');
    spyOn(component as any, 'unsubscribeForLiveServeConnection');
    component.contestInfo = USER_SHOWDOWN_DATA;
    component['initContestDetails']();
    expect(component.eventId).toEqual(USER_SHOWDOWN_DATA.eventDetails.id);
    expect(component.event).toEqual(component.events);
    expect(component.events).toEqual(component.contestInfo.eventDetails);
  });

  it('initContestDetails with checkCommentaryToBeCalledForEvent true', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(true);
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'getInitialLeaderBoardData');
    spyOn(component as any, 'getInitialLiveOverlayData');
    spyOn(component as any, 'unsubscribeForLiveServeConnection');
    component.contestInfo = USER_SHOWDOWN_DATA;
    component['initContestDetails']();
    expect(component.eventId).toEqual(USER_SHOWDOWN_DATA.eventDetails.id);
    expect(component.event).toEqual(component.events);
    expect(component.events).toEqual(component.contestInfo.eventDetails);
    expect(component.eventArray).toEqual(['1722516']);
  });

  it('initContestDetails with clockdata', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(true);
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'getInitialLeaderBoardData');
    spyOn(component as any, 'getInitialLiveOverlayData');
    spyOn(component as any, 'unsubscribeForLiveServeConnection');
    spyOn(component as any, 'createClockForEventFromInit');

    component.contestInfo = USER_SHOWDOWN_DATA;
    component.contestInfo.eventDetails.clockData = {ev_id:1};
    component['initContestDetails']();
    expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).toHaveBeenCalledWith(component.contestInfo.eventDetails.clockData, component.event);
    expect(component['createClockForEventFromInit']).toHaveBeenCalled();
    expect(component.eventId).toEqual(USER_SHOWDOWN_DATA.eventDetails.id);
  });

  it('initContestDetails without clockdata', () => {
    spyOn(component as any, 'checkCommentaryToBeCalledForEvent').and.returnValue(true);
    spyOn(component as any, 'initScoresFromEventComments');
    spyOn(component as any, 'updateEventCommentaryAvailability');
    spyOn(component as any, 'setEventLiveStatus');
    spyOn(component as any, 'openLiveServConnection');
    spyOn(component as any, 'getInitialLeaderBoardData');
    spyOn(component as any, 'getInitialLiveOverlayData');
    spyOn(component as any, 'unsubscribeForLiveServeConnection');
    spyOn(component as any, 'createClockForEventFromInit');

    component.contestInfo = USER_SHOWDOWN_DATA;
    component.contestInfo.eventDetails.clockData = null;
    component['initContestDetails']();
    expect(component['createClockForEventFromInit']).not.toHaveBeenCalled();
    expect(component.eventId).toEqual(USER_SHOWDOWN_DATA.eventDetails.id);
  });
  it('should show Overlay ', () => {
    component.showOverlayFunction();
    expect(component.showOverlay).toBeTruthy();
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('#initWelcomeOverlay', () => {
    it('should set liveManualTutorial as false', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return true;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return false;
        }
      });
      component['initWelcomeOverlay'](true);
      expect(component.liveManualTutorial).toBeFalsy();
    });
    it('should set liveManualTutorial as true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return true;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return true;
        }
      });
      component['liveManualTutorial'] = true;
      component['initWelcomeOverlay'](true);
      expect(component.liveManualTutorial).toBeTruthy();
    });
    it('should set showLiveOverlay as true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return false;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return false;
        }
      });
      component['liveManualTutorial'] = true;
      component['initWelcomeOverlay'](true);
      expect(component.showLiveOverlay).toBeTruthy();
    });
    it('should not set showLiveOverlay as true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return false;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return false;
        }
      });
      component['showLiveOverlay'] = false;
      component['initWelcomeOverlay'](false);
      expect(component.showLiveOverlay).toBeFalsy();
    });

    it('should set liveManualTutorial as false', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return false;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return true;
        }
      });
      component['showLiveOverlay'] = false;
      component['initWelcomeOverlay'](true);
      expect(component.showLiveOverlay).toBeTruthy();
    });
  });

  describe('#triggerLiveTutorial', () => {
    it('should call initWelcomeOverlay', () => {
      spyOn(component as any, 'initWelcomeOverlay');
      component.showLiveOverlay = false;
      component['triggerLiveTutorial']();
      expect(component['initWelcomeOverlay']).toHaveBeenCalled();
    });
    it('should throw error', () => {
      component.welcomeCard = undefined;
      cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
      component['triggerLiveTutorial']();
      expect(component.welcomeCard).toBeUndefined();
    });
  });

  describe('#getInitialLiveOverlayData', () => {
    it('should set welcomeCard data', () => {
      component['getInitialLiveOverlayData']();
      expect(component.welcomeCard).not.toBeUndefined();
    });
    it('should throw error', () => {
      component.welcomeCard = undefined;
      cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
      component['getInitialLiveOverlayData']();
      expect(component.welcomeCard).toBeUndefined();
    });
  });

  describe('#getLiveOverlayData', () => {
    beforeEach(() => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return null;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return null;
        }
      });
    });
    it('should call CMS when all conditions are met', () => {
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).toHaveBeenCalled();
    });
    it('should throw error', () => {
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).toHaveBeenCalled();
    });
    it('should not call CMS when isOverlayLoaded is true', () => {
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = true;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when isOverlayLoaded is true', () => {
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = true;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when isLeaderboardLoaded is false', () => {
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = false;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when isMyEntriesLoaded is false', () => {
      component['isMyEntriesLoaded'] = false;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when liveOverlaySeen is true', () => {
      component['isMyEntriesLoaded'] = false;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when liveOverlaySeen and welcomeOverlaySeen are true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return 'true';
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return 'true';
        }
      });
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).not.toHaveBeenCalled();
    });
    it('should not call CMS when liveOverlaySeen is true and welcomeOverlaySeen is null', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return 'true';
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return null;
        }
      });
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).toHaveBeenCalled();
    });
    it('should not call CMS when liveOverlaySeen is null and welcomeOverlaySeen is true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return null;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return null;
        }
      });
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).toHaveBeenCalled();
    });
    it('should not call CMS when liveOverlaySeen is null and welcomeOverlaySeen is true', () => {
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('getItem').and.callFake((callback) => {
        if (callback === LIVE_OVERLAY.OVERLAY) {
          return null;
        } else if (callback === LIVE_OVERLAY.WELCOME_OVERLAY) {
          return 'true';
        }
      });
      component['isMyEntriesLoaded'] = true;
      component['isLeaderboardLoaded'] = true;
      component['isOverlayLoaded'] = false;
      component['getLiveOverlayData']();
      expect(cmsService.getWelcomeOverlay).toHaveBeenCalled();
    });
  });

  describe('#unSubscribeChannel', () => {
    it('should unsubscribe showdown channel when channel is available', () => {
      component['unSubscribeChannel'](null, () => {});
      expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
    });
    it('should unsubscribe showdown channel when channel is available', () => {
      component['unSubscribeChannel']('1234', () => {});
      expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
    });
  });
  describe('addAWSLog', () => {
    it('should push data AWS', () => {
      component['addAWSLog']([{id: 1}] as any);
      expect(awsService.addAction).toHaveBeenCalled();
    });
    it('should not push data to AWS', () => {
      component['addAWSLog'](null);
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
  });

  describe('#createClockUpdate', () => {
    it('should add the clock to event', () => {
        component.event = { clock: undefined, started: true } as any;
        const update = { id: 123, seconds: '1' } as any;
        component['createClockUpdate'](update);
        expect(component.event.clock).not.toBeUndefined();
    });
    it('should not call liveEventClockProviderService', () => {
        component.event = { clock: {}, started: true } as any;
        const update = { id: 123, seconds: '1' } as any;
        component['createClockUpdate'](update);
        expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });
});

  describe('#checkIfRecordExist', () => {
    it('should return false if no updated records', () => {
      component['updatedLeaderBoardEntries'] = [];
      const result = component.checkIfRecordExist("1");
      expect(result).toBe(true);
    });
    it('should return true if record found in updated array', () => {
      component['updatedLeaderBoardEntries'] = [{
        'id': '1',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'prizes': []
      }];
      const result = component.checkIfRecordExist("1");
      expect(result).toBe(true);
    });
    it('should return false if record not found in updated array', () => {
      component['updatedLeaderBoardEntries'] = [{
        'id': '2',
        'index': 0,
        'contestId': '60520915caf74d3428154ba4',
        'userId': '1',
        'betId': 'O/189716734/0001870',
        'stake': '5',
        'priceNum': '11',
        'priceDen': '1',
        'voided': false,
        'overallProgressPct': 20,
        'winningamount': 10,
        'rank': 1,
        'prizes': []
      }];
      const result = component.checkIfRecordExist("1");
      expect(result).toBe(false);
    });
  });

  describe('#createClockForEvent', () => {
    it('should add the clock to event', () => {
        component.event = { clock: undefined, started: true } as any;
        const update = { id: 123, seconds: '1' } as any;
        component['createClockForEventFromInit']();
        expect(component.event.clock).not.toBeUndefined();
    });
    it('should not add the clock to the event', () => {
        component.event = { clock: undefined, started: false } as any;
        const update = { id: 123, seconds: '1' } as any;
        component['createClockForEventFromInit']();
        expect(component.event.clock).toBeUndefined();
    });
    it('should not call liveEventClockProviderService', () => {
        component.event = { clock: {}, started: true } as any;
        const update = { id: 123, seconds: '1' } as any;
        component['createClockForEventFromInit']();
        expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
    });
});
describe('decodeInitialData', () => {
  it('decodeInitialData with my entries', () => {
    component.leaderboardData = USER_SHOWDOWN_DATA;
    component.contestInfo = USER_SHOWDOWN_DATA;
    component['contestId'] = '602f52152c05212d1b9336bc';
    component.homeName = 'arsenal';
    component.awayName = 'madrid';
    component['decodeInitialData']();
    expect(component.contestInfo).not.toBeNull();
    expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['arsenal','madrid'],'16');
  });
});
});