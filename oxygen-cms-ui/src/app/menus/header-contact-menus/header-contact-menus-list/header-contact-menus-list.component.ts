import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {Router} from '@angular/router';

import {HeaderContactMenu} from '../../../client/private/models/headercontactmenu.model';
import {HeaderContactMenusCreateComponent} from '../header-contact-menus-create/header-contact-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';


@Component({
  templateUrl: './header-contact-menus-list.component.html',
  styleUrls: ['./header-contact-menus-list.component.scss']
})
export class HeaderContactMenusListComponent implements OnInit {

  public headerContactMenus: Array<HeaderContactMenu>;
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
      'name': 'In App',
      'property': 'inApp'
    },
    {
      'name': 'Label',
      'property': 'label'
    },
    {
      'name': 'Auth Required',
      'property': 'authRequired'
    },
    {
      'name': 'Start Url',
      'property': 'startUrl'
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
    this.apiClientService.headerContactMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: HeaderContactMenu[]) => {
        this.headerContactMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createHeaderContactMenu(): void {
    this.dialogService.showCustomDialog(HeaderContactMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add new header contact menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (headerContactmenu: HeaderContactMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerContactMenu()
          .save(headerContactmenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: HeaderContactMenu) => {
            this.headerContactMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/header-contact-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(headerContactMenu: HeaderContactMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Header Contact Menu',
      message: 'Are You Sure You Want to Remove Header Contact Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.headerContactMenu()
          .delete(headerContactMenu.id)
          .subscribe(() => {
            _.remove(this.headerContactMenus, {id: headerContactMenu.id});
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
      .headerContactMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Header Contact menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
