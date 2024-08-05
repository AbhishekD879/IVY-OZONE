import { FiveASideBetService } from './five-a-side-bet.service';
import { fakeAsync, flush } from '@angular/core/testing';

describe('#FiveASideBet', () => {
  let bet;
  let yourcallMarketsService;
  let yourcallProviderService;
  let pubsubService;
  let localeService;
  let coreTools;
  let playersArray;
  let rolesArray;

  const selectedPlayersMock = new Map();
  selectedPlayersMock.set('Player1', { statId: 3 });
  selectedPlayersMock.set('Player3', { statId: 7 });

  beforeEach(() => {
    playersArray = [
      {
        id: 10,
        name: 'L. Messi',
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      } as any,
      {
        id: 7,
        name: 'C. Ronaldo',
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      } as any,
      {
        id: 8,
        name: 'A. Oxlade-Chamberlain',
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      } as any,
      {
        id: 9,
        name: 'R. O\'Sullivan',
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      } as any,
      {
        id: 11,
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      } as any
    ];

    rolesArray = [
      {
        statId: 1,
        roleId: 'Position1'
      } as any,
      {
        statId: 2,
        roleId: 'Position2',
        stat: 'Tackles'
      } as any,
      {
        statId: 2,
        roleId: 'Position3'
      } as any,
      {
        statId: 4,
        roleId: 'Position4'
      } as any,
      {
        statId: 5,
        roleId: 'Position5'
      } as any
    ];

    yourcallMarketsService = {
      game: {
        obEventId: 123456
      },
      getMarketInstance: jasmine.createSpy('getMarketInstance').and.returnValue({})
    };

    yourcallProviderService = {
      calculateAccumulatorOdds:  jasmine.createSpy('getMarketInstance').and.returnValue(Promise.resolve()),
      isValidResponse: jasmine.createSpy('isValidResponse'),
      helper: {
        parseOddsValue: jasmine.createSpy('parseOddsValue').and.callFake(x => Promise.resolve(x))
      }
    };

    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };

    pubsubService = {
      publish: jasmine.createSpy('publish'),
      API: {
        ADD_TO_YC_BETSLIP: 'ADD_TO_YC_BETSLIP'
      }
    };

    coreTools = {
      getOwnDeepProperty: jasmine.createSpy('getOwnDeepProperty')
    };

    bet = new FiveASideBetService(
      yourcallMarketsService as any,
      yourcallProviderService as any,
      pubsubService as any,
      localeService as any,
      coreTools as any,
    );
    bet.initialize({ id: 123456 } as any);
    spyOn(bet, 'betUpdated').and.callThrough();
    spyOn(bet, 'clearErrors').and.callThrough();
    spyOn(bet, 'parseError').and.callThrough();
    spyOn(bet, 'getPriceUpdateParams').and.callThrough();
  });

  it('should init instance', () => {
    expect(bet).toBeTruthy();
    expect(bet.eventEntity).toEqual({ id: 123456 } as any);
    expect(bet.game).toEqual({ obEventId: 123456 } as any);
  });

  describe('initialize', () => {
    it('should initialize bet with proper event', () => {
      yourcallMarketsService.game = {
        obEventId: 567890
      } as any;
      bet.initialize({ id: 567890 } as any);
      expect(bet['game']).toEqual({
        obEventId: 567890
      } as any);
      expect(bet.eventEntity).toEqual({ id: 567890 } as any);
    });
  });

  describe('playersObject', () => {
    it('should return players object literal', () => {
      bet.addRole(playersArray[0], rolesArray[0], 1);
      expect(bet.playersObject['Position1']).toBeTruthy();
    });
    it('should not update bet, if updateBet input is false', () => {
      bet.addRole(playersArray[0], rolesArray[0], 1, false);
      expect(bet.betUpdated).not.toHaveBeenCalled();
    });
  });

  describe('errorMessage', () => {
    it('should return samePlayerErrorMessage if it not empty', () => {
      bet['samePlayerErrorMessage'] = 'samePlayerErrorMessage';
      bet['priceUpdateErrorMessage'] = 'priceUpdateErrorMessage';
      expect(bet.errorMessage).toEqual('samePlayerErrorMessage');
    });
    it('should return priceUpdateErrorMessage if samePlayerErrorMessage is empty', () => {
      bet['samePlayerErrorMessage'] = '';
      bet['priceUpdateErrorMessage'] = 'priceUpdateErrorMessage';
      expect(bet.errorMessage).toEqual('priceUpdateErrorMessage');
    });
    it('should return empty string if bet is in edit state', () => {
      bet['priceUpdateErrorMessage'] = 'priceUpdateErrorMessage';
      bet.setEditState();
      expect(bet.errorMessage).toEqual('');
    });
  });

  describe('disabledRolesMarked', () => {
    it('should return samePlayersMarked if it truthy', () => {
      bet['samePlayersMarked'] = true;
      bet['conflictPlayersMarked'] = false;
      expect(bet.disabledRolesMarked).toBeTruthy();
    });
    it('should return conflictPlayersMarked if samePlayerErrorMessage is falsy', () => {
      bet['samePlayersMarked'] = false;
      bet['conflictPlayersMarked'] = true;
      expect(bet.disabledRolesMarked).toBeTruthy();
    });
    it('should return false if both is falsy', () => {
      bet['samePlayersMarked'] = false;
      bet['conflictPlayersMarked'] = false;
      expect(bet.disabledRolesMarked).toBeFalsy();
    });
  });

  describe('addToBetslip', () => {
    it('should add selections to betslip if bet is valid', () => {
      bet.eventEntity = {
        typeId: 111,
        id: 22
      };
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.isValid = true;
      bet.addToBetslip();
      expect(pubsubService.publish).toHaveBeenCalledWith('ADD_TO_YC_BETSLIP', jasmine.anything());
    });
    it('shouldn`t add selections to betslip if bet is not valid', () => {
      bet.isValid = false;
      bet.addToBetslip();
      expect(pubsubService.publish).not.toHaveBeenCalled();
    });
  });

  it('addRole should add role to bed anc call betUpdated method', () => {
    bet.addRole(playersArray[0], rolesArray[0], 1);
    expect(bet.betUpdated).toHaveBeenCalled();
    expect(bet.roleEmpty(rolesArray[0].roleId)).toBeFalsy();
  });

  describe('roleEmpty', () => {
    it('should return false if role empty', () => {
      expect(bet.roleEmpty(rolesArray[0].roleId)).toBeTruthy();
    });
    it('should return false if role empty', () => {
      bet.addRole(playersArray[0], rolesArray[0], 1);
      expect(bet.roleEmpty(rolesArray[0].roleId)).toBeFalsy();
    });
  });

  describe('getRole', () => {
    it('should return false if role empty', () => {
      expect(bet.getRole(rolesArray[0].roleId)).toBeFalsy();
    });
    it('should return false if role empty', () => {
      bet.addRole(playersArray[0], rolesArray[0], 1);
      expect(bet.getRole(rolesArray[0].roleId)).toBeTruthy();
    });
  });

  it('clearRole should remove role to and call betUpdated method', () => {
    bet.addRole(playersArray[0], rolesArray[0], 1);
    bet.clearRole(rolesArray[0].roleId);
    expect(bet.betUpdated).toHaveBeenCalledTimes(2);
    expect(bet.roleEmpty(rolesArray[0].roleId)).toBeTruthy();
  });

  it('clear should remove all call betUpdated, clearErrors  methods', () => {
    bet.addRole(playersArray[0], rolesArray[0], 1);
    bet.addRole(playersArray[1], rolesArray[1], 1);
    bet.clear();
    expect(bet.betUpdated).toHaveBeenCalledTimes(3);
    expect(bet.clearErrors).toHaveBeenCalled();
    expect(bet['selectedPlayers'].size).toEqual(0);
  });

  it('should call betUpdated from updateBet method', () => {
    bet.updateBet();

    expect(bet.betUpdated).toHaveBeenCalled();
  });

  describe('isRoleDisabled', () => {
    it('should return false if roles not marked', () => {
      bet['conflictPlayersMarked'] = false;
      expect(bet.isRoleDisabled('123')).toBeFalsy();
    });
    it('should return false if roles marked and player have conflict', () => {
      bet['conflictPlayersMarked'] = true;
      const role = bet.addRole(playersArray[0], rolesArray[0], 1);
      role.setConflict();
      expect(bet.isRoleDisabled(rolesArray[0].roleId)).toBeFalsy();
    });
    it('should return true if roles marked and player doesn`t have conflict', () => {
      const role = bet.addRole(playersArray[1], rolesArray[2], 1);
      role.resetConflict();
      bet['conflictPlayersMarked'] = true;
      expect(bet.isRoleDisabled(rolesArray[2].roleId)).toBeTruthy();
    });
    it('should return true if roles marked and role not filled yet', () => {
      bet['conflictPlayersMarked'] = true;
      expect(bet.isRoleDisabled(rolesArray[0].roleId)).toBeTruthy();
    });
  });

  describe('checkPlayerDuplicateForStat', () => {
    it('should set error for duplicate players for stat', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.addRole(playersArray[0], rolesArray[2], 1);
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.checkPlayerDuplicateForStat();
      expect(bet['samePlayerErrorMessage']).toEqual('yourCall.fiveASideDefaultError');
      expect(bet['samePlayersMarked']).toBeTruthy();
    });
    it('should`t set error if there are no duplicate players for stat', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.checkPlayerDuplicateForStat();
      expect(bet['samePlayerErrorMessage']).toBeFalsy();
      expect(bet['samePlayersMarked']).toBeFalsy();
    });
  });
  describe('validateBet', () => {
    it('should return if all validations are valid', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.samePlayerErrorMessage = '';
      bet.priceUpdateErrorMessage = '';
      bet['validateBet']();
      expect(bet.isValid).toBeTruthy();
    });
    it('should return false if samePlayerErrorMessage is set', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.samePlayerErrorMessage = 'samePlayerErrorMessage';
      bet.priceUpdateErrorMessage = '';
      bet['validateBet']();
      expect(bet.isValid).toBeFalsy();
    });
    it('should return false if priceUpdateErrorMessage is set', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.addRole(playersArray[0], rolesArray[0], 1);
      bet.samePlayerErrorMessage = '';
      bet.priceUpdateErrorMessage = 'priceUpdateErrorMessage';
      bet['validateBet']();
      expect(bet.isValid).toBeFalsy();
    });
    it('should return false if count of selection less then 2', () => {
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.samePlayerErrorMessage = '';
      bet.priceUpdateErrorMessage = '';
      bet['validateBet']();
      expect(bet.isValid).toBeFalsy();
    });
  });

  it('getSelectionForBetslip should return valid selection for BYB Betslip', () => {
    const role = bet.addRole(playersArray[0], rolesArray[1], 1);
    expect(bet['getSelectionForBetslip'](role)).toEqual({
      selectedInfo: {
        player: {
          id: 10,
          name: 'L. Messi',
          teamColors: {
            primaryColour: '#777',
            secondaryColour: '#675d5d'
          }
        },
        stat: {
          id: 2,
          title: 'Tackles'
        },
        statVal: 1
      },
      id: jasmine.anything(),
      marketType: 'playerBets',
      player: 'L. Messi',
      playerObj: {
        id: 10,
        name: 'L. Messi',
        teamColors: {
          primaryColour: '#777',
          secondaryColour: '#675d5d'
        }
      },
      statObj: { id: 2, title: 'Tackles' },
      playerId: 10,
      statistic: 'Tackles',
      stat: 1,
      statisticId: 2,
      type: 1,
      value: 1,
      condition: 3,
      odds: {
        type: 1,
        condition: 3,
        value: 1
      },
      edit: false,
      disable: false
    });
  });

  describe('updatePrices', () => {
    it('shouldn`t call calculateAccumulatorOdds if there are no players added to bet', () => {
      bet.formattedPrice = '5/1';
      bet.updatePrices();
      expect(yourcallProviderService.calculateAccumulatorOdds).not.toHaveBeenCalled();
      expect(bet['clearErrors']).toHaveBeenCalled();
      expect(bet.formattedPrice).toBeFalsy();
    });
    it('should follow Success flow', fakeAsync(() => {
      yourcallProviderService.calculateAccumulatorOdds = jasmine.createSpy('calculateAccumulatorOdds').and.returnValue(
        Promise.resolve('10/1')
      );
      bet.addRole(playersArray[0], rolesArray[1], 1);
      bet.updatePrices();
      expect(bet.loadingOdds).toBeTruthy();
      expect(bet['getPriceUpdateParams']).toHaveBeenCalled();
      expect(yourcallProviderService.calculateAccumulatorOdds).toHaveBeenCalledWith({
        obEventId: 123456,
        selectionIds: [],
        playerSelections: [
          {
            statId: 2,
            playerId: 10,
            line: 1
          }
        ]
      });
      flush();
      expect(bet.loadingOdds).toBeFalsy();
      expect(bet.formattedPrice).toEqual('10/1');
      expect(bet['clearErrors']).toHaveBeenCalled();
    }));
    it('should follow Error flow: not parse error if response not valid', fakeAsync(() => {
      yourcallProviderService.calculateAccumulatorOdds = jasmine.createSpy('calculateAccumulatorOdds').and.returnValue(
        Promise.reject({} as any)
      );
      bet.addRole(playersArray[0], rolesArray[1], 1);
      yourcallProviderService.isValidResponse = jasmine.createSpy('isValidResponse').and.returnValue(false);
      bet.updatePrices();
      flush();
      expect(bet['parseError']).not.toHaveBeenCalled();
    }));
    it('should follow Error flow: should set default message and mark all players as conflict' +
      'if there is no error message in error response', fakeAsync(() => {
      yourcallProviderService.calculateAccumulatorOdds = jasmine.createSpy('calculateAccumulatorOdds').and.returnValue(
        Promise.reject({} as any)
      );
      bet.addRole(playersArray[0], rolesArray[1], 1);
      yourcallProviderService.isValidResponse = jasmine.createSpy('isValidResponse').and.returnValue(true);

      bet.updatePrices();
      flush();
    }));
    it('should follow Error flow: mark conflict players (when count of found players' +
      'same as should be) and format error message', fakeAsync(() => {
      yourcallProviderService.calculateAccumulatorOdds = jasmine.createSpy('calculateAccumulatorOdds').and.returnValue(
        Promise.reject({} as any)
      );
      coreTools.getOwnDeepProperty = jasmine.createSpy().and.returnValue('Cannot combine: [MESSI TO HAVE 2 OR MORE CROSSES in ' +
        'PLAYER TOTAL CROSSES] and [OXLADE-CHAMBERLAIN TO SCORE 1 OR MORE GOALS INSIDE BOX in PLAYER TOTAL GOALS ' +
        'INSIDE BOX] and [O\'SULLIVAN TO SCORE 1 OR MORE GOALS OUTSIDE BOX in PLAYER TOTAL GOALS OUTSIDE BOX]');
      yourcallProviderService.isValidResponse = jasmine.createSpy('isValidResponse').and.returnValue(true);
      const roles = [
        bet.addRole(playersArray[0], rolesArray[1], 1),
        bet.addRole(playersArray[2], rolesArray[0], 1),
        bet.addRole(playersArray[3], rolesArray[2], 1),
        bet.addRole(playersArray[1], rolesArray[3], 1),
      ];
      bet.updatePrices();
      flush();
      expect(bet.errorMessage).toEqual('Cannot combine: Messi to have 2 or more crosses and Oxlade-Chamberlain ' +
        'to score 1 or more goals inside box and O\'Sullivan to score 1 or more goals outside box');
      expect(bet.disabledRolesMarked).toBeTruthy();
      expect(roles.map(role => role.hasConflict)).toEqual([true, true, true, false]);
    }));
    it('should follow Error flow: mark all players as conflict (when count of found players' +
      'less then should be) and format error message', fakeAsync(() => {
      yourcallProviderService.calculateAccumulatorOdds = jasmine.createSpy('calculateAccumulatorOdds').and.returnValue(
        Promise.reject({} as any)
      );
      coreTools.getOwnDeepProperty = jasmine.createSpy().and.returnValue('Cannot combine: [MESSI TO HAVE 2 OR MORE CROSSES in ' +
        'PLAYER TOTAL CROSSES] and [OXLADE-CHAMBERLAIN TO SCORE 1 OR MORE GOALS INSIDE BOX in PLAYER TOTAL GOALS ' +
        'INSIDE BOX] and [RONALDINHO TO SCORE 1 OR MORE GOALS OUTSIDE BOX in PLAYER TOTAL GOALS OUTSIDE BOX]');
      yourcallProviderService.isValidResponse = jasmine.createSpy('isValidResponse').and.returnValue(true);
      const roles = [
        bet.addRole(playersArray[0], rolesArray[1], 1),
        bet.addRole(playersArray[2], rolesArray[0], 1),
        bet.addRole(playersArray[3], rolesArray[2], 1),
        bet.addRole(playersArray[1], rolesArray[3], 1),
        bet.addRole(playersArray[4], rolesArray[4], 1),
      ];
      bet.updatePrices();
      flush();
      expect(bet.errorMessage).toEqual('Cannot combine: Messi to have 2 or more crosses and Oxlade-Chamberlain ' +
        'to score 1 or more goals inside box and Ronaldinho to score 1 or more goals outside box');
      expect(bet.disabledRolesMarked).toBeTruthy();
      expect(roles.map(role => role.hasConflict)).toEqual([true, true, true, true, true]);
    }));
  });
  it('camelizeErrorText should`t fail in edge case', () => {
    expect(bet['camelizeErrorText'](undefined as any)).toEqual('');
  });
  it('setEditState should set edit state', () => {
    expect(bet['isEditState']).toBeFalsy();
    bet.setEditState();
    expect(bet['isEditState']).toBeTruthy();
  });
  it('resetEditState should set edit state', () => {
    bet.setEditState();
    expect(bet['isEditState']).toBeTruthy();
    bet.resetEditState();
    expect(bet['isEditState']).toBeFalsy();
  });

  it('#backupPlayers should save copy of selected players', () => {
    bet.addRole(playersArray[0], rolesArray[1], 1);
    bet.backupPlayers();
    expect(bet['backupSelectedPlayers']).toEqual(bet['selectedPlayers']);
    expect(bet['backupSelectedPlayers'].size).toBe(1);
  });

  it('#clearPlayersBackup should clear selected players copy', () => {
    bet.addRole(playersArray[0], rolesArray[1], 1);
    bet.clearPlayersBackup();
    expect(bet['backupSelectedPlayers']).toEqual(undefined);
  });

  it('#clearPlayersBackup should restore players from backup', () => {
    bet.addRole(playersArray[0], rolesArray[1], 1);
    bet.backupPlayers();
    bet.clear();
    bet.restorePlayers();

    expect(bet['selectedPlayers'].size).toBe(1);
  });

  it('#clearPlayersBackup should not restore', () => {
    bet.addRole(playersArray[0], rolesArray[1], 1);
    bet.clear();
    bet.restorePlayers();

    expect(bet['selectedPlayers'].size).toBe(0);
    expect(bet['backupSelectedPlayers']).toEqual(undefined);
    expect(bet.betUpdated).toHaveBeenCalledTimes(2);
  });
});
