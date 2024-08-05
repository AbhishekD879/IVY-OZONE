import { FiveASideService } from './five-a-side.service';
import { playersMock, playersWithoutStats, playersWithStats, optaMock } from './five-a-side.mock';
import { fakeAsync, tick } from '@angular/core/testing';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { Observable, of, throwError } from 'rxjs';

describe('#FiveASideService', () => {
  let service;
  let cmsService;
  let yourcallProviderService;
  let yourcallMarketsService;
  let coreToolsService;
  let domSanitizer;
  let fiveASideBetService;
  let windowRefService;

  beforeEach(() => {
    coreToolsService = new CoreToolsService();

    cmsService = {
      getFiveASideFormations: jasmine.createSpy('getFiveASideFormations'),
      getTeamsColors: jasmine.createSpy('getTeamsColors').and.returnValue(of([])),
      getFiveASideStaticBlocks: jasmine.createSpy('getFiveASideStaticBlocks')
    };
    yourcallProviderService = {
      getPlayers: jasmine.createSpy('getPlayers').and.returnValue(Promise.resolve(playersMock))
    };
    yourcallMarketsService = {
      game: {
        homeTeam: {
          title: 'Liverpool'
        },
        visitingTeam: {
          title: 'Arsenal'
        }
      },
      getStatisticsForPlayer: jasmine.createSpy('getStatisticsForPlayer').and.returnValue(of([]))
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    fiveASideBetService = {
      addRole: jasmine.createSpy('addRole'),
      updateBet: jasmine.createSpy('updateBet')
    };
    windowRefService = {
      document: {
        querySelector:jasmine.createSpy().and.callFake(param => {
          switch (param) {
            case 'div#opta-scoreboard-overlay-wrapper':
              return {
                classList: {
                  add: jasmine.createSpy('add')
                }
              } as any;
            case 'scoreboard-overlay':
               return {
                setAttribute: jasmine.createSpy('setAttribute')
               };
            default:
               return {};
          }
        }),
        createElement: jasmine.createSpy().and.callFake(param => {
          switch (param) {
            case 'scoreboard-container':
              return document.createElement('scoreboard-container');
            case 'scoreboard-overlay':
              return {
                setAttribute: jasmine.createSpy('setAttribute')
               };
            case 'div':
              return {
                setAttribute: jasmine.createSpy('setAttribute'),
                appendChild: jasmine.createSpy('appendChild'),
                classList: {
                  add: jasmine.createSpy('add')
                }
               };
          }
        }),
        body: {
          appendChild: jasmine.createSpy('appendChild'),
          classList: {
            add: jasmine.createSpy('add'),
            remove: jasmine.createSpy('remove')
          }
        }
      }
    };
    service = new FiveASideService(
      cmsService,
      yourcallProviderService,
      yourcallMarketsService,
      coreToolsService,
      domSanitizer,
      fiveASideBetService,
      windowRefService
    );
  });

  it('should create service instance', () => {
    expect(service).toBeTruthy();
  });

  describe('#getFormations', () => {
    it('should call getFormations method', () => {
      service.getFormations();

      expect(cmsService.getFiveASideFormations).toHaveBeenCalled();
      expect(service.game).toEqual({
        homeTeam: {
          title: 'Liverpool'
        },
        visitingTeam: {
          title: 'Arsenal'
        }
      });
    });
  });

  describe('#getPlayerList', () => {
    beforeEach(() => {
      service.game = yourcallMarketsService.game;
    });

    describe('should return players without stats', () => {
      let optaData;

      it('should call getPlayerList method and return players without stats', () => {
        optaData = null;
      });
      it('should call getPlayerList method and return players without stats', () => {
        optaData = {};
      });
      it('should call getPlayerList method and return players when no opta at storage', () => {
        optaData = { data: { } };
      });
      it('should call getPlayerList method and return players when opta has empty players data (no team arrays)', () => {
        optaData = { data: { players: {} } };
      });
      it('should call getPlayerList method and return players without stats if no OPTA playes', () => {
        optaData = { data: { players: { home: [], away: [] } } };
      });

      afterEach(fakeAsync(() => {
        spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
        service.getPlayerList(12345).subscribe();
        tick(200);
        expect(service.playerList).toEqual(playersWithoutStats);
      }));
    });

    it('should call getPlayerList method and return players with stats', fakeAsync(() => {
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaMock));
      service.teamsColors = {
        Liverpool: { primaryColour: '#fff', secondaryColour: undefined },
        Arsenal: { primaryColour: '#fff', secondaryColour: undefined }
      };
      service.getPlayerList(12345).subscribe();
      tick(200);

      expect(service.playerList).toEqual(playersWithStats);
    }));
  });

  describe('#sortPlayers', () => {
    beforeEach(() => {
      service.game = yourcallMarketsService.game;
    });
    it('should call sortPlayers method', fakeAsync(() => {
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaMock));
      service.getPlayerList(12345).subscribe();
      tick(200);
      service.sortPlayers({stat: 'Passes'} as any);

      expect(service.playerList.allPlayers[0].passes).toEqual(60);
      expect(service.playerList.allPlayers[1].passes).toEqual(50);

      service.sortPlayers({stat: 'Passes'} as any, 'home');

      expect(service.playerList.allPlayers[0].passes).toEqual(60);
      expect(service.playerList.allPlayers[1].passes).toEqual(50);
    }));
  });

  describe('#parsePlayer', () => {
    let optaPlayer;
    let banachplayer;

    beforeEach(() => {
      optaPlayer = {
        attendance: {
          appearances: 0
        },
        goalKeeper: {
          conceeded: 1,
          totalSaves: 1,
          penaltySaves: 1,
        },
      } as any;
      banachplayer = {
        id: '1',
        name: 'Oleh',
        team: {
          title: 'Team'
        }
      };
    });

    it('should parsePlayer when appearance 0', () => {
      const result = service['parsePlayer'](optaPlayer, banachplayer);
      expect(result).toEqual({
        id: '1',
        name: 'Oleh',
        teamName: 'Team',
        teamColors: undefined,
        appearances: 0,
        cleanSheets: undefined,
        tackles: undefined,
        passes: undefined,
        crosses: undefined,
        assists: undefined,
        shots: undefined,
        shotsOnTarget: undefined,
        shotsOutsideTheBox: undefined,
        goals: undefined,
        goalsInsideTheBox: undefined,
        goalsOutsideTheBox: undefined,
        cards: undefined,
        cardsRed: undefined,
        cardsYellow: undefined,
        position: { long: undefined, short: undefined },
        penaltySaves: 1,
        conceeded: 0,
        saves: 0,
        isGK: false,
      });
    });

    it('should opta statistics be available',() => {
      service['parsePlayer'](optaPlayer, banachplayer);

      expect(service.optaStatisticsAvailable).toBeFalsy();
    });

    it('should opta statistics not be available ',() => {
      optaPlayer.attendance.appearances = 1;
      service['parsePlayer'](optaPlayer, banachplayer);

      expect(service.optaStatisticsAvailable).toBeTruthy();
    });
  });

  describe('#sortByProperties', () => {
    it('should sort case#1', () => {
      const items = [{
        id: 2,
        name: 'a'
      }, {
        id: 2,
        name: 'c'
      }, {
        id: 2,
        name: 'b'
      }];

      const result = service.sortByProperties(items, ['id', 'name']);

      expect(result).toEqual(
        [{
          id: 2,
          name: 'a'
        }, {
          id: 2,
          name: 'b'
        }, {
          id: 2,
          name: 'c'
        }]
      );
    });

    it('should sort case#2', () => {
      const items = [{
        id: 3,
        name: 'a'
      }, {
        id: 1,
        name: 'c'
      }, {
        id: 5,
        name: 'b'
      }];

      const result = service.sortByProperties(items, ['id', 'name']);

      expect(result).toEqual(
        [{
          id: 5,
          name: 'b'
        }, {
          id: 3,
          name: 'a'
        }, {
          id: 1,
          name: 'c'
        }]
      );
    });

    it('should sort case#3', () => {
      const items = [{
        id: 3,
        name: 'a'
      }, {
        id: 1,
        name: 'c'
      }, {
      id: 5,
      name: 'b'
      }, {
        id: 5,
        name: 'b'
      }];

      const result = service.sortByProperties(items, ['id', 'name']);

      expect(result).toEqual(
        [{
          id: 5,
          name: 'b'
        },
         {
          id: 5,
          name: 'b'
        }, {
          id: 3,
          name: 'a'
        }, {
          id: 1,
          name: 'c'
        }]
      );
    });

    it('should sort case#4', () => {
      const items = [{
        id: 3,
        name: 'a'
      }, {
        id: 1,
        name: 'c'
      }];

      const result = service.sortByProperties(items, []);

      expect(result).toEqual(
        [{
          id: 1,
          name: 'c'
        },
        {
          id: 3,
          name: 'a'
        }]
      );
    });

    it('should sort case#5', () => {
      coreToolsService.getOwnDeepProperty = jasmine.createSpy('getOwnDeepProperty').and.returnValue(undefined);
      const items = [{
        id: 3,
        name: 'a'
      }, {
        id: 1,
        name: 'c'
      }];

      const result = service.sortByProperties(items, ['id', 'name']);

      expect(result).toEqual(
        [{
          id: 1,
          name: 'c'
        },
        {
          id: 3,
          name: 'a'
        }]
      );
    });
  });

  describe('#initTeamsColors', () => {
    beforeEach(() => {
      service.game = yourcallMarketsService.game;
      spyOn(console, 'warn');
    });
    it('should call initTeamsColors method (same ob ID)', () => {
      service.teamsColors = {
        primaryColour: 'string',
        secondaryColour: 'string'
      };
      service.activeObEventId = 123;
      service.initTeamsColors('16', 123).subscribe();

      expect(cmsService.getTeamsColors).not.toHaveBeenCalled();
    });

    it('should not call getTeamsColors if teamsColorObservable exists', () => {
      service.teamsColorObservable = of({});
      service.activeObEventId = 124;
      service.initTeamsColors('16', 124).subscribe();

      expect(cmsService.getTeamsColors).not.toHaveBeenCalled();
    });

    it('should call initTeamsColors method (same ob ID)', () => {
      service.teamsColors = {
        primaryColour: 'string',
        secondaryColour: 'string'
      };
      service.activeObEventId = 1234;
      service.initTeamsColors('16', 123).subscribe();

      expect(cmsService.getTeamsColors).toHaveBeenCalled();
    });

    it('should call initTeamsColors method (same ob ID)', () => {
      cmsService.getTeamsColors.and.returnValue(throwError('error'));
      service.teamsColors = {
        primaryColour: 'string',
        secondaryColour: 'string'
      };
      service.activeObEventId = 1234;
      service.initTeamsColors('16', 123).subscribe();

      expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['Liverpool', 'Arsenal'], '16');
      expect(service.teamsColors).toEqual({});
    });

    it('should call initTeamsColors method new ob ID', () => {
      cmsService.getTeamsColors.and.returnValue(of([{
        teamName: 'Liverpool',
        primaryColour: '#fff',
        id: 'string',
        sportId: '16',
        secondaryNames: ['string1', 'string2']
      }, {
        teamName: 'Arsenal',
        primaryColour: '#fff',
        id: 'string',
        sportId: '16',
        secondaryNames: ['string1', 'string2']
      }
      ]));
      service.activeObEventId = 1234;
      service.initTeamsColors('16', 123).subscribe();

      expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['Liverpool', 'Arsenal'], '16');
      expect(service.teamsColors).toEqual({
        Liverpool: {
          primaryColour: '#fff', secondaryColour: '#675d5d', teamsImage: undefined,
          fiveASideToggle: undefined,
          highlightCarouselToggle: undefined
        },
        Arsenal: {
          primaryColour: '#fff', secondaryColour: '#675d5d', teamsImage: undefined,
          fiveASideToggle: undefined,
          highlightCarouselToggle: undefined
        }
      });
    });

    it('should call initTeamsColors method new ob ID and test for teams image', () => {
      cmsService.getTeamsColors.and.returnValue(of([{
        teamName: 'Liverpool',
        primaryColour: '#fff',
        id: 'string',
        sportId: '16',
        secondaryNames: ['string1', 'string2'],
        teamsImage: 'https://cms.coral.co.uk/cms//images/uploads/svg/image1.svg',
        fiveASideToggle: true,
        highlightCarouselToggle: true
      }, {
        teamName: 'Arsenal',
        primaryColour: '#fff',
        id: 'string',
        sportId: '16',
        secondaryNames: ['string1', 'string2'],
        teamsImage: 'https://cms.coral.co.uk/cms//images/uploads/svg/image2.svg',
        fiveASideToggle: true,
        highlightCarouselToggle: true
      }
      ]));
      service.activeObEventId = 1234;
      service.initTeamsColors('16', 123).subscribe();

      expect(cmsService.getTeamsColors).toHaveBeenCalledWith(['Liverpool', 'Arsenal'], '16');
      expect(service.teamsColors).toEqual({
        Liverpool: {
          primaryColour: '#fff', secondaryColour: '#675d5d',
          teamsImage: 'https://cms.coral.co.uk/cms//images/uploads/svg/image1.svg',
          fiveASideToggle: true,
          highlightCarouselToggle: true
        },
        Arsenal: {
          primaryColour: '#fff', secondaryColour: '#675d5d',
          teamsImage: 'https://cms.coral.co.uk/cms//images/uploads/svg/image2.svg',
          fiveASideToggle: true,
          highlightCarouselToggle: true
        }
      });
    });
  });

  describe('showView', () => {
    it('showViewHandler should set view activeItem and player props', () => {
      service.showView({
        view: 'view',
        item: 'item',
        player: 'player'
      } as any);
      expect(service.activeItem).toEqual('item' as any);
      expect(service.view).toEqual('view' as any);
      expect(service.player).toEqual('player' as any);
    });

    it(`should not update player if Not player data`, () => {
      service['player'] = 'player';

      service.showView({
        view: 'view'
      } as any);

      expect(service['player']).toEqual('player');
    });

    it('should set Edit Mode', () => {
      service['player'] = 'player';

      service.showView({
        view: 'view'
      } as any, true);

      expect(service['player']).toEqual('player');
      expect(service.isEditMode).toBe(true);
    });

    describe('#playerListScrollPosition', () => {
      it('should set playerListScrollPosition', () => {
        service.playerListScrollPosition = 5;
        expect(service['scrollPosition']).toEqual(5);
      });
      it('should get playerListScrollPosition', () => {
        service['scrollPosition'] = 6;
        expect(service.playerListScrollPosition).toEqual(6);
      });
    });

    it(`should not update item if Not item data`, () => {
      service['item'] = 'qwerty';

      service.showView({
        view: 'item'
      } as any);

      expect(service['item']).toEqual('qwerty');
    });
  });

  describe('hideView', () => {
    it('hideView should reset view prop', () => {
      service['view'] = 'qwerty';
      service['player'] = 'player';
      service['item'] = 'item';
      service.hideView();
      expect(service['view']).toEqual('');
      expect(service['item']).toBeUndefined();
      expect(service['player']).toBeUndefined();
    });
  });

  describe('activeView', () => {
    it('should return service.view', () => {
      service['view'] = 'qwerty';
      expect(service.activeView).toEqual('qwerty');
    });
  });

  describe('activeFormation', () => {
    it('should return service.formation', () => {
      service['formation'] = 'Traditional';
      expect(service.formation).toEqual('Traditional');
    });

    it('should set value service.formation', () => {
      expect(service.formation).toEqual(undefined);
      service.activeFormation = 'Traditional';

      expect(service.activeFormation).toEqual('Traditional');
    });
  });

  describe('activeItem', () => {
    it('should return service.item', () => {
      service['item'] = 'qwerty' as any;
      expect(service.activeItem).toEqual('qwerty');
    });
  });

  describe('activePlayer', () => {
    it('should return service.player', () => {
      service['player'] = 'qwerty' as any;
      expect(service.activePlayer).toEqual('qwerty');
    });
  });

  describe('#activeMatrixFormation', () => {
    it('should get velue', () => {
      const matrix = [{ roleId: '123' }];
      service['matrixFormation'] = matrix as any;
      expect(service.activeMatrixFormation).toEqual(matrix);
    });

    it('should set velue', () => {
      const matrix = [{ roleId: '123' }];
      service.activeMatrixFormation = matrix as any;
      expect(service['matrixFormation']).toEqual(matrix);
    });
  });

  describe('#checkHexColor', () => {
    it('should return color', () => {
      const color = service.checkHexColor('#4da2f9', '123456');

      expect(color).toEqual('#4da2f9');
    });
    it('should return default color', () => {
      const color = service.checkHexColor('123456', '#675d5d');

      expect(color).toEqual('#675d5d');
    });
  });

  describe('isGK', () => {
    it('should return true', () => {
      expect(
        service['isGK']({ position: { title: 'Goalkeeper'} }, {})
      ).toBeTruthy();
    });

    it('should return true', () => {
      expect(
        service['isGK']({}, { position: 'Goalkeeper' })
      ).toBeTruthy();
    });

    it('should return false', () => {
      expect(
        service['isGK']({}, {})
      ).toBeFalsy();
    });
  });

  describe('applyStatEdit', () => {
    beforeEach(() => {
      service.item = { stat: 'Goals', statId: 1 };
    });

    it('should edit stats', () => {
      const changedItem = { stat: 'Passes', statId: 2 };
      service.applyStatEdit(changedItem);
      expect(service.item).toEqual(changedItem);
    });

    it('should not edit stats', () => {
      service.applyStatEdit(service.item);
      expect(service.item).toEqual(service.item);
    });
  });

  describe('saveDefaultStat', () => {
    beforeEach(() => {
      service.item = { stat: 'Goals', statId: 1 };
    });

    it('should save default stat', () => {
      service.saveDefaultStat();
      expect(service.item.defaultStat).toEqual({ stat: 'Goals', statId: 1 });
    });

    it('should not save default stat', () => {
      service.item.defaultStat = {};
      service.saveDefaultStat();
      expect(service.item.defaultStat).toBe(service.item.defaultStat);
    });
  });

  describe('restoreDefaultStat', () => {
    beforeEach(() => {
      service.item = { stat: 'Goals', statId: 1 };
    });

    it('should restore default stat', () => {
      service.item.defaultStat = { stat: 'To Be Carded', statId: 3 };
      service.restoreDefaultStat();
      expect(service.item).toEqual({ stat: 'To Be Carded', statId: 3, defaultStat: null });
    });

    it('should not restore default stat', () => {
      service.restoreDefaultStat();
      expect(service.item).toEqual(service.item);
    });
  });

  describe('loadPlayerStats', () => {
    it('should get players from playersStats', () => {
      service.playerStats[`111-22`] = [1, 2];
      service.loadPlayerStats(111, 22).subscribe(res => {
        expect(res).toBe(service.playerStats[`111-22`]);
      });
    });

    it('should get players from service', () => {
      yourcallMarketsService.getStatisticsForPlayer.and.returnValue(of({
        allData: [
          { id: 11, title: 'Woodwork' },
          { id: 13, title: 'Cards' },
          { id: 21, title: 'Goals' },
          { id: 22, title: 'Shoots' },
          { id: 23, title: 'Goals' }
        ]
      }));
      service.loadPlayerStats(333, 44).subscribe(res => {
        expect(res).toEqual([
          { id: 21, title: 'Goals' },
          { id: 23, title: 'Goals' },
          { id: 22, title: 'Shoots' },
          { id: 13, title: 'To Be Carded' }
        ]);
      });
    });

    it('should throw error', () => {
      yourcallMarketsService.getStatisticsForPlayer.and.returnValue(of(null));
      const errorSpy = jasmine.createSpy('errorSpy');
      service.loadPlayerStats(333, 44).subscribe(null, errorSpy);
      expect(errorSpy).toHaveBeenCalled();
    });
  });

  it('getPlayerStats', () => {
    service.playerStats[`111-22`] = [1, 2];
    expect(service.getPlayerStats(111, 22)).toBe(service.playerStats[`111-22`]);
  });

  describe('getJourneyStaticBlocks', () => {
    const staticBlockArray = [
      {
        htmlMarkup: `<h2 style="text-align: center;">
                        <span style="color: #252835;">5-A-Side</span>
                     </h2>↵
                     <p style="text-align: center;">
                        Welcome to our new feature 5-A-Side. You have a free &pound;1 bet to use, simply build your team and odds to place!
                     </p>`,
        title: 'five-a-side-free-bet'
      }
    ];
    const staticBlockObject = {
      'five-a-side-free-bet': {
        htmlMarkup: `<h2 style="text-align: center;">
                        <span style="color: #252835;">5-A-Side</span>
                     </h2>↵
                     <p style="text-align: center;">
                        Welcome to our new feature 5-A-Side. You have a free &pound;1 bet to use, simply build your team and odds to place!
                     </p>`,
        title: 'five-a-side-free-bet'
      }
    };

    it('should get static blocks', fakeAsync(() => {
      domSanitizer.bypassSecurityTrustHtml.and.returnValue(staticBlockObject['five-a-side-free-bet']);
      cmsService.getFiveASideStaticBlocks.and.returnValue(of(staticBlockArray));

      service.getJourneyStaticBlocks().subscribe();
      tick();

      expect(service['journeyItems']).toEqual(jasmine.any(Object)); // in fact it'ss equal staticBlockObject
    }));

    it('should return static blocks',() => {
      service['journeyItems'] = staticBlockObject;

      service.getJourneyStaticBlocks().subscribe(data => {
        expect(data).toEqual(service['journeyItems']);
      });
    });
  });

  describe('#getFormation', () => {
    it('should return formation, if it is part of cms list', () => {
      const formations = [{ actualFormation: '0-1-1-2'}] as any;
      const pitchFormation = '0-1-1-2';
      const response = service.getFormation(formations, pitchFormation);
      expect(response).not.toBeNull();
    });
    it('should not return formation, if it is not part of cms list', () => {
      const formations = [{ actualFormation: '0-1-1-2'}] as any;
      const pitchFormation = '0-1-1-3';
      const response = service.getFormation(formations, pitchFormation);
      expect(response).toBeUndefined();
    });
  });

  describe('#buildPitchPlayers', () => {
    it('should build pitch players with proper data', () => {
      const players = ['player-1-5-2-2', 'player-2-23-3-3', 'player-3-7-4-4'];
      const response = service.buildPitchPlayers(players);
      expect(response).toEqual([
        { index: 0, player: '5', statId: 2, line: 2, count: 1},
        { index: 1, player: '23', statId: 3, line: 3, count: 2},
        { index: 2, player: '7', statId: 4, line: 4, count: 3}
      ]);
    });

    it('should not build pitch players without proper data', () => {
      const players = ['player-5', 'player-23', 'player-7'];
      const response = service.buildPitchPlayers(players);
      expect(response).toEqual([]);
    });
  });
  describe('#setPlayerDetails', () => {
    it('should not call addRole, if pitch is null', () => {
      spyOn(service, 'addRole').and.returnValue(of());
      const players = {
        allPlayers: []
      } as any;
      service['setPlayerDetails'](null, players, null);
      expect(service.addRole).not.toHaveBeenCalled();
    });
    it('should not call addRole, if pitch does not contain players', () => {
      spyOn(service, 'addRole').and.returnValue(of());
      const players = {
        allPlayers: []
      } as any;
      const pitch = {
      } as any;
      service['setPlayerDetails'](pitch, players, null);
      expect(service.addRole).not.toHaveBeenCalled();
    });
    it('should not call addRole, if pitch does not  contain 0 players', () => {
      spyOn(service, 'addRole').and.returnValue(of());
      const players = {
        allPlayers: []
      } as any;
      const pitch = {
        players: []
      } as any;
      service['setPlayerDetails'](pitch, players, null);
      expect(service.addRole).not.toHaveBeenCalled();
    });
    it('should  call addRole, if pitch  contain 1 players', () => {
      spyOn(service, 'addRole').and.returnValue(Observable.create(observer => {
        observer.next();
        observer.complete();
      }));
      const players = {
        allPlayers: [{
          id: '21'
        }]
      } as any;
      const pitch = {
        players: [{index: 0, player:'21'}]
      } as any;
      service.matrixFormation = { 0: {}} as any;
      service['setPlayerDetails'](pitch, players, null);
      expect(service.addRole).toHaveBeenCalled();
    });
    it('should call addRole, if pitch contain more than or equal to 2 players', () => {
      spyOn(service, 'addRole').and.returnValue(Observable.create(observer => {
        observer.next();
        observer.complete();
      }));
      const players = {
        allPlayers: [{
          id: '21'
        },{
          id: '2'
        }]
      } as any;
      const pitch = {
        players: [{index: 0, player:'21'}, {index: 1, player:'2'}, {index: 2, player:'5'}]
      } as any;
      service.matrixFormation = { 0: {}} as any;
      service['setPlayerDetails'](pitch, players, null);
      expect(service.addRole).toHaveBeenCalled();
      expect(fiveASideBetService.updateBet).toHaveBeenCalled();
    });
    it('should not call addRole, if player is not present in banach players list', () => {
      spyOn(service, 'addRole').and.returnValue(of());
      const players = {
        allPlayers: [{
          id: '3'
        },{
          id: '2'
        }]
      } as any;
      const pitch = {
        players: [{index: 0, player:'21'}]
      } as any;
      service['setPlayerDetails'](pitch, players, null);
      expect(service.addRole).not.toHaveBeenCalled();
    });
  });

  describe('#addRole', () => {
      const player = {
        id: 1
      } as any;
      const item = {
        statId: 1,
        roleId: '1_2'
      } as any;
      const evententity = {
        id: '12345'
      } as any;
      const pitchPlayer = { count: 1 };
    it('should set player stats, if it contains stat values', () => {
      spyOn(service, 'setPlayerStats');
      spyOn(service, 'loadPlayerStats').and.returnValue(of([{id: 1}]));
      service['addRole'](player, item, evententity, pitchPlayer)
      .subscribe(() => {
        expect(service['setPlayerStats']).toHaveBeenCalled();
      });
    });
    it('should not add to selected players, if no stat values', () => {
      spyOn(service, 'setPlayerStats');
      spyOn(service, 'loadPlayerStats').and.returnValue(of(null));
      service['addRole'](player, item, evententity, pitchPlayer).subscribe(() => {
        expect(service['setPlayerStats']).not.toHaveBeenCalled();
      });
    });
    it('should not add to selected players, if the response has no data', () => {
      spyOn(service, 'setPlayerStats');
      spyOn(service, 'loadPlayerStats').and.returnValue(of([]));
      service['addRole'](player, item, evententity, pitchPlayer).subscribe(() => {
        expect(service['setPlayerStats']).not.toHaveBeenCalled();
      });
    });
    it('should set player stats, if it contains stat values and update bet if it is the last player', () => {
      spyOn(service, 'setPlayerStats');
      spyOn(service, 'loadPlayerStats').and.returnValue(of([{id: 1}]));
      const pitchPlayerMock = { count: 2 };
      service['addRole'](player, item, evententity, pitchPlayerMock).subscribe(() => {
        expect(service['setPlayerStats']).toHaveBeenCalled();
      });
    });
  });

  describe('#setPlayerStats', () => {
    it('should add player, if playerstats match with the request', () => {
      const item = { stat: 'Passes', statId: '2'} as any;
      const response = [{ id: '3', title: 'Goals'}] as any;
      const player = {} as any;
      const pitchPlayer = { statId: 3};
      service['setPlayerStats'](item, response, player, pitchPlayer);
      expect(fiveASideBetService.addRole).toHaveBeenCalled();
    });
    it('should not add player, if playerstats does not match with the request', () => {
      const item = { stat: 'Passes', statId: '2'} as any;
      const response = [{ id: '2', title: 'Passes'}] as any;
      const player = {} as any;
      const pitchPlayer = { statId: 3};
      service['setPlayerStats'](item, response, player, pitchPlayer);
      expect(fiveASideBetService.addRole).not.toHaveBeenCalled();
    });
  });

  describe('#isLineupAvailable', () => {
    let optaData;
    beforeEach(() => {
      optaData = { data: { participants: { home: { lineup: { id: 1}}, away: {lineup: { id: 1}}}}};
    });
    it('should return true, if optainfo in localstorage', () => {
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(true);
    });
    it('should return true, if only home contain lineup in localstorage(case away-lineup-null)', () => {
      optaData = { data: { participants: { home: { lineup: { id: 1}}, away: {lineup: null}}}};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(true);
    });
    it('should return true, if only home contain lineup in localstorage(case away-null)', () => {
      optaData = { data: { participants: { home: { lineup: { id: 1}}, away:null}}};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(true);
    });
    it('should return false, if no participants in localstorage', () => {
      optaData = { data: { participants: null}};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(false);
    });
    it('should return true, if only away contain lineup in localstorage(case home-lineup-null)', () => {
      optaData = { data: { participants: { away: { lineup: { id: 1}}, home: {lineup: null}}}};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(true);
    });
    it('should return true, if only home contain lineup in localstorage(case home-null)', () => {
      optaData = { data: { participants: { away: { lineup: { id: 1}}, home:null}}};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(true);
    });
    it('should return false, if no data property in optainfo', () => {
      optaData = { data: null};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(false);
    });
    it('should return false, if optainfo is empty object', () => {
      optaData = {};
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(false);
    });
    it('should return false, if optainfo is null', () => {
      optaData = null;
      spyOn(service._localStorage, 'getItem').and.returnValue(JSON.stringify(optaData));
      const response = service.isLineupAvailable(123);
      expect(response).toBe(false);
    });
  });

  describe('#setLineUps', () => {
    it('should not create overlaywrapper, if overlay wrapper already exist', () => {
      spyOn(service as any, 'createOverlayWrapper');
      service.setLineUps(12345, 'FOOTBALL');
      expect(service['createOverlayWrapper']).not.toHaveBeenCalled();
    });
    it('should create overlaywrapper, if overlay wrapper does not exist', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      service.setLineUps(12345, 'FOOTBALL');
      expect(windowRefService.document.createElement).toHaveBeenCalledWith('scoreboard-overlay');
    });
  });
});
