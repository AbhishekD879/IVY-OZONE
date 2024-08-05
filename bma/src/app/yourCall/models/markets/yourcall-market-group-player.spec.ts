import { YourCallMarketGroupPlayer } from './yourcall-market-group-player';

describe('#YourCallMarketGroupPlayer', () => {
  let model;

  beforeEach(() => {
    model = new YourCallMarketGroupPlayer({} as any);
  });

  it('should create instance', () => {
    expect(model).toBeTruthy();
  });

  describe('#_populate', () => {
    it('should call _populate method  when isUndefined selection value', () => {
      expect(model.selections).toEqual([]);
      model.setData({
        _game: {
          homeTeam: {
            title: 'homeTeam'
          },
          visitingTeam: {
            title: 'visitingTeam'
          }
        }
      });

      model._populate([{
        selections: [{
          title: 'title',
          id: '2'
        }]
      }]);

      expect(model.selections).toEqual([{
        title: 'Title',
        value: '2',
        id: '2',
        group: undefined
      }]);
    });

    it('should call _populate', () => {
      expect(model.selections).toEqual([]);
      model.setData({
        _game: {
          homeTeam: {
            title: 'homeTeam'
          },
          visitingTeam: {
            title: 'visitingTeam'
          }
        }
      });

      model._populate([{
        selections: [{
          title: 'title',
          value: '1',
          id: '2'
        }]
      }]);

      expect(model.selections).toEqual([{
        title: 'Title',
        value: '1',
        id: '2',
        group: undefined
      }]);
    });

    it('should call _populate and return false', () => {
      expect(model._populate(undefined)).toEqual(false);

      expect(model._populate([{}] as any)).toEqual(false);

      expect(model._populate([] as any)).toEqual(false);
    });
  });

  describe('#getSelectionsForGroup', () => {
    it('shoul call getSelectionsForGroup method', () => {
      model.setData({
        _game: {
          homeTeam: {
            title: 'homeTeam'
          },
          visitingTeam: {
            title: 'visitingTeam'
          }
        }
      });

      model._populate([{
        selections: [{
          title: 'title',
          value: '1',
          id: '2'
        }]
      }]);
      const result = model.getSelectionsForGroup(1);

      expect(result).toEqual([]);
    });
  });
});
