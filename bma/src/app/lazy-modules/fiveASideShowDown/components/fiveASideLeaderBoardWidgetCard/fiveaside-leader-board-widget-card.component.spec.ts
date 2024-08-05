import { FiveasideLeaderBoardWidgetCardComponent
} from '@lazy-modules/fiveASideShowDown/components/fiveASideLeaderBoardWidgetCard/fiveaside-leader-board-widget-card.component';
import { of } from 'rxjs';

describe('FiveasideLeaderBoardWidgetCardComponent', () => {
  let component: FiveasideLeaderBoardWidgetCardComponent;
  let coreToolsService,
  widgetService,
  lobbyService,
  pubSub,
  entryService,
  liveServeUpdateService,
  userService,
  subscriberService,
  rulesEntryService,
  router,
  cmsService,
  leaderBoardService,
  changeDetectorRef,
  awsService;

  beforeEach(() => {
    coreToolsService = {
      uuid: jasmine.createSpy('uuid').and.returnValue('1234')
    };
    widgetService = {
      getEventLiveStatus: jasmine.createSpy('getEventLiveStatus'),
      setScoresFromEventComments: jasmine.createSpy('setScoresFromEventComments'),
      clockUpdate: jasmine.createSpy('clockUpdate')
    };
    lobbyService = {
      setEventStateByStartDate: jasmine.createSpy('setEventStateByStartDate')
    };
    pubSub = {
      API: {
        SHOWDOWN_LIVE_SCORE_UPDATE: 'SHOWDOWN_LIVE_SCORE_UPDATE',
        SHOWDOWN_LIVE_CLOCK_UPDATE: 'SHOWDOWN_LIVE_CLOCK_UPDATE',
        SHOWDOWN_LIVE_EVENT_UPDATE: 'SHOWDOWN_LIVE_EVENT_UPDATE'
      },
      subscribe: jasmine.createSpy().and.callFake((a, b, cb)=> cb()),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    entryService = {
      entriesCreation: jasmine.createSpy('entriesCreation').and.returnValue([{id: 1}] as any)
    };
    liveServeUpdateService = {
      updateEventComments: jasmine.createSpy('updateEventComments'),
      updateClock: jasmine.createSpy('updateClock'),
      updateEventLiveData: jasmine.createSpy('updateEventLiveData')
    };
    userService = {
      username: 'username',
      bppToken: 'abc123'
    };
    subscriberService = {
      unSubscribeShowDownChannels: jasmine.createSpy('unSubscribeShowDownChannels'),
      userEntryUpdates: jasmine.createSpy('userEntryUpdates')
    };
    rulesEntryService = {
      trackGTMEvent: jasmine.createSpy('trackGTMEvent')
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/sport/football/matches'
    };
    cmsService = {
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of([]))
    };
    leaderBoardService = {
      getDynamicClass: jasmine.createSpy('getDynamicClass').and.returnValue('digitThree'),
      hasImageForHomeAway: jasmine.createSpy('hasImageForHomeAway').and.returnValue(true),
      setDefaultTeamColors: jasmine.createSpy('setDefaultTeamColors').and.returnValue([{id: 1}, {id: 2}] as any)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };
    awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    component = new FiveasideLeaderBoardWidgetCardComponent(coreToolsService,
      widgetService,
      lobbyService,
      pubSub,
      entryService,
      liveServeUpdateService, userService, subscriberService, rulesEntryService, router,
      cmsService, leaderBoardService, changeDetectorRef,awsService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  describe('#ngOnInit', () => {
    it('should not initialize data, if no widget data', () => {
      spyOn(component as any, 'initEntryDetails');
      component.widgetData = null;
      component.ngOnInit();
      expect(component['initEntryDetails']).not.toHaveBeenCalled();
    });
    it('should not initialize data, if no event entity', () => {
      spyOn(component as any, 'initEntryDetails');
      component.widgetData = {} as any;
      component.eventEntity = null;
      component.ngOnInit();
      expect(component['initEntryDetails']).not.toHaveBeenCalled();
    });
    it('should initialize data', () => {
      spyOn(component as any, 'initEntryDetails');
      spyOn(component as any, 'initWidgetDetails');
      spyOn(component as any, 'subscribeForLiveUpdates');
      component.widgetData = {} as any;
      component.eventEntity = {} as any;
      component.ngOnInit();
      expect(component['initEntryDetails']).toHaveBeenCalled();
    });
  });
  it('should unsubscribe in ngOndestroy', () => {
    component['subscriber'] = 'component';
    component.ngOnDestroy();
    expect(pubSub.unsubscribe).toHaveBeenCalledWith('component');
  });
  it('should initialize entry details without username', () => {
    component.widgetData = { id: 1} as any;
    userService.username = null;
    component['initEntryDetails']();
    expect(component['entryChannel']).not.toBeNull();
  });
  it('should initialize entry details', () => {
    component.widgetData = { id: 1} as any;
    userService.username = 'username';
    component['initEntryDetails']();
    expect(component['entryChannel']).not.toBeNull();
  });
  it('should initialize widget details', () => {
    spyOn(component as any, 'getTeamsColors');
    component['initWidgetDetails']();
    expect(component['subscriber']).toEqual('LeaderBoardWidget_1234');
    expect(widgetService.getEventLiveStatus).toHaveBeenCalled();
  });
  it('should create handlers for all the subscribed channels', () => {
    spyOn(component as any, 'createEventHanler');
    component['subscribeForLiveUpdates']();
    expect(component['createEventHanler']).toHaveBeenCalledTimes(3);
  });
  describe('#createEventHanler', () => {
    beforeEach(() => {
      component['subscriber'] = 'component';
    });
    it('should not call liveserve function, if no update data', () => {
      component['createEventHanler']('SHOWDOWN_LIVE_SCORE_UPDATE', 'updateEventComments', 'setScoresFromEventComments');
      expect(liveServeUpdateService.updateEventComments).not.toHaveBeenCalled();
    });
    it('should not call liveserve function, if no update_id not equal to event_id', () => {
      component.eventEntity = {id: 123} as any;
      pubSub.subscribe.and.callFake((a, b, cb)=> cb({id: 234})),
      component['createEventHanler']('SHOWDOWN_LIVE_SCORE_UPDATE', 'updateEventComments', 'setScoresFromEventComments');
      expect(liveServeUpdateService.updateEventComments).not.toHaveBeenCalled();
    });
    it('should not call liveserve function, if no update_payload', () => {
      component.eventEntity = {id: 123} as any;
      pubSub.subscribe.and.callFake((a, b, cb)=> cb({id: 123})),
      component['createEventHanler']('SHOWDOWN_LIVE_SCORE_UPDATE', 'updateEventComments', 'setScoresFromEventComments');
      expect(liveServeUpdateService.updateEventComments).not.toHaveBeenCalled();
    });
    it('should call liveserve function, if it satisfies all conditions', () => {
      component.eventEntity = {id: 123} as any;
      pubSub.subscribe.and.callFake((a, b, cb)=> cb({id: 123, payload: {}})),
      component['createEventHanler']('SHOWDOWN_LIVE_SCORE_UPDATE', 'updateEventComments', 'setScoresFromEventComments');
      expect(liveServeUpdateService.updateEventComments).toHaveBeenCalled();
      expect(widgetService.setScoresFromEventComments).toHaveBeenCalled();
    });
    it('should call widget function, if not provided', () => {
      component.eventEntity = {id: 123} as any;
      pubSub.subscribe.and.callFake((a, b, cb)=> cb({id: 123, payload: {}})),
      component['createEventHanler']('SHOWDOWN_LIVE_SCORE_UPDATE', 'updateEventComments', null);
      expect(liveServeUpdateService.updateEventComments).toHaveBeenCalled();
      expect(widgetService.setScoresFromEventComments).not.toHaveBeenCalled();
    });
  });
  it('#onWidgetClick should trigger and navigate(isMatchURL-true)', () => {
    component.widgetData = { id: '123'} as any;
    component.onWidgetClick();
    expect(router.navigate).toHaveBeenCalledWith(['/5-a-side/leaderboard', '123']);
  });
  it('#onWidgetClick should trigger navigate and isMatchesUrl spy is false', () => {
    spyOn(component as any, 'isMatchesURL').and.returnValue(false);
    component.widgetData = { id: '123'} as any;
    component.onWidgetClick();
    expect(router.navigate).toHaveBeenCalledWith(['/5-a-side/leaderboard', '123']);
    expect(rulesEntryService.trackGTMEvent).toHaveBeenCalled();
  });
  it('#onWidgetClick should trigger navigate and isMatchesUrl spy is true', () => {
    spyOn(component as any, 'isMatchesURL').and.returnValue(true);
    component.widgetData = { id: '123'} as any;
    component.onWidgetClick();
    expect(router.navigate).toHaveBeenCalledWith(['/5-a-side/leaderboard', '123']);
    expect(rulesEntryService.trackGTMEvent).toHaveBeenCalled();
  });
  it('#onWidgetClick should trigger and navigate(isMatchURL-false)', () => {
    router.url = 'check';
    component.widgetData = { id: '123'} as any;
    component.onWidgetClick();
    expect(router.navigate).toHaveBeenCalledWith(['/5-a-side/leaderboard', '123']);
  });
  describe('#userEntryHandler', () => {
    it('should not initiate entrydetails, if 1st condition fails', () => {
      component['userEntryHandler']([] as any);
      expect(component.entryDetails).toBeUndefined();
    });
    it('should not initiate entrydetails, if 2nd condition fails', () => {
      component.widgetData = { id: '123' } as any;
      component['userEntryHandler']({ myEntries: [{ contestId: '456' }] } as any);
      expect(component.entryDetails).toBeUndefined();
    });
    it('should initiate entrydetails, if 3rd condition fails', () => {
      component.widgetData = { id: '123' } as any;
      component['isComponentDestroyed'] = true;
      component['userEntryHandler']({ myEntries: [{ contestId: '123' }] } as any);
      expect(component.entryDetails).not.toBeNull();
    });
    it('should initiate entrydetails, if all conditions satisfies', () => {
      component.widgetData = { id: '123' } as any;
      component['isComponentDestroyed'] = false;
      component['userEntryHandler']({ myEntries: [{ contestId: '123' }] } as any);
      expect(component.entryDetails).not.toBeNull();
    });
    it('should initiate entrydetails, if my entries is null', () => {
      component.widgetData = { id: '123' } as any;
      component['isComponentDestroyed'] = false;
      component['userEntryHandler']({ myEntries: null } as any);
      expect(component.entryDetails).not.toBeNull();
    });
    it('should initiate entrydetails, if my leaderboard data is null', () => {
      component.widgetData = { id: '123' } as any;
      component['isComponentDestroyed'] = false;
      component['userEntryHandler'](null as any);
      expect(component.entryDetails).not.toBeNull();
    });
  });
  describe('#entryUpdateHandler', () => {
    it('should not initiate entrydetails, if 1st condition fails', () => {
      component['entryUpdateHandler']([]);
      expect(component.entryDetails).toBeUndefined();
    });
    it('should not initiate entrydetails, if 2nd condition fails', () => {
      component.widgetData = { id: '123'} as any;
      component['entryUpdateHandler']([{ contestId: '456'}] as any);
      expect(component.entryDetails).toBeUndefined();
    });
    it('should initiate entrydetails, if 3rd condition fails', () => {
      component.widgetData = { id: '123'} as any;
      component['isComponentDestroyed'] = true;
      component['entryUpdateHandler']([{ contestId: '123'}] as any);
      expect(component.entryDetails).not.toBeNull();
    });
    it('should initiate entrydetails, if all conditions satisfies', () => {
      component.widgetData = { id: '123'} as any;
      component['isComponentDestroyed'] = false;
      component['entryUpdateHandler']([{ contestId: '123'}] as any);
      expect(component.entryDetails).not.toBeNull();
    });
  });
  describe('#getTeamsColors', () => {
    it('should fetch team colors', () => {
      component.leaderBoardWidget = { homeTeam: 'ABC', awayTeam: 'DEF'} as any;
      component['getTeamsColors']();
      expect(component.teamColors).not.toBeNull();
    });
  });
  describe('#setMaskedName', () => {
    it('should not return username, if no usrename', () => {
      const response = component.setMaskedName(null);
      expect(response).toEqual('');
    });
    it('should return username, if 1st condition satisfies', () => {
      const response = component.setMaskedName('Masked');
      expect(response).toEqual('Mas***');
    });
    it('should return username, if 2nd condition satisfies', () => {
      const response = component.setMaskedName('Monstermax');
      expect(response).toEqual('Monst***');
    });
  });
  it('should return class based on rank', () => {
    component.entryDetails = { rank: 123} as any;
    expect(component.getClass()).toEqual('digitThree');
  });
  it('should return signposting Url', () => {
    expect(component.getSignpostingUrl('url')).not.toBeNull();
  });

  describe('#fixedDecimals', () => {
    it('should return with decimals fixed to 2', () => {
      const result = component.fixedDecimals("0.1231231");
      expect(result).toEqual("0.12");
    });
    it('should return without decimals', () => {
      const result = component.fixedDecimals("10.0");
      expect(result).toEqual("10");
    });
  });
});
