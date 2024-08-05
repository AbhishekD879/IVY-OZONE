import { Component, OnInit } from '@angular/core';
import { Breadcrumb, DataTableColumn } from '@root/app/client/private/models';
import { BetpackOnboardService } from '@root/app/client/private/services/betpack-onboard.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { HttpResponse } from '@angular/common/http';
import { onboardingConstants } from '../constants/betpack-market-place.constants';
import { onboardImageDataModel, OnboardModel } from '../model/bet-pack-banner.model';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@root/app/app.constants';
import { Order } from '@app/client/private/models/order.model';

@Component({
  selector: 'app-onboarding-betpack',
  templateUrl: './onboarding-betpack.component.html',
  styleUrls: ['./onboarding-betpack.component.scss']
})
export class OnboardingBetpackComponent implements OnInit {
  public onboardConstats: any = onboardingConstants;
  public newOnboardData: Array<OnboardModel>;
  public disabled: boolean = true;
  public buttonDisabled: boolean = true;
  public isLoading: boolean = false;
  public onboardImageData: onboardImageDataModel;
  public onboardData: Array<OnboardModel>;
  public onboardFormData: any;
  public breadcrumbsData: Breadcrumb[];
  public searchField: string = '';
  public reorderImage: boolean = false;
  searchableProperties: string[] = [
    'imageLabel',
    'imageType'
  ];
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Image Label',
      property: 'imageLabel',
      link: {
        hrefProperty: 'id'
      },
      type: 'link',
    },
    {
      name: 'Image Type',
      property: 'imageType',
    }
  ];

  constructor(private betpackOnboardService: BetpackOnboardService,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    public snackBar: MatSnackBar,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.newOnboardData = this.betpackOnboardService.getOnboardData();
    this.betpackOnboardService.setCreateOnboardData(this.newOnboardData);
    this.loadIntialData();
  }

