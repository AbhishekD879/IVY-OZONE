import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { AppConstants } from '@app/app.constants';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import * as _ from 'lodash';
import { IMyStable } from './onboarding-my-stable.model';
import { ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES, onboarding_my_stable } from '../onboarding-coupon-stat-widgets/on-boarding-overlay.constants';
import { Router} from '@angular/router';

@Component({
  selector: 'app-onboarding-mystable',
  templateUrl: './onboarding-mystable.component.html',
  styleUrls: ['./onboarding-mystable.component.scss']
})
export class OnboardingMystableComponent implements OnInit {

   public apiEndpoint: string = 'my-stable'
  public fieldOrItemName: string = 'myStable'
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('onboardImageUpload') private onboardImageUpload: ElementRef;

  protected ONBOARDING_MY_STABLE: { [key: string]: string } = onboarding_my_stable;

  public myStable: IMyStable;
  public imgEntityId: string;
  public onboardFormData: any;


  constructor(protected apiService: ApiClientService,
    protected dialogService: DialogService,
    protected brandService: BrandService,
    public snackBar: MatSnackBar,
    protected globalLoaderService: GlobalLoaderService,
    private router: Router

  ) {
    this.verifyOnboarding = this.verifyOnboarding.bind(this);
  }

  ngOnInit(): void {
    this.loadInitialData();
  }

  private loadInitialData(): void {
    this.apiService.myStableService().getDetailsByBrand(this.apiEndpoint).subscribe((data: { body: IMyStable }) => {
      if (!data.body) {
        this.myStable=ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES;
      }else{
        this.myStable = data.body;
        this.myStable.fileName = data.body.onboardImageDetails?.originalname?data.body.onboardImageDetails?.originalname:'';
        this.myStable.imageUrl = data.body.onboardImageDetails?.path?data.body.onboardImageDetails?.path:'';
        this.imgEntityId = this.myStable.id;
      }
        this.actionButtons?.extendCollection(this.myStable);
      }, error => {
        if (error.status === 404) {
          this.myStable = this.getDefaultValues();
          this.router.navigate(['/on-boarding-overlay/onboarding-mystable']);
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  private getDefaultValues(): IMyStable {
    const popup = { ...ONBOARDING_OVERLAY_MyStable_DEFAULT_VALUES };
    popup.brand = this.brandService.brand;
    return popup;
  }

   private save(): void {
    if (this.myStable.id) {
      this.sendRequest('updateOnBoardingMyStable');
    } else {
      this.sendRequest('saveOnBoardingMyStable');
    }
  }


  private sendRequest(requestType: string, isInitialLoad: boolean = false): void {
    this.apiService.myStableService()[requestType](this.myStable, this.apiEndpoint).map((response) => response.body)
      .subscribe((data: IMyStable) => {
        this.myStable = data;
        this.actionButtons.extendCollection(this.myStable);
        if (!isInitialLoad) {
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

  prepareToUploadFile(event) {
    console.log('event', event);
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg', 'image/svg+xml'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"jpeg\" ,\"jpg\",\"svg\" and \"png\".'
      });
      return;
    }
    this.imgEntityId ? this.UpdateUploadImage(file, this.imgEntityId) : this.uploadImage(file);
  }

  uploadImage(file) {
    this.onboardFormData = new FormData();
    this.onboardFormData.append('onboardImg', file);
    this.onboardFormData.append('isActive', this.myStable.isActive);
    this.onboardFormData.append('buttonText', this.myStable.buttonText);
    this.onboardFormData.append('brand', this.brandService.brand);
    this.globalLoaderService.showLoader();
    this.apiService.myStableService().postNewMyStableImage(this.onboardFormData, this.apiEndpoint).map((imgResponse: HttpResponse<IMyStable>) => {
        return imgResponse.body;
      })
      .subscribe((res) => {
        this.myStable.fileName = res.onboardImageDetails.originalname;
        this.myStable.imageUrl = res.onboardImageDetails.path;
        this.myStable = _.extend(res, _.pick(this.myStable, 'isActive', 'buttonText', 'fileName'));
        this.snackBar.open('Image Was Uploaded.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  UpdateUploadImage(file, id) {
    this.onboardFormData = new FormData();
    this.onboardFormData.append('onboardImg', file);
    this.onboardFormData.append('isActive', this.myStable.isActive);
    this.onboardFormData.append('buttonText', this.myStable.buttonText);
    this.onboardFormData.append('brand', this.brandService.brand);
    this.globalLoaderService.showLoader();
    this.apiService.myStableService().updateNewMyStableImage(this.onboardFormData, this.apiEndpoint, id)
      .map((imgResponse: HttpResponse<IMyStable>) => {
        return imgResponse.body;
      })
      .subscribe((res) => {
        this.myStable.fileName = res.onboardImageDetails.originalname;
        this.myStable.imageUrl = res.onboardImageDetails.path;
        this.myStable = _.extend(res, _.pick(this.myStable, 'isActive', 'fileName', 'buttonText'));
        this.snackBar.open('Image Was Uploaded.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  public removeUploadMystableImage(): void {
    const input = this.onboardImageUpload.nativeElement;
    input.value = '';
    this.myStable.fileName = '';
    this.globalLoaderService.showLoader();

    this.apiService.myStableService().removeMyStableUploadedImage(this.myStable.id, this.apiEndpoint)
      .map((myStableResponse: HttpResponse<IMyStable>) => {
        return myStableResponse.body;
      })
      .subscribe((res) => {
        this.myStable = _.extend(res, _.pick(this.myStable, 'isActive', 'fileName', 'buttonText'));
        this.snackBar.open('Image Was Removed.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  verifyOnboarding(def: IMyStable): boolean {
    return !!(def && def.fileName && def.buttonText && def.buttonText.length <= 12);
  }

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

  handleUploadImageClick() {
    const input = this.onboardImageUpload.nativeElement;
    input.click();
  }

  getButtonName(fileName): string {
    return fileName && fileName.length > 0 ? 'Change File' : 'Upload File';
  }

  private revert(): void {
    this.loadInitialData();
  }
}
