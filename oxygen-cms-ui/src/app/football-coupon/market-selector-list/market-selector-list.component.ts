import * as _ from 'lodash';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { MarketSelector } from '@app/client/private/models/marketselector.model';
import { MarketSelectorCreateComponent } from '../market-selector-create/market-selector-create.component';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { AppConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';

@Component({
  templateUrl: './market-selector-list.component.html',
  styleUrls: ['./market-selector-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class MarketSelectorListComponent implements OnInit {

  public marketSelectors: MarketSelector[];
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Name',
      'property': 'title',
      'link': {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      'name': 'Template Name',
      'property': 'templateMarketName'
    },
    {
      'name': 'Headers',
      'property': 'header'
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
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.marketSelector()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: MarketSelector[]) => {
        this.marketSelectors = data;
        this.globalLoaderService.hideLoader();
      }, error => {
         console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createMarketSelector(): void {
    this.dialogService.showCustomDialog(MarketSelectorCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Coupon Market Selector',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (marketSelector: MarketSelector) => {
        this.apiClientService.marketSelector()
          .add(marketSelector)
          .map(response => {
            return response.body;
          })
          .subscribe((data: MarketSelector) => {
            this.marketSelectors.push(data);
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

  removeHandler(marketSelector: MarketSelector): void {
    this.dialogService.showConfirmDialog({
      title: 'Coupon Market Selector',
      message: 'Are You Sure You Want to Remove Market Selector?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.marketSelector()
          .delete(marketSelector.id)
          .subscribe(() => {
            _.remove(this.marketSelectors, {id: marketSelector.id});
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
      .marketSelector()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Market selector order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
