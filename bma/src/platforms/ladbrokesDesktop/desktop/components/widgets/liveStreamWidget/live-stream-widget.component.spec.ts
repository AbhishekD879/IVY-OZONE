import { LiveStreamWidgetComponent } from './live-stream-widget.component';
import { of } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { IOutcome } from '@core/models/outcome.model';
import { IScores } from '@desktop/models/live-stream-widget.model';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LDLiveStreamWidgetComponent', () => {
  let component: LiveStreamWidgetComponent;

  let pubSubService, sportEventHelperService, liveStreamWidgetService,
    routingHelperService, userService, filtersService, inplayHelperService;
  let tempEvent;

  beforeEach(() => {
    pubSubService = {
      subscriptions: {},
      subscribe: jasmine.createSpy('subscribe').and.callFake((nameSpace, event, callback) => {
        pubSubService.subscriptions[event] = callback;
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish').and.callFake((event, data) => {
        pubSubService.subscriptions[event] && pubSubService.subscriptions[event](data);
      }),
      API: pubSubApi
    };

    sportEventHelperService = {
      getOddsScore: jasmine.createSpy('getOddsScore'),
      getEventCurrentPoints: jasmine.createSpy('getEventCurrentPoints'),
      isLive: jasmine.createSpy('isLive'),
      isHalfTime: jasmine.createSpy('isHalfTime'),
      isClockAllowed: jasmine.createSpy('isClockAllowed'),
      getTennisSetIndex: jasmine.createSpy('getTennisSetIndex'),
      isCashOutEnabled: jasmine.createSpy('isCashOutEnabled')
    };

    liveStreamWidgetService = {
      sendGTM: jasmine.createSpy('sendGTM'),
      findOddsHeader: jasmine.createSpy('findOddsHeader'),
      getData: jasmine.createSpy('getData').and.returnValue(of([]))
    };


    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('some-link')
    };

    userService = {
      status: true
    };

    filtersService = {
      groupBy: jasmine.createSpy('groupBy').and.returnValue([])
    };

    tempEvent = {
      id: 123,
      categoryName: 'football',
      comments: {
        teams: {player_1: {id: 1}, player_2: {id: 2}},
        setsScores: {}
      },
      markets: [{
        id: 2,
        outcomes: [
          { id: '123' } as any,
          { id: '456' } as any,
          { id: '789' } as any
        ]
      }]
    } as any;

    inplayHelperService = {
      unsubscribeForLiveUpdates: jasmine.createSpy('unsubscribeForLiveUpdates')
    };

    liveStreamWidgetService.getData.and.returnValue(of({tempEvent}));

    component = new LiveStreamWidgetComponent(pubSubService, sportEventHelperService, liveStreamWidgetService,
      routingHelperService, userService, filtersService, inplayHelperService);
    component.ngOnInit();

    component.outcomes = [
      { id: '123' } as any,
      { id: '456' } as any,
      { id: '789' } as any
    ];
  });

  it('should create and initialize component', () => {
    expect(component).toBeTruthy();
    expect(component.isLoggedIn).toEqual(true);
    expect(pubSubService.subscribe).toHaveBeenCalledWith('liveStreamWidget', 'DELETE_SELECTION_FROMCACHE',
      jasmine.anything());
    expect(pubSubService.subscribe).toHaveBeenCalledWith('liveStreamWidget', 'SET_PLAYER_INFO',
      jasmine.anything());
    expect(pubSubService.subscribe).toHaveBeenCalledWith('liveStreamWidget', 'DELETE_EVENT_FROM_CACHE',
      jasmine.anything());
  });

  it('should notify that live stream is available', fakeAsync(() => {
    component = new LiveStreamWidgetComponent(pubSubService, sportEventHelperService, liveStreamWidgetService,
      routingHelperService, userService, filtersService, inplayHelperService);

    liveStreamWidgetService.getData.and.returnValue(of(tempEvent));
    component.ngOnInit();
    tick();
    expect(pubSubService.publish).toHaveBeenCalledWith('WIDGET_VISIBILITY', { liveStream: true });
  }));

  it('should notify that live stream is NOT available', fakeAsync(() => {
    component = new LiveStreamWidgetComponent(pubSubService, sportEventHelperService, liveStreamWidgetService,
      routingHelperService, userService, filtersService, inplayHelperService);

    liveStreamWidgetService.getData.and.returnValue(of(null));
    component.ngOnInit();
    tick();
    expect(pubSubService.publish).toHaveBeenCalledWith('WIDGET_VISIBILITY', { liveStream: false });
  }));

  it('should handle change of user status', fakeAsync(() => {
    pubSubService.publish(pubSubService.API.SET_PLAYER_INFO, { status: false });
    tick();
    expect(component.isLoggedIn).toEqual(false);
    pubSubService.publish(pubSubService.API.SET_PLAYER_INFO, { status: true });
    tick();
    expect(component.isLoggedIn).toEqual(true);
  }));

  it('should handle selection deletion - for stored event', fakeAsync(() => {
    component.event = tempEvent;
    const update = { selectionId: '123', marketId: 2, eventId: 123 };
    pubSubService.publish(pubSubService.API.DELETE_SELECTION_FROMCACHE, update);
    tick();
    expect(component.outcomes[0]).toBeUndefined();

    pubSubService.publish(pubSubService.API.DELETE_SELECTION_FROMCACHE, update);
    tick();
    const expectedOutcomes = [undefined, { id: '456' }, { id: '789' }] as IOutcome[];
    expect(component.outcomes).toEqual(expectedOutcomes);
  }));

  it('should handle selection deletion - for NOT stored event', fakeAsync(() => {
    const update = { selectionId: '999', marketId: 2, eventId: 123 };
    pubSubService.publish(pubSubService.API.DELETE_SELECTION_FROMCACHE, update);
    tick();

    const expectedOutcomes = [{ id: '123' }, { id: '456' }, { id: '789' }] as IOutcome[];
    expect(component.outcomes).toEqual(expectedOutcomes);
  }));

  it('should handle WS event deletion', fakeAsync(() => {
    component.event = tempEvent;
    pubSubService.publish(pubSubService.API.DELETE_EVENT_FROM_CACHE, 7);
    tick();
    expect(pubSubService.unsubscribe).not.toHaveBeenCalled();

    pubSubService.publish(pubSubService.API.DELETE_EVENT_FROM_CACHE,  123);
    tick();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  }));

  it('should handle Reload inplay event and call reloadComponent', fakeAsync(() => {
    spyOn(component as any, 'reloadComponent');
    pubSubService.publish(pubSubService.API.RELOAD_IN_PLAY);

    expect(component.reloadComponent).toHaveBeenCalled();
  }));

  it('onDestroy unsubscribe from PubSub', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('liveStreamWidget');
  });

  it('onDestroy should unsubscribeForLiveUpdates from InplayHelperService if event was set', () => {
    component.event = tempEvent;
    component.ngOnDestroy();
    expect(inplayHelperService.unsubscribeForLiveUpdates).toHaveBeenCalledWith([tempEvent]);
  });

  it('onDestroy should NOT unsubscribeForLiveUpdates from InplayHelperService if event was NOT set', () => {
    component.event = null;
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalled();
    expect(inplayHelperService.unsubscribeForLiveUpdates).not.toHaveBeenCalled();
  });

  describe('initStreamViewData', () => {
    it('event exists', () => {
      component.event = tempEvent as any;
      component['initStreamViewData']();
      expect(component.event).toEqual(tempEvent);

      expect(pubSubService.publish).toHaveBeenCalledWith('WIDGET_VISIBILITY', { liveStream: true });
      expect(component.category).toBe('football');
      expect(component.teams).toEqual({player_1: {id: 1}, player_2: {id: 2}} as any);
      expect(component.edpUrl).toBe('/some-link/all-markets/watch-live');
      expect(component.scores).toEqual([]);
      expect(component.outcomes).toEqual([]);
    });
  });

  it('openLoginDialog should call sendGTM and publish OPEN_LOGIN_DIALOG event', () => {
    component.sportName = 'sportName';

    component.openLoginDialog();

    expect(liveStreamWidgetService.sendGTM).toHaveBeenCalledWith('login link', 'sportName');
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'livestream' });
  });

  it('trackById returns formatted text', () => {
    expect(component.trackById(1, { id: '123' } as IOutcome)).toEqual('123_1');
    expect(component.trackById(1, {} as IOutcome)).toEqual('1');
  });

  it('sendCollapseGTM', () => {
    component.sportName = 'football';
    component.sendCollapseGTM();
    expect(liveStreamWidgetService.sendGTM).toHaveBeenCalledWith('collapse', 'football');
    liveStreamWidgetService.sendGTM.calls.reset();
    component.sendCollapseGTM();
    expect(liveStreamWidgetService.sendGTM).not.toHaveBeenCalled();
  });

  it('sendViewAllGTM', () => {
    component.sportName = 'football';
    component.sendViewAllGTM();
    expect(liveStreamWidgetService.sendGTM).toHaveBeenCalledWith('view all', 'football');
  });

  it('sendPlayGTM', () => {
    component.sportName = 'football';
    component.sendPlayGTM();
    expect(liveStreamWidgetService.sendGTM).toHaveBeenCalledWith('play', 'football');
  });

  it('sendRegisterGTM', () => {
    component.sportName = 'football';
    component.sendRegisterGTM({ target: { tagName: 'A' } });
    expect(liveStreamWidgetService.sendGTM).toHaveBeenCalledWith('register link', 'football');
    liveStreamWidgetService.sendGTM.calls.reset();
    component.sendRegisterGTM({ target: { tagName: 'BR' } });
    expect(liveStreamWidgetService.sendGTM).not.toHaveBeenCalled();
  });

  it('getOddsScore', () => {
    sportEventHelperService.getOddsScore.and.returnValue(0);
    expect(component.getOddsScore()).toEqual('0 - 0');
  });

  it('getCurrentOddsScore', () => {
    sportEventHelperService.getEventCurrentPoints.and.returnValue(1);
    expect(component.getCurrentOddsScore()).toEqual('1 - 1');
  });

  it('isTennis to equal false for non tenis category', () => {
    expect(component.isTennis()).toEqual(false);
  });

  it('getSetsScores ', () => {
    component.event = tempEvent;
    component.teams = { player_1: {id: '1'} , player_2: {id: '2'}};
    const scores: IScores = {};
    scores['1'] = 1;
    scores['2'] = 2;
    expect(component.getSetsScores(scores)).toEqual('1 - 2');
  });

  it('isLive ', () => {
    sportEventHelperService.isLive.and.returnValue(false);
    sportEventHelperService.isHalfTime.and.returnValue(false);
    sportEventHelperService.isClockAllowed.and.returnValue(false);
    sportEventHelperService.getTennisSetIndex.and.returnValue('false');

    expect(component.isLive()).toEqual(false);
  });

  it('isHalfTime', () => {
    sportEventHelperService.isHalfTime.and.returnValue(false);
    expect(component.isHalfTime()).toEqual(false);
  });

  it('isClock', () => {
    sportEventHelperService.isHalfTime.and.returnValue(false);
    sportEventHelperService.isClockAllowed.and.returnValue(false);

    expect(component.isClock()).toEqual(false);

    sportEventHelperService.isHalfTime.and.returnValue(false);
    sportEventHelperService.isClockAllowed.and.returnValue(true);

    expect(component.isClock()).toEqual(true);

    sportEventHelperService.isHalfTime.and.returnValue(true);
    sportEventHelperService.isClockAllowed.and.returnValue(false);

    expect(component.isClock()).toEqual(false);

    sportEventHelperService.isHalfTime.and.returnValue(true);
    sportEventHelperService.isClockAllowed.and.returnValue(true);

    expect(component.isClock()).toEqual(false);
  });

  it('getSetIndex', () => {
    sportEventHelperService.getTennisSetIndex.and.returnValue('Set 1');
    expect(component.getSetIndex()).toEqual('Set 1');
  });

  it('getOddsHeader', () => {
    liveStreamWidgetService.findOddsHeader.and.returnValue('home,draw,away');
    expect(component.getOddsHeader(1, 1)).toEqual('draw');
  });

  it('isShowOddButton', () => {
    liveStreamWidgetService.findOddsHeader.and.returnValue('home,draw,away');
    expect(component.isShowOddButton(1)).toEqual(false);
  });

  it('isCashOutEnabled', () => {
    sportEventHelperService.isCashOutEnabled.and.returnValue(true);
    expect(component.isCashOutEnabled()).toEqual(true);
  });

});
