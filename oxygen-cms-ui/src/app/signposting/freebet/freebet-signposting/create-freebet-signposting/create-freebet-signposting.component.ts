import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models/breadcrumb.model';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { SignpostingInfo } from '@root/app/signposting/models/signposting.model';
import { SignpostingConstants, defaultSignpostingData, selectThresholdTypes } from '@root/app/signposting/constants/signposting.constants';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { BrandService } from '@root/app/client/private/services/brand.service';

@Component({
  selector: 'app-create-freebet-signposting',
  templateUrl: './create-freebet-signposting.component.html',
  styleUrls: ['./create-freebet-signposting.component.scss']
})

export class CreateFreebetSignpostingComponent implements OnInit {

  public signpostingConstants: any = SignpostingConstants;
  public breadcrumbsData: Breadcrumb[];
  public signpostingData: SignpostingInfo;
  public signpostingDataMemory: SignpostingInfo;
  public id: string;
  public isLoading: boolean = true;
  public isEdit: boolean = false;
  public selectThresholdTypeEnum: any = selectThresholdTypes;
  public selectThresholdTypeOptions: string[] = Object.keys(selectThresholdTypes);

  /**
   * Constructor
   * @param router: Router 
   * @param globalLoaderService: GlobalLoaderService
   * @param route: ActivatedRoute
   * @param dialogService: DialogService
   * @param apiClientService: ApiClientService
   */
  constructor(
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
    private route: ActivatedRoute,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private brandService: BrandService) { }

  /**
   * ngOnInit
  */
  ngOnInit(): void {
    this.onLoad();
  }

  /**
   * Initialise signposting data on load
   * @returns - {void}
   */
  private onLoad(): void {
    this.id = this.route.snapshot.params.id;
    defaultSignpostingData.brand = this.brandService.brand;
    if (this.id) {
      this.showHideSpinner(true);
      this.apiClientService.freebetSignpostingService().getSignposting(this.id).map((response: any) => response.body).subscribe(res => {
        this.signpostingDataMemory = JSON.parse(JSON.stringify(res));
        this.signpostingData = res;
        this.isLoading = false;
        this.isEdit = true;
        this.breadcrumbsData = [{
          label: 'Freebet Signposting',
          url: '/signposting/freebet-signposting'
        },
        {
          label: this.signpostingData.title,
          url: `/freebet-signposting/${this.id}`
        }];
        this.showHideSpinner(false);
      });
    } else {
      this.signpostingData = JSON.parse(JSON.stringify(defaultSignpostingData));
      this.isLoading = false;
      this.isEdit = false;
      this.breadcrumbsData = [{
        label: 'Freebet Signposting',
        url: '/signposting/freebet-signposting'
      }, {
        label: 'Create',
        url: `/freebet-signposting/create`
      }];
    }
  }

  /**
   * Validate the form
   * @returns - {boolean}
   */
  public isValidForm(): boolean {
    if (this.isEdit) {
      return this.isValidEditForm();
    } else {
      return this.isValidCreateForm();
    }
  }

  /**
   * Validate the create form
   * @returns - {boolean}
   */
  private isValidCreateForm(): boolean {
    let messageDisplayValid: boolean = false;
    let isthresholdValid: boolean = false;
    let isTitleValid: boolean = false;

    // title
    if (this.signpostingData.title && this.signpostingData.title.length > 0) {
      isTitleValid = true;
    }

    // signpost
    if (this.signpostingData.signPost && this.signpostingData.signPost.length <= 100) {
      messageDisplayValid = true;
    }

    // threshold value
    if (this.signpostingData.price.priceType === this.selectThresholdTypeEnum.Fractional) {
      if (this.signpostingData.price.priceNum && this.signpostingData.price.priceDen) {
        isthresholdValid = true;
      }
    } else {
      if (this.signpostingData.price.priceDec) {
        isthresholdValid = true;
      }
    }

    if (isTitleValid && messageDisplayValid && isthresholdValid) {
      return false;
    } else {
      return true;
    }
  }

  /**
  * Validate the edit form
  * @returns - {boolean}
  */
  private isValidEditForm(): boolean {
    let isBtnDisabled: boolean = true;
    let isMessageDisplayChanged: boolean = false;
    let isthresholdChanged: boolean = false;
    let isActiveChanged: boolean = false;

    let isFieldEmpty: boolean = this.isValidCreateForm();

    if (isFieldEmpty) {
      return isBtnDisabled;
    } else {
      if (this.signpostingData && this.signpostingDataMemory) {
        // isActive
        if (this.signpostingData.isActive !== this.signpostingDataMemory.isActive) {
          isActiveChanged = true;
        }

        // messageDisplay
        if (this.signpostingData.signPost !== this.signpostingDataMemory.signPost) {
          isMessageDisplayChanged = true;
        }

        // threshold type - fractional
        if (this.signpostingData.price.priceType === this.selectThresholdTypeEnum.Fractional) {
          if (this.signpostingData.price.priceNum
            && Number(this.signpostingData.price.priceNum) !== Number(this.signpostingDataMemory.price.priceNum)) {
            isthresholdChanged = true;
          }

          if (this.signpostingData.price.priceDen
            && Number(this.signpostingData.price.priceDen) !== Number(this.signpostingDataMemory.price.priceDen)) {
            isthresholdChanged = true;
          }
        } else {
          // threshold type - decimal
          if (this.signpostingData.price.priceDec
            && Number(this.signpostingData.price.priceDec) !== Number(this.signpostingDataMemory.price.priceDec)) {
            isthresholdChanged = true;
          }
        }
      }

      if (isMessageDisplayChanged || isthresholdChanged || isActiveChanged) {
        isBtnDisabled = false;
      }

      return isBtnDisabled;
    }
  }

