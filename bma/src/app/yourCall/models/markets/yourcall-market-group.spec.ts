import { YourCallMarketGroup } from './yourcall-market-group';

describe('#YourCallMarketGroup', () => {
  let model;

  beforeEach(() => {
    model = new YourCallMarketGroup({} as any);
  });

  it('should create instance', () => {
    expect(model).toBeTruthy();
  });

  describe('#add', () => {
    it('should call add method', () => {
      model.add({id: '12345'} as any);

      expect(model.markets).toEqual([{ id: '12345' }]as any);
    });
  });

  it('should get id', () => {
    model.add({ id: '12345' } as any);
    model.add({ id: '12345' } as any);
    model.add({ id: '12345' } as any);

    expect(model.id).toEqual('12345,12345,12345');
  });

  it('should get count', () => {
    model.add({ id: '12345' } as any);
    model.add({ id: '12345' } as any);
    model.add({ id: '12345' } as any);

    expect(model.count).toEqual(3);
  });

  describe('#_populate', () => {
    it('should call _populate method equal market id', () => {
      const market = { id: '12345', populate: jasmine.createSpy('populate') } as any;
      model.add(market);
      model._populate([{ id: '12345' }] as any);

      expect(market.populate).toHaveBeenCalled();
    });

    it('should call _populate method mot equal market id', () => {
      const market = { id: '12245', populate: jasmine.createSpy('populate') } as any;
      model.add(market);
      model._populate([{ id: '12345' }] as any);

      expect(market.populate).not.toHaveBeenCalled();
    });
  });

  describe('#parseTitle', () => {
    it('should call parseTitle method when no game', () => {
      model.title = 'title';
      model.parseTitle();

      expect(model.title).toEqual('title');
    });

    it('should call parseTitle method when no homeTeam', () => {
      model.setData({
        _game: {}
      });
      model.title = 'title';
      model.parseTitle();

      expect(model.title).toEqual('title');
    });


    it('should call parseTitle method when no visitingTeam', () => {
      model.setData({
        _game: {
          homeTeam: {
            title: 'homeTeam'
          }
        }
      });
      model.title = 'title';
      model.parseTitle();

      expect(model.title).toEqual('title');
    });

    it('should call parseTitle method when game is present', () => {
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
      model.title = 'HOME vs AWAY';
      model.parseTitle();

      expect(model.title).toEqual('homeTeam vs visitingTeam');
    });
  });
});
