import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';

import {HeaderMenu} from '@app/client/private/models/headermenu.model';
import {HeaderMenusCreateComponent} from '../header-menus-create/header-menus-create.component';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {AppConstants} from '@app/app.constants';
import {Order} from '@app/client/private/models/order.model';

@Component({
  templateUrl: './header-menus-list.component.html',
  styleUrls: ['./header-menus-list.component.scss']
})
export class HeaderMenusListComponent implements OnInit {

  public headerMenus: Array<HeaderMenu>;
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
      'name': 'Parent',
      'property': 'parent'
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
    this.apiClientService.headerMenu()
      .findAllByBrand()
      .map(response => {
        const menues = response.body;
        return menues.map((h) => {
          if (h.parent) {
            const menu = _.find(menues, (hM) => hM.id === h.parent);
            h.parent = menu ? menu.linkTitle : '';
          }
          return h;
        });
      })
      .subscribe((data: HeaderMenu[]) => {
        this.headerMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createHeaderMenu(): void {
    this.dialogService.showCustomDialog(HeaderMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Header Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (headerMenu: HeaderMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerMenu()
          .save(headerMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: HeaderMenu) => {
            this.headerMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/header-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(headerMenu: HeaderMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Header Menu',
      message: 'Are You Sure You Want to Remove Header Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerMenu()
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
      .headerMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Header menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
