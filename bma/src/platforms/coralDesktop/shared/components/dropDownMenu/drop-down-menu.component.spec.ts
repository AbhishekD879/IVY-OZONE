import { DropDownMenuComponent } from './drop-down-menu.component';

import { IMenuItem } from '@shared/components/dropDownMenu/drop-down-menu.model';

describe('DesktopDropDownMenuComponent', () => {
  let component: DropDownMenuComponent;

  beforeEach(() => {
    component = new DropDownMenuComponent();
  });

  it('getSelectedItemName - should set selected item from menu', () => {
    component.menuList = [{ name: 'Match Result' }] as IMenuItem[];
    expect(component.getSelectedItemName('Match Result')).toBe('Match Result');
  });

  it('getSelectedItemName - should set selected item from menu if it is exist', () => {
    component.menuList = [{ name: 'Match Result' }] as IMenuItem[];
    expect(component.getSelectedItemName('Total Goals Over/Under 2.5')).toBe('Total Goals Over/Under 2.5');
  });

  it('getSelectedItemName - should set selected text item from menu', () => {
    component.menuList = [{
      templateMarketName: 'Match Result',
      text: 'Match Result'
    }] as IMenuItem[];
    expect(component.getSelectedItemName('Match Result', 'templateMarketName')).toBe('Match Result');
  });

  it('getSelectedItemName - should set selected item name from menu', () => {
    component.menuList = [{
      templateMarketName: 'Match Result',
      name: 'Match Result'
    }] as IMenuItem[];
    expect(component.getSelectedItemName('Match Result', 'templateMarketName')).toBe('Match Result');
  });

  it('getSelectedItemName - should set selected item title from menu', () => {
    component.menuList = [{
      templateMarketName: 'Match Result',
      title: 'Match Result'
    }] as IMenuItem[];
    expect(component.getSelectedItemName('Match Result', 'templateMarketName')).toBe('Match Result');
  });

  it('getSelectedItemName - should set selected item from menu if it is exist', () => {
    component.menuList = [{ templateMarketName: 'Match Result' }] as IMenuItem[];
    expect(component.getSelectedItemName('Total Goals Over/Under 2.5', 'templateMarketName')).toBe('Total Goals Over/Under 2.5');
  });

  it('ngOnChanges', () => {
    component.selectedListItem = '2';

    const changes = {
      menuList: {
        currentValue: [{ text: '1', name: '1', title: '1'}],
        previousValue: [{ text: '1', name: '1', title: '1'}, { text: '2', name: '2', title: '2'}],
        firstChange: true
      }
    };
    component.ngOnChanges(changes as any);
    expect(component.selectedListItem).toEqual('1');
  });

  it('ngOnChanges should not set selectedListItem if menu doesn\'t changed', () => {
    const changes = {
      menuList: undefined
    };
    component.ngOnChanges(changes as any);
    expect(component.selectedListItem).toBeUndefined();
  });

  it('ngOnChanges should set new selected item', () => {
    const changes = {
      menuList: {
        currentValue: [{ text: '2', name: '2', title: '2'}, { text: '3', name: '3', title: '3'}],
        previousValue: undefined,
        firstChange: true
      },
      selectedItem: {
        previousValue: '2',
        currentValue: '3',
        firstChange: true
      }
    };
    component.ngOnChanges(changes as any);
    expect(component.selectedListItem).toEqual('3');
  });
});
