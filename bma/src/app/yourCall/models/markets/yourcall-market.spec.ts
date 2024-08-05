import { YourCallMarket } from './yourcall-market';
import { Subject } from 'rxjs';

describe('YourCallMarket', () => {
  let model;
  const selectionData = { title: 'title' };

  beforeEach(() => {
    model = new YourCallMarket(selectionData);
  });

  it('Should get markets selection title for betslip', () => {
    const selection = {
      dashboardTitle: 'dashboardTitle',
      title: 'title'
    };

    const actualResult = model.getBetslipTitle(selection);
    expect(actualResult).toEqual('<strong class="value">dashboardtitle</strong> title');
  });

  it('Should get markets withut a Val', () => {
    const selection = {
      dashboardTitle: 'dashboardTitle',
      title: 'title'
    };
    spyOn(model, 'getSelectionTitle').and.returnValue(undefined);
    const actualResult = model.getBetslipTitle(selection);
    expect(actualResult).toEqual('<strong class="value">undefined</strong> title');
  });

  describe('#toggleLoading', () => {
    it('should call toggleLoading method', () => {
      expect(model.loading).toEqual(false);

      model.toggleLoading();

      expect(model.loading).toEqual(true);
    });
  });

  describe('#_populate', () => {
    it('should call _populate method', () => {
      const result = model._populate();

      expect(result).toEqual(true);
    });
  });

  describe('#populate', () => {
    it('should call populate method', () => {
      model.populate();

      expect(model._loaded).toEqual(true);
    });

    it('should call populate method _loaded = true', () => {
      model._loaded = true;
      model.populate();

      expect(model._loaded).toEqual(true);
    });

    it('should call populate method with subject', () => {
      const subject = new Subject();
      model.registerAfterLoad(subject);

      model.populate();

      expect(model._loaded).toEqual(true);
    });
  });

  describe('#registerAfterLoad', () => {
    it('should call registerAfterLoad method', () => {
      model.registerAfterLoad({});

      expect(model._afterLoad).toEqual({});
    });
  });

  describe('#isLoaded', () => {
    it('should call isLoaded method', () => {
      const result = model.isLoaded();

      expect(result).toEqual(false);
    });
  });

  describe('#setData', () => {
    it('should call setData method', () => {
      expect(model.date).toBeUndefined();
      model.setData({
        date: 'date'
      });

      expect(model.date).toEqual('date');
    });
  });

  describe('#getTitle', () => {
    it('should call getTitle method', () => {
      const result = model.getTitle();

      expect(result).toEqual('title');
    });
  });

  describe('#game', () => {
    it('should get game', () => {
      expect(model.game).toEqual(undefined);
    });

    it('should set game', () => {
      model.game = {};
      expect(model.game).toEqual({});
    });
  });

  describe('#isSelected', () => {
    it('should call isSelected method', () => {
      const result = model.isSelected({} as any);

      expect(result).toEqual(false);
    });
  });

  describe('#addSelection', () => {
    it('should call addSelection method single', () => {
      model.addSelection({} as any);

      expect(model.selected[0]).toEqual({});
    });

    it('should call addSelection method multi', () => {
      model.multi = true;
      model.addSelection({} as any);

      expect(model.selected).toEqual([{}]);
    });
  });

  describe('#editSelection', () => {
    it('should call editSelection method (edit and multi) = true', () => {
      model.edit = true;
      model.multi = true;
      const selection = {
        id: 'selection'
      } as any;
      const newSelection = {
        id: 'newSelection'
      } as any;
      model.selected[0] = selection;
      model.editSelection(selection, newSelection);

      expect(model.selected[0]).toEqual(newSelection);
    });

    it('should call editSelection method edit = true and multi = false', () => {
      model.edit = true;
      model.multi = false;
      const selection = {
        id: 'selection'
      } as any;
      const newSelection = {
        id: 'newSelection'
      } as any;
      model.selected[0] = selection;
      model.editSelection(selection, newSelection);

      expect(model.selected[0]).toEqual(selection);
    });

    it('should call editSelection method (edit and multi) = false', () => {
      model.edit = false;
      model.multi = false;
      const selection = {
        id: 'selection'
      } as any;
      const newSelection = {
        id: 'newSelection'
      } as any;
      model.selected[0] = selection;
      model.editSelection(selection, newSelection);

      expect(model.selected[0]).toEqual(selection);
    });
  });

  describe('#removeSelection', () => {
    it('should call removeSelection method for multi', () => {
      model.multi = true;
      model.selected = [{ id: 'id' }, { id: 'id1' }];
      model.removeSelection({ id: 'id' });

      expect(model.selected).toEqual([{ id: 'id1' }]);
    });

    it('should call removeSelection method for single', () => {
      model.order = 12;
      model.selected = [{}] as any;
      model.multi = false;
      model.removeSelection({});

      expect(model.selected).toEqual([]);
      expect(model.order).toEqual(undefined);
    });
  });

  describe('#clearSelections', () => {
    it('should call clearSelections method', () => {
      model.selected = [{}, {}, {}] as any;
      model.clearSelections();

      expect(model.selected).toEqual([]);
    });
  });

  describe('#_findIndex', () => {
    it('should call _findIndex method', () => {
      model.selected = [{id: 'id'}];
      const result = model._findIndex({id: 'id'});

      expect(result).toEqual(0);
    });
  });

  describe('sortSelections', () => {
    beforeEach(() => {
      model.selections = [
        { title: 'player1', odds: '2.341' },
        { title: 'player2', odds: '1.5' }
      ];
    });

    it('should not sort selections', () => {
      model.id = 999;
      model.sortSelections();
      expect(model.selections).toEqual([
        { title: 'player1', odds: '2.341' },
        { title: 'player2', odds: '1.5' }
      ]);
    });

    it('should sort selections', () => {
      model.id = 29;
      model.sortSelections();
      expect(model.selections).toEqual([
        { title: 'player2', odds: '1.5' },
        { title: 'player1', odds: '2.341' }
      ]);
    });
  });

  describe('#removeSelection missing', () => {
    it('removeSelection', () => {
      model.multi = true;
      model.removeSelection({marketType : 'Player Bet' , idd: 1});
    });

    it('removeSelection', () => {
      model.multi = true;
      model.removeSelection({marketType : 'Playetesf' , idd: 1});
    });
  });
});
