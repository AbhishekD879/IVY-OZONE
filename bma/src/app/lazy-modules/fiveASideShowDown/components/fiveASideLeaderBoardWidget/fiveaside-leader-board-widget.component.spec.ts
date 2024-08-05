import { FiveasideLeaderBoardWidgetComponent
} from '@lazy-modules/fiveASideShowDown/components/fiveASideLeaderBoardWidget/fiveaside-leader-board-widget.component';
import { of, throwError } from 'rxjs';
import { LEADERBOARD_MOCK } from '@lazy-modules/fiveASideShowDown/components/fiveASideLeaderBoardWidget/fiveaside-leader-board-widget.mock';

describe('FiveasideLeaderBoardWidgetComponent', () => {
  let component: FiveasideLeaderBoardWidgetComponent;
  let leaderBoardService,
  userService,
  widgetService,
  liveServeSubscriberService,
  changeDetectorRef,
  carouselService,
  pubsub,
  carouselInstanceMock,
  navigationService,
  router;

  beforeEach(() => {
    leaderBoardService = {
      getLeaderBoardInformation: jasmine.createSpy('getLeaderBoardInformation').and.returnValue(of({contests: LEADERBOARD_MOCK}))
    };
    userService = {
      username: 'username'
    };
    widgetService = {
      buildLeaderBoardData: jasmine.createSpy('buildLeaderBoardData')
    };
    liveServeSubscriberService = {
      createChannels: jasmine.createSpy('createChannels').and.returnValue([{id: 1}] as any),
      openLiveServeConnectionForUpdates: jasmine.createSpy('openLiveServeConnectionForUpdates'),
      unSubscribeLiveServeConnection: jasmine.createSpy('unSubscribeLiveServeConnection').and.returnValue([{id: 1}] as any)
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck'),
      detectChanges: jasmine.createSpy('detectChanges')
    };
    carouselService = {
      get: jasmine.createSpy('get').and.callFake(() => carouselInstanceMock)
    };
    carouselInstanceMock = {
      next: jasmine.createSpy('next'),
      previous: jasmine.createSpy('previous'),
      toIndex: jasmine.createSpy('toIndex')
    };
    pubsub = {
      unsubscribe: jasmine.createSpy('unsubscribe'),
      subscribe: jasmine.createSpy('subscribe'),
      API: {
        SHOWDOWN_LIVE_EVENT_RESULTED: 'SHOWDOWN_LIVE_EVENT_RESULTED'
      }
    };
    navigationService = {
      changeEmittedFromChild: {
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb && cb(true))
      }
    };
    router = {
      url: '/horse-racing/featured'
    };
    component = new FiveasideLeaderBoardWidgetComponent(leaderBoardService,
      userService, widgetService, liveServeSubscriberService, changeDetectorRef,
      carouselService, pubsub, navigationService, router);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should get leaderboard data in ngOnInit (Case: isMatchesURL-false)', () => {
    spyOn(component as any, 'getLeaderboardData');
    spyOn(component as any, 'isMatchesURL').and.returnValue(false);
    component['init']();
    expect(component['getLeaderboardData']).toHaveBeenCalled();
  });
  it('should get leaderboard data in ngOnInit (Case: isMatchesURL-true)', () => {
    spyOn(component as any, 'getLeaderboardData');
    spyOn(component as any, 'isMatchesURL').and.returnValue(true);
    component.showDownData = [];
    component['init']();
    expect(component['getLeaderboardData']).toHaveBeenCalled();
  });
  it('should unsubscribe channels in ngOnDestroy', () => {
    spyOn(component as any, 'unsubscribeChannels');
    component.ngOnDestroy();
    expect(component['unsubscribeChannels']).toHaveBeenCalled();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('FiveasideLeaderBoardWidgetComponent');
  });
  it('should unsubscribe channels in ngOnDestroy(navigationServiceSubscription: true)', () => {
    spyOn(component as any, 'unsubscribeChannels');
    component['navigationServiceSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();
    expect(component['unsubscribeChannels']).toHaveBeenCalled();
    expect(pubsub.unsubscribe).toHaveBeenCalledWith('FiveasideLeaderBoardWidgetComponent');
    expect(component['navigationServiceSubscription'].unsubscribe).toHaveBeenCalled();
  });
  it('should unsubscribe channels', () => {
    component['unsubscribeChannels']();
    expect(component['channelsList']).not.toBeNull();
  });
  describe('#setActiveWidgetSlide', () => {
    it('should set card active flag as true', () => {
      component['showDownData'] = [{active : false, eventDetails : {}}] as any;
      component['setActiveWidgetSlide']();
      expect(component['showDownData'][0].active).toBeTruthy();
    });
    it('should not set card active flag as true when events are empty', () => {
      component['showDownData'] = [{active : false, eventDetails : null}] as any;
      component['setActiveWidgetSlide']();
      expect(component['showDownData'][0].active).toBeFalsy();
    });
    it('should not set card active flag as true when events are missing', () => {
      component['showDownData'] = [{active : false}] as any;
      component['setActiveWidgetSlide']();
      expect(component['showDownData'][0].active).toBeFalsy();
    });
    it('should not set card active flag as true when contests are missing', () => {
      component['showDownData'] = [] as any;
      component['setActiveWidgetSlide']();
      expect(component['showDownData'].length).toEqual(0);
    });
    it('should not set card active flag as true when contests are null', () => {
      component['showDownData'] = null;
      component['setActiveWidgetSlide']();
      expect(component['showDownData']).toBeFalsy();
    });
  });
  describe('#getLeaderboardData', () => {
    beforeEach(() => {
      spyOn(component as any, 'hidePreEventContests');
      spyOn(component as any, 'setActiveWidgetSlide');
    });
    it('should fetch data with success (Case: Data Exists)', () => {
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData).not.toBeNull();
    });
    it('should fetch data with success (Case: No Response)', () => {
      leaderBoardService.getLeaderBoardInformation.and.returnValue(of(null));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should fetch data with success (Case: Empty array)', () => {
      leaderBoardService.getLeaderBoardInformation.and.returnValue(of([]));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should fetch data with success (Case: Contests Empty array)', () => {
      leaderBoardService.getLeaderBoardInformation.and.returnValue(of({ contests: [] }));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should fetch data with success (Case: Contests Empty array)', () => {
      leaderBoardService.getLeaderBoardInformation.and.returnValue(of({ contests: null }));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should not initialize data ehen service failed with response', () => {
      leaderBoardService.getLeaderBoardInformation.and.returnValue(throwError('error'));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should not make API call if not logged in', () => {
      userService.username = null;
      leaderBoardService.getLeaderBoardInformation.and.returnValue(throwError('error'));
      spyOn(component as any, 'initLeaderBoardData');
      component['getLeaderboardData']();
      expect(component.showDownData.length).toEqual(0);
    });
  });
  it('should init leaderboard data', () => {
    spyOn(component as any, 'openLiveServeConnection');
    spyOn(component as any, 'unsubscribeChannels');
    component['initLeaderBoardData']();
    expect(component['openLiveServeConnection']).toHaveBeenCalled();
  });
  it('should open Live serve', () => {
    component['eventIds'] = ['123'];
    component['openLiveServeConnection']();
    expect(component['channelsList']).not.toBeNull();
  });
  it('#isOneCard should return boolean', () => {
    component.showDownData = [];
    expect(component['isOneCard']).toBeFalsy();
    component.showDownData = [{id: 1}] as any;
    expect(component['isOneCard']).toBeTruthy();
  });
  describe('gotToSlide', () => {
    it(`should slide`, () => {
      spyOn(component as any, 'handleActiveShowdown');
      component.goToSlide(3);
      expect(carouselInstanceMock.toIndex).toHaveBeenCalledWith(3);
    });
  });
  describe('handleActiveSlide', () => {
    beforeEach(() => {
      component.showDownData = [{}, {}] as any;
    });
    it('should set active showdownData index', () => {
      component.handleActiveSlide(1);
      expect(component.showDownData[0].active).toBeTruthy();
      expect(component.showDownData[1].active).toBeFalsy();
      expect(component.activeSlideIndex).toBe(0);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it(`should Not detectChanges if no showdownData by index`, () => {
      component.handleActiveSlide(3);
      expect(changeDetectorRef.detectChanges).not.toHaveBeenCalled();
    });
    it(`should return nothing if slideIndex id Not integer`, () => {
      component.handleActiveSlide(1.123);
      expect(component.activeSlideIndex).toEqual(0);
    });
  });
  describe('#handleResultedEvent', () => {
    it('should remove resulted events from showdownData if event exists', () => {
      component.showDownData = [{event: '123'}, {event: '345'}] as any;
      component['handleResultedEvent']('345');
      expect(component.showDownData.length).toEqual(1);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });
  });
  describe('#hidePreEventContests', () => {
    it('should not hide if started is true', () => {
      component.showDownData = [{ eventDetails: { started: true } }] as any;
      component['hidePreEventContests']();
      expect(component.showDownData.length).toEqual(1);
    });
    it('should not hide if started is false', () => {
      component.showDownData = [{ eventDetails: { started: false } }] as any;
      component['hidePreEventContests']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should not hide if started is missing', () => {
      component.showDownData = [{ eventDetails: {} }] as any;
      component['hidePreEventContests']();
      expect(component.showDownData.length).toEqual(0);
    });
    it('should not hide if event is null', () => {
      component.showDownData = [{ eventDetails: null }] as any;
      component['hidePreEventContests']();
      expect(component.showDownData.length).toEqual(0);
    });
  });
  describe('#handleStartedEvent', () => {
    it('should add event to showdownData', () => {
      component['showDownData'] = [];
      component['masterShowDownData'] = [{ event: '1', eventDetails: {} }] as any;
      component['handleStartedEvent']('1');
      expect(component.showDownData.length).toEqual(1);
    });
    it('should not add event to showdownData when events are missing', () => {
      component['showDownData'] = [];
      component['masterShowDownData'] = [{ event: '1', eventDetails: null }] as any;
      component['handleStartedEvent']('1');
      expect(component.showDownData.length).toEqual(0);
    });
    it('should not add event to showdownData when events are null', () => {
      component['showDownData'] = [];
      component['masterShowDownData'] = [{ event: '1', eventDetails: {} }] as any;
      component['handleStartedEvent']('1');
      expect(component.showDownData.length).toEqual(1);
    });
    it('should add event to showdownData when that event doesnt exists', () => {
      component['showDownData'] = [{ event: '123', events: [{}] }] as any;
      component['masterShowDownData'] = [{ event: '1', eventDetails: {} }] as any;
      component['handleStartedEvent']('1');
      expect(component.showDownData.length).toEqual(2);
    });
    it('should not add event to showdownData when that event exists', () => {
      component['showDownData'] = [{ event: '123', events: [{}] }] as any;
      component['masterShowDownData'] = [{ event: '1', eventDetails: null }, { event: '123', eventDetails: null }] as any;
      component['handleStartedEvent']('123');
      expect(component.showDownData.length).toEqual(1);
    });
  });
  describe('#checkEventAlreadyExists', () => {
    it('should return true if event exists', () => {
      component['showDownData'] = [{event : '1'}] as any;
      expect(component['checkEventAlreadyExists']('1')).toBeTruthy();
    });
    it('should return false if event exists', () => {
      component['showDownData'] = [{event : '1'}] as any;
      expect(component['checkEventAlreadyExists']('2')).toBeFalsy();
    });
    it('should return false if event input is undefined', () => {
      component['showDownData'] = [{event : '1'}] as any;
      expect(component['checkEventAlreadyExists'](undefined)).toBeFalsy();
    });
  });
  it('#postLoginTrigger to have been called', () => {
    spyOn(component as any, 'getLeaderboardData');
    pubsub.subscribe.and.callFake((a, method, cb) => {
        cb();
    });
    component['postLoginTrigger']();
    expect(component['getLeaderboardData']).toHaveBeenCalled();
  });
  describe('#checkDataLoad', () => {
    it('should not call getLeaderBoard, if loaded is false', () => {
      spyOn(component as any, 'getLeaderboardData');
      spyOn(component as any, 'isMatchesURL').and.returnValue(false);
      navigationService.changeEmittedFromChild.subscribe.and.callFake(cb => cb && cb(false));
      component['checkDataLoad']();
      expect(component['getLeaderboardData']).not.toHaveBeenCalled();
    });
    it('should not call getLeaderBoard, if loaded is true and showDown has data', () => {
      spyOn(component as any, 'getLeaderboardData');
      spyOn(component as any, 'isMatchesURL').and.returnValue(false);
      navigationService.changeEmittedFromChild.subscribe.and.callFake(cb => cb && cb(true));
      component.showDownData = [{id:1}] as any;
      component['checkDataLoad']();
      expect(component['getLeaderboardData']).not.toHaveBeenCalled();
    });
    it('should not call getLeaderBoard, if loaded is true, no showDown and isMAtchesUrl false', () => {
      spyOn(component as any, 'getLeaderboardData');
      spyOn(component as any, 'isMatchesURL').and.returnValue(false);
      navigationService.changeEmittedFromChild.subscribe.and.callFake(cb => cb && cb(true));
      component.showDownData = [] as any;
      component['checkDataLoad']();
      expect(component['getLeaderboardData']).not.toHaveBeenCalled();
    });
  });
  describe('#isMatchesURL', () => {
    it('should return true', () => {
      router.url = '/sport/football/matches';
      const response = component['isMatchesURL']();
      expect(response).toBe(true);
    });
    it('should return false', () => {
      router.url = '/sport/football';
      const response = component['isMatchesURL']();
      expect(response).toBe(false);
    });
  });
  describe('#showLeaderboard', () => {
    it('should set showLeaderboard', () => {
      component.showLeaderboard = true;
      expect(component['_showLeaderboard']).toEqual(true);
    });
    it('should get showLeaderboard', () => {
      component['_showLeaderboard'] = true;
      expect(component.showLeaderboard).toEqual(true);
    });
  });
});
