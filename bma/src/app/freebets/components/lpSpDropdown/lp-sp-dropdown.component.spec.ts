import { LpSpDropdownComponent } from './lp-sp-dropdown.component';

describe('LpSpDropdownComponent', () => {
  let component: LpSpDropdownComponent;

  beforeEach(() => {
    component = new LpSpDropdownComponent();
  });

  it('ngOnInit', () => {
    component.options = [
      {
        name: 'LP',
        value: '10'
      },
      {
        name: 'SP',
        value: 'SP'
      }
    ];
    component.selectedValue = 'SP';
    component.ngOnInit();
    expect(component.selectedItem).toEqual(component.options[1]);
  });

  describe('toggleList', () => {
    it('toggleList', () => {
      component.toggleList();
      expect(component.listOpen).toEqual(true);
    });

    it('toggleList open', () => {
      component.listOpen = true;
      component.toggleList();
      expect(component.listOpen).toEqual(false);
    });

    it('toggleList disabled', () => {
      component.disabled = true;
      component.toggleList();
      expect(component.listOpen).toEqual(false);
    });
  });

  describe('selectItem', () => {
    it('selectItem', () => {
      const menuItem = { name: 'LP', value: '10' };
      component.listOpen = true;
      component.selectItem(menuItem);
      expect(component.selectedItem).toEqual(menuItem);
      expect(component.listOpen).toEqual(false);
    });

    it('toggleList disabled', () => {
      const menuItem = { name: 'LP', value: '10' };
      component.disabled = true;
      component.selectItem(menuItem);
      expect(component.selectedItem).not.toEqual(menuItem);
    });
  });

  describe('clickOutside', () => {
    it('click outside', () => {
      component.listOpen = true;
      component.clickOutside();
      expect(component.listOpen).toEqual(false);
    });

    it('click inside', () => {
      component.listOpen = true;
      component.clickInside = true;
      component.clickOutside();
      expect(component.listOpen).toEqual(true);
    });
  });

  it('trackByName', () => {
    expect(component.trackByName(2, { name: 'test' } as any)).toEqual('2_test');
  });

  it('updateSelectedItem (!selectedValue)', () => {
    component.ngOnInit();
    component['updateSelectedItem']();
    expect(component.selectedItem).toEqual(undefined);
  });

  it('updateSelectedItem', () => {
    component.selectedValue = 'test';
    component.options = <any>[{name: 't'}, {name: 'test'}];
    component.ngOnInit();
    component['updateSelectedItem']();
    expect(component.selectedItem).toEqual(component.options[1]);
  });
});
