import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {Router} from '@angular/router';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {YourCallAPIService} from '../../service/your-call.api.service';
import {YourCallMarket} from '../../../client/private/models';
import {YcMarketsCreateComponent} from '../yc-markets-create/yc-markets-create.component';
import {AppConstants} from '@app/app.constants';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'yc-markets-list',
  templateUrl: './yc-markets-list.component.html',
  styleUrls: ['./yc-markets-list.component.scss']
})
export class YcMarketsListComponent implements OnInit {
  marketsData: Array<YourCallMarket>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Market Title',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'DS Market',
      property: 'dsMarket'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private marketsAPIService: YourCallAPIService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.marketsAPIService.getMarketsList()
      .subscribe((data: any) => {
        this.marketsData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  createMarket(): void {
    const dialogRef = this.dialog.open(YcMarketsCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newMarket => {
      if (newMarket) {
        this.marketsAPIService.createMarket(newMarket)
          .map((yourCallMarket: HttpResponse<YourCallMarket>) => {
            return yourCallMarket.body;
          })
          .subscribe((yourCallMarket: YourCallMarket) => {
            if (yourCallMarket) {
              this.marketsData.push(yourCallMarket);
              this.router.navigate([`/yc/yc-markets/${yourCallMarket.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting market
   * @param {YourCallMarket} market
   */
  removeMarket(market: YourCallMarket): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove YourCall Market',
      message: 'Are You Sure You Want to Remove YourCall Market?',
      yesCallback: () => {
        this.sendRemoveRequest(market);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {YourCallMarket} market
   */
  sendRemoveRequest(market: YourCallMarket): void {
    this.marketsAPIService.deleteMarket(market.id)
      .subscribe((data: any) => {
        this.marketsData.splice(this.marketsData.indexOf(market), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'YourCall Market is Removed.'
        });
      });
  }

  reorderHandler(newOrder: Order): void {
    this.marketsAPIService.postNewMarketsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('YourCall Markets Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
    });
  }
}
