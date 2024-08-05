import { YourCallMarketPlayer } from './yourcall-market-player';

describe('YourCallMarketPlayer', () => {
  let model;

  const selectionData = { title: 'title' };

  beforeEach(() => {
    model = new YourCallMarketPlayer(selectionData);
  });

  it('should create instance', () => {
    expect(model).toBeTruthy();
  });

  describe('#getSelectionsForGroup', () => {
    it('Should get Selections For Group and filter with filterBy', () => {
      model.filterBy = 'gameId';
      model.selections = [{
        group: 2,
        player1Id: '3',
        gameId: '1'
      }, {
        group: 3,
        player1Id: '3',
        gameId: '234'
      }]as any;

      const res =  model.getSelectionsForGroup('1');
      expect(res).toEqual([{
        group: 2,
        player1Id: '3',
        gameId: '1'
      }]);
    });

    it('Should get Selections For Group and filter without filterBy, by group', () => {
      model.selections = [{
        group: 1,
        player1Id: '22',
        gameId: '234'
      }, {
        group: 3,
        player1Id: '555',
        gameId: '234'
      }]as any;

      const res =  model.getSelectionsForGroup(3);
      expect(res).toEqual([{
        group: 3,
        player1Id: '555',
        gameId: '234'
      }]);
    });
  });

  describe('#getTitle', () => {
    it('Should return empty string', () => {

      const result = model.getTitle();
      expect(result).toEqual('');
    });
  });

  describe('#sortListByField', () => {
    it('Should sort list by selected field', () => {
      const list = [{
        name: 'list2',
        id: 4
      }, {
        name: 'list1',
        id: 2
      }] as any;

      const result = YourCallMarketPlayer.sortListByField(list);
      expect(result).toEqual([{
        name: 'list1',
        id: 2
      }, {
        name: 'list2',
        id: 4
      }] as any);
    });
  });

  describe('#initGroups', () => {
    it('Should create group', () => {
      model.setData({
        _game: {
          homeTeam: {
            title: 'homeTeam',
            players: 'qqqqq'
          },
          visitingTeam: {
            title: 'visitingTeam',
            players: {
              player1: [2, 4]
            }
          },
          byb: {
            homeTeam: {
              id: 456
            },
            visitingTeam: {
              id: 347
            }
          }
        } as any
      });
      model.initGroups();

      expect(model.groups).toEqual([{
        title: 'homeTeam',
        value: 456
      }, {
        title: 'visitingTeam',
        value: 347
      }]);
    });
  });

  describe('#populate', () => {
    it('Should return true', () => {
      YourCallMarketPlayer.sortListByField = jasmine.createSpy().and.returnValue([{
        name: 'list1',
        id: 2
      }, {
        name: 'list2',
        id: 4
      }]);
      model.setData({
        _game: {
          id: 123,
          homeTeam: {
            title: 'homeTeam',
            players: [1, 2]
          },
          visitingTeam: {
            title: 'visitingTeam',
            players: {
              player1: []
            }
          }
        } as any
      });

      const result = model.populate();

      expect(model.available).toEqual(true);
      expect(model.gameId).toEqual(123);
      expect(model.players).toEqual([{
        name: 'list1',
        id: 2
      }, {
        name: 'list2',
        id: 4
      }, {
        name: 'list1',
        id: 2
      }, {
        name: 'list2',
        id: 4
      }]);
      expect(result).toEqual(true);
    });
  });

  describe('#getBetslipTitle', () => {
    it('Should get betslip title for To Be Carded', () => {
      const selection = {
        player: 'Player Name',
        stat: 1,
        value: 1,
        statistic: 'To Be Carded'
      };

      const result = model.getBetslipTitle(selection);
      expect(result).toEqual('<strong class="value">Player Name To Be Carded</strong>');
    });

    it('Should get betslip title for To Concede', () => {
      const selection = {
        player: 'Player Name',
        stat: 1,
        value: 1,
        statistic: 'To Concede'
      };

      const result = model.getBetslipTitle(selection);
      expect(result).toEqual('<strong class="value">Player Name To Concede 1+ Goals</strong>');
    });

    it('Should get betslip title for To Concede if value=0', () => {
      const selection = {
        player: 'Player Name',
        stat: 0,
        value: 0,
        statistic: 'To Concede'
      };

      const result = model.getBetslipTitle(selection);
      expect(result).toEqual('<strong class="value">Player Name To Keep A Clean Sheet</strong>');
    });

    it('Should get betslip title for To Keep A Clean Sheet', () => {
      const selection = {
        player: 'Player Name',
        stat: 1,
        value: 1,
        statistic: 'To Keep A Clean Sheet'
      };

      const result = model.getBetslipTitle(selection);
      expect(result).toEqual('<strong class="value">Player Name To Keep A Clean Sheet</strong>');
    });

    it('Should get betslip title with To Make', () => {
      const selection = {
        player: 'Player Name',
        stat: 1,
        value: 1,
        statistic: 'Passes'
      };

      const result = model.getBetslipTitle(selection);
      expect(result).toEqual('<strong class="value">Player Name To Make 1+ Passes</strong>');
    });

    it('should get betslip title with "X.X Anytime Goalscorer"', () => {
      const result = model.getBetslipTitle({
        player: 'Player Name',
        stat: 1, value: 1,
        statistic: 'Goals'
      });
      expect(result).toEqual('<strong class="value">Player Name Anytime Goalscorer</strong>');
    });
  });

  describe('#getSelectionTitle', () => {
    it('Should get selection title for To Be Carded', () => {
      const selection = {
        player: 'Player Name',
        stat: 1,
        value: 1,
        statistic: 'To Be Carded'
      };

      const result = model.getSelectionTitle(selection);
      expect(result).toEqual('Player Name To Be Carded');
    });

    it('Should get selection title for all other markets', () => {
      const selection = {
        player: 'Player Name',
        stat: '1',
        value: '1',
        statistic: 'Crosses'
      };

      const result = model.getSelectionTitle(selection);
      expect(result).toEqual('Player Name To Have 1+ Crosses');
    });

    it('Should get selection title for Shots Against The Woodwork', () => {
      const selection = {
        player: 'Player Name',
        stat: '1',
        value: '1',
        statistic: 'Shots Against The Woodwork'
      };

      const result = model.getSelectionTitle(selection);
      expect(result).toEqual('Player Name To Have 1+ Shots Hit The Woodwork');
    });
  });
});
