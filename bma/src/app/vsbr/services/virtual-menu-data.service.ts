import { Injectable } from '@angular/core';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';
import { FIRST_CATEGORY } from '@app/vsbr/constants/virtual-sports.constant';

@Injectable()
export class VirtualMenuDataService {
  private virtualMenu: IVirtualSportsMenuItem[] = [];
  private activeParent: number;
  private activeChild: number;

  get activeParentIndex(): number {
    return this.activeParent;
  }

  set activeParentIndex(activeParent: number) {
    this.activeParent = activeParent;
  }

  get activeChildIndex(): number {
    return this.activeChild;
  }

  set activeChildIndex(activeChild: number) {
    this.activeChild = activeChild;
  }

  get menu(): IVirtualSportsMenuItem[]  {
    return this.virtualMenu;
  }

  /**
   * Set both parent and child menu
   * @param virtualMenu - parent and child menu
   */
  set menu(virtualMenu: IVirtualSportsMenuItem[]) {
    this.virtualMenu = virtualMenu;
  }

  /**
   * Get child categories for specific parent category
   * @param parentAlias - parent category alias
   */
  getChildMenuItems(parentAlias: string): IVirtualSportsMenuItem[] | undefined {
    const parent: IVirtualSportsMenuItem = this.getParentMenuItem(parentAlias);
    return parent && parent.childMenuItems || undefined;
  }

  /**
   * Get specific parent category
   * @param parentAlias - parent category alias
   */
  getParentMenuItem(parentAlias: string): IVirtualSportsMenuItem | undefined {
    return this.menu.find((parent: IVirtualSportsMenuItem ) => parent.alias === parentAlias);
  }

  /**
   * Get index of specific parent category
   * @param alias - parent category alias
   */
  getParentIndex(alias?: string): number {
    return this.menu.findIndex((parent: IVirtualSportsMenuItem) => parent.alias === alias);
  }

  /**
   * Get index of specific child category
   * @param parentAlias - parent category alias
   * @param childAlias - child category alias
   */
  getChildIndex(parentAlias: string, childAlias?: string): number | undefined {
    if (parentAlias && childAlias) {
      const childMenu: IVirtualSportsMenuItem[] = this.getChildMenuItems(parentAlias);
      return childMenu && childMenu.length && childMenu.findIndex(child => child.alias === childAlias);
    }

    if (parentAlias && !childAlias) {
      const childMenu: IVirtualSportsMenuItem[] = this.getChildMenuItems(parentAlias);
      return childMenu && childMenu.length ? FIRST_CATEGORY : undefined;
    }

    return;
  }

  /**
   * Check if menu contain at least one parent category
   */
  hasParents(): boolean {
    return this.menu && !!this.menu.length;
  }

  /**
   * Check if  first parent category has childs categories
   */
  hasFirstChild(): boolean {
    return this.menu && this.menu.length && this.menu[0].childMenuItems && !!this.menu[0].childMenuItems.length;
  }

  /**
   * Check if there is at least one parent and one child category
   */
  hasParentAndChild(): boolean {
    return this.hasParents() && this.hasFirstChild();
  }

  /**
   * Clear all service data
   */
  destroy(): void {
    this.menu = [];
    this.activeParentIndex = 0;
    this.activeChildIndex = 0;
  }
}
