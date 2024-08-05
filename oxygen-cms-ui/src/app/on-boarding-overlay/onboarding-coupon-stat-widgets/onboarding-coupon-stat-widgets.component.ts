import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { onboarding_stat_widget, ONBOARDING_OVERLAY_DEFAULT_VALUES } from './on-boarding-overlay.constants';
import { ICouponStatWidget } from './onboarding-coupon-stat-widgets.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';
import { AppConstants } from '@root/app/app.constants';
import { FormGroup } from '@angular/forms';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';


@Component({
  selector: 'app-onboarding-coupon-stat-widgets',
  templateUrl: './onboarding-coupon-stat-widgets.component.html',
  styleUrls: ['./onboarding-coupon-stat-widgets.component.scss']
})
export class OnboardingCouponStatWidgetComponent implements OnInit {
  public isLoading: boolean = false;
  public apiEndpoint: string = 'coupon-stats-widget'
  public fieldOrItemName:string = 'couponStatsWidget'
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  public couponStatWidget: ICouponStatWidget;
  protected ONBOARDING_STAT: {[key: string]: string} = onboarding_stat_widget;
  public form: FormGroup;


  constructor(protected apiService: ApiClientService,
    protected dialogService: DialogService,
    protected brandService: BrandService,
    public snackBar: MatSnackBar,
    protected globalLoaderService: GlobalLoaderService,

    ) {
      this.verifyOnboarding = this.verifyOnboarding.bind(this);

    }

  ngOnInit(): void {
    this.loadInitialData();
  }

  /**
   * To Verify Onboarding
   * @param {ICouponStatWidget}
   * @returns {boolean}
   */


  verifyOnboarding(def: ICouponStatWidget): boolean {
    return !!(def && def.imageUrl && def.buttonText && def.buttonText.length <= 12);
  }

  public uploadCouponWidgetStat(formData: FormData): void {
    this.globalLoaderService.showLoader();
    this.apiService
        .couponStatWidgetService()
        .postNewCouponStatImage(this.couponStatWidget.id, formData, this.apiEndpoint)
        .map((couponStatResponse: HttpResponse<ICouponStatWidget>) => {
          return couponStatResponse.body;
        })
        .subscribe((banner: ICouponStatWidget) => {
          this.couponStatWidget = _.extend(banner, _.pick(this.couponStatWidget, 'isEnable', 'buttonText'));

          this.snackBar.open('Image Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
          this.globalLoaderService.hideLoader();
        }, () => {
          this.globalLoaderService.hideLoader();
        });
  }


  public remove(): void {
    this.globalLoaderService.showLoader();
    this.apiService
        .couponStatWidgetService()
        .removeCouponStatImage(this.couponStatWidget.id,this.apiEndpoint)
        .map((couponStatResponse: HttpResponse<ICouponStatWidget>) => {
          return couponStatResponse.body;
        })
        .subscribe((banner) => {
          this.couponStatWidget = _.extend(banner, _.pick(this.couponStatWidget, 'isEnable', 'imageLabel', 'buttonText'));

          this.snackBar.open('Image Was Removed.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
          this.globalLoaderService.hideLoader();
        }, () => {
          this.globalLoaderService.hideLoader();
        });
  }

  /**
   * To Handle actions
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        break;
    }
  }

  /**
   * To Load initial data
   */
  private loadInitialData(): void {
    this.apiService.couponStatWidgetService()
     .getDetailsByBrand(this.apiEndpoint)
     .subscribe((data: {body: ICouponStatWidget}) => {
        this.couponStatWidget = data.body;
        this.actionButtons?.extendCollection(this.couponStatWidget);
      }, error => {
        if (error.status === 404) {
          this.couponStatWidget = this.getDefaultValues();
          this.sendRequest('saveOnBoardingCouponStat', true);
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }



  /**
   * To assign default values
   * @returns {ICouponStatWidget}
   */
  private getDefaultValues(): ICouponStatWidget {
    const popup = {...ONBOARDING_OVERLAY_DEFAULT_VALUES};
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
   * To handle save and edit scenarios
   */
  private save(): void {

    
    if (this.couponStatWidget.createdAt) {
      this.sendRequest('updateOnBoardingCouponStat');
    } else {
      this.sendRequest('saveOnBoardingCouponStat');
    }
  }

  /**
   * To revert changes
   */
  private revert(): void {
    this.loadInitialData();
  }

  /**
   * To save and edit
   * @param {string} requestType
   */
  private sendRequest(requestType: string, isInitialLoad:boolean = false): void {
    this.apiService.couponStatWidgetService()[requestType](this.couponStatWidget, this.apiEndpoint)
      .map((response) => response.body)
      .subscribe((data: ICouponStatWidget) => {
        this.couponStatWidget = data;
        this.actionButtons.extendCollection(this.couponStatWidget);
        if(!isInitialLoad) {
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }
}
