import { YourCallMarketGroupItem } from './yourcall-market-group-item';

describe('#YourCallMarketGroupItem', () => {
  let model;
  const selectionData = { title: 'title' };

  beforeEach(() => {
    model = new YourCallMarketGroupItem(selectionData);
    model.parent = {
      count: 1,
      getTitle: () => 'title',
      title: 'title'
    };

    model._locale = {
      getString: (string) => {
        if (string === 'yourCall.wholeMatch') {
          return 'yourCall.wholeMatch';
        }

        if (string === 'yourCall.firstHalf') {
          return 'yourCall.firstHalf';
        }

        if (string === 'yourCall.secondHalf') {
          return 'yourCall.secondHalf';
        }
      }
    };
  });

  it('should create instance', () => {
    expect(model).toBeTruthy();
  });

  describe('#cols', () => {
    it('should get cols', () => {
      expect(model.cols).toEqual(false);
    });

    it('should get cols when 3 ', () => {
      model._populate([{
        title: 'title',
        id: '2'
      }, {
        title: 'title',
        id: '2'
      }, {
        title: 'title',
        id: '2'
      }]);
      model.selection = [{}, {}, {}];
      expect(model.cols).toEqual(3);
    });
  });

  it('should get onlyChild', () => {
    expect(model.onlyChild).toEqual(true);
  });

  describe('#getTitle', () => {
    it('should call getTitle method', () => {
      const result = model.getTitle();
      expect(result).toEqual('title ');
    });
  });

  describe('#getShortTitle', () => {
    it('if onlyChild', () => {
      const result = model.getShortTitle();
      expect(result).toEqual('');
    });

    it('if parent.title match title', () => {
      model.parent.count = 2;
      const result = model.getShortTitle();

      expect(result).toEqual('yourCall.wholeMatch');
    });

    it('if firstHalf', () => {
      model.title = 'HALF TIME';
      model.parent.count = 2;
      const result = model.getShortTitle();
      expect(result).toEqual('yourCall.firstHalf');
    });

    it('if secondHalf', () => {
      model.title = '2ND';
      model.parent.count = 2;
      const result = model.getShortTitle();
      expect(result).toEqual('yourCall.secondHalf');
    });

    it('if onlyChild', () => {
      model.title = 'NO TIME';
      model.parent.count = 2;
      const result = model.getShortTitle();
      expect(result).toEqual('NO TIME');
    });
  });

  describe('#_populate', () => {
    it('should call _populate method  when isUndefined selection value', () => {
      expect(model.selections).toEqual([]);

      model._populate([{
        title: 'title',
        id: '2'
      }]);

      expect(model.selections).toEqual([{
        title: 'Title',
        value: '2',
        id: '2'
      }]);
    });

    it('should call _populate', () => {
      expect(model.selections).toEqual([]);

      model._populate([{
        title: 'title',
        value: '1',
        id: '2'
      }]);

      expect(model.selections).toEqual([{
        title: 'Title',
        value: '1',
        id: '2'
      }]);
    });
  });

  it('ucWord', () => {
    expect(YourCallMarketGroupItem.ucWord('VAN DIJK')).toEqual('Van Dijk');
    expect(YourCallMarketGroupItem.ucWord('N. KEÏTA')).toEqual('N. Keïta');
    expect(YourCallMarketGroupItem.ucWord('ALEXANDER-ARNOLD')).toEqual('Alexander-Arnold');
    expect(YourCallMarketGroupItem.ucWord(`O'BRIEN`)).toEqual(`O'Brien`);
    expect(YourCallMarketGroupItem.ucWord('G.FERNANDES')).toEqual('G.Fernandes');
  });

  it('ucWord', () => {
    YourCallMarketGroupItem.ucWord('')
  });
});
