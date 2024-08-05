import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {Router} from '@angular/router';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {BybAPIService} from '../../service/byb.api.service';
import {BrandService} from '../../../client/private/services/brand.service';
import {BybMarket} from '../../../client/private/models';
import {BybMarketsCreateComponent} from '../byb-markets-create/byb-markets-create.component';
import {AppConstants} from '../../../app.constants';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'byb-markets-list',
  templateUrl: './byb-markets-list.component.html',
  styleUrls: ['./byb-markets-list.component.scss']
})

export class BybMarketsListComponent implements OnInit {

  marketsData: Array<BybMarket>;
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
      name: 'Market Group Name',
      property: 'bybMarket'
    },
    {
      name: 'Market Grouping',
      property: 'marketGrouping'
    },
    {
      name: 'Incident Grouping',
      property: 'incidentGrouping'
    },
    {
      name: 'Market Type',
      property: 'marketType'
    },
    {
      name: 'Popular Market',
      property: 'popularMarket',
      type: 'boolean'
    },
    {
      name: 'Market Description',
      property: 'marketDescription'
    },
    {
      name: 'Stat',
      property: 'stat'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private bybAPIService: BybAPIService,
    private brandService: BrandService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.bybAPIService.getMarketsList()
      .subscribe((data: any) => {
        this.marketsData = data.body;
      });
  }

  createMarket(): void {
    const dialogRef = this.dialog.open(BybMarketsCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newMarket => {
      if (newMarket) {
        _.extend(newMarket, {
          brand: this.brandService.brand
        });
        this.bybAPIService.createMarket(newMarket)
          .map((bybMarket: HttpResponse<BybMarket>) => {
            return bybMarket.body;
          })
          .subscribe((bybMarket: BybMarket) => {
            if (bybMarket) {
              this.marketsData.push(bybMarket);
              this.router.navigate([`/byb/byb-markets/${bybMarket.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting market
   * @param {BybMarket} market
   */
  removeMarket(market: BybMarket): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove BuildYourBet Market',
      message: 'Are You Sure You Want to Remove BuildYourBet Market?',
      yesCallback: () => {
        this.sendRemoveRequest(market);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {BybMarket} market
   */
  sendRemoveRequest(market: BybMarket): void {
    this.bybAPIService.deleteMarket(market.id)
      .subscribe((data: any) => {
        this.marketsData.splice(this.marketsData.indexOf(market), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'BuildYourBet Market is Removed.'
        });
      });
  }

  reorderHandler(newOrder: Order): void {

    this.bybAPIService.postNewMarketsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('BuildYourBet Markets Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
    });
  }
}
