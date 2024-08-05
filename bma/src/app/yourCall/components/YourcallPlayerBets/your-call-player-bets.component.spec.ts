import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { YourCallPlayerBetsComponent } from './your-call-player-bets.component';
import { playerListObj, storage } from './your-call-player-bets.mock';

describe('YourCallPlayerBetsComponent', () => {
  let yourCallMarketsService, fiveASideService, changeDetector, bybSelectedSelectionsService;
  let yourcallProviderService, componentFactoryResolver, dialogService, infoDialogService, localeService, windowRefService;
  let component: YourCallPlayerBetsComponent;
  let selection, selection2;

  beforeEach(() => {
    selection2 = {
      'obtainedPlayerFeed': {}, 'selectedInfo': undefined, 'obtainedStatValues': {}, 'obtainedStatValuesToDisplay': {}, 'marketType': '1',
      'players': undefined, 'playerObj': {}, 'statObj': {}, 'gameId': '16', 'iddInc': {}, 'relatedTeamType': 1, 'relatedPlayerId': 1,
      'title': 'R. Ronaldo', 'status': 1, 'odds': '1', 'bettingValue1': '1', 'bettingValue2': '1',
      'displayOrder': 1, 'id': 1, 'playerId': 1, 'statistic': '1', 'value': 1, 'type': 1, 'idd': ''
    };
    selection = {
      'obtainedPlayerFeed': {}, 'selectedInfo': {}, 'obtainedStatValues': {}, 'obtainedStatValuesToDisplay': {}, 'marketType': '1',
      'players': undefined, 'playerObj': {}, 'statObj': {}, 'gameId': '16', 'iddInc': {}, 'relatedTeamType': 1, 'relatedPlayerId': 1,
      'title': 'Ronaldo', 'status': 1, 'odds': '1', 'bettingValue1': '1', 'bettingValue2': '1',
      'displayOrder': 1, 'id': 1, 'playerId': 1, 'statistic': '1', 'value': 1, 'type': 1, 'idd': ''
    };
    yourCallMarketsService = {
      addSelection: jasmine.createSpy('addSelection'),
      removeSelection: jasmine.createSpy('removeSelection'),
      selectValue: jasmine.createSpy('selectValue'),
      selectedSelectionsSet: new Set(),
      getStatisticsForPlayer: jasmine.createSpy('getStatisticsForPlayer').and.returnValue({
        then: () => {
        }
      }),
      isRestoredNeeded: jasmine.createSpy('isRestoredNeeded').and.returnValue(true),
      betsArrayToRestore: jasmine.createSpy('betsArrayToRestore').and.returnValue({}),
      restoredMarketDone: jasmine.createSpy('restoredMarketDone').and.returnValue({}),
      getStatValues: jasmine.createSpy('getStatValues').and.returnValue({
        then: () => {
        }
      }),
      playerBetRemovalsubject$ : {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      betPlacedStatus$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      showBetRemovalsubject$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      },
      oldNewplayerStatIdsubject$: {
        subscribe: jasmine.createSpy('subscribe').and.returnValue(of(true)),
        next: jasmine.createSpy('next').and.returnValue(of(true))
      }
    };
    fiveASideService = {
      getFormations: jasmine.createSpy('getFormations').and.returnValue(of([{
        id: '1',
        actualFormation: '1-1-1-1',
        position1: 'position1',
        stat1: { id: 1, title: 'title1' },
        position2: 'position2',
        stat2: { id: 1, title: 'title2' },
        position3: 'position3',
        stat3: { id: 1, title: 'title3' },
        position4: 'position4',
        stat4: { id: 1, title: 'title4' },
        position5: 'position5',
        stat5: { id: 1, title: 'title5' },
      }])),
      getPlayerList: jasmine.createSpy('getPlayerList').and.returnValue(of(playerListObj)),
    } as any;
    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('string')
    };
    componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
    yourcallProviderService = {
      getMarketSelections: jasmine.createSpy('getMarketSelections').and.returnValue(Promise.resolve({ 'data': [{ 'selections': [selection] }] })),
      showCardPlayers: {}
    };
    bybSelectedSelectionsService = {
      callGTM: jasmine.createSpy('callGTM').and.returnValue(true),
      duplicateIdd: new Set(),
      betPlacementSubject$: new Subject<any>(),
    };
    windowRefService = {
      nativeWindow: {
        localStorage: {
          getItem: jasmine.createSpy('getItem').and.returnValue(true)
        }
      }
    };
    component = new YourCallPlayerBetsComponent(
      yourCallMarketsService,
      fiveASideService,
      yourcallProviderService,
      componentFactoryResolver,
      dialogService,
      infoDialogService,
      localeService,
      bybSelectedSelectionsService,
      changeDetector, windowRefService
    );
    component.showCardSelections = [selection];
    component.eventEntity = {
      cashoutAvail: '', categoryCode: '', categoryId: '', categoryName: '', displayOrder: 1, eventSortCode: '',
      eventStatusCode: '', id: 16, liveServChannels: '', liveServChildrenChannels: '', typeId: '', typeName: '', name: '', startTime: ''
    };
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
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      spyOn(component, "setStatMarket");
    });
    it('should call restoredMarketDone', fakeAsync(() => {
      spyOn(component, "showCardSelectionMarket");
      spyOn(component, "backup");
      yourCallMarketsService.betsArrayToRestore = jasmine.createSpy().and.returnValue(['test1', 'test2']);
      spyOn(component, "showcardRestore").and.returnValue(Promise.resolve({} as any));
      spyOn(component, "restoreBet").and.returnValue(Promise.resolve({} as any));
      spyOn(component, "callLocalStorageToFetchPlayerBets");
      component.market = { grouping: 'To Be Shown A Card' };
      component.showcardMarket = { marketName: 'To Be Shown A Card' } as any;
      component['getPlayerList'] = jasmine.createSpy();
      component['showcardRestore'] = jasmine.createSpy('showcardRestore').and.returnValue(Promise.resolve({}));
      component.ngOnInit();
      tick();
      expect(component.backup).toHaveBeenCalledWith();
    }));
    it('should call restoredMarketDone reject case', fakeAsync(() => {
      spyOn(component, "showCardSelectionMarket");
      spyOn(component, "backup");
      yourCallMarketsService.betsArrayToRestore = jasmine.createSpy().and.returnValue(['test1', 'test2']);
      component['showcardRestore'] = jasmine.createSpy('showcardRestore').and.returnValue(Promise.resolve({}));
      spyOn(component, "restoreBet").and.returnValue(Promise.reject({} as any) as any);
      spyOn(component, "callLocalStorageToFetchPlayerBets");
      component.market = { grouping: 'group' };
      component.showcardMarket = { marketName: 'To Be Shown A Card' } as any;
      component['getPlayerList'] = jasmine.createSpy();
      component.ngOnInit();
      tick();
      expect(changeDetector.markForCheck).toHaveBeenCalled();
    }));
  });

  describe('callLocalStorageToFetchPlayerBets', () => {
    it('when callLocalStorageToFetchPlayerBets called', () => {
      component.eventEntity = { id: 16 } as any;
      windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('OX.yourCallStoredData').and.returnValue(JSON.stringify(storage));
      // spyOn(component.localStorage, 'getItem').and.returnValue(JSON.stringify(storage));
      component.callLocalStorageToFetchPlayerBets();
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBeGreaterThan(0);
    });
  });

  describe('deletePlayer', () => {
    beforeEach(() => {
      yourcallProviderService.showCardPlayers = { 'Ronaldo': true };
      component.playersList = {
        allPlayers: [{
          id: 1, name: 'Ronaldo', teamName: '', teamColors: { primaryColour: '', secondaryColour: '' }, appearances: undefined,
          cleanSheets: undefined, tackles: undefined, passes: undefined, crosses: undefined, assists: undefined,
          shots: undefined, shotsOnTarget: undefined, shotsOutsideTheBox: undefined, goalsInsideTheBox: undefined,
          goalsOutsideTheBox: undefined, goals: undefined, cards: undefined, cardsRed: undefined, cardsYellow: undefined,
          position: { long: '', short: '' }, penaltySaves: undefined, conceeded: undefined, saves: undefined, isGK: false
        }], home: undefined, away: undefined
      };
    });
    it('when player is not present', () => {
      component.deletePlayer(2);
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
    });
    it('when allplayer list is not present', () => {
      component.playersList = undefined;
      component.deletePlayer(1);
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
    });
    it('when player is not same', () => {
      yourcallProviderService.showCardPlayers = {};
      yourcallProviderService.showCardPlayers = { 'Trint': true };
      component.deletePlayer(1);
      expect(yourcallProviderService.showCardPlayers['Trint']).toBe(true);
    });
    it('when playerList of player has initial and deleted', () => {
      yourcallProviderService.showCardPlayers = { 'R. Ronaldo': true };
      component.playersList = {
        allPlayers: [{
          id: 1, name: 'R. Ronaldo', teamName: '', teamColors: { primaryColour: '', secondaryColour: '' }, appearances: undefined,
          cleanSheets: undefined, tackles: undefined, passes: undefined, crosses: undefined, assists: undefined,
          shots: undefined, shotsOnTarget: undefined, shotsOutsideTheBox: undefined, goalsInsideTheBox: undefined,
          goalsOutsideTheBox: undefined, goals: undefined, cards: undefined, cardsRed: undefined, cardsYellow: undefined,
          position: { long: '', short: '' }, penaltySaves: undefined, conceeded: undefined, saves: undefined, isGK: false
        }], home: undefined, away: undefined
      };
      component.showCardSelections = [selection2];
      component.deletePlayer(1);
      expect(yourcallProviderService.showCardPlayers['R. Ronaldo']).toBe(false);
    });
    it('when selction of players has initials and deleted', () => {
      component.showCardSelections = [selection2];
      component.deletePlayer(1);
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(false);
    });
    it('when player is deleted', () => {
      component.deletePlayer(1);
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(false);
    });
  });

  describe('showcardPlayer', () => {
    beforeEach(() => {
      spyOn(component, 'playerAvailabe');
      spyOn(component, 'addRemoveBetBuilder');
      component.marketSelected = [{ 'grouping': 'To Be Shown A Card' }];
    });
    it('should call addRemoveBetBuilder when selection is present', () => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      yourcallProviderService.showCardPlayers = { 'Ronaldo': false };
      component.showcardPlayer({ name: 'Ronaldo' });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
      expect(component.playerAvailabe).not.toHaveBeenCalled();
    });
    it('should call addRemoveBetBuilder when player has initial', () => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      yourcallProviderService.showCardPlayers = { 'R. Ronaldo': false };
      component.showcardPlayer({ name: 'R. Ronaldo' });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(yourcallProviderService.showCardPlayers['R. Ronaldo']).toBe(true);
      expect(component.playerAvailabe).not.toHaveBeenCalled();
    });
    it('should call addRemoveBetBuilder when selection has initial', () => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      yourcallProviderService.showCardPlayers = { 'Ronaldo': false };
      component.showCardSelections = [selection2];
      component.showcardPlayer({ name: 'Ronaldo' });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
      expect(component.playerAvailabe).not.toHaveBeenCalled();
    });
    it('should call addRemoveBetBuilder cta button false', () => {
      yourcallProviderService.showCardPlayers = { 'Ronaldo': false };
      component.showcardPlayer({ name: 'Ronaldo' });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(false);
      expect(component.playerAvailabe).not.toHaveBeenCalled();
    });
    it('should call player available when selection is not present', () => {
      component.showcardPlayer({ name: 'Trint' });
      expect(component.addRemoveBetBuilder).not.toHaveBeenCalled();
      expect(component.playerAvailabe).toHaveBeenCalled();
    });
  });

  describe('displayOverlay', () => {
    it('stats pop up should be displayed', () => {
      component.market = { title: 'To Be Shown A Card' };
      const event: any = { stopPropagation: jasmine.createSpy() };
      component.displayOverlay({} as any, 'To Be Shown A Card', event);
      expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    });
  });

  describe('teamLogo', () => {
    it('should  set empty image string for the teamsImage', () => {
      const TEAMSIMAGEPATH = {
        imagepath: '',
        filename: ''
      };
      const player = {
        teamColors: {
          primaryColour: '#fff',
          secondaryColour: '#000',
          teamsImage: TEAMSIMAGEPATH,
        }
      };
      component.teamLogo(player as any);
      expect(component.teamsImage).toBe('');
    });
    it('should  set image string for the teamsImage', () => {
      const TEAMSIMAGEPATH = {
        imagepath: 'https://cms.ladbrokes.com/image1.svg',
        filename: 'image1.svg'
      };
      const player = {
        teamColors: {
          primaryColour: '#fff',
          secondaryColour: '#000',
          teamsImage: TEAMSIMAGEPATH,
        }
      };
      component.teamLogo(player as any);
      expect(component.teamsImage).toBe('https://cms.coral.co.uk/cms//images/uploads/svg/image1.svg');
    });
  });

  describe('change', () => {
    beforeEach(() => {
      component.incrementer = 1;
      component.stats = { 'maxValue': 3, 'minValue': 1, 'average': 2 };
      component.selectedInfo = { 'player': {}, 'stat': { 'title': 'tackles' }, 'statVal': '', 'obtainedStatValuesToDisplay': {} };
    });
    it('when market is not passes and no change in incrementer', () => {
      component.change(1, { 'name': 'Ronaldo' } as any);
      expect(component.odds).toBe('2+');
    });
    it('when market is not passes and incrementer is more than max value', () => {
      component.change(3, { 'name': 'Ronaldo' } as any);
      expect(component.odds).toBe('1+');
    });
    it('when market is not passes and incrementer is less than min value', () => {
      component.change(-1, { 'name': 'Ronaldo' } as any);
      expect(component.odds).toBe('3+');
    });
    it('when market is passes', () => {
      component.playerStatId = '1';
      yourCallMarketsService.selectedSelectionsSet.add('1-10');
      component.selectedInfo = { 'player': {}, 'stat': { 'title': 'Passes' }, 'statVal': '', 'obtainedStatValuesToDisplay': {} }
      component.incrementer = 5;
      component.stats = { 'maxValue': 15, 'minValue': 5, 'average': 10 };
      component.change(1, { 'name': 'Ronaldo' } as any);
      expect(component.odds).toBe('10+');
    });
  });

  describe('showcardRestore', () => {
    beforeEach(() => {
      spyOn(component, 'showCardSelectionMarket');
    });
    it('when show card player is restored', fakeAsync(() => {
      yourcallProviderService.showCardPlayers = { 'Ronaldo': false };
      component.showcardRestore('Ronaldo');
      tick();
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
    }));
    it('when show card player is restored and player has initial', fakeAsync(() => {
      yourcallProviderService.showCardPlayers = { 'R. Ronaldo': false };
      component.showcardRestore('R. Ronaldo');
      tick();
      expect(yourcallProviderService.showCardPlayers['R. Ronaldo']).toBe(true);
    }));
    it('when show card player is restored and selection players has initials', fakeAsync(() => {
      yourcallProviderService = {
        getMarketSelections: jasmine.createSpy('getMarketSelections').and.returnValue(Promise.resolve({ 'data': [{ 'selections': [selection2] }] }))
      };
      component = new YourCallPlayerBetsComponent(
        yourCallMarketsService,
        fiveASideService,
        yourcallProviderService,
        componentFactoryResolver,
        dialogService,
        infoDialogService,
        localeService,
        bybSelectedSelectionsService,
        changeDetector, windowRefService
      );
      spyOn(component, 'showCardSelectionMarket');
      component.eventEntity = {
        cashoutAvail: '', categoryCode: '', categoryId: '', categoryName: '', displayOrder: 1, eventSortCode: '',
        eventStatusCode: '', id: 16, liveServChannels: '', liveServChildrenChannels: '', typeId: '', typeName: '', name: '', startTime: ''
      };
      yourcallProviderService.showCardPlayers = { 'Ronaldo': false };
      component.showcardRestore('Ronaldo');
      tick();
      expect(yourcallProviderService.showCardPlayers['Ronaldo']).toBe(true);
    }));
    it('Rejected during restore for show card market', fakeAsync(() => {
      let rejected: boolean = false;
      component.showcardRestore('trint').catch(() => {
        rejected = true;
      });
      tick();
      expect(rejected).toBe(true);
    }));
  });

  describe('showCardSelectionMarket', () => {
    it('show card selection when data is present', fakeAsync(() => {
      component.marketsSet = [{ 'grouping': 'To Be Shown A Card' }];
      component.showCardSelectionMarket();
      tick();
      expect(yourcallProviderService.getMarketSelections).toHaveBeenCalled();
    }));
  });

  describe('getBackup', () => {
    it('backup should return show card player status', () => {
      yourcallProviderService.showCardPlayers = { 'Ronaldo': true };
      expect(component.getBackup('Ronaldo')).toBe(true);
    });
  });

  describe('addRemoveBetBuilder', () => {
    it('when player is added', () => {
      component.addRemoveBetBuilder(1, selection, {}, '');
      expect(yourCallMarketsService.removeSelection).not.toHaveBeenCalled();
      expect(yourCallMarketsService.selectValue).toHaveBeenCalled();
    });
    it('when player is deleted', () => {
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.addRemoveBetBuilder(1, selection, {}, '');
      expect(yourCallMarketsService.removeSelection).toHaveBeenCalled();
      expect(yourCallMarketsService.selectValue).not.toHaveBeenCalled();
    });
  });


  describe('getPlayerList', () => {
    it('when getPlayerList called', () => {
      spyOn(component as any, "teamNamesFormation");
      component.getPlayerList();
      expect(fiveASideService.getFormations).toHaveBeenCalled();
      expect(component.playersList).toEqual(playerListObj as any);
      expect(component.teamNamesFormation).toHaveBeenCalled();
    });
  });

  describe('teamNamesFormation', () => {
    it('when teamNamesFormation called', () => {
      spyOn(component as any, "teamSelectValue");
      component.game = { homeTeam: { players: {} }, visitingTeam: { players: {} } } as any;
      component.teamNames = [] as any;
      component.playersList = { home: {}, away: {}, allPlayers: {} } as any;
      component.teamNamesFormation();
      expect(component.teamSelectValue).toHaveBeenCalled();
    });
    it('when teamNamesFormation called when empty', () => {
      spyOn(component as any, "teamSelectValue");
      component.game = { homeTeam: { players: null }, visitingTeam: { players: null } } as any;
      component.teamNames = [] as any;
      component.playersList = {} as any;
      component.teamNamesFormation();
      expect(component.teamSelectValue).toHaveBeenCalled();
    });
    it('when teamNamesFormation called when undefined', () => {
      spyOn(component as any, "teamSelectValue");
      component.game = { homeTeam: { players: null }, visitingTeam: { players: null } } as any;
      component.teamNames = [] as any;
      component.teamNamesFormation();
      expect(component.teamSelectValue).toHaveBeenCalled();
    });
  });

  describe('teamSelectValue', () => {
    it('when teamSelectValue called isteamSelected true1', () => {
      const value = {
        players: [{
          "id": 1,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        },
        {
          "id": 17,
          "name": "A. Lokonga",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": true
        }]
      } as any;
      spyOn(component as any, "expanded");
      spyOn(component as any, "isteamSelected").and.returnValue(true);
      spyOn(component as any, "addSelection");
      component.teamSelectValue(value as any);
      expect(component.addSelection).not.toHaveBeenCalled();
    });
    it('when teamSelectValue called isteamSelected true1', () => {
      const value = {
        players: [{
          "id": 1,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        },
        {
          "id": 17,
          "name": "A. Lokonga",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": true
        }]
      } as any
      spyOn(component as any, "expanded");
      spyOn(component as any, "isteamSelected").and.returnValue(false);
      spyOn(component as any, "addSelection");
      component.teamSelectValue(value as any);
      expect(component.addSelection).toHaveBeenCalled();
    });
  });

  describe('expanded', () => {
    it('when expanded called true when compare ID', () => {
      component.compareId = 123;
      component.market = {
        stat: "offsides", grouping: "Player Bets", players: [{
          "id": 1,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      yourCallMarketsService.selectedSelectionsSet.add(component.compareId);
      component.showCardPlayers = { 'A. Lacazette': true };
      spyOn(component as any, "rangeValues").and.returnValue([Object({ id: 1, name: 'A. Lacazette', teamName: 'Arsenal', teamColors: Object({ primaryColour: '#777', secondaryColour: '#675d5d' }), position: Object({}), isGK: false })]);
      spyOn(component as any, "backup");
      component.expanded(player as any, 0);
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
      expect(component.backup).toHaveBeenCalled();
    });
    it('when expanded called true when compare diff ID', () => {
      component.compareId = 123;
      component.market = {
        stat: "offsides", grouping: "Player Bets", players: [{
          "id": 5,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      yourCallMarketsService.selectedSelectionsSet.add(component.compareId);
      yourcallProviderService.showCardPlayers = { 'A. Lacazette': true };
      spyOn(component as any, "rangeValues").and.returnValue([Object({ id: 1, name: 'A. Lacazette', teamName: 'Arsenal', teamColors: Object({ primaryColour: '#777', secondaryColour: '#675d5d' }), position: Object({}), isGK: false })]);
      spyOn(component as any, "backup");
      component.expanded(player as any, 0);
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
      expect(component.backup).toHaveBeenCalled();
    });
    it('when expanded called true when compare no ID', () => {
      component.compareId = 123;
      component.market = {
        stat: "offsides", grouping: "Player Bets", players: [{
          "id": 1,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.showCardPlayers = { 'A. Lacazette': false };
      spyOn(component as any, "rangeValues").and.returnValue([Object({ id: 1, name: 'A. Lacazette', teamName: 'Arsenal', teamColors: Object({ primaryColour: '#777', secondaryColour: '#675d5d' }), position: Object({}), isGK: false })]);
      spyOn(component as any, "backup");
      component.expanded(player as any, 0);
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
      expect(component.backup).toHaveBeenCalled();
    });
    it('when expanded called true when compare diff ID', () => {
      component.compareId = 123;
      component.market = {
        stat: "offsides", grouping: "Player Bets", players: [{
          "id": 5,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      yourCallMarketsService.selectedSelectionsSet.add(1);
      yourcallProviderService.showCardPlayers = { 'A. Lacazette': false };
      spyOn(component as any, "rangeValues").and.returnValue([Object({ id: 1, name: 'A. Lacazette', teamName: 'Arsenal', teamColors: Object({ primaryColour: '#777', secondaryColour: '#675d5d' }), position: Object({}), isGK: false })]);
      spyOn(component as any, "backup");
      component.expanded(player as any, 0);
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
      expect(component.backup).toHaveBeenCalled();
    });
    it('when expanded called true when compare no stat', () => {
      const compareId = 123;
      component.market = {
        stat: "offsides", grouping: "To Be Shown a Card", players: [{
          "id": 5,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      component.expanded(player as any, 0);

      expect(component.odds).toEqual("+1");
    });
    it('when expanded called true when compare no stat', () => {
      const compareId = 123;
      component.market = {
        stat: "Goalscorer", grouping: "group", players: [{
          "id": 5,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      component.expanded(player as any, 0);

      expect(component.odds).toEqual("+1");
    });
    it('when expanded called true when compare no stat', () => {
      const compareId = 123;
      component.market = {
        stat: "Goalscorer", grouping: "Player Bets", players: [{
          "id": 5,
          "name": "A. Lacazette",
          "teamName": "Arsenal",
          "teamColors": {
            "primaryColour": "#777",
            "secondaryColour": "#675d5d"
          },
          "position": {},
          "isGK": false
        }]
      } as any;
      const player = {
        "id": 1,
        "name": "A. Lacazette",
        "teamName": "Arsenal",
        "teamColors": {
          "primaryColour": "#777",
          "secondaryColour": "#675d5d"
        },
        "position": {},
        "isGK": false
      }
      component.expanded(player as any, 0);

      expect(component.odds).toEqual("+1");
    });
  });

  describe('#isteamSelected', () => {
    it('should call isteamSelected method1', () => {
      const team = {
        "abbreviation": null,
        "title": "Both Teams",
        "players": null
      };
      component.selected = [];
      const result = component.isteamSelected(team as any);
      expect(result).toBe(false);
    });

    it('should call isteamSelected method2', () => {
      const team = {
        "abbreviation": null,
        "title": "Both Teams",
        "players": null
      };
      component.selected = [team];
      const result = component.isteamSelected(team);
      expect(result).toBe(true);
    });
  });

  describe('#addSelection', () => {
    it('should call addSelection method single', () => {
      component.addSelection({} as any);

      expect(component.selected[0]).toEqual({});
    });
    it('should call addSelection method multi', () => {
      component.multi = true;
      component.addSelection({} as any);

      expect(component.selected).toEqual([{}]);
    });
  });

  describe('#playerAvailabe', () => {
    it('should call playerAvailabe method single', () => {
      component.enabled = undefined;
      component.playerAvailabe();
      expect(infoDialogService.openInfoDialog).toHaveBeenCalled();
    });
  });

  describe('#prepareStatsValues', () => {
    it('should prepare stats values', () => {
      component.selectedInfo.stat = {
        title: 'Shots'
      }
      component['prepareStatsValues'](20, 10);
      expect(component.obtainedStatValuesToDisplay).toEqual(
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]);
    });
    it('should prepare stats values only for Passes', () => {
      component.selectedInfo.stat = {
        title: 'Passes'
      }
      component['prepareStatsValues'](20, 10);
      expect(component.obtainedStatValuesToDisplay).toEqual([10, NaN, NaN]);
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
        obtainedStatValuesToDisplay: [],
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
        iddInc: 'undefined-1',
        idd: 'undefined-1-undefined',
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
        value: undefined
      } as any);
    });
  });

  describe('#rangeValues', () => {
    it('should return rangeValues 4', fakeAsync(() => {
      spyOn(component, "getRange");
      component.market.stat = "Passes";
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({ data: [{ title: 'Passes' }] }));
      component.rangeValues({ id: 1 } as any);
      tick();
      expect(component.obtainedPlayerFeed).toEqual([{ title: 'Passes' }] as any);
    }));

    it('should return rangeValues 4', fakeAsync(() => {
      spyOn(component, "getRange");
      spyOn(component, "playerAvailabe");
      component.market.stat = "Passes";
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({ data: [{ title: 'Passes1' }] }));
      component.rangeValues({ id: 1 } as any);
      tick();
      expect(component.playerAvailabe).toHaveBeenCalled();
    }));
  });

  describe('#getRange', () => {
    it('should return getRange', fakeAsync(() => {
      const playerId = 1;
      component.compareId = 123;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }
      yourCallMarketsService.selectedSelectionsSet.add(component.compareId);
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 1, minValue: 1 } }));
      component.getRange({ playerId: 1 } as any, { statId: 1 } as any);
      tick();
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
    }));
    it('should return getRange', fakeAsync(() => {
      const playerId = 1;
      component.compareId = 123;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }
      yourCallMarketsService.selectedSelectionsSet.add(component.compareId);
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 1, minValue: 1 } }));
      component.getRange(playerId as any, { statId: 1 } as any);
      tick();
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
    }));
    it('should return getRange', fakeAsync(() => {
      const playerId = 1;
      component.compareId = 123;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }
      yourCallMarketsService.selectedSelectionsSet.add('1-undefined-1');
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 1, minValue: 1 } }));
      component.getRange(playerId as any, { statId: 1 } as any);
      tick();
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
    }))
    it('should return getRange', fakeAsync(() => {
      const playerId = 1;
      component.compareId = 123;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.showCardPlayers = { 'A. Lacazette': false };
      component.showcardPlayer({ name: 'A. Lacazette' });
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 1, minValue: 1 } }));
      component.getRange({ playerId: 1 } as any, { statId: 1 } as any);
      tick();
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
    }));
    it('should return getRange when no id match', fakeAsync(() => {
      const playerId = 1;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }

      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 1, minValue: 1 } }));
      component.getRange({ playerId: 123 } as any, { statId: 1 } as any);
      tick();
      expect(component.prepareStatsValues).toHaveBeenCalled()
    }));
    it('should return getRange when no id with same max with diff id', fakeAsync(() => {
      const playerId = 1;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 4, minValue: 4 } }));
      component.getRange({ playerId: 1 } as any, { statId: 1 } as any);
      tick();
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
      expect(component.prepareStatsValues).toHaveBeenCalled()
    }));
    it('should return getRange when no diff max same id', fakeAsync(() => {
      const playerId = 123;
      spyOn(component, "prepareStatsValues");
      component.teamNames[0] = { players: [{ id: 1, name: 'A. Lacazette' }] }

      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({ data: { average: 1, maxValue: 4, minValue: 4 } }));
      component.getRange({ playerId: 123 } as any, { statId: 1 } as any);
      tick();
      expect(component.prepareStatsValues).toHaveBeenCalled()
    }));
  });

  describe('#done', () => {
    it('should return done', () => {
      spyOn(component, "addRemoveBetBuilder");
      spyOn(component, "selectionMarket").and.returnValue({ iddInc: "1-1-2-3" } as any);
      component.incremented = true;
      const addId = "1-1-2-3-0";
      component.market = { stat: "offsides", grouping: "Player Bets" };
      const player = { name: "A. Lacazette" };
      yourCallMarketsService.selectedSelectionsSet.add(addId);
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      component.done({ name: "A. Lacazette" } as any, { stat: "offsides", grouping: "Player Bets" });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
    });
    it('should return done differe addid', () => {
      spyOn(component, "addRemoveBetBuilder");
      spyOn(component, "selectionMarket").and.returnValue({ iddInc: "1-1-2-3" } as any);
      component.incremented = true;
      const addId = 1;
      component.market = { stat: "offsides", grouping: "Player Bets" };
      const player = { name: "A. Lacazette" };
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.showCardPlayers = { 'A. Lacazette': false };
      component.showcardPlayer({ name: 'A. Lacazette' });
      component.done({ name: "A. Lacazette" } as any, { stat: "offsides", grouping: "Player Bets" });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
    });
    it('should return done when no incremented1', () => {
      spyOn(component, "addRemoveBetBuilder");
      spyOn(component, "selectionMarket").and.returnValue({ idd: "1-2-3-4" } as any);
      component.incremented = false;
      const addId = "1-2-3-4";
      component.market = { stat: "offsides", grouping: "Player Bets" };
      const player = { name: "A. Lacazette" };
      yourCallMarketsService.selectedSelectionsSet.add(addId);
      component.showCardPlayers = { 'A. Lacazette': true };
      component.showcardPlayer({ name: 'A. Lacazette' });
      component.done({ name: "A. Lacazette" } as any, { stat: "offsides", grouping: "Player Bets" });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(component.showCardPlayers['A. Lacazette']).toBe(true);
    });
    it('should return done when no incremented2', () => {
      spyOn(component, "addRemoveBetBuilder");
      spyOn(component, "selectionMarket").and.returnValue({ idd: "1-2-3-4" } as any);
      component.incremented = false;
      const addId = 1;
      component.market = { stat: "offsides", grouping: "Player Bets" };
      const player = { name: "A. Lacazette" };
      yourCallMarketsService.selectedSelectionsSet.add(3);
      component.showCardPlayers = { 'A. Lacazette': false };
      component.showcardPlayer({ name: 'A. Lacazette' });
      component.done({ name: "A. Lacazette" } as any, { stat: "offsides", grouping: "Player Bets" });
      expect(component.addRemoveBetBuilder).toHaveBeenCalled();
      expect(component.showCardPlayers['A. Lacazette']).toBe(false);
    });
    it('should return done when  incremented3', () => {
      spyOn(component, "showcardPlayer");
      spyOn(component, "selectionMarket").and.returnValue({ iddInc: "1-1-2-3" } as any);
      component.incremented = false;
      component.market = { stat: "Goalscorer", grouping: "Player Bets" };
      component.showcardMarket = { marketName: "To Be Shown A Card" } as any;
      const player = { name: "A. Lacazette" };
      component.done({ name: "A. Lacazette" } as any, { stat: "Goalscorer", grouping: "Player Bets" });
      expect(component.showcardPlayer).not.toHaveBeenCalled();

    });
    it('should return done when no incremented4', () => {
      spyOn(component, "showcardPlayer");
      spyOn(component, "selectionMarket").and.returnValue({ idd: "1-2-3-4" } as any);
      component.incremented = false;
      component.market = { grouping: "TO BE SHOWN A CARD" };
      component.showcardMarket = { marketName: "TO BE SHOWN A CARD" } as any;
      const player = { name: "A. Lacazette" };

      component.done({ name: "A. Lacazette" } as any, { grouping: "TO BE SHOWN A CARD" });
      expect(component.showcardPlayer).toHaveBeenCalled();
    });
  });

  describe('#restoreBet', () => {
    it('should catch error when minValue < value < maxValue', fakeAsync(() => {
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          minValue: 1,
          maxValue: 10
        }
      }));
      component.market.players = [{
        name: 'player name',
        position: {
          title: 'Defender'
        },
        id: 1
      }];
      component.eventEntity = { id: 123 } as any;
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 25 }).catch(() => { });
      tick();

      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1,
        statId: undefined
      });
      expect(yourCallMarketsService.addSelection).not.toHaveBeenCalled();
    }));
    it('should catch error from getStatisticsForPlayer', fakeAsync(() => {
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.reject('error'));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      component.eventEntity = { id: 123 } as any;
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 }).catch(error => {
        expect(error).toEqual('error');
      });
      tick();

      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).not.toHaveBeenCalledWith();
      expect(yourCallMarketsService.addSelection).not.toHaveBeenCalled();
    }));
    it('should call yourCallMarketsService.addSelection1', fakeAsync(() => {
      const localIdd = 1;
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          minValue: 1,
          maxValue: 10
        }
      }));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      component.eventEntity = { id: 123 } as any;
      component.showcardPlayer({ name: 'player name' });
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 });

      tick();
      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1,
        statId: undefined
      });
      expect(yourCallMarketsService.addSelection).toHaveBeenCalled();
    }));
    it('should call yourCallMarketsService.addSelection2', fakeAsync(() => {
      const localIdd = "";
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          minValue: 1,
          maxValue: 10
        }
      }));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      component.eventEntity = { id: 123 } as any;
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 });

      tick();
      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1,
        statId: undefined
      });
      expect(changeDetector.markForCheck).toHaveBeenCalled();
    }));
    it('should call yourCallMarketsService.addSelection3', fakeAsync(() => {
      const localIdd = 1;
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          minValue: 1,
          maxValue: 10
        }
      }));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      component.eventEntity = { id: 123 } as any;
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 });

      tick();
      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1,
        statId: undefined
      });
      expect(changeDetector.markForCheck).toHaveBeenCalled();
    }));
    it('should call yourCallMarketsService.addSelection4', fakeAsync(() => {
      const localIdd = "";
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      yourCallMarketsService.getStatValues.and.returnValue(Promise.resolve({
        data: {
          minValue: 1,
          maxValue: 10
        }
      }));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      component.eventEntity = { id: 123 } as any;
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 });

      tick();
      expect(yourCallMarketsService.getStatisticsForPlayer).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1
      });
      expect(yourCallMarketsService.getStatValues).toHaveBeenCalledWith({
        obEventId: '123',
        playerId: 1,
        statId: undefined
      });
      expect(changeDetector.markForCheck).toHaveBeenCalled();
    }));
    it('should catch error', fakeAsync(() => {
      yourCallMarketsService.getStatisticsForPlayer.and.returnValue(Promise.resolve({
        data: [{
          title: 'statisticTitle',
          minValue: 1,
          maxValue: 10
        }]
      }));
      component.market.players = [{
        name: 'player name',
        id: 1,
        position: {
          title: 'Defender'
        }
      }];
      yourCallMarketsService.getStatValues.and.returnValue(Promise.reject());
      yourCallMarketsService.addSelection = jasmine.createSpy('addSelection');
      component['restoreBet']({ playerName: 'player name', statisticTitle: 'statisticTitle', value: 10 }).then(() => {
        // eslint-disable-next-line
        console.log('ee');
      }, () => {
        // eslint-disable-next-line
        console.log('ddd');
      });
      tick();
      expect(yourCallMarketsService.addSelection).not.toHaveBeenCalled();
    }));
  });

  describe('getShowCard', () => {
    it('backup should return show card player status', () => {
      component.showCardPlayers = { 'Ronaldo': true };
      const result = component.getShowCard('Ronaldo');
      expect(result).toBe(true);
    });
  });

  describe('backup', () => {
  
    it('when playerBetRemovalsubject subscribed when incremented', fakeAsync(() => {
       const  selection={
        selectedID:'1-8-1',
        playerId:1
      }
      component.teamNames = [{players: [{id: 1,name: 'ronaldo'}]}]
      component.incrementer=3;
      component.playerStatId='1-8';
     yourcallProviderService.showCardPlayers = { 'ronaldo': false };
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject<any>();
      component.backup();
     yourCallMarketsService.playerBetRemovalsubject$.next(selection);
      tick();
      yourCallMarketsService.selectedSelectionsSet.add('1-8-1');
     // expect( yourCallMarketsService.selectedSelectionsSet.delete('1-8-1'));
      expect(yourcallProviderService.showCardPlayers['ronaldo']).toBe(false);
    }));

    it('when playerBetRemovalsubject subscribed when incremented with true', fakeAsync(() => {
      const  selection={
        selectedID:'1-8-1',
        playerId:1
      }
      component.prePlayerId=1;
      component.teamNames = [{players: [{id: 1,name: 'ronaldo'}]}];
      component.incrementer=3;
      component.playerStatId='1-8';
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
     yourcallProviderService.showCardPlayers = { 'ronaldo': true };
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject<any>();
      component.backup();
     yourCallMarketsService.playerBetRemovalsubject$.next(selection);
      tick();     
     // expect( yourCallMarketsService.selectedSelectionsSet.delete('1-8-2'));
      expect(yourcallProviderService.showCardPlayers['ronaldo']).toBe(true);
    }));


    it('when playerBetRemovalsubject subscribed with no incremented', fakeAsync(() => {
      const  selection={
        selectedID:'1-8-1',
        playerId:1
      }
      component.teamNames = [{players: [{id: 1,name: 'ronaldo'}]}]
      component.incrementer=0;
      component.compareId='1-8-1';
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
     yourcallProviderService.showCardPlayers = { 'ronaldo': false };
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject<any>();
      component.backup();
     yourCallMarketsService.playerBetRemovalsubject$.next(selection);
      tick();
      expect(yourcallProviderService.showCardPlayers['ronaldo']).toBe(false);
    }));

    it('when playerBetRemovalsubject subscribed with no incremented with true', fakeAsync(() => {
      const  selection={
        selectedID:'1-8-1',
        playerId:1
      }
      component.compareId='1-8-3';
      component.teamNames = [{players: [{id: 1,name: 'ronaldo'}]}]
      component.incrementer=0
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
     yourcallProviderService.showCardPlayers = { 'ronaldo': true };
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject<any>();
      component.backup();
     yourCallMarketsService.playerBetRemovalsubject$.next(selection);
      tick();
      expect(yourcallProviderService.showCardPlayers['ronaldo']).toBe(true);
    }));

    it('playerBetRemovalsubject$ all through scenario', fakeAsync(() => {
      component.teamNames = [{ players: [] }];
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject();
      yourCallMarketsService.selectedSelectionsSet.add(1);
      component.backup();
      yourCallMarketsService.playerBetRemovalsubject$.next({ selectedID: 1, playerId: 10 });
      tick();
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBe(0);
    }));
  
    it('playerBetRemovalsubject$ all through scenario', fakeAsync(() => {
      component.teamNames =[{ players: [] }];
      yourCallMarketsService.playerBetRemovalsubject$ = new Subject();
      yourCallMarketsService.selectedSelectionsSet.add(2);
      component.backup();
      yourCallMarketsService.playerBetRemovalsubject$.next({ selectedID: 1, playerId: 10 });
      tick();
      expect(yourCallMarketsService.selectedSelectionsSet.size).toBe(1);
    })); 


    it('when oldNewplayerStatIdsubject subscribed with incremented', fakeAsync(() => {
      const selection = {
        oldId: '1-8-1',
        newID: '1-8-3',
        oldPlayerId:1,
        newPlayerId:17
      }
      component.prePlayerId=1;
      component.teamNames = [{ players: [{ id: 1, name: 'ronaldo' },{ id: 17, name: 'lakzatos' }] }]
      component.incrementer = 3;
      component.incremented = true;
      component.oddInc=true;
      component.previousPlayerStatID = '1-8-1';
      component.updatedPlayerStatId = '1-8-3';
      spyOn(component,'selectionMarket').and.returnValue({iddInc: '1-8'}as any),

      component.showCardPlayers = { 'ronaldo': true, 'lakzatos':true };
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
      yourCallMarketsService.oldNewplayerStatIdsubject$ = new Subject<any>();
      component.backup();
      yourCallMarketsService.oldNewplayerStatIdsubject$.next(selection);
      tick();
     expect(yourCallMarketsService.selectedSelectionsSet.delete(component.previousPlayerStatID));
     expect(yourCallMarketsService.selectedSelectionsSet.add(component.updatedPlayerStatId));
      expect(component.showCardPlayers['ronaldo']).toBe(true);
    }));
  
    it('when oldNewplayerStatIdsubject subscribed with no incremented', fakeAsync(() => {
      const selection = {
        oldId: '1-8-1',
        newID: '1-8-3',
        oldPlayerId:1
      }
     
      component.prePlayerId=1;
      component.teamNames = [{ players: [{ id: 1, name: 'ronaldo' }] }]
      component.incrementer = 0;
      component.incremented = false;
      component.oddInc = false;
      component.compareId='1-8-1';
      component.updatedPlayerStatId = '1-8-3';
      component.showCardPlayers = {'ronaldo': false  };
      yourCallMarketsService.oldNewplayerStatIdsubject$ = new Subject<any>();
      component.backup();
      yourCallMarketsService.oldNewplayerStatIdsubject$.next(selection);
      tick();
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
      expect(component.showCardPlayers['ronaldo']).toEqual(false);
    }));

    it('inside 1st if', fakeAsync(() => {
      yourCallMarketsService.showBetRemovalsubject$ = new Subject<any>();
      spyOn(component, 'deletePlayer')
      yourCallMarketsService.selectedSelectionsSet.add('1-8-3');
      component.backup();
      yourCallMarketsService.showBetRemovalsubject$.next('1-8-3');
      tick();
      expect(component.deletePlayer).toHaveBeenCalled();
    }));

    it('inside 1st if1 undefined', fakeAsync(() => {
      yourCallMarketsService.showBetRemovalsubject$ = new Subject<any>();
      spyOn(component, 'deletePlayer')
      yourCallMarketsService.selectedSelectionsSet.add('1-8-2');
      component.backup();
      yourCallMarketsService.showBetRemovalsubject$.next();
      tick();
      expect(component.deletePlayer).not.toHaveBeenCalled();
    }));

    it('inside 2nd if with true', fakeAsync(() => {
      yourCallMarketsService.betPlacedStatus$ = new Subject<any>();
      spyOn(component, 'deletePlayer')
      yourCallMarketsService.selectedSelectionsSet.add('1-8-2');
      component.backup();
      yourCallMarketsService.betPlacedStatus$.next(true);
      tick();
      expect(component.showCardPlayers).toEqual({})
    }));

    it('inside 2nd if with false', fakeAsync(() => {
      yourCallMarketsService.betPlacedStatus$ = new Subject<any>();
      spyOn(component, 'deletePlayer')
      yourCallMarketsService.selectedSelectionsSet.add('1-8-2');
      component.backup();
      component.showCardPlayers = 1 as any;
      yourCallMarketsService.betPlacedStatus$.next(false);
      tick();
      expect(component.showCardPlayers as any).toBe(1);
    }));
  }); 
  
  describe('setStatMarket', () => {
    it('when market stat is defined', () => {
      component.market = { 'stat': 'assits' };
      component.setStatMarket();
      expect(component.statMarket).toBe('assits');
    });
    it('when market is goalscorer', () => {
      component.market = { 'grouping': 'To Be Shown A Card' };
      component.setStatMarket();
      expect(component.statMarket).toBe('To Be Shown A Card');
    });
    it('when market is to be shown a card', () => {
      component.market = { 'grouping': 'Goalscorer' };
      component.setStatMarket();
      expect(component.statMarket).toBe('Goalscorer');
    });
  });
});
