import { YourCallPlayerStatsComponent } from '@edp/components/markets/playerStats/your-call-player-stats.component';
import { Subscription } from 'rxjs';
import { fakeAsync } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';

describe('YourCallPlayerStatsComponent', () => {
  const tag = 'YourCallPlayerStatsCtrl';

  let component: YourCallPlayerStatsComponent;

  let filtersService;
  let pubSubService;
  let yourCallPlayerStatsGTMService;
  let windowRefService;
  let router;
  let routingState;
  let markets;

  beforeEach(() => {
    filtersService = {
      getTeamName: jasmine.createSpy('getTeamName').and.returnValue(''),
      orderBy: jasmine.createSpy('orderBy')
    };
    pubSubService = {
      API: {
        DELETE_SELECTION_FROM_CACHE: 'DELETE_SELECTION_FROM_CACHE',
        DELETE_MARKET_FROM_CACHE: 'DELETE_MARKET_FROM_CACHE'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    yourCallPlayerStatsGTMService = {
      sendChangeStatisticGTM: jasmine.createSpy('sendChangeStatisticGTM'),
      sendGTMData: jasmine.createSpy('sendGTMData'),
      sendTeamSwitcherGTM: jasmine.createSpy('sendTeamSwitcherGTM')
    };
    windowRefService = {
      nativeWindow: {
        location: {
          hash: 'hash'
        }
      }
    };
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(new Subscription())
      }
    };
    routingState = {
      getCurrentUrl: jasmine.createSpy('getCurrentUrl').and.returnValue('')
    };

    component = new YourCallPlayerStatsComponent(
      filtersService,
      pubSubService,
      yourCallPlayerStatsGTMService,
      windowRefService,
      router,
      routingState
    );
    markets = [{
      cashoutAvail: 'cashoutAvail',
      correctPriceTypeCode: 'correctPriceTypeCode',
      dispSortName: 'dispSortName',
      eachWayFactorNum: 100,
      eachWayFactorDen: 100,
      eachWayPlaces: 'eachWayPlaces',
      header: 'header',
      id: '12',
      isAntepost: 'isAntepost',
      isGpAvailable: 'isGpAvailable',
      isResulted: 'isResulted',
      isLpAvailable: 'isLpAvailable',
      isMarketBetInRun: true,
      isSpAvailable: true,
      isDisplayed: true,
      liveServChannels: 'liveServChannels',
      isEachWayAvailable: false,
      liveServChildrenChannels: 'liveServChildrenChannels',
      templateMarketName: 'templateMarketName',
      marketsNames: 'marketsNames',
      marketStatusCode: 'S',
      name: 'name',
      nextScore: 122,
      outcomes: [],
      periods: [],
      displayOrder: 'displayOrder',
      scores: [
        {
          outcomeid: 1
        },
        {
          outcomeid: 2
        }
      ],
      players: {
        scores: {
          number: 123,
          score: 'score',
          outcomeid: 'outcomeid'
        },
      filteredScore: {},
      activeScoreOutcome: 'activeScoreOutcome'
      }
    },
      {
      cashoutAvail: 'cashoutAvail',
      correctPriceTypeCode: 'correctPriceTypeCode',
      dispSortName: 'dispSortName',
      eachWayFactorNum: 100,
      eachWayFactorDen: 100,
      eachWayPlaces: 'eachWayPlaces',
      header: 'header',
      id: 'id',
      isAntepost: 'isAntepost',
      isGpAvailable: 'isGpAvailable',
      isResulted: 'isResulted',
      isLpAvailable: 'isLpAvailable',
      isMarketBetInRun: true,
      isSpAvailable: true,
      isDisplayed: true,
      liveServChannels: 'liveServChannels',
      isEachWayAvailable: false,
      liveServChildrenChannels: 'liveServChildrenChannels',
      templateMarketName: 'templateMarketName',
      marketsNames: 'marketsNames',
      marketStatusCode: 'marketStatusCode',
      name: 'name',
      nextScore: 122,
      outcomes: [],
      periods: [],
      displayOrder: 'displayOrder',
      players: {
        scores: {
          number: 123,
          score: 'score',
          outcomeid: 'outcomeid'
        },
      filteredScore: {},
      activeScoreOutcome: 'activeScoreOutcome'
      }
    }
    ];
    component['marketsGroup'] = {
      markets: markets
    } as any;
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });



  describe('ngOnInit', () => {
    it('ngOnInit', fakeAsync(() => {
      router.events.subscribe.and.callFake((cb) => cb('test'));

      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValue([]);
      component.eventEntity = {
        name: 'TeamA vs TeamB'
      } as any;
      component.marketsGroup = [{
        templateMarketName: 'templateMarketName',
        filteredOutcomes: [],
        players: []
      }] as any;

      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((p1, p2 , cb) => {
        return cb('test');
      });

      component.ngOnInit();

      expect(pubSubService.subscribe).toHaveBeenCalledWith(tag, pubSubService.API.DELETE_SELECTION_FROM_CACHE, jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(tag, pubSubService.API.DELETE_MARKET_FROM_CACHE, jasmine.any(Function));
      expect(router.events.subscribe).toHaveBeenCalledWith(jasmine.any(Function));
    }));

    it('deleteEvent and deleteMarket to have been called', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb('event'));
      component['deleteEvent'] = jasmine.createSpy('deleteEvent');
      component['deleteMarket'] = jasmine.createSpy('deleteMarket');

      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValue([]);
      component.eventEntity = {
        name: 'TeamA vs TeamB'
      } as any;
      component.marketsGroup = [{
        templateMarketName: 'templateMarketName',
        filteredOutcomes: [],
        players: []
      }] as any;

      component.ngOnInit();

      expect(component['deleteEvent']).toHaveBeenCalledWith('event' as any);
      expect(component['deleteMarket']).toHaveBeenCalledWith('event');
    }));



    it('routingState.getCurrentUrl should not have been called', fakeAsync(() => {
      router.events.subscribe.and.callFake((cb) => cb('test'));

      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValue([]);
      component.eventEntity = {
        name: 'TeamA vs TeamB'
      } as any;
      component.marketsGroup = [{
        templateMarketName: 'templateMarketName',
        filteredOutcomes: [],
        players: []
      }] as any;

      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((p1, p2 , cb) => {
        return cb('test');
      });

      component.ngOnInit();

      expect(routingState.getCurrentUrl).not.toHaveBeenCalled();
    }));

    it('routingState getCurrentUrl should have been  called', fakeAsync(() => {
      router.events.subscribe.and.callFake((cb) => cb(
        new NavigationEnd(1, '/', '/')
      ));

      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValue([]);
      component.eventEntity = {
        name: 'TeamA vs TeamB'
      } as any;
      component.marketsGroup = [{
        templateMarketName: 'templateMarketName',
        filteredOutcomes: [],
        players: []
      }] as any;

      pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((p1, p2 , cb) => {
        return cb('test');
      });

      component.ngOnInit();

      expect(routingState.getCurrentUrl).toHaveBeenCalled();
    }));

  });

  describe('trackByIndex', () => {
    it('should call trackByIndex', () => {

      component.trackByIndex(20);

      expect(component['trackByIndex']).toBeTruthy();
    });

  });

  describe('filterMarketsForLoop', () => {
    it('should call playersScoresData', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;

      filtersService.orderBy = jasmine.createSpy('orderBy').and.returnValue(markets);
      component.getFilteredCleanOutcomes = jasmine.createSpy('getFilteredCleanOutcomes').and.returnValue(markets[0]);
      component.playersScoresData = jasmine.createSpy('playersScoresData').and.callFake((p1, p2, p3) => {
        return [markets[0]];
      });

      component.filterMarketsForLoop();

      expect(component['playersScoresData']).toHaveBeenCalled();
    });

  });

  describe('getPlayerScoreOutcome', () => {
    it('should call getPlayerScoreOutcome', () => {
      markets[0].outcomes = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 123,
        displayOrder: 1221,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        name: 'modifyOutcomes'
      }];
      component['sortedOutcomes'] = {
        '12outcomes':  [markets[0].outcomes]
      };

      component.getPlayerScoreOutcome(12, 33, 'outcomes');

      expect(component['getPlayerScoreOutcome']).toBeTruthy();
    });

  });

  describe('setMiddleScoreValue', () => {
    it('should call getPlayerScoreOutcome', () => {
      markets[0].outcomes = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 123,
        displayOrder: 1221,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        name: 'modifyOutcomes'
      }];
      component['sortedOutcomes'] = {
        '12outcomes':  [markets[0].outcomes]
      };
      component['playersScores'] = {
        filteredMarketId:  {
          playerName: {
            scores: [{
              score: 'scores',
              number: '1',
              outcomeid: 'outcomeid',
            }],
            displayArray: [
              {
                score: 'scores',
                number: '1',
                outcomeid: 'outcomeid',
              }
            ]
          }
        }
      };

      component['setMiddleScoreValue']('filteredMarketId', 'playerName');

      expect(component['setMiddleScoreValue']).toBeTruthy();
    });

  });


    describe('isDisabled', () => {
    it('result should be true', () => {
      markets[0].outcomes = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 123,
        displayOrder: 1221,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        name: 'name'
      }];
      component['sortedOutcomes'] = {
        '12outcomes':  markets[0].outcomes
      };

      component['eventEntity'] = {
        eventStatusCode:  'S',
        resulted: true
      } as any;

      const result = component.isDisabled(markets[0], 'name', 'outcomes');

      expect(result).toBe(true);
    });

    it('should return isNotActiveOutcomes', () => {
      markets[0].outcomes = [{
        correctPriceType: 'correctPriceType',
        correctedOutcomeMeaningMinorCode: 123,
        displayOrder: 1221,
        fakeOutcome: true,
        icon: true,
        id: 'id',
        name: 'name'
      }];
      component['sortedOutcomes'] = {
        '12outcomes':  markets[0].outcomes
      };

      component['eventEntity'] = {
        eventStatusCode:  'q',
        resulted: true
      } as any;

     const result =  component.isDisabled(markets[0], 'name', 'outcomes');

      expect(result).toBe(true);
    });
      beforeEach(() => {
        markets[0].outcomes = [{
          correctPriceType: 'correctPriceType',
          correctedOutcomeMeaningMinorCode: 123,
          displayOrder: 1221,
          fakeOutcome: true,
          icon: true,
          id: 'id',
          name: 'name',
          outcomeStatusCode: 'A'
        }];
      });


      it('should return isNotActiveEvent true', () => {
      component['sortedOutcomes'] = {
        '12outcomes':  markets[0].outcomes
      };

      component['eventEntity'] = {
        eventStatusCode:  'q',
        resulted: true
      } as any;

      const result = component.isDisabled(markets[0], 'name', 'outcomes');

       expect(result).toBe(true);
    });

    it('should return isNotActiveMarket true', () => {
      component['sortedOutcomes'] = {
        '12outcomes':  markets[0].outcomes
      };

      component['eventEntity'] = {
        eventStatusCode:  'q',
        resulted: false
      } as any;

      const result = component.isDisabled(markets[0], 'name', 'outcomes');

       expect(result).toBe(true);
    });

    it('should return false', () => {
      component['sortedOutcomes'] = {
        '12outcomes':  markets[0].outcomes
      };
      markets[0].marketStatusCode = 'P';

      component['eventEntity'] = {
        eventStatusCode:  'q',
        resulted: false
      } as any;

      const result = component.isDisabled(markets[0], 'name', 'outcomes');

       expect(result).toBe(false);
    });
  });


  describe('isDisplayed', () => {
    it('should call isDisplayed', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;

      component.isDisplayed();

      expect(component['isDisplayed']).toBeTruthy();
    });

  });

  describe('buildPlayersList', () => {
      beforeEach(() => {
        component['marketsGroup'] = {
          markets: markets
        } as any;

        markets[0].outcomes = {
          outcame: {
            correctPriceType: 'correctPriceType',
            correctedOutcomeMeaningMinorCode: 123,
            displayOrder: 1221,
            fakeOutcome: true,
            icon: true,
            id: 'id',
            name: 'modifyOutcomes'
          }
        };

        filtersService['filterPlayerName'] = jasmine.createSpy('filterPlayerName').and.callFake((p1) => {
          return 'playerName';
        });
    });
    it(' filtersService filterPlayerName should have been not called', () => {
      filtersService['filterPlayerName'] = jasmine.createSpy('filterPlayerName');
      markets[0].templateMarketName = 'Player_Stats_Tackles';

      component.buildPlayersList('modifyOutcomes', markets[0]);

      expect(filtersService['filterPlayerName']).not.toHaveBeenCalled();
    });

    it('setMiddleScoreValue should have benn called ', () => {
      component['setMiddleScoreValue'] = jasmine.createSpy('setMiddleScoreValue');

      markets[0].outcomes.outcame.name = ' to win 4+ Player_Stats_Tackles must to have this text';
      markets[0].templateMarketName = 'Player_Stats_Tackles';

      component.buildPlayersList('Player_Stats_Tackles', markets[0]);

      expect(component['setMiddleScoreValue']).toHaveBeenCalled();
    });

    it('setMiddleScoreValue should have not  been  called ', () => {
      component['setMiddleScoreValue'] = jasmine.createSpy('setMiddleScoreValue');

      markets[0].outcomes.outcame.name = ' to win 4+ Player_Stats_Tackles must to have this text';
      markets[0].templateMarketName = 'Player_Stats_Tackles';

      component.buildPlayersList('test', markets[0]);

      expect(filtersService['filterPlayerName']).not.toHaveBeenCalled();
    });

    it('setMiddleScoreValue should have  been  called ', () => {
      component['setMiddleScoreValue'] = jasmine.createSpy('setMiddleScoreValue');
      component['playersScores']['12Player_Stats_Tackles'] = {
        playerName: {
          scores: []
        }
      };

      markets[0].outcomes.outcame.name = ' to win 4+ Player_Stats_Tackles must to have this text';
      markets[0].outcomes.outcame.displayOrder = 'test';
      markets[0].templateMarketName = 'Player_Stats_Tackles';

      component.buildPlayersList('Player_Stats_Tackles', markets[0]);

      expect(component['setMiddleScoreValue']).toHaveBeenCalled();
    });
  });

  describe('modifyOutcomes', () => {

    it('filtersService  filterPlayerName should not have been called ', () => {

      component['marketsGroup'] = {
        markets: markets
      } as any;

      filtersService['filterPlayerName'] = jasmine.createSpy('filterPlayerName');

      markets[0].outcomes = {
        filter: jasmine.createSpy().and.callFake((cb) => {
          const outcame = {
            correctPriceType: 'correctPriceType',
            correctedOutcomeMeaningMinorCode: 123,
            displayOrder: 1221,
            fakeOutcome: true,
            icon: true,
            id: 'id',
            name: ['tes', 'tes']
          };
          cb(outcame);
        })
      };

      component.modifyOutcomes('modifyOutcomes', markets[0]);

      expect(filtersService['filterPlayerName']).not.toHaveBeenCalled();
    });

    it('filtersService  filterPlayerName should have been called ', () => {

      component['marketsGroup'] = {
        markets: markets
      } as any;

      filtersService['filterPlayerName'] = jasmine.createSpy('filterPlayerName');

      markets[0].outcomes = {
        filter: jasmine.createSpy().and.callFake((cb) => {
          const outcame = {
            correctPriceType: 'correctPriceType',
            correctedOutcomeMeaningMinorCode: 123,
            displayOrder: 1221,
            fakeOutcome: true,
            icon: true,
            id: 'id',
            name: ['modifyOutcomes', 'modifyOutcomes']
          };
          cb(outcame);
        })
      };

      component.modifyOutcomes('modifyOutcomes', markets[0]);

      expect(filtersService['filterPlayerName']).toHaveBeenCalled();
    });

  });

  describe('setHeaderTitle', () => {
    it('should call playersScoresData', () => {

      component.setHeaderTitle('Cards');

      expect(component['setHeaderTitle']).toBeTruthy();
    });

    it('should call playersScoresData', () => {

      component.setHeaderTitle('assists');

      expect(component['setHeaderTitle']).toBeTruthy();
    });

    it('should call playersScoresData', () => {

      component.setHeaderTitle('');

      expect(component['setHeaderTitle']).toBeTruthy();
    });

  });

  describe('getFilteredCleanOutcomes', () => {

    it('buildPlayersList should have been called ', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;
      markets[0].templateMarketName = [
        'Player_Stats_Shots',
        'Player_Stats_Shots test'
      ];

      component['buildPlayersList'] = jasmine.createSpy('buildPlayersList');
      component.getFilteredCleanOutcomes(markets[0], 'test');

      expect(component['buildPlayersList']).toHaveBeenCalledWith('test', markets[0]);
    });

    it('modifyOutcomes should have benn called ', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;
      markets[0].templateMarketName = [
        'Player_Stats_Shots',
        'Player_Stats_Shots test'
      ];

      component['modifyOutcomes'] = jasmine.createSpy('modifyOutcomes');
      component.getFilteredCleanOutcomes(markets[0], 'test');

      expect(component['modifyOutcomes']).toHaveBeenCalled();
    });

    it('buildPlayersList should not have been called ', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;
      markets[0].templateMarketName = [
        'Player_Stats',
        'Player_Stats test'
      ];

      component['buildPlayersList'] = jasmine.createSpy('buildPlayersList');
      component.getFilteredCleanOutcomes(markets[0], 'test');

      expect(component['buildPlayersList']).not.toHaveBeenCalled();
    });

    it('modifyOutcomes not to have been called', () => {
      component['marketsGroup'] = {
        markets: markets
      } as any;
      markets[0].templateMarketName = [
        'Player_Stats',
        'Player_Stats test'
      ];
      component['sortedOutcomes']['12test'] = 'qq';


      component['modifyOutcomes'] = jasmine.createSpy('modifyOutcomes');
      component.getFilteredCleanOutcomes(markets[0], 'test');

      expect(component['modifyOutcomes']).not.toHaveBeenCalled();
    });

  });


  it('ngOnDestroy', () => {
    component['routeChangeSuccessHandler'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(tag);
    expect(component['routeChangeSuccessHandler'].unsubscribe).toHaveBeenCalled();
  });

  it('ngOnDestroy should not call routeChangeSuccessHandler unsubscribe', () => {
    component['routeChangeSuccessHandler'] = '' as any;
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(tag);
  });

  it('sendUpdateStatisticGTM', () => {
    const marketEntity = {
      name: 'marketEntity name'
    };
    const player = {
      name: 'player name'
    };
    const value = 10;
    component.sendUpdateStatisticGTM(marketEntity, player, value);

    expect(yourCallPlayerStatsGTMService.sendChangeStatisticGTM).toHaveBeenCalled();
  });

  describe('calculateGTMEventLabel', () => {
    let sectionFlags;

    beforeEach(() => {
      sectionFlags = {
        wasCollapsed: true,
        wasExpanded: true
      };
      component['marketsGroup'] = {
        markets: markets
      } as any;
    });

    it('should not be defined for collapsed and expanded', () => {
      expect(component.calculateGTMEventLabel(true, sectionFlags)).toBeUndefined();
      expect(component.calculateGTMEventLabel(false, sectionFlags)).toBeUndefined();
    });

    it('should expand accordion by sectionFlags', () => {
      sectionFlags.wasCollapsed = false;
      sectionFlags.wasExpanded = true;
      expect(component.calculateGTMEventLabel(false, sectionFlags)).toEqual('collapse accordion ');
    });

    it('should expand accordion if isDefaultExpanded', () => {
      sectionFlags.wasCollapsed = true;
      sectionFlags.wasExpanded = false;
      expect(component.calculateGTMEventLabel(true, sectionFlags)).toEqual('collapse accordion ');

      sectionFlags.wasCollapsed = false;
      sectionFlags.wasExpanded = true;
      expect(component.calculateGTMEventLabel(true, sectionFlags)).toEqual('collapse accordion ');

      sectionFlags.wasCollapsed = false;
      sectionFlags.wasExpanded = false;
      expect(component.calculateGTMEventLabel(true, sectionFlags)).toEqual('collapse accordion ');
    });

    it('should collapse accordion by sectionFlags', () => {
      sectionFlags.wasCollapsed = true;
      sectionFlags.wasExpanded = false;
      expect(component.calculateGTMEventLabel(false, sectionFlags)).toEqual('expand accordion ');
    });

    it('should collapse accordion by sectionFlags with isDefaultExpanded', () => {
      sectionFlags.wasCollapsed = false;
      sectionFlags.wasExpanded = false;
      expect(component.calculateGTMEventLabel(false, sectionFlags)).toEqual('expand accordion ');
    });
  });

  describe('', () => {
    let marketsToggleState;
    const eventLabel = 'collapse accordion ';

    beforeEach(() => {
      marketsToggleState = {
        templateMarketName: 'Template name',
        wasCollapsed: true,
        wasExpanded: false
      };
      component.marketsToggleState = [marketsToggleState];
      component.mainMarketToggleState = marketsToggleState;
      component['marketsGroup'] = {
        markets: markets
      } as any;
    });

    describe('sendToggleMarketsGTM', () => {
      it('should call sendGTMData', () => {
        spyOn(component, 'calculateGTMEventLabel').and.returnValue(eventLabel);
        component.sendToggleMarketsGTM(0, true);

        expect(component.calculateGTMEventLabel).toHaveBeenCalledWith(true, marketsToggleState);
        expect(yourCallPlayerStatsGTMService.sendGTMData).toHaveBeenCalledWith(eventLabel, marketsToggleState.templateMarketName);
      });

      it('should not call sendGTMData', () => {
        spyOn(component, 'calculateGTMEventLabel').and.returnValue(undefined);
        component.sendToggleMarketsGTM(0, true);

        expect(yourCallPlayerStatsGTMService.sendGTMData).not.toHaveBeenCalled();
      });
    });

    describe('accordionsStateInit', () => {
      it('should call sendGTMData', () => {
        component['marketsGroup'] = {
          markets: markets
        } as any;
        component['accordionsStateInit']();

        expect(component['accordionsStateInit']).toBeTruthy();
      });
    });

    describe('sendMainMarketsGTM', () => {
      it('should call sendGTMData', () => {
        spyOn(component, 'calculateGTMEventLabel').and.returnValue(eventLabel);
        component.sendMainMarketsGTM(true);

        expect(component.calculateGTMEventLabel).toHaveBeenCalledWith(true, marketsToggleState);
        expect(yourCallPlayerStatsGTMService.sendGTMData).toHaveBeenCalledWith(eventLabel, jasmine.any(String));
      });

      it('should not call sendGTMData', () => {
        spyOn(component, 'calculateGTMEventLabel').and.returnValue(undefined);
        component.sendMainMarketsGTM(true);

        expect(yourCallPlayerStatsGTMService.sendGTMData).not.toHaveBeenCalled();
      });
    });
  });

  describe('getSwitchers', () => {
    it('component getSwitchers length should be 2', () => {
      component.eventEntity = {
        name: 'TeamA vs TeamB'
      } as any;
      const result: any = component.getSwitchers();
      result[0].onClick();

      expect(filtersService.getTeamName).toHaveBeenCalledTimes(2);
      expect(result.length).toEqual(2);
    });
  });

  describe('playersScoresData', () => {
    beforeEach(() => {
      component.playersScores = {
        '111(H)': {
          displayOrder: 1,
          name: 'some name'
        }
      } as any;
    });

    it('should order by displayOrder name', () => {
      component.playersScoresData('111', '(H)', true);
      expect(filtersService.orderBy).toHaveBeenCalledWith([1, 'some name'], ['displayOrder', 'name']);
    });

    it('should return playersScores by key', () => {
      const result = component.playersScoresData('111', '(H)', false);

      expect(filtersService.orderBy).not.toHaveBeenCalled();
      expect(result).toEqual(component.playersScores['111(H)']);
    });
  });
});
