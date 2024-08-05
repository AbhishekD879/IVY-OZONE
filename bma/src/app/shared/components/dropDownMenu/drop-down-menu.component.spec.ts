import { DropDownMenuComponent } from './drop-down-menu.component';

describe('DropDownMenuComponent', () => {
  let component: DropDownMenuComponent;
  let changeDetectorRef;

  const testStr = 'title';

  beforeEach(() => {
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new DropDownMenuComponent(changeDetectorRef);
    component.menuList = [{ title: testStr }] as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    it(`should set 'selectionNameKey' to 'nameKey' if 'selectionNameKey' is defined`, () => {
      component.selectionNameKey = testStr;
      component.ngOnInit();

      expect(component.nameKey).toEqual(component.selectionNameKey);
    });

    it(`should set one of mock nameKeys to 'nameKey' if 'selectionNameKey' is Not defined`, () => {
      component.ngOnInit();

      expect(component.nameKey).toEqual('title');
    });

    it(`should set 'selectionValueKeys' to 'valueKeys' if 'selectionValueKeys' is defined`, () => {
      component.selectionNameKey = testStr;
      component.selectionValueKeys = [testStr];
      component.ngOnInit();

      expect(component.valueKeys).toEqual(component.selectionValueKeys);
    });

    it(`should set [nameKey] to 'valueKeys' if 'selectionValueKeys' is Not defined`, () => {
      component.selectionNameKey = testStr;
      component.ngOnInit();

      expect(component.valueKeys).toEqual([testStr]);
    });

    it(`should set 'selectedListItem'`, () => {
      component['getSelectedItemName'] = jasmine.createSpy('getSelectedItemName');
      component.selectedItem = testStr;
      component.ngOnInit();

      expect(component['getSelectedItemName']).toHaveBeenCalledWith(component.selectedItem);
    });
  });

  describe('trackByFn', () => {
    it(`should return item property by 'nameKey'`, () => {
      const item = { title: testStr } as any;
      component.nameKey = 'title';

      expect(component.trackByFn(1, item)).toEqual(item.title);
    });
  });

  describe('clickItem', () => {
    const menuItemStub = { title: testStr } as any;

    beforeEach(() => {
      spyOn(component.clickFunction, 'emit');
      component.selectionNameKey = 'title';
      component.valueKeys = ['title'];
    });

    it('should emit item values', () => {
      component.clickItem(menuItemStub);

      expect(component.clickFunction.emit).toHaveBeenCalledWith([jasmine.any(String)] as any);
    });

    it('should hide dropDownMenu', () => {
      spyOn(component, 'menuToggle');

      component.clickItem(menuItemStub);

      expect(component.menuToggle).toHaveBeenCalledWith(false);
    });

    it(`should set 'selectedListItem'`, () => {
      component.nameKey = 'title';
      component.clickItem(menuItemStub);

      expect(component.selectedListItem).toEqual(menuItemStub.title);
    });
  });

  describe('getSelectedItemName', () => {
    const menuListStub = [{ title: testStr }] as any;

    beforeEach(() => {
      component.menuList = menuListStub;
      component.selectionNameKey = 'title';
      component.valueKeys = ['title'];
      component.nameKey = 'title';
    });

    it(`should find item with valueKeys if 'menuList' has such item`, () => {
      expect(component['getSelectedItemName'](testStr)).toEqual(menuListStub[0].title);
    });

    it(`should return send attribute if Not find item with valueKeys in 'menuList'`, () => {
      const titleStub = 'Some title';

      expect(component['getSelectedItemName'](titleStub)).toEqual(titleStub);
    });
  });

  describe('getItemValues', () => {
    it(`should return item values by 'valueKeys'`, () => {
      component.valueKeys = ['title', 'name'];

      expect(component['getItemValues']({ title: '1', name: '2' } as any)).toEqual(['1', '2']);
    });
  });

  describe('menuToggle', () => {
    beforeEach(() => {
      component.showMenu = true;
    });

    it('should set showMenu if showMenu Not equal show', () => {
      component.menuToggle(false);

      expect(component.showMenu).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should toggle show menu if show is not defined', () => {
      component.menuToggle();

      expect(component.showMenu).toBeFalsy();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

  });

  describe('clickHandler', () => {
    let event: any;

    beforeEach(() => {
      event = { cancelable: true, preventDefault: jasmine.createSpy() };
    });

    it(`should return if event is Not 'cancelable'`, () => {
      event.cancelable = false;

      component.clickHandler(event);

      expect(event.preventDefault).not.toHaveBeenCalled();
    });

    it(`should preventDefault if event is 'cancelable'`, () => {
      component.clickHandler(event);

      expect(event.preventDefault).toHaveBeenCalled();
    });

    it(`should hide menu if event is 'cancelable'`, () => {
      spyOn(component, 'menuToggle');

      component.clickHandler(event);

      expect(component.menuToggle).toHaveBeenCalledWith(false);
    });
  });

  describe('getSelectedItemName', () => {
    const menuListStub = [
      {
        title: 'Match betting',
        templateMarketName: 'Match Result'
      },
      {
        title: 'Draw no Bet',
        templateMarketName: 'Draw no Bet'
      }
    ] as any;

    const updatedMenuListStub = [{
      title: 'Match betting',
      templateMarketName: 'Match Result'
    }] as any;

    beforeEach(() => {
      component.menuList = menuListStub;
      component.selectionNameKey = 'title';
      component.selectedItem = 'Draw no Bet';
    });

    it('should test ngOnChange when menu items was updated', () => {
      spyOn(component, 'initMenu').and.callThrough();

       component.ngOnChanges({
         menuList: {
           currentValue: updatedMenuListStub,
           previousValue: menuListStub
         }
       } as any);

       expect(component.initMenu).toHaveBeenCalled();
    });

    it('should test ngOnChanges when not active menu element was deleted', () => {
      spyOn(component, 'initMenu').and.callThrough();

      const updatedMenuListStubWithPresentSelector = [{
        title: 'Match betting',
        templateMarketName: 'Match Result'
      }, {
        title: 'Draw no Bet',
        templateMarketName: 'Draw no Bet'
      }] as any;

      component.ngOnChanges({
        menuList: {
          currentValue: updatedMenuListStubWithPresentSelector,
          previousValue: menuListStub
        }
      } as any);

      expect(component.initMenu).not.toHaveBeenCalled();
    });

    it('should test ngOnChanges when amount of menu items the same', () => {
      spyOn(component, 'initMenu').and.callThrough();

      component.ngOnChanges({
        menuList: {
          currentValue: menuListStub,
          previousValue: menuListStub
        }
      } as any);

      expect(component.initMenu).not.toHaveBeenCalled();
    });

    it('should test ngOnChanges when no Previous value', () => {
      spyOn(component, 'initMenu').and.callThrough();

      component.ngOnChanges({
        menuList: {
          currentValue: menuListStub,
          previousValue: undefined
        }
      } as any);

      expect(component.initMenu).not.toHaveBeenCalled();
    });

    it('should test ngOnChanges when no current value', () => {
      spyOn(component, 'initMenu').and.callThrough();

      component.ngOnChanges({
        menuList: {
          currentValue: undefined,
          previousValue: menuListStub
        }
      } as any);

      expect(component.initMenu).not.toHaveBeenCalled();
    });

    it('should test ngOnChanges when no Menu update', () => {
      spyOn(component, 'initMenu').and.callThrough();

      component.ngOnChanges({
        notAMenuList: {}
      } as any);

      expect(component.initMenu).not.toHaveBeenCalled();
    });

    it('ngOnChanges should not set selectedListItem if menu doesn\'t changed', () => {
      component.selectedListItem = undefined;
      const changes = {
        menuList: undefined
      };
      component.ngOnChanges(changes as any);
      expect(component.selectedListItem).toBeUndefined();
    });

    it('ngOnChanges should set new selected item', () => {
      const changes = {
        menuList: {
          currentValue: [{ text: '2', name: '2', title: '2' }, { text: '3', name: '3', title: '3' }],
          previousValue: undefined,
          firstChange: true
        },
        selectedItem: {
          previousValue: '2',
          currentValue: '3',
          firstChange: true
        }
      };
      component.valueKeys = ['title'];
      component.ngOnChanges(changes as any);
      expect(component.selectedListItem).toEqual('3');
    });
  });
});
