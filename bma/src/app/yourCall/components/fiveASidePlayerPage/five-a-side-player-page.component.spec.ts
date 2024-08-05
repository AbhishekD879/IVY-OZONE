import { FiveASidePlayerPageComponent } from './five-a-side-player-page.component';
import { flush, tick, fakeAsync } from '@angular/core/testing';
import { Subject } from 'rxjs';
import {
  activeItemMock,
  activeMatrixFormation,
  eventEntityMock,
  playerMock
} from '@yourcall/components/fiveASidePlayerPage/five-a-side-player-page.component.mock';

describe('FiveASidePlayerPageComponent', () => {
  let component: FiveASidePlayerPageComponent;
  let yourCallMarketsService;
  let fiveASideBet;
  let fiveASideService;
  let infoDialogService;
  let localeService;
  let gtmService;
  let changeDetectorRef;
  let userService;

  beforeEach(() => {
    fiveASideService = {
      showView: jasmine.createSpy(),
      hideView: jasmine.createSpy(),
      activeItem: activeItemMock,
      activePlayer: playerMock,
      activeMatrixFormation: activeMatrixFormation,
      applyStatEdit: jasmine.createSpy('applyStatEdit'),
      restoreDefaultStat: jasmine.createSpy('restoreDefaultStat'),
      saveDefaultStat: jasmine.createSpy('saveDefaultStat'),
      playerListScrollPosition: jasmine.createSpy()
    };
    yourCallMarketsService = {
      getStatValues: jasmine.createSpy('getStatValues').and.returnValue({
        then: () => {
        }
      })
    };
    fiveASideBet = {
      clearRole: jasmine.createSpy('clearRole'),
      addRole: jasmine.createSpy('addRole'),
      setEditState: jasmine.createSpy('setEditState'),
      resetEditState: jasmine.createSpy('resetEditState'),
      playersObject: {
        id: {
          statValue: 4
        }
      },
      backupPlayers: jasmine.createSpy('backupPlayers'),
      restorePlayers: jasmine.createSpy('restorePlayers'),
      updateBet: jasmine.createSpy('updateBet'),
      clearPlayersBackup: jasmine.createSpy('clearPlayersBackup'),
      restorePlayersAfterStatChange: jasmine.createSpy('restorePlayersAfterStatChange')
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog').and.callFake((a, b, c, d, callback, arr) => {
        arr[0].handler();
        arr[1].handler();
      }),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('changeDetectorRef')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    userService = {
      oddsFormat: 'frac'
    };

    component = new FiveASidePlayerPageComponent(yourCallMarketsService, fiveASideBet, fiveASideService,
      infoDialogService, localeService, gtmService, changeDetectorRef, userService);
    component.item = { ...activeItemMock };
    component.player = playerMock;
    component.eventEntity = eventEntityMock;
  });

  it('should create FiveASidePlayerPageComponent', () => {
    expect(component).toBeTruthy();
  });

  it('should ngOninit', fakeAsync(() => {
    component.item = component.player = undefined;
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve());
    component.addDebounceListener = jasmine.createSpy('addDebounceListener');
    component.ngOnInit();
    flush();

    expect(component.playerStatMap.length).toBeGreaterThan(0);
    expect(component.subtitleEnding).toEqual('Shots On Target');
    expect(component.gradient).toEqual('linear-gradient(180deg, #777777 25%, rgba(119,119,119,0.90) 60%), url(/assets/shield.svg)');
    expect(yourCallMarketsService.getStatValues).toHaveBeenCalled();

    expect(component.buttonsModel).toBeUndefined();
    expect(component.addDebounceListener).toHaveBeenCalled();
    expect(component.isNoButtonsMarket).toEqual(false);
    expect(component.oddsFormat).toBeDefined();
    expect(fiveASideBet.backupPlayers).toHaveBeenCalled();
    expect(component.betButtonTitle).toBe('addPlayer');
  }));

  it('should ngOninit', () => {
    fiveASideService.activeItem.stat = 'To Be Carded';
    component.player.teamColors = undefined;
    component.ngOnInit();

    expect(component.gradient).toBeUndefined();
    expect(component.isNoButtonsMarket).toEqual(true);
  });

  it('ngOninit should set subtitleEnding to Goals', fakeAsync(() => {
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve());
    component.addDebounceListener = jasmine.createSpy('addDebounceListener');
    fiveASideService.activeItem = {
      rowIndex: 2,
      collIndex: 7,
      position: 'Sharpshooter',
      stat: 'To Concede',
      statId: 4,
      selected: true
    } as any;
    component.ngOnInit();
    flush();
    expect(component.subtitleEnding).toEqual('Goals');
    expect(component.isNoButtonsMarket).toEqual(false);
  }));
  it('ngOninit should set subtitleEnding to empty string', fakeAsync(() => {
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve());
    component.addDebounceListener = jasmine.createSpy('addDebounceListener');
    fiveASideService.activeItem = {
      rowIndex: 2,
      collIndex: 7,
      position: 'Sharpshooter',
      stat: 'To Be Carded',
      statId: 4,
      selected: true
    } as any;
    component.ngOnInit();
    flush();
    expect(component.subtitleEnding).toEqual('');
  }));

  it('ngOninit should set subtitleEnding to empty string', fakeAsync(() => {
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve());
    component.addDebounceListener = jasmine.createSpy('addDebounceListener');
    fiveASideService.activeItem = {
      rowIndex: 2,
      collIndex: 7,
      position: 'Sharpshooter',
      stat: 'To Keep A Clean Sheet',
      statId: 4,
      selected: true
    } as any;

    fiveASideService.activePlayer.position.short = 'GK';
    component.ngOnInit();
    flush();
    expect(component.subtitleEnding).toEqual('');
  }));

  it('#getStatValues: on getting response data', fakeAsync(() => {
    const data = {
      minValue: 1,
      maxValue: 2,
      average: 3
    };
    fiveASideService.activeItem.stat = 'Shots On Target';
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data }));
    component.ngOnInit();
    flush();

    expect(component.subtitleEnding).toEqual('Shots On Target');
    expect(yourCallMarketsService.getStatValues).toHaveBeenCalled();

    expect(component.buttonsModel).toEqual(data);
    expect(component.value).toEqual(data.average);
    expect(fiveASideBet.setEditState).toHaveBeenCalled();
  }));

  describe('ngOnInit', () => {
    it('should set correct average to Player - Add Mode', fakeAsync(() => {
      const data = {
        minValue: 1,
        maxValue: 2,
        average: 3
      };
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({data}));
      component.ngOnInit();
      flush();
      expect(component.value).toEqual(3);
      expect(component.buttonsModel.average).toEqual(3);
    }));

    it('should set correct average to Player - Edit Mode', fakeAsync(() => {
      fiveASideService.isEditMode = true;
      fiveASideService.activeItem = {
        roleId: 'id'
      } as any;
      fiveASideBet.playersObject = {
        id: {
          statValue: 4
        }
      } as any;
      const data = {
        minValue: 1,
        maxValue: 2,
        average: 3
      };
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({data}));
      component.ngOnInit();
      flush();
      expect(component.value).toEqual(4);
      expect(component.buttonsModel.average).toEqual(4);
      expect(component.betButtonTitle).toBe('updatePlayer');
    }));

    it('should call updateButtonsMarketsState', () => {
      component['updateButtonsMarketsState'] = jasmine.createSpy('updateButtonsMarketsState');

      component.ngOnInit();

      expect(component['updateButtonsMarketsState']).toHaveBeenCalled();
    });
  });

  describe('#addDebounceListener', () => {
    beforeEach(() => {
      component.role = jasmine.createSpyObj(['changeStatValue']);
    });
    it('', fakeAsync(() => {
      const prevSub = { unsubscribe: jasmine.createSpy('unsubscribe') } as any;
      component['subscription'] = prevSub;
      component.addDebounceListener();
      component['clicks'].next(1);
      tick(250);
      expect(prevSub.unsubscribe).toHaveBeenCalledTimes(1);
      expect(component.role.changeStatValue).toHaveBeenCalledWith(1);
    }));

    it('should call role.changeStatValue', fakeAsync(() => {
      component['clicks'] = new Subject();
      component.addDebounceListener();
      component['clicks'].next(1);
      tick(250);
      expect(component.role.changeStatValue).toHaveBeenCalledWith(1);
    }));

    it(`should debounce clicks`, fakeAsync(() => {
      component.addDebounceListener();
      component['clicks'].next(1);
      component['clicks'].next(2);
      component['clicks'].next(3);
      tick(250);
      expect(component.role.changeStatValue).toHaveBeenCalledTimes(1);
      expect(component.role.changeStatValue).toHaveBeenCalledWith(3);
    }));
  });

  describe('#addPlayer', () => {
    it(`should hideView (Case: formation found)`, () => {
      component.item = {
        rowIndex: 2,
        collIndex: 1,
        position: 'Baller',
        stat: 'Goals outside',
        statId: 6,
        roleId: 'position3'
      } as any;
      component.addPlayer();
      expect(fiveASideService.activeMatrixFormation[2].stat).toBe('Goals outside');
      expect(fiveASideService.applyStatEdit).toHaveBeenCalled();
      expect(fiveASideBet.resetEditState).toHaveBeenCalled();
      expect(fiveASideService.hideView).toHaveBeenCalled();
    });
    it(`should hideView (Case: formation not found)`, () => {
      component.item = {
        rowIndex: 3,
        collIndex: 6,
        position: 'Sniper',
        stat: 'Goals outside',
        statId: 3,
        roleId: 'position6'
      } as any;
      component.addPlayer();
      expect(fiveASideService.activeMatrixFormation[3].stat).toBe('Shots');
      expect(fiveASideService.applyStatEdit).toHaveBeenCalled();
      expect(fiveASideBet.resetEditState).toHaveBeenCalled();
      expect(fiveASideService.hideView).toHaveBeenCalled();
    });
  });

  describe('#backHandler', () => {
    it(`should show 'player-list' and clear role`, () => {
      component.item.roleId = 'id';
      component.backHandler();
      expect(fiveASideBet.resetEditState).toHaveBeenCalled();
      expect(fiveASideService.showView).toHaveBeenCalledWith({ view: 'player-list' });
      expect(component.fiveASideBet.clearRole).toHaveBeenCalledWith('id');
    });

    it('should hide View when Edit Mode enabled', () => {
      fiveASideService.isEditMode = true;
      component.backHandler();
      expect(fiveASideBet.restorePlayers).toHaveBeenCalled();
      expect(fiveASideBet.updateBet).toHaveBeenCalledTimes(1);
      expect(fiveASideService.hideView).toHaveBeenCalled();
    });
  });

  describe('removeSelection', () => {
    it('should show remove selection pop-up', () => {
      component.removeSelection();
      expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith('string', 'string', null, 'fiveASideRemoveSelDialog', null,
        [
          { caption: 'string', cssClass: 'btn-style4', handler: jasmine.any(Function) },
          { caption: 'string', handler: jasmine.any(Function) }
        ]);
    });
  });

  describe('updateButtonsMarketsState', () => {
    it('should set isNoButtonsMarket to true', () => {
      component['updateButtonsMarketsState']('To Be Carded');

      expect(component.isNoButtonsMarket).toBeTruthy();
    });

    it('should set isNoButtonsMarket to false', () => {
      component['updateButtonsMarketsState']('Shots On Target');

      expect(component.isNoButtonsMarket).toBeFalsy();
    });
  });

  describe('removePlayer', () => {
    it('should remove player', () => {
      component.item = {
        rowIndex: 1,
        collIndex: 2,
        position: 'string',
        stat: 'string',
        statId: 1,
        roleId: 'position1'
      };
      component['removePlayer']();
      expect(fiveASideService.restoreDefaultStat).toHaveBeenCalled();
      expect(fiveASideBet.resetEditState).toHaveBeenCalled();
      expect(fiveASideBet.clearRole).toHaveBeenCalled();
      expect(infoDialogService.closePopUp).toHaveBeenCalled();
      expect(fiveASideService.hideView).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalledWith(
        'trackEvent', {
          eventCategory: '5-A-Side',
          eventAction: 'Delete Player',
          eventLabel: 'string'
        }
      );
    });
  });

  describe('should ngOnDestroy', () => {
    it('ngOnDestroy', () => {
      component['subscription'] = <any>{
        unsubscribe: jasmine.createSpy('unsubscribe')
      };
      component.ngOnDestroy();
      expect(component['subscription'].unsubscribe).toHaveBeenCalled();
      expect(fiveASideBet.clearPlayersBackup).toHaveBeenCalled();
    });
  });

  describe('#changeValue', () => {
    beforeEach(() => {
      component.item.stat = 'Assists';
      component.buttonsModel = {
        minValue: 1,
        maxValue: 3,
        average: 2
      };
      component.value = component.buttonsModel.average;
      component['clicks'] = new Subject();
    });

    it('should changeValue', () => {
      component.changeValue('Plus' as any);

      expect(component.value).toEqual(3);
    });

    it('should changeValue', () => {
      component.buttonsModel = {
        minValue: 1,
        maxValue: 10,
        average: 1
      };
      component.value = 3;
      component.changeValue('Minus' as any);

      expect(component.value).toEqual(2);
    });

    it('should changeValue', () => {
      component.item.stat = 'Passes';
      component.buttonsModel = {
        minValue: 1,
        maxValue: 10,
        average: 5
      };
      component.value = 5;
      component.changeValue('Plus' as any);

      expect(component.value).toEqual(10);
    });

    it('should`t changeValue if value not changed', () => {
      component.buttonsModel = {
        minValue: 1,
        maxValue: 10,
        average: 5
      };
      component.value = 1;
      component.changeValue('Minus' as any);

      expect(component.value).toEqual(1);
    });

    it('should`t changeValue if buttonsModel empty', () => {
      component.buttonsModel = undefined;
      component.value = 0;
      component.changeValue('Minus' as any);

      expect(component.value).toEqual(0);
    });
  });

  describe('@createPlayerStatMap', () => {
    it('not GK markets', () => {
      component.player.position.short = 'MF';
      component['createPlayerStatMap']();
      expect(component.playerStatMap[1].statLabel).toBe('goals');
      expect(component.playerStatMap[1].statValue).toBe(0);
      expect(component.playerStatMap[4].statLabel).toBe('passes');
      expect(component.playerStatMap[4].statValue).toBe(35);
    });

    it('GK markets', () => {
      component.player.isGK = true;
      component['createPlayerStatMap']();
      expect(component.playerStatMap[1].statLabel).toBe('conceeded');
      expect(component.playerStatMap[1].statValue).toBe(3);
      expect(component.playerStatMap[4].statLabel).toBe('penaltySaves');
      expect(component.playerStatMap[4].statValue).toBe(5);
    });
  });

  it('#changeStat', fakeAsync( () => {
    fiveASideService.isEditMode = true;
    const data = {
      minValue: 1,
      maxValue: 2,
      average: 7
    };
    yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data }));

    const newStat = { id: 6, title: 'Assists' } as any;

    component.changeStat(newStat);
    flush();
    expect(fiveASideService.saveDefaultStat).toHaveBeenCalledTimes(1);
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: '5-A-Side',
      eventAction: 'Edit Market',
      eventLabel: 'Assists'
    });
    expect(component.item.stat).toBe(newStat.title);
    expect(component.item.statId).toBe(newStat.id);
    expect(component.value).toBe(7);
    expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({ obEventId: '8', playerId: 18, statId: 6 });
  }));
});
