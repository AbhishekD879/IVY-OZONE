import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {Router} from '@angular/router';

import {BottomMenu} from '../../../client/private/models/bottommenu.model';
import {BottomMenusCreateComponent} from '../bottom-menus-create/bottom-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './bottom-menus-list.component.html',
  styleUrls: ['./bottom-menus-list.component.scss']
})
export class BottomMenusListComponent implements OnInit {

  public bottomMenus: Array<BottomMenu>;
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
      'name': 'Section',
      'property': 'section'
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
    this.apiClientService.bottomMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: BottomMenu[]) => {
        this.bottomMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createBottomMenu(): void {
    this.dialogService.showCustomDialog(BottomMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add new bottom menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (bottomMenu: BottomMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.bottomMenu()
          .save(bottomMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: BottomMenu) => {
            this.bottomMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/bottom-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(bottomMenu: BottomMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Bottom Menu',
      message: 'Are You Sure You Want to Remove Bottom Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.bottomMenu()
          .delete(bottomMenu.id)
          .subscribe(() => {
            _.remove(this.bottomMenus, {id: bottomMenu.id});
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
      .bottomMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Bottom menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
