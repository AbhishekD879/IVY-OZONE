import { YourCallMarketPlayerBetsComponent } from './your-call-market-player-bets.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('YourCallMarketPlayerBetsComponent', () => {
  let component: YourCallMarketPlayerBetsComponent;

  const market = {
    obtainedStatValuesToDisplay: undefined,
    obtainedPlayerFeed: [],
    obtainedStatValues: 'obtainedStatValues',
    key: 'keyMarket',
    playerObj: undefined,
    statObj: {statobj: 'stat'},
    stat: {stat: 'stat'}
  };


  /**
   * WARNING!
   * All those mocks below are outside "beforeEach" cycle,
   * do not rely on them as they're probably redefined in specs while executing..
   *
   * TODO: refactor and fix this spec not to have const-alike mocks definition
   */
  const pubSubService = {
    publish: jasmine.createSpy('publish'),
    API: {
      YC_NOTIFICATION_TOGGLED: 'YC_NOTIFICATION_TOGGLED'
    }
  } as any;
  const yourcallDashboardService = {
    getStatValues: jasmine.createSpy('getStatValues'),
    trackEditingPlayerBet: jasmine.createSpy('trackEditingPlayerBet')
  } as any;
  const localeService = {
    getString: jasmine.createSpy().and.returnValue('select')
  } as any;
  const yourcallMarketsService = {
    isRestoredNeeded: jasmine.createSpy('isRestoredNeeded').and.returnValue(true),
    betsArrayToRestore: jasmine.createSpy('betsArrayToRestore').and.returnValue(['first']),
    restoredMarketDone: jasmine.createSpy('restoredMarketDone'),
    onMarketToggled: jasmine.createSpy('onMarketToggled'),
    getStatisticsForPlayer: jasmine.createSpy('getStatisticsForPlayer').and.returnValue(Promise.resolve({
      data: [{ title: 'B' }, { title: 'A' }]
    })),
    getStatValues: jasmine.createSpy('getStatValues').and.returnValue(Promise.resolve({})),
    editSelection: jasmine.createSpy('editSelection'),
    trackSelectingPlayerBet: jasmine.createSpy('trackSelectingPlayerBet'),
    selectValue: jasmine.createSpy('selectValue'),
    addSelection: jasmine.createSpy('addSelection'),
    playerStatsCache: {
      11003002: {
        data: {}
      }
    },
    statsValuesCache: {
      11: {
        data: {}
      }
    },
    updatedStatValsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
    updatedPlayersubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
    },
    updatedStatsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
    },
  } as any;
  const routingState = {
    getRouteParam: jasmine.createSpy().and.returnValue(1003002)
  } as any;
  const activatedRoute = {} as any;

  const changeDetectorRef = {
    markForCheck: jasmine.createSpy('markForCheck')
  } as any;

  beforeEach(() => {
    jasmine.clock().uninstall();
    jasmine.clock().install();

    component = new YourCallMarketPlayerBetsComponent(
      yourcallMarketsService,
      localeService,
      pubSubService,
      yourcallDashboardService,
      routingState,
      activatedRoute,
      changeDetectorRef
    );

    component.market = {
      obtainedStatValuesToDisplay: undefined,
      obtainedPlayerFeed: [],
      obtainedStatValues: 'obtainedStatValues',
      key: 'keyMarket',
      playerObj: undefined,
      statObj: {
        statobj: 'stat'
      },
      stat: {
        stat: 'stat'
      }
    };

    component.selectedInfo = {
      player: undefined,
      stat: {
        stat: 'new stat'
      },
      statVal: {
        statVal: 'statVal'
      }
    } as any;

    (component['PASSES_INCREMENTS'] as any) = 5;
    component.editMode = false;
    component.marketInfo = 'marketInfo';
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should call restoredMarketDone', fakeAsync(() => {
      component['restoreBet'] = jasmine.createSpy('restoreBet').and.returnValue(Promise.resolve);
      component.ngOnInit();

      tick();
      expect(component.obtainedPlayerFeed).toEqual([]);
      expect(component.obtainedStatValues).toEqual('obtainedStatValues');
      expect(component.selectedStatValuesModel).toEqual({stat: 'stat'} as any);
      expect(component.selectedStatModel).toEqual({statobj: 'stat'});
      expect(component.obtainedStatValuesToDisplay).toEqual([]);
      expect(component.selectedInfo.player).toEqual(null);
      expect(component.selectedInfo.stat).toEqual({statobj: 'stat'});
      expect(component.selectedInfo.statVal).toEqual({stat: 'stat'});
      expect(component.playerLabel).toEqual('select');
      expect(component.statLabel).toEqual('select');
    //   expect(yourcallMarketsService.restoredMarketDone).toHaveBeenCalledWith('keyMarket');
    }));

    it('should catch error and call restoredMarketDone1', fakeAsync(() => {
      yourcallMarketsService.betsArrayToRestore.and.returnValue(throwError(['err']));
      yourcallMarketsService.betsArrayToRestore = jasmine.createSpy('betsArrayToRestore').and.returnValue(['first']);
      component['restoreBet'] = jasmine.createSpy().and.returnValue(throwError('err'));

      component.ngOnInit();

      tick();
    //   expect(yourcallMarketsService.restoredMarketDone).toHaveBeenCalledWith('keyMarket');
    }));

    it('should call restoredMarketDone when promise reject', fakeAsync(() => {
      component['restoreBet'] = jasmine.createSpy('restoreBet').and.returnValue(Promise.reject);
      localeService.getString.and.returnValue('change');
      yourcallMarketsService.betsArrayToRestore = jasmine.createSpy('betsArrayToRestore').and.returnValue(['first']);
      component.hideButton = true;
      component.ngOnInit();

      tick();
      expect(component.playerLabel).toEqual('change');
      expect(component.statLabel).toEqual('change');
    //   expect(yourcallMarketsService.restoredMarketDone).toHaveBeenCalledWith('keyMarket');
    //   expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));

    it('should not do promise.all()', () => {
      component.editMode = true;
      yourcallMarketsService.isRestoredNeeded.and.returnValue(false);
      component.ngOnInit();

      expect(component.selectedPlayerModel).toEqual(undefined);
      expect(component.selectedStatModel).toEqual({statobj: 'stat'});
      expect(component.selectedStatValuesModel).toEqual({stat: 'stat'} as any);
    });

    // it('should catch error and call restoredMarketDone', fakeAsync(() => {
    //   yourcallMarketsService.isRestoredNeeded.and.returnValue(true);
    //   yourcallMarketsService.betsArrayToRestore = jasmine.createSpy('betsArrayToRestore').and.returnValue(['first']);
    //   component['restoreBet'] = jasmine.createSpy().and.returnValue(Promise.reject());
    //   component.ngOnInit();

    //   tick();
    // //   expect(yourcallMarketsService.restoredMarketDone).toHaveBeenCalledWith('keyMarket');
    // //   expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    // }));
  });

  describe('#setDefaultValues', () => {
    it('set default values if market is available', () => {
      component.market.playerObj = {
        name: 'Name'
      };
      component.setDefaultValues();


      expect(component.selectedInfo.player).toEqual({
        name: 'Name'
      });
      expect(component.selectedInfo.stat).toEqual({
        statobj: 'stat'
      });
      expect(component.selectedInfo.statVal).toEqual({
        stat: 'stat'
      });
      expect(component.obtainedPlayerFeed).toEqual([]);
      expect(component.obtainedStatValues).toEqual('obtainedStatValues');
    });

    it('set default values if market is not available', () => {
      component.market.playerObj = null;
      component.market.statObj = null;
      component.market.stat = null;

      component.setDefaultValues();

      expect(component.selectedInfo.player).toEqual(undefined);
      expect(component.selectedInfo.stat).toEqual({
        stat: 'new stat'
      });
      expect(component.selectedInfo.statVal).toEqual({
        statVal: 'statVal'
      });
      expect(component.obtainedPlayerFeed).toEqual([]);
      expect(component.obtainedStatValues).toEqual('obtainedStatValues');
    });
  });

  describe('#onPlayerUpdate', () => {
    it('should call onMarketToggled when selectedPlayerModel = null', () => {
      component.selectedPlayerModel = 'null';
      component.onPlayerUpdate();

      expect(pubSubService.publish).toHaveBeenCalledWith('YC_NOTIFICATION_TOGGLED');
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalledWith(50);
    });

    it('should call onMarketToggled when selectedPlayerModel available', fakeAsync(() => {
      const player = {
        id: 1,
        name: 'new name'
      };
      component.selectedPlayerModel = player;
      component.obEventId = '1003002';
      yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({}));
      component.onPlayerUpdate();

      tick();
      expect(component.selectedInfo.player).toEqual(player);
      expect(component.market.disable).toEqual(true);
      expect(pubSubService.publish).toHaveBeenCalledWith('YC_NOTIFICATION_TOGGLED');
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));
  });

  describe('#onStatsUpdate', () => {
    it('should call onMarketToggled when selectedStatModel = null', () => {
      component.selectedStatModel = 'null';
      component.onStatsUpdate();

      expect(component.obtainedStatValues).toEqual(null);
      expect(component.obtainedStatValuesToDisplay).toEqual([]);
      expect(component.selectedStatValuesModel).toEqual(null);
      expect(pubSubService.publish).toHaveBeenCalledWith('YC_NOTIFICATION_TOGGLED', false);
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalledWith(50);
    });

    it('should not call trackEditingPlayerBet', fakeAsync(() => {
      const player = {
        id: 1,
        name: 'new name'
      };
      const data = {
        average: 1,
        maxValue: 10,
        minValue: 1
      };
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component.selectedPlayerModel = player;
      component.editMode = false;
      component.obEventId = '1003002';
      yourcallMarketsService.getStatValues.and.returnValue(Promise.resolve({data}));
      component['prepareStatsValues'] = jasmine.createSpy('prepareStatsValues');

      component.onStatsUpdate();

      tick();
      expect(component.selectedInfo.stat).toEqual({title: 'Shots', id: 1});
      expect(yourcallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '1003002',
        playerId: 1,
        statId: 1
      });
      expect(component['triggerUpdate']).toEqual(true);
      expect(component.obtainedStatValues).toEqual(data);
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
      expect(yourcallDashboardService.trackEditingPlayerBet).not.toHaveBeenCalled();
    }));

    it('should call getStatValues', fakeAsync(() => {
      const player = {
        id: 1,
        name: 'new name'
      };
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component.selectedPlayerModel = player;
      component.obEventId = '1003002';
      component.onStatsUpdate();

      tick();
      expect(component.selectedInfo.stat).toEqual({title: 'Shots', id: 1});
      expect(yourcallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '1003002',
        playerId: 1,
        statId: 1
      });
    }));

    it('should call trackEditingPlayerBet', fakeAsync(() => {
      const player = {
        id: 1,
        name: 'new name'
      };
      const data = {
        average: 1,
        maxValue: 10,
        minValue: 1
      };
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component.selectedPlayerModel = player;
      component.editMode = true;
      component.obEventId = '1003002';
      yourcallMarketsService.getStatValues.and.returnValue(Promise.resolve({data}));
      component['prepareStatsValues'] = jasmine.createSpy('prepareStatsValues');

      component.onStatsUpdate();

      tick();
      expect(component.selectedInfo.stat).toEqual({title: 'Shots', id: 1});
      expect(yourcallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '1003002',
        playerId: 1,
        statId: 1
      });
      expect(component['triggerUpdate']).toEqual(true);
      expect(component.obtainedStatValues).toEqual(data);
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalled();
    //   expect(yourcallDashboardService.trackEditingPlayerBet).toHaveBeenCalledWith('statistic', {
    //     player: undefined,
    //     stat: { title: 'Shots', id: 1 },
    //     statVal: { statVal: 'statVal' }
    //   });
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    }));
    it('shoiuld return  nothing', fakeAsync(() => {
      const player = {
        id: 1,
        name: 'new name'
      };
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component.selectedPlayerModel = player;
      component.editMode = true;
      component.obEventId = '1003002';
      yourcallMarketsService.getStatValues.and.returnValue(Promise.resolve({}));
      yourcallMarketsService.onMarketToggle = jasmine.createSpy('onMarketToggle');
      component['prepareStatsValues'] = jasmine.createSpy('prepareStatsValues');

      component.onStatsUpdate();

      tick();
      expect(yourcallMarketsService.onMarketToggle).not.toHaveBeenCalled();
    }));
  });

  describe('#onStatValueChange', () => {
    it('should cvall only trackEditingPlayerBet', () => {
      component.hideButton = false;
      component.onStatValueChange();

    //   expect(yourcallDashboardService.trackEditingPlayerBet).toHaveBeenCalledWith('statVal', {
    //     player: undefined,
    //     stat: {stat: 'new stat'},
    //     statVal: null
    //   });
    });
    it('should call editSelection', () => {
      component.hideButton = true;
      component.selectedStatValuesModel = 'selectedStatValuesModel';
      component.selectionMarket = jasmine.createSpy('selectionMarket').and.returnValue({
        id: 1,
        stat: 'stat'
      });
      component.onStatValueChange();

    //   expect(yourcallDashboardService.trackEditingPlayerBet).toHaveBeenCalledWith('statVal', {
    //     player: undefined,
    //     stat: {stat: 'new stat'},
    //     statVal: 'selectedStatValuesModel'
    //   });
      expect(yourcallMarketsService.editSelection).toHaveBeenCalledWith('marketInfo', market, {id: 1,
        stat: 'stat'
      });
      expect(pubSubService.publish).toHaveBeenCalledWith('YC_NOTIFICATION_TOGGLED');
    });
  });

  describe('#done', () => {
    it('should call all services', () => {
      component.selectedPlayerModel = {name: 'player name'};
      component.selectedStatModel = {title: 'stat title'};
      component.selectedStatValuesModel = 'selectedStatValuesModel';
      component.selectionMarket = jasmine.createSpy('selectionMarket').and.returnValue({
        id: 1,
        stat: 'stat'
      });
      component.done();

    //   expect(yourcallMarketsService.trackSelectingPlayerBet).toHaveBeenCalledWith('player name', 'stat title', 'selectedStatValuesModel');
      expect(yourcallMarketsService.selectValue).toHaveBeenCalledWith(market, {id: 1,
        stat: 'stat'
      });
    });
  });

  describe('#saveEditChanges', () => {
    it('should call editSelection', () => {
      const selection = {gameId: '1', obtainedPlayerFeed: 'obtainedPlayerFeed'};
      component.selectionMarket = jasmine.createSpy('selectionMarket').and.returnValue({
        id: 1,
        stat: 'stat'
      });

      component.saveEditChanges(selection as any);

      expect(yourcallMarketsService.editSelection).toHaveBeenCalledWith(market, selection, {
        id: 1,
        stat: 'stat'
      });
    });
  });

  describe('#trackBy', () => {
    it('should get result from trackByStats', () => {
      const result = component.trackByStats(1, 2);

      expect(result).toEqual('12');
    });
    it('should get result from trackByPlayers', () => {
      const player = {
        id: 1,
        name: 'player name',
        team: {
          id: 1
        }
      };
      const result = component.trackByPlayers(1, player as any);

      expect(result).toEqual('11');
    });
    it('should get result from trackByFeed', () => {
      const feed = {
        id: 1,
      };

      const result = component.trackByFeed(1, feed);

      expect(result).toEqual(1);
    });
  });

  describe('#selectionMarket', () => {
    it('should return selection', () => {
      const baseTime = new Date();
      component.selectedInfo = {
        player: {
          name: 'player name'
        },
        stat: {
          title: 'stat title',
          id: 1
        }
      } as any;

      component.market.players = [
        {
          position: {
            title: 'Goalkeeper',
          },
          name: 'O. Kahn'
        },
        {
          position: {
            title: 'Forward',
          },
          name: 'T. Henry'
        }
      ] as any;

      jasmine.clock().mockDate(baseTime);

      const result = component.selectionMarket(true);

      expect(result).toEqual({
        selectedInfo: {
          player: {
            name: 'player name'
          },
          stat: {
            title: 'stat title',
            id: 1
          }
        },
        obtainedPlayerFeed: undefined,
        obtainedStatValues: undefined,
        obtainedStatValuesToDisplay: undefined,
        id: baseTime.getTime(),
        marketType: 'playerBets',
        players: [
          {
            position: {
              title: 'Goalkeeper',
            },
            name: 'O. Kahn'
          },
          {
            position: {
              title: 'Forward',
            },
            name: 'T. Henry'
          }
        ],
        filteredPlayers: [
          {
            position: {
              title: 'Forward',
            },
            name: 'T. Henry'
          }
        ],
        player: 'player name',
        playerObj: {
          name: 'player name'
        },
        statObj: {
          title: 'stat title',
          id: 1
        },
        playerId: undefined,
        statistic: 'stat title',
        stat: undefined,
        statisticId: 1,
        type: 1,
        value: undefined,
        condition: 3,
        odds: {
          type: 1,
          condition: 3,
          value: undefined
        },
        gameId: undefined,
        edit: true,
        disable: false
      } as any);

    });
  });

  describe('#oddsObj', () => {
    it('should return oddsObj', () => {
      const result = component['oddsObj']();

      expect(result).toEqual({
        type: 1,
        condition: 3,
        value: {
          statVal: 'statVal'
        }
      } as any);
    });
  });

  describe('#getAverage', () => {
    it('should return minValue', () => {
      component.obtainedStatValues = {
        average: '1',
        maxValue: '30',
        minValue: '10'
      };

      expect(component['average']).toBe('10');
    });
    it('should return maxValue', () => {
      component.obtainedStatValues = {
        average: '15',
        maxValue: '10',
        minValue: '1'
      };

      expect(component['average']).toEqual('10');
    });
    it('should return obtainedStatValues.average', () => {
      component.obtainedStatValues = {
        average: 5,
        maxValue: 10,
        minValue: 1
      };

      expect(component['average'] as any).toEqual(5);
    });
  });

  describe('#prepareStatsValues', () => {
    beforeEach(() => {
      component.ngOnInit();
      component.obtainedStatValues = {
        maxValue: 30,
        minValue: 10
      };
    });

    it('should prepare stats values', () => {
      component.selectedStatModel = {
        title: 'Shots'
      };
      component['prepareStatsValues']();

      expect(component.obtainedStatValuesToDisplay).toEqual(
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]);
      expect(component.market.disable).toEqual(false);
      expect(component['triggerUpdate']).toEqual(false);
    });

    it('should prepare stats values only for Passes', () => {
      component.selectedStatModel = {
        title: 'Passes'
      };
      component['prepareStatsValues']();

      expect(component.obtainedStatValuesToDisplay).toEqual([10, 15, 20, 25, 30]);
      expect(component.market.disable).toEqual(false);
      expect(component['triggerUpdate']).toEqual(false);
    });

    it('should prepare stats values only for Passes', () => {
      component.selectedStatModel = {
        title: 'Passes'
      };
      component.obtainedStatValues = {
        average: '15',
        maxValue: '10',
        minValue: '1'
      };
      component.selectedStatValuesModel = undefined;
      component['prepareStatsValues']();

      expect(component.selectedStatValuesModel).toEqual('10');
    });

    it('should prepare stats values only for Passes', () => {
      component.selectedStatModel = {
        title: 'Passes'
      };
      component.hideButton = true;
      component['triggerUpdate'] = true;
      component.selectionMarket = jasmine.createSpy('selectionMarket').and.returnValue({});
      component['prepareStatsValues']();

      expect(yourcallMarketsService.editSelection).toHaveBeenCalled();
    });
  });

