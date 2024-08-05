import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {UserMenu} from '../../../client/private/models/usermenu.model';
import {UserMenusCreateComponent} from '../user-menus-create/user-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './user-menus-list.component.html',
  styleUrls: ['./user-menus-list.component.scss']
})
export class UserMenusListComponent implements OnInit {

  public userMenus: Array<UserMenu>;
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
      'name': 'Show User Menu',
      'property': 'showUserMenu'
    },
    {
      'name': 'Active If Logout',
      'property': 'activeIfLogout',
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
    this.apiClientService.userMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: UserMenu[]) => {
        this.userMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createUserMenu(): void {
    this.dialogService.showCustomDialog(UserMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New User Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (userMenu: UserMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.userMenu()
          .save(userMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: UserMenu) => {
            this.userMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/user-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(userMenu: UserMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'User Menu',
      message: 'Are You Sure You Want to Remove User Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.userMenu()
          .delete(userMenu.id)
          .subscribe(() => {
            _.remove(this.userMenus, {id: userMenu.id});
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
      .userMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`User menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
