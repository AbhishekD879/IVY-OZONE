import {Component, OnInit, ViewChild} from '@angular/core';

import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {ApiClientService} from '../../../client/private/services/http/index';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DateRange} from '../../../client/private/models/dateRange.model';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import {BetReceiptBannerTablet} from '../../../client/private/models/betreceiptbannertablet.model';
import {BetReceiptBanner} from '../../../client/private/models/betreceiptbanner.model';
import * as _ from 'lodash';

@Component({
  selector: 'app-receipt-edit',
  templateUrl: './receipt-edit.component.html',
  styleUrls: ['./receipt-edit.component.scss']
})
export class ReceiptEditComponent implements OnInit {

  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  public banner: BetReceiptBanner | BetReceiptBannerTablet;
  public type: string;

  @ViewChild('actionButtons')
  public actionButtons;

  constructor(
    public snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public saveChanges(): void {
    this.getService()
        .edit(this.banner)
        .map((response: HttpResponse<any>) => {
          return response.body;
        })
        .subscribe((banner) => {
          this.banner = banner;
          this.actionButtons.extendCollection(this.banner);
          this.dialogService.showNotificationDialog({
            title: `Bet Receipt Banner ${this.type} Saving`,
            message: `Bet Receipt Banner ${this.type} is Saved.`
          });
    });
  }

  public handleDateUpdate(data: DateRange): void {
    this.banner.validityPeriodStart = data.startDate;
    this.banner.validityPeriodEnd = data.endDate;
  }

  public remove(): void {
    this.getService()
        .removeBannerImage(this.banner.id)
        .map((bannerResponse: HttpResponse<any>) => {
          return bannerResponse.body;
        })
        .subscribe((banner) => {
          this.banner = _.extend(banner, _.pick(this.banner, 'disabled', 'name', 'description',
            'validityPeriodEnd', 'validityPeriodStart'));
          this.snackBar.open('Image Was Removed.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  public isValidForm(banner): boolean {
    return !!(banner.name &&
      banner.name.length > 0 &&
      banner.validityPeriodStart && banner.validityPeriodStart.length > 0 &&
      banner.validityPeriodEnd && banner.validityPeriodEnd.length > 0);
  }

  public removeBanner(): void {
    this.showHideSpinner();
    this.getService()
        .remove(this.banner.id)
        .subscribe(() => {
          this.router.navigate([`/banners/receipt/${this.type.toLowerCase()}`]);
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  public isUseImageAvailable(): boolean {
    return this.type === 'Mobile';
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  public uploadBanner(file): void {
    this.globalLoaderService.showLoader();
    this.getService()
        .postNewBannerImage(this.banner.id, file)
        .map((bannerResponse: HttpResponse<any>) => {
          return bannerResponse.body;
        })
        .subscribe((banner) => {
          this.globalLoaderService.hideLoader();
          this.banner = _.extend(banner, _.pick(this.banner, 'disabled', 'name', 'description',
            'validityPeriodEnd', 'validityPeriodStart'));

          this.snackBar.open(`Bet Receipt Banner ${this.type} Image is Uploaded.`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }, () => {
          this.globalLoaderService.hideLoader();
        });
  }

  private loadInitData(isLoading: boolean = true): void {
    this.showHideSpinner();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.type = params.type.charAt(0).toUpperCase() + params.type.slice(1);
      this.getService()
          .getById(params['id'])
          .map((bannerResponse: HttpResponse<any>) => {
            return bannerResponse.body;
          })
          .subscribe((banner: any) => {
            this.banner = banner;

            this.showHideSpinner(false);
            this.breadcrumbsData = [{
              label: `Bet Receipt Banners ${this.type}`,
              url: `/banners/receipt/${this.type.toLowerCase()}`
            }, {
              label: this.banner.name,
              url: `/banners/receipt/${this.type.toLowerCase()}/${this.banner.id}`
            }];
          }, () => {
            this.showHideSpinner(false);
          });
    });
  }

  private getService(): any {
    return this.apiClientService[`betReceipt${this.type}Banner`]();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeBanner();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

}