//   describe('#restoreBet', () => {
//     it('should catch error when minValue < value < maxValue', fakeAsync(() => {
//       yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
//         data: [{
//           title: 'statisticTitle',
//           minValue: 1,
//           maxValue: 10
//         }]
//       }));
//       yourcallMarketsService.getStatValues.and.returnValue(Promise.resolve({
//         data: {
//           minValue: 1,
//           maxValue: 10
//         }
//       }));
//       component.market.players = [{
//         name: 'player name',
//         position: {
//           title: 'Defender'
//         },
//         id: 1
//       }];
//       component.obEventId = '123';

//       component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 25 }).catch(() => {});
//       tick();

//       expect(yourcallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
//         obEventId: '123',
//         playerId: 1
//       });
//       expect(yourcallMarketsService.getStatValues).toHaveBeenCalledWith({
//         obEventId: '123',
//         playerId: 1,
//         statId: undefined
//       });
//       expect(yourcallMarketsService.addSelection).not.toHaveBeenCalled();
//     }));

//     it('should catch error from getStatisticsForPlayer', fakeAsync(() => {
//       yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.reject('error'));
//       component.market.players = [{
//         name: 'player name',
//         id: 1,
//         position: {
//           title: 'Defender'
//         }
//       }];
//       component.obEventId = '123';

