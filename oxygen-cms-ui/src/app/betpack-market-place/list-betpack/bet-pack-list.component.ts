import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AppConstants } from '@root/app/app.constants';
import { DataTableColumn } from '@root/app/client/private/models';
import { Order } from '@root/app/client/private/models/order.model';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { BetPackModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';

@Component({
  selector: 'bet-pack-list',
  templateUrl: './bet-pack-list.component.html'
})
export class BetPackListComponent implements OnInit {
  betPackData: Array<BetPackModel>;
  getDataError: string;
  disableCreate: boolean = false;
  isReady: boolean;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'BetPack Name',
      property: 'betPackTitle',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Start Date',
      property: 'betPackStartDate',
      type: 'date'
    },
    {
      name: 'End Date',
      property: 'betPackEndDate',
      type: 'date'
    },
    {
      name: 'Featured Enabled',
      property: 'futureBetPack',
      type: 'boolean'
    },
    {
      name: 'Filter',
      property: 'filterList',
    },
    {
      name: 'Active/ Deactive',
      property: 'betPackActive',
      type: 'boolean'
    }
  ];

  constructor(public router: Router,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private globalLoaderService: GlobalLoaderService) { }

  ngOnInit(): void {
    this.loadBetPacks();
  }

  /**
  * Load List of Campaigns
  * @returns - {void}
  */
  public loadBetPacks(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.betpackService().getBetPackData().map((response: HttpResponse<BetPackModel[]>) => response.body)
      .subscribe((data: BetPackModel[]) => {
        let count = 0;
        this.betPackData = data;
        this.isReady = true
        this.betPackData.forEach(bet => {
          if (bet.betPackActive === true) {
            count = count + 1;
          }
        });
        if (count >= 20) { this.disableCreate = true; }
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
    this.globalLoaderService.hideLoader();
  }

  /**
  * Get Active and Inactive betpack count
  * @returns - {active: number, inactive: number}
  */
  get betPackAmount(): ActiveInactiveExpired {
    const activeBetpack = this.betPackData && this.betPackData.filter(betpack => betpack.betPackActive === true);
    const activeBetpackAmount = activeBetpack && activeBetpack.length;
    const inactiveBetpackAmount = this.betPackData.length - activeBetpackAmount;

    return {
      active: activeBetpackAmount,
      inactive: inactiveBetpackAmount
    };
  }

  /**
  * Remove betPack Check
  * @param {BetPackModel} betPack - ;
  * *  @returns - {void}
  */
  public removeBetPack(betPack: BetPackModel): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove BetPack',
      message: 'Are You Sure You Want to Remove BetPack?',
      yesCallback: () => {
        this.sendRemoveRequest(betPack);
      }
    });
  }

  /**
  * Remove Campaign Call
  * @param {BetPackModel} betPack - ;
  * *  @returns - {void}
  */
  public sendRemoveRequest(betPack: BetPackModel): void {
    this.apiClientService.betpackService().deleteBetPack(betPack.id)
      .subscribe((data: any) => {
        this.loadBetPacks();
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'BetPack is Removed.'
        });
      });
  }

  /**
  * Navigate to Campaign Edit
  *  @returns - {void}
  */
  public openCreateBetPack(): void {
    this.router.navigateByUrl('betpack-market/betpack-list/create');
  }

  /**
 * reorderHandler for betpack
 *  @returns - {void}
 */
  public reorderHandler(newOrder: Order): void {
    this.apiClientService
      .betpackService()
      .reorderBetPack(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Bet Pack order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