/**
* Load List of Onboard Betpack
*  @returns - {void}
*/
  loadIntialData(isLoading: boolean = true): void {
    this.onboardData = undefined;
    this.showHideSpinner();
    this.apiClientService.onboardbetpackService().getOnboardData().map((response: HttpResponse<onboardImageDataModel>) => response.body)
      .subscribe((res: onboardImageDataModel) => {
        this.onboardData = [];
        if (res) {
          this.onboardImageData = res;
          this.onboardImageData.images.forEach(newImage => {
            this.onboardData.push(newImage);
          }); 
          this.newOnboardData.forEach((img) => {
            this.onboardData.push(img);
            this.buttonDisabled = false;
          })
          this.disabled = res.isActive;
          this.betpackOnboardService.sendEditRequest(this.onboardImageData);
        }
        else {
          this.onboardImageData = null;
          this.newOnboardData.forEach((img) => {
            this.onboardData.push(img);
            this.buttonDisabled = false;
          })
        }
        this.showHideSpinner(false);
      }, error => {
        this.onboardData = [];
        this.showHideSpinner(false);
        this.errorNotify(error);
      });
  }

    /**
   * To show or hide spinner
   * @param {boolean} toShow
   */
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
  * uploaded notification.
  * @returns - {void}
  */
  uploadNotify() {
    this.dialogService.showNotificationDialog({
      title: 'Uploaded',
      message: 'Betpack onboarding configuration uploaded successfully'
    });
  }

  /**
  * Error notification.
  * @returns - {void}
  */
  errorNotify(error: any) {
    this.dialogService.showNotificationDialog({
      title: 'Error',
      message: JSON.stringify(error)
    });
  }

  /**
* prepare form data.
* @returns - {void}
*/
  constructFormData(): FormData {
    this.onboardFormData = new FormData();
    this.onboardFormData.append('isActive', this.disabled);
    this.onboardFormData.append('brand', this.brandService.brand);
    for (let i = 0; i < this.onboardData.length; i++) {
      this.onboardFormData.append(`images[${i}].imageLabel`, this.onboardData[i].imageLabel);
      if (this.onboardImageData && this.onboardImageData.id && this.onboardData[i].onboardImageDetails) {
        this.onboardFormData.append(`images[${i}].onboardImageDetails.filename`, this.onboardData[i].onboardImageDetails.filename);
        this.onboardFormData.append(`images[${i}].onboardImageDetails.filetype`, this.onboardData[i].onboardImageDetails.filetype);
        this.onboardFormData.append(`images[${i}].onboardImageDetails.originalname`, this.onboardData[i].onboardImageDetails.originalname);
        this.onboardFormData.append(`images[${i}].onboardImageDetails.path`, this.onboardData[i].onboardImageDetails.path);
        this.onboardFormData.append(`images[${i}].onboardImageDetails.size`, this.onboardData[i].onboardImageDetails.size);
      }
      else {
        this.onboardFormData.append(`images[${i}].onboardImg`, this.onboardData[i].onboardImg);
      }
      this.onboardFormData.append(`images[${i}].nextCTAButtonLabel`, this.onboardData[i].nextCTAButtonLabel);
      this.onboardFormData.append(`images[${i}].imageType`, this.onboardData[i].imageType);
    }
    return this.onboardFormData;
  }

 /**
  * Remove Onboard Betpack
  * @returns - {void}
  */
  removeOnboardBetPack(event: OnboardModel) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Onboard',
      message: 'Are you sure you want to remove Betpack Onboarded Image?',
      yesCallback: () => {
        this.removeImageRequest(event);
      }
    });
  }
  removeImageRequest(eventId: OnboardModel): void {
    this.showHideSpinner();
    if (eventId.id && !eventId.isAdd) {
      this.apiClientService.onboardbetpackService().deleteOnboardImage(this.onboardImageData.id, eventId.id).subscribe((deleteRes) => {
        this.loadIntialData();
        this.isValid();
        this.showHideSpinner(false);
        this.snackBar.open('Saved Betpack Onboarding image Removed!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
    }
    else {
      this.onboardData.forEach((Image: OnboardModel, index) => {
         /* istanbul ignore else */
        if (Image.id === eventId.id) {
          this.onboardData.splice(index, 1);
        }
      });
      this.newOnboardData.forEach((newImage: OnboardModel, index) => {
        if (newImage.id === eventId.id) {
          this.newOnboardData.splice(index, 1);
          this.betpackOnboardService.setUpdateOnboardData(this.newOnboardData);
          this.showHideSpinner(false);
          this.snackBar.open('Unsaved Betpack Onboarding image Removed!', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
      })
      this.isValid();
    }
  }

  /**
  * To enable and disable active checkbox
  * @returns - {boolean}
  */ 
  activeStatus(): void {
    this.disabled = !this.disabled;
    this.isValid();
  }

  /**
  * To enable and disable button
  * @returns - {boolean}
  */
  isValid(): void {
    let newAddedRecords = this.betpackOnboardService.getOnboardData();
    let isTableUpdated = newAddedRecords.length > 0;
    if (this.onboardData && this.onboardData.length === 0) {
      this.buttonDisabled = true;
    }
    else if (this.onboardImageData.isActive != this.disabled || isTableUpdated) {
      this.buttonDisabled = false;
    }
    else {
      this.buttonDisabled = true;
    }
  }

  /**
   * reordering the table data
   * @param newOrder 
   */
  reorderHandler(newOrder: Order): void {
    if (this.onboardImageData.images.length > 0) {
      this.reorderImage = true;
      this.saveChanges();
    }
    else {
      this.betpackOnboardService.setUpdateOnboardData(this.onboardData);
    }
  }
  
  /**
   * set empty data
   * @returns - {void}
   */
  setEmpty(): void {
    this.buttonDisabled = true;
    this.onboardData = [];
    this.newOnboardData = [];
    this.betpackOnboardService.setEmpty(this.newOnboardData);
  }

  /**
  * Save splash data form.
  * @returns - {void}
  */
  saveChanges(): void {
    if (this.reorderImage) {
      this.sendSaveRequest();
    }
    else {
      this.dialogService.showConfirmDialog({
        title: 'Save Onboard',
        message: 'Are you sure you want to save Betpack Onboarding configuration?',
        yesCallback: () => {
          this.sendSaveRequest();
        }
      });
    }
  }

  sendSaveRequest(isLoading: boolean = true): void {
    this.showHideSpinner();

    if (this.onboardImageData && this.onboardImageData.id) {
      this.apiClientService.onboardbetpackService().putOnboardData(this.constructFormData(), this.onboardImageData.id).map((response: HttpResponse<onboardImageDataModel>) => response.body)
        .subscribe(res => {
          if (res) {
            this.setEmpty();
            this.onboardData = undefined;
            this.loadIntialData();
            if (!this.reorderImage) {
              this.uploadNotify();
            }
            else {
              this.snackBar.open('Betpack onboarding image order saved!', 'Ok!', {
                duration: AppConstants.HIDE_DURATION,
              });
            }
            this.showHideSpinner(false);
            this.reorderImage = false;
          }
        }, error => {
          this.showHideSpinner(false);
          this.errorNotify(error);
          this.reorderImage = false;
        });
    }
    else {
      this.apiClientService.onboardbetpackService().postOnboardData(this.constructFormData()).subscribe((res: any) => {
        if (res) {
          this.setEmpty();
          if (!this.reorderImage) {
            this.uploadNotify();
          }
          else {
            this.snackBar.open('Betpack onboarding image order saved!', 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          }
          this.onboardData = undefined;
          this.loadIntialData();
          this.showHideSpinner(false);
          this.reorderImage = false;
        }
      }, error => {
        this.showHideSpinner(false);
        this.errorNotify(error);
        this.reorderImage = false;
      });
    }
  }
}
