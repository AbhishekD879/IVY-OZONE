import * as _ from 'lodash';

import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { GamingSubMenu } from '@root/app/client/private/models/gaming-submenu.model';
import { DataTableColumn } from '../../../client/private/models/dataTableColumn';
import { ApiClientService } from '../../../client/private/services/http';
import { DialogService } from '../../../shared/dialog/dialog.service';
import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { GamingMenusCreateComponent } from '../gaming-menus-create/gaming-menus-create.component';
import { AppConstants } from '../../../app.constants';
import { Order } from '@root/app/client/private/models/order.model';

@Component({
  templateUrl: './gaming-menus-list.component.html'
})
export class GamingMenusListComponent implements OnInit {

  public gamingSubMenus: Array<GamingSubMenu>;
  public error: string;
  public searchField: string = '';

  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Title',
      'property': 'title',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    },
    {
      'name': 'Link',
      'property': 'url'
    },
    {
      'name': 'Destination Window',
      'property': 'target'
    },
    {
      'name': 'Is Native',
      'property': 'isNative',
      'type': 'boolean'
    }
  ];

  public searchableProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.apiClientService.gamaingSubMenuService()
      .findAllByBrand()
      .map(response => response.body)
      .subscribe((data: GamingSubMenu[]) => {
        this.gamingSubMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createGamingSubMenu() {
    this.dialogService.showCustomDialog(GamingMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Gaming Sub-Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (gamingSubMenu: GamingSubMenu) => {
        this.globalLoaderService.showLoader();
        const recordWithMaxSortOrder = _.maxBy(this.gamingSubMenus, 'sortOrder');
        if (recordWithMaxSortOrder) {
          gamingSubMenu.sortOrder = recordWithMaxSortOrder.sortOrder + 1;
        }
        this.apiClientService.gamaingSubMenuService()
          .save(gamingSubMenu)
          .map(response => response.body)
          .subscribe((data: GamingSubMenu) => {
            this.gamingSubMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/gaming-submenus/${data.id}`]);
          }, error => {
            console.error(error);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(gamingSubMenu: GamingSubMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Gaming SubMenu',
      message: `Are You Sure You Want to Remove Gaming sub-menu: ${ gamingSubMenu.title }?`,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.gamaingSubMenuService()
          .delete(gamingSubMenu.id)
          .subscribe(() => {
            _.remove(this.gamingSubMenus, {id: gamingSubMenu.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .gamaingSubMenuService()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Gaming sub menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