//       component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 }).catch(error => {
//         expect(error).toEqual('error');
//       });
//       tick();

//       expect(yourcallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
//         obEventId: '123',
//         playerId: 1
//       });
//       expect(yourcallMarketsService.getStatValues).not.toHaveBeenCalledWith();
//       expect(yourcallMarketsService.addSelection).not.toHaveBeenCalled();
//     }));
//     it('should call yourcallMarketsService.addSelection', fakeAsync(() => {
//       yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
//         data: [{
//           title: 'statisticTitle',
//           minValue: 1,
//           maxValue: 10
//         }]
//       }));
//       yourcallMarketsService.getStatValues.and.returnValue(Promise.resolve({
//         data: {
//           minValue: 1,
//           maxValue: 10
//         }
//       }));
//       component.market.players = [{
//         name: 'player name',
//         id: 1,
//         position: {
//           title: 'Defender'
//         }
//       }];
//       component.obEventId = '123';
//       component['restoreBet']({playerName: 'player name', statisticTitle: 'statisticTitle', value: 10});

//       tick();
//       expect(yourcallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
//         obEventId: '123',
//         playerId: 1
//       });
//       expect(yourcallMarketsService.getStatValues).toHaveBeenCalledWith({
//         obEventId: '123',
//         playerId: 1,
//         statId: undefined
//       });
//       expect(yourcallMarketsService.addSelection).toHaveBeenCalled();
//       expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
//     }));

