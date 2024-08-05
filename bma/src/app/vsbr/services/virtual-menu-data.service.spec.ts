import { VirtualMenuDataService } from '@app/vsbr/services/virtual-menu-data.service';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';

describe('VirtualMenuDataService', () => {
  let service;
  let virtualMenu: IVirtualSportsMenuItem[];

  beforeEach(() => {
    virtualMenu = [{
      name: 'menuItem-1',
      inApp: true,
      svgId: 'svgId',
      targetUri: 'targetUri',
      targetUriSegment: 'targetUriSegment',
      priority: 1,
      alias: 'menu-item-1',
      childMenuItems: [{
        name: 'childMenuItem1',
        inApp: true,
        svgId: 'svgId',
        targetUri: 'targetUri',
        targetUriSegment: 'targetUriSegment',
        priority: 1,
        alias: 'child-menu-item-1'
      }]
    }, {
      name: 'menuItem-2',
      inApp: true,
      svgId: 'svgId',
      targetUri: 'targetUri',
      targetUriSegment: 'targetUriSegment',
      priority: 2,
      alias: 'menu-item-2',
      childMenuItems: null
    }
    ];

    service = new VirtualMenuDataService();
    service.menu = virtualMenu;
  });

  it('@getChildMenuItems should return child categories for specific parent category', () => {
    const childMenu = service.getChildMenuItems('menu-item-1');

    expect(childMenu === service.menu[0].childMenuItems).toBeTruthy();
  });

  it('@getChildMenuItems should return undefined if specific parent category doesn\'t contains childs or parent alias is invalid ', () => {
    const childMenu2 = service.getChildMenuItems('menu-item-2');
    const childMenu3 = service.getChildMenuItems('menu-item-3');

    expect(childMenu2).toBeUndefined();
    expect(childMenu3).toBeUndefined();
  });

  it('@getParentMenuItem should return parent category for specific parent alias', () => {
    const parentMenuItem = service.getParentMenuItem('menu-item-1');

    expect(parentMenuItem === service.menu[0]).toBeTruthy();
  });

  it('@getParentMenuItem should return undefined if specific parent alias is invalid', () => {
    const parentMenuItem = service.getParentMenuItem('menu-item-3');

    expect(parentMenuItem).toBeUndefined();
  });

  it('@getParentIndex should return index of parent category', () => {
    const parentIndex = service.getParentIndex('menu-item-1');

    expect(parentIndex).toEqual(0);
  });

  it('@getParentIndex should return -1 if there is no parent category with alias', () => {
    const parentIndex = service.getParentIndex('menu-item-4');

    expect(parentIndex).toEqual(-1);
  });

  describe('@getChildIndex', () => {
    it('should return undefined if parent and child alias is empty', () => {
      const childIndex = service.getChildIndex();

      expect(childIndex).toBeUndefined();
    });

    it('should return index of child category if parent and child alias are valid', () => {
      const childIndex = service.getChildIndex('menu-item-1', 'child-menu-item-1');

      expect(childIndex).toEqual(0);
    });

    it('should return 0 if only parent alias is set as argument', () => {
      const childIndex = service.getChildIndex('menu-item-1');

      expect(childIndex).toEqual(0);
    });

    it('should return 0 if only parent alias is set as argument and parent does\'nt contain childs', () => {
      const childIndex = service.getChildIndex('menu-item-2');

      expect(childIndex).toBeUndefined();
    });
  });

  it('@hasParents should check if menu contains parent categories', () => {
    expect(service.hasParents()).toBeTruthy();
  });

  it('@hasParents should return false if menu contains parent categories', () => {
    const localService = new VirtualMenuDataService();

    localService.menu = [];

    expect(localService.hasParents()).toBeFalsy();
  });

  it('@hasFirstChild should return true if first parent contains at least one child', () => {
    expect(service.hasFirstChild()).toBeTruthy();
  });

  it('@hasFirstChild should return false if first parent does\'nt contains childs', () => {
    const localService = new VirtualMenuDataService();

    localService.menu = [];

    expect(localService.hasFirstChild()).toBeFalsy();
  });

  it('@hasParentAndChild should return true if there is at least one parent and child', () => {
    expect(service.hasParentAndChild()).toBeTruthy();
  });

  it('@hasParentAndChild should return false if there are no any parents and childs', () => {
    const localService = new VirtualMenuDataService();

    localService.menu = [];

    expect(localService.hasParentAndChild()).toBeFalsy();
  });

  it('@destroy should destroy all menu data', () => {
    service.destroy();

    expect(service.menu).toEqual([]);
    expect(service.activeParentIndex).toEqual(0);
    expect(service.activeChildIndex).toEqual(0);
  });

});

