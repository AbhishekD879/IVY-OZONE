import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';

import {HeaderSubMenu} from '@app/client/private/models/headersubmenu.model';
import {HeaderSubMenusCreateComponent} from '../header-sub-menus-create/header-sub-menus-create.component';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';
import {Order} from '@app/client/private/models/order.model';

@Component({
  templateUrl: './header-sub-menus-list.component.html',
  styleUrls: ['./header-sub-menus-list.component.scss']
})
export class HeaderSubMenusListComponent implements OnInit {

  public headerMenus: Array<HeaderSubMenu>;
  public error: string;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Link Title',
      'property': 'linkTitle',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    },
    {
      'name': 'Target Uri',
      'property': 'targetUri'
    },
    {
      'name': 'Brand',
      'property': 'brand'
    },
    {
      'name': 'In App',
      'property': 'inApp',
      'type': 'boolean'
    }
    ];
  public searchableProperties: Array<string> = [
    'linkTitle'
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
    this.apiClientService.headerSubMenu()
      .findAllByBrand()
      .map(response => response.body)
      .subscribe((data: HeaderSubMenu[]) => {
        this.headerMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createHeaderMenu(): void {
    this.dialogService.showCustomDialog(HeaderSubMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Header Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (headerMenu: HeaderSubMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerSubMenu()
          .save(headerMenu)
          .map(response => response.body)
          .subscribe((data: HeaderSubMenu) => {
            this.headerMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/header-submenus/${data.id}`]);
          }, error => {
            console.error(error);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(headerMenu: HeaderSubMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Header Menu',
      message: 'Are You Sure You Want to Remove Header Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerSubMenu()
          .delete(headerMenu.id)
          .subscribe(() => {
            _.remove(this.headerMenus, {id: headerMenu.id});
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
      .headerSubMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Header menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
