import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {ConnectMenu} from '../../../client/private/models/connectmenu.model';
import {ConnectMenusCreateComponent} from '../connect-menus-create/connect-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './connect-menus-list.component.html',
  styleUrls: ['./connect-menus-list.component.scss']
})
export class ConnectMenusListComponent implements OnInit {

  public connectMenus: Array<ConnectMenu>;
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
      'name': 'Link Subtitle',
      'property': 'linkSubtitle'
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
    }, {
      'name': 'Upgrade Popup',
      'property': 'upgradePopup',
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
    this.apiClientService.connectMenu()
      .findAllByBrand()
      .map(response => {
        const menues = response.body;
        return menues.map((m) => {
          if (m.parent) {
            m.parent = _.find(menues, (cM) => cM.id === m.parent).linkTitle;
          }

          return m;
        });
      })
      .subscribe((data: ConnectMenu[]) => {
        this.connectMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createConnectMenu(): void {
    this.dialogService.showCustomDialog(ConnectMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Connect Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (connectMenu: ConnectMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.connectMenu()
          .save(connectMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: ConnectMenu) => {
            this.connectMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/connect-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(connectMenu: ConnectMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Connect Menu',
      message: 'Are You Sure You Want to Remove Connect Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.connectMenu()
          .delete(connectMenu.id)
          .subscribe(() => {
            _.remove(this.connectMenus, {id: connectMenu.id});
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
      .connectMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Connect menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
