import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {RightMenu} from '../../../client/private/models/rightmenu.model';
import {RightMenusCreateComponent} from '../right-menus-create/right-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './right-menus-list.component.html',
  styleUrls: ['./right-menus-list.component.scss']
})
export class RightMenusListComponent implements OnInit {

  public rightMenus: Array<RightMenu>;
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
      'name': 'Section',
      'property': 'section'
    },
    {
      'name': 'In App',
      'property': 'inApp',
      'type': 'boolean'
    },
    {
      'name': 'Show Item For',
      'property': 'showItemFor',
    },
    {
      'name': 'Show Only on iOS',
      'property': 'showOnlyOnIOS',
      'type': 'boolean'
    },
    {
      'name': 'Show Only on Android',
      'property': 'showOnlyOnAndroid',
      'type': 'boolean'
    },
    {
      'name': 'Menu View Item',
      'property': 'menuItemView'
    },
    {
      'name': 'Icon Alignment',
      'property': 'iconAligment'
    },
    {
      'name': 'Auth Required',
      'property': 'authRequired',
      'type': 'boolean'
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
    this.apiClientService.rightMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: RightMenu[]) => {
        this.rightMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createRightMenu(): void {
    this.dialogService.showCustomDialog(RightMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Right Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (rightMenu: RightMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.rightMenu()
          .save(rightMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: RightMenu) => {
            this.rightMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/right-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(rightMenu: RightMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Right Menu',
      message: 'Are You Sure You Want to Remove Right Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.rightMenu()
          .delete(rightMenu.id)
          .subscribe(() => {
            _.remove(this.rightMenus, {id: rightMenu.id});
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
      .rightMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Right menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
