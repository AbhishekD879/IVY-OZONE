import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {BankingMenu} from '../../../client/private/models/bankingmenu.model';
import {BankingMenusCreateComponent} from '../banking-menus-create/banking-menus-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './banking-menus-list.component.html',
  styleUrls: ['./banking-menus-list.component.scss']
})
export class BankingMenusListComponent implements OnInit {

  public bankingMenus: Array<BankingMenu>;
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
    this.apiClientService.bankingMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: BankingMenu[]) => {
        this.bankingMenus = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createBankingMenu(): void {
    this.dialogService.showCustomDialog(BankingMenusCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Banking Menu',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (bankingMenu: BankingMenu) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.bankingMenu()
          .save(bankingMenu)
          .map(response => {
            return response.body;
          })
          .subscribe((data: BankingMenu) => {
            this.bankingMenus.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/banking-menus/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(bankingMenu: BankingMenu): void {
    this.dialogService.showConfirmDialog({
      title: 'Banking Menu',
      message: 'Are You Sure You Want to Remove Banking Menu?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.bankingMenu()
          .delete(bankingMenu.id)
          .subscribe(() => {
            _.remove(this.bankingMenus, {id: bankingMenu.id});
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
      .bankingMenu()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Banking menu order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