//     it('should catch error', fakeAsync(() => {
//       yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
//         data: [{
//           title: 'statisticTitle',
//           minValue: 1,
//           maxValue: 10
//         }]
//       }));
//       component.market.players = [{
//         name: 'player name',
//         id: 1,
//         position: {
//           title: 'Defender'
//         }
//       }];
//       yourcallMarketsService.getStatValues.and.returnValue(Promise.reject());
//       yourcallMarketsService.addSelection = jasmine.createSpy('addSelection');
//       component['restoreBet']({playerName: 'player name', statisticTitle: 'statisticTitle', value: 10}).then(() => {
// eslint-disable-next-line 
//         console.log('ee');
//       }, () => {
// eslint-disable-next-line
//         console.log('ddd');
//       });
//       tick();
//       expect(yourcallMarketsService.addSelection).not.toHaveBeenCalled();
//     }));
//   });

  describe('#toInitState', () => {
    it('should clear all values', () => {
      component['toInitState'](true);

      expect(component.selectedPlayerModel).toEqual(null);
      expect(component.selectedStatValuesModel).toEqual(null);
      expect(component.obtainedPlayerFeed).toEqual(null);
      expect(component.obtainedStatValues).toEqual(null);
      expect(component.obtainedStatValuesToDisplay).toEqual([]);
      expect(component.selectedInfo.player).toEqual(null);
      expect(component.selectedInfo.stat).toEqual(null);
      expect(component.selectedInfo.statVal).toEqual(null);
    });
  });

  describe('#checkForSelectedValues', () => {
    it('it should have obtainedStatValues', () => {
      component.selectedPlayerModel = {name: 'player name', id: 1};
      component.obEventId = '1003002';
      component.obtainedPlayerFeed = null;
      component.obtainedStatValues = null;
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component['prepareStatsValues'] = jasmine.createSpy('prepareStatsValues');

      component['checkForSelectedValues']();

      expect(component.obtainedPlayerFeed).toEqual({} as any);
      expect(component.obtainedStatValues).toEqual({} as any);
    });

    it('should not have obtainedPlayerFeed', () => {
      component.selectedPlayerModel = undefined;

      component['checkForSelectedValues']();

      expect(component.obtainedPlayerFeed).toEqual(undefined);
    });

    it('should not have obtainedStatValues', () => {
      component.selectedPlayerModel = {name: 'player name', id: 1};
      component.obEventId = '1003002';
      component.obtainedPlayerFeed = null;

      component['checkForSelectedValues']();

      expect(component.obtainedStatValues).toEqual(undefined);
    });

    it('should obtainedPlayerFeed to equel obtainedPlayerFeed', () => {
      component.selectedPlayerModel = {name: 'player name', id: 1};
      component.obEventId = '1003002';
      component.obtainedPlayerFeed = { id: '1', min: 1, max: 10} as any;

      component['checkForSelectedValues']();

      expect(component.obtainedPlayerFeed).toEqual({ id: '1', min: 1, max: 10} as any);
    });

    it('should obtainedStatValues to equel obtainedStatValues', () => {
      component.selectedPlayerModel = {name: 'player name', id: 1};
      component.obEventId = '1003002';
      component.obtainedPlayerFeed = { id: '1', min: 1, max: 10} as any;
      component.obtainedStatValues = 'obtainedStatValues';
      component.selectedStatModel = {
        title: 'Shots',
        id: 1
      };
      component['prepareStatsValues'] = jasmine.createSpy('prepareStatsValues');

      component['checkForSelectedValues']();

      expect(component.obtainedPlayerFeed).toEqual({ id: '1', min: 1, max: 10} as any);
      expect(component.obtainedStatValues).toEqual('obtainedStatValues');
    });
  });

  afterEach(() => {
    jasmine.clock().uninstall();
  });

  describe('onPlayerUpdate', () => {

    it('should update Player', fakeAsync(() => {
      component.market = {};
      component.selectedPlayerModel = { id: 12, title: 'Shots' };
      component.selectedInfo = {
        player: {},
        stat: 1,
        statVal: 1,
        obtainedStatValuesToDisplay: [10, 15, 20, 25, 30]
      };
      yourcallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{ title: 'B' }, { title: 'A' }]
      }));

      component.onPlayerUpdate();
      tick();

      expect(component.selectedInfo.player).toEqual({ id: 12, title: 'Shots' });
      expect(component.obtainedPlayerFeed).toEqual([{ title: 'A'}, { title: 'B'}] as any);
      expect(component.market.disable).toEqual(true);
      expect(yourcallMarketsService.onMarketToggled).toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith('YC_NOTIFICATION_TOGGLED');
    }));
  });
});