  /**
   * Save changes confirmation
   * @returns - {void}
  */
  public saveChanges(): void {
    let messageStatus: string = this.id ? 'Save' : 'Create';
    this.dialogService.showConfirmDialog({
      title: `${messageStatus} Signposting`,
      message: `Are you sure you want to ${messageStatus.toLocaleLowerCase()} signposting configuration?`,
      yesCallback: () => {
        this.sendSaveRequest();
      }
    });
  }

  /**
   * Service call for create/update signposting
   * @returns - {void}
  */
  private sendSaveRequest(): void {
    this.showHideSpinner();
    this.updatePriceDatatype();
    if (this.id) {
      this.apiClientService.freebetSignpostingService().updateSignposting(this.signpostingData).subscribe((res) => {
        if (res) {
          this.showHideSpinner(false);
          this.uploadNotify();
        }
      }, error => {
        this.showHideSpinner(false);
        this.errorNotify(error);
      });
    } else {
      this.apiClientService.freebetSignpostingService().createSignposting(this.signpostingData).subscribe((res) => {
        if (res) {
          this.showHideSpinner(false);
          this.uploadNotify();
        }
      }, error => {
        this.showHideSpinner(false);
        this.errorNotify(error);
      });
    }
  }

  /**
   * Update datatypes of price on save
   * @returns - {void}  
  */
  private updatePriceDatatype(): void {
    if (this.signpostingData && this.signpostingData.price) {
      if (this.signpostingData.price.priceType === this.selectThresholdTypeEnum.Fractional) {
        this.signpostingData.price.priceNum = Number(this.signpostingData.price.priceNum);
        this.signpostingData.price.priceDen = Number(this.signpostingData.price.priceDen);
        this.signpostingData.price.priceDec = null;
      } else {
        this.signpostingData.price.priceDec = Number(this.signpostingData.price.priceDec);
        this.signpostingData.price.priceNum = null;
        this.signpostingData.price.priceDen = null;
      }
    }
  }

  /**
   * Upload notification.
   * @param isDelete 
   * @returns - {void}
  */
  private uploadNotify(isDelete: boolean = false): void {
    const self = this;
    let messageStatus: string;
    if (isDelete) {
      messageStatus = 'Removed';
    } else {
      messageStatus = this.id ? 'Saved' : 'Created';
    }
    this.dialogService.showNotificationDialog({
      title: `${messageStatus} Signposting`,
      message: `Freebet signposting configuration is ${messageStatus.toLocaleLowerCase()} successfully.`,
      closeCallback() {
        self.router.navigate(['signposting/freebet-signposting']);
      }
    });
  }

  /**
   * Error notification
   * @returns - {void}
  */
  private errorNotify(error: any): void {
    this.dialogService.showNotificationDialog({
      title: 'Error',
      message: JSON.stringify(error)
    });
  }

  /**
   * To show or hide spinner
   * @param {boolean} toShow
   * @returns - {void}
  */
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Revert changes confirmation
   * @returns - {void}
  */
  public revertChanges(): void {
    this.dialogService.showConfirmDialog({
      title: 'Revert Changes',
      message: 'Are you sure you want to revert the changes?',
      yesCallback: () => {
        this.revertFormChanges();
      }
    });
  }


  /**
   * Revert changes
   * @returns - {void}
  */
  private revertFormChanges(): void {
    if (this.id && this.signpostingDataMemory) {
      this.signpostingData = JSON.parse(JSON.stringify(this.signpostingDataMemory));
    } else {
      this.signpostingData = JSON.parse(JSON.stringify(defaultSignpostingData));
    }
  }


  /**
   * To enable and disable active checkbox
   * @returns - {void}
  */
  public activeStatus(): void {
    this.signpostingData.isActive = !this.signpostingData.isActive;
  }

  /**
   * Delete confirmation.
   * @returns - {void}
  */
  public remove(): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Signposting`,
      message: `Are you sure you want to remove the signposting?`,
      yesCallback: () => {
        this.removeRequest();
      }
    });
  }

  /**
   * Service call to delete signposting
   * @returns - {void}
  */
  private removeRequest(): void {
    this.showHideSpinner(true);
    this.apiClientService.freebetSignpostingService().deleteSignposting(this.signpostingData.id).subscribe((res) => {
      if (res) {
        this.showHideSpinner(false);
        this.uploadNotify(true);
        this.router.navigate(['signposting/freebet-signposting']);
      }
    }, error => {
      this.showHideSpinner(false);
      this.errorNotify(error);
    });
  }

}
