import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import LeftSideBar from './left-menu.api.js';
import { MenuItem } from '../models/menu-item';

@Component({
  selector: 'cms-left-menu',
  templateUrl: './left-menu.component.html',
  styleUrls: ['./left-menu.component.scss']
})
export class LeftMenuComponent implements OnInit {
  links: MenuItem[];

  constructor(
    private route: ActivatedRoute
  ) {

  }

  private activateMenu(): void {
    setTimeout(() => {
      LeftSideBar.activate();
    }, 1e3);
  }

  ngOnInit(): void {
    this.links = this.route.snapshot.data['mainData'][0].body.menu;
    this.sortMenuItems(this.links);
    this.links.forEach(menuItem => this.sortMenuItemsRecursively(menuItem));
    this.activateMenu();
  }

  private sortMenuItemsRecursively(menuItem) {
    if (menuItem['sub-menus']) {
      this.sortMenuItems(menuItem['sub-menus']);
      menuItem['sub-menus'].forEach(subItem => this.sortMenuItemsRecursively(subItem));
    }
  }

  private sortMenuItems(menuItems) {
    menuItems.sort((link1: any, link2: any) => {
      const firstEmpty = this.isNullOrUndefined(link1.displayOrder);
      const secondEmpty = this.isNullOrUndefined(link2.displayOrder);
      if (firstEmpty && secondEmpty) {
        return 0;
      } else if (firstEmpty) {
        return 1;
      } else if (secondEmpty) {
        return -1;
      } else {
        return (+link1.displayOrder) - (+link2.displayOrder);
      }
    });
  }
  private isNullOrUndefined(variable) {
    return (variable === null || variable === undefined);
  }
}
