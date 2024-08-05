import {Component, OnInit} from '@angular/core';

import {HttpResponse} from '@angular/common/http';
import {ActivatedRoute, Params, Router} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {ReceiptCreateComponent} from '../receipt-create/receipt-create.component';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'app-receipt-list',
  templateUrl: './receipt-list.component.html',
  styleUrls: ['./receipt-list.component.scss']
})
export class ReceiptListComponent implements OnInit {

  public isLoading: boolean = false;
  public banners: any[] = [];
  public type: string;
  public searchField: string = '';

  public searchableProperties: string[] = [
    'name'
  ];

  public dataTableColumns: any[] = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Validity Period Start',
      property: 'validityPeriodStart',
      type: 'date'
    },
    {
      name: 'Validity Period End',
      property: 'validityPeriodEnd',
      type: 'date'
    }
  ];

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    this.showHideSpinner();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.type = params.type.charAt(0).toUpperCase() + params.type.slice(1);
      this.getService()
          .findAllByBrand()
          .map((response: HttpResponse<any>) => {
            return response.body;
          })
          .subscribe((banners: any[]) => {
            this.banners = banners;
            this.showHideSpinner(false);
          },  () => {
            this.showHideSpinner(false);
          });
    });
  }

  public createBanner(): void {
    this.dialogService.showCustomDialog(ReceiptCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: `Add New Bet Receipt Banner ${this.type}`,
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (banner) => {
        this.getService()
            .add(banner)
            .map((result: HttpResponse<any>) => {
              return result.body;
            })
            .subscribe((result: any) => {
          this.banners.push(result);
          this.router.navigate([`/banners/receipt/${this.type.toLowerCase()}/${result.id}`]);
        }, () => {
          console.error(`Can not create Bet Receipt Banner ${this.type}`);
        });
      }
    });
  }

  public removeBanner(banner: any): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Bet Receipt Banner ${this.type}`,
      message: `Are You Sure You Want to Remove Bet Receipt Banner ${this.type}?`,
      yesCallback: () => {
        this.banners = this.banners.filter((l) => {
          return l.id !== banner.id;
        });
        this.getService()
            .remove(banner.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: `Bet Receipt Banner ${this.type} is Removed.`
          });
        });
      }
    });
  }

  public reorderHandler(newOrder: Order): void {
    this.getService()
        .postNewBannersOrder(newOrder)
        .subscribe(() => {
      this.snackBar.open(`Bet Receipt Banners ${this.type} Order Saved!!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  public get bannersAmount(): ActiveInactiveExpired {
    const activePromos = this.banners && this.banners.filter(banner => banner.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.banners.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  private getService(): any {
    return this.apiClientService[`betReceipt${this.type}Banner`]();
  }

}
