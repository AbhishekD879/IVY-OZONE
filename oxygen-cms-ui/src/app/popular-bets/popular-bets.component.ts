import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { PopularBets } from '@app/client/private/models/popularBets.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { POPULAR_BETS_VALUES } from './popular-bets-overlay.constants';
import { Router } from '@angular/router';
import { GlobalLoaderService } from '../shared/globalLoader/loader.service';

@Component({
  selector: 'app-popular-bets',
  templateUrl: './popular-bets.component.html'
})
export class PopularbetsComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  popularBetsFormGroup: FormGroup;
  popularBetsFormData: PopularBets;
  HourMin: any = [{ time: 'Hour', short: true }, { time: 'Minute', short: false }];
  isBetReceiptRoute: boolean;
  title: string;

  constructor(
    private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private router: Router,
    private globalLoaderService: GlobalLoaderService
  ) {
  }

  ngOnInit(): void {
    this.title = 'Most Popular/Trending Bets Configuration for';
    this.isBetReceiptRoute = this.router.url.includes('most-popular/bet-receipt');
    this.title = !this.isBetReceiptRoute ? `${this.title} BetSlip` : `${this.title} Bet Receipt` ;
    this.loadInitialData();
  }

  /**
    * To Load initial data
  */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.apiService.popularBetsApiService()
      .getDetailsByBrand()
      .subscribe((data: { body: PopularBets }) => {
        if (!data.body) {
          this.popularBetsFormData = POPULAR_BETS_VALUES;
        } else {
          this.popularBetsFormData = data.body;
        }
        this.globalLoaderService.hideLoader();
        this.createFormGroup();
        this.actionButtons?.extendCollection(this.popularBetsFormData);
      }, error => {
        if (error.status === 404) {
          this.popularBetsFormData = this.getDefaultValues();
          this.createFormGroup();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
        this.globalLoaderService.hideLoader();
      });
  }

    /**
    * To create form group data for fields
  */
  public createFormGroup(): void {
    this.popularBetsFormGroup = new FormGroup({
      active: new FormControl(this.popularBetsFormData?.active || true),
      displayForAllUsers: new FormControl(this.popularBetsFormData?.displayForAllUsers || true),
      mostBackedIn: new FormControl(this.popularBetsFormData?.mostBackedIn || '', [Validators.required]),
      eventStartsIn: new FormControl(this.popularBetsFormData?.eventStartsIn || '', [Validators.required]),
      maxSelections: new FormControl(this.popularBetsFormData?.maxSelections || '', [Validators.required, Validators.min(2), Validators.max(5)]),
      betRefreshInterval: new FormControl(this.popularBetsFormData?.betRefreshInterval || '', [Validators.required, Validators.min(1), Validators.maxLength(3)]),
      isTimeInHours: new FormControl(this.popularBetsFormData?.isTimeInHours || true),
      isQuickBetReceiptEnabled: new FormControl(this.popularBetsFormData?.isQuickBetReceiptEnabled || true),
      enableBackedUpTimes : new FormControl(this.popularBetsFormData?.enableBackedUpTimes || true)
    });
  }

  /**
  * To assign default values
  * @returns {PopularBets}
  */
  private getDefaultValues(): PopularBets {
    const popup = { ...POPULAR_BETS_VALUES };
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
  * To Handle actions
  * @param {string} event
  */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        break;
    }
  }

  /**
  * To save and edit
  * @param {string} requestType
  */
  saveChanges(): void {

    if (this.popularBetsFormData.createdAt) {
      this.sendRequest('updateCMSPopularBetsData');
    } else {
      this.sendRequest('saveCMSPopularBetsData');
    }
  }

  /**
  * To save and edit
  * @param {string} requestType
  */
  private sendRequest(requestType: string, isInitialLoad: boolean = false): void {
    this.globalLoaderService.showLoader();
    this.apiService.popularBetsApiService()[requestType](this.popularBetsFormData)
      .map((response) => response.body)
      .subscribe((data: PopularBets) => {
        this.popularBetsFormData = data;
        this.actionButtons?.extendCollection(this.popularBetsFormData);
        this.globalLoaderService.hideLoader();
        if (!isInitialLoad) {
          this.dialogService.showNotificationDialog({
            title: 'Success',
            message: 'Your changes have been saved'
          });
        }
      }, () => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });

  }

  /**
    * To revert changes
  */
  revertChanges(): void {
    this.loadInitialData();
  }

  /**
    * To validate form data to enable save changes button
  */
  isFormValid(popularBetsFormData) : boolean { 
    return !!(popularBetsFormData.betRefreshInterval && popularBetsFormData.maxSelections >=2 && popularBetsFormData.maxSelections <=5 && popularBetsFormData.betRefreshInterval >=1 && popularBetsFormData.betRefreshInterval.toString().length <=3);
  }
}
