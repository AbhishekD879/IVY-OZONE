import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { BetpackOnboardService } from '@root/app/client/private/services/betpack-onboard.service';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Breadcrumb } from '@app/client/private/models';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { onboardingConstants } from '../../constants/betpack-market-place.constants';
import { onboardImageDataModel, onboardImageFile, OnboardModel } from '../../model/bet-pack-banner.model';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';

@Component({
  selector: 'app-edit-onboard',
  templateUrl: './edit-onboard.component.html',
  styleUrls: ['./edit-onboard.component.scss']
})
export class EditOnboardComponent implements OnInit {
  @ViewChild('imageUploadInput') private imageUploadInput: ElementRef;

  public onboardConstats: any = onboardingConstants
  public onboardImageData: onboardImageDataModel;
  public onboardingEditFormGroup: FormGroup
  public currentAdditem: OnboardModel;
  public disableBottons: boolean = true;
  public buttonChange: boolean = false;
  public isLoading: boolean = false;
  public constructOnboardData: OnboardModel;
  public uploadImageName: string
  public imageToUpload: onboardImageFile;
  public editOnboardData: OnboardModel
  public editOnboardFormData: any = new FormData();
  public id: string;
  public checkImage:boolean = false;
  public editOnboard: string;
  public breadcrumbsData: Breadcrumb[];
  public formData: OnboardModel;
  public unsavedOnboardData: Array<OnboardModel>;

  constructor(private formBuilder: FormBuilder,
    private router: Router,
    private betpackOnboardService: BetpackOnboardService,
    private globalLoaderService: GlobalLoaderService,
    private route: ActivatedRoute,
    private dialogService: DialogService,
    private apiClientService: ApiClientService) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params.id;
    this.onboardImageData = this.betpackOnboardService.getOnboardEditData();
    this.unsavedOnboardData = this.betpackOnboardService.getCreateOnboardData();
    this.editFormGorup();
    this.setValueToForm();    
    this.disableBottons = this.isValueChanges()
  }

  /**
  * editFormGorup
  * @returns - {void}
  */
  public editFormGorup(): void {
    this.onboardingEditFormGroup = this.formBuilder.group({
      imageType: new FormControl('', [Validators.required]),
      onboardImageDetails: new FormControl({ value: '', disabled: true }, [Validators.required]),
      imageLabel: new FormControl('', [Validators.required, Validators.maxLength(50)]),
      nextCTAButtonLabel: new FormControl('', [Validators.required, Validators.maxLength(50)]),
    });
  }

  /**
* check if form is valid.
* @returns - {boolean}
*/
  isValidForm(): boolean {
    return this.onboardingEditFormGroup.valid;
  }

  /**
* check if form is change.
* @returns - {boolean}
*/
  isValueChanges(): boolean {
    this.onboardingEditFormGroup.valueChanges.subscribe((val: OnboardModel) => {
      let imageLabel = this.onboardingEditFormGroup.get('imageLabel').value.length;
      let buttonLabel = this.onboardingEditFormGroup.get('nextCTAButtonLabel').value.length;
      if (this.currentAdditem) {
        this.disableBottons = (val.nextCTAButtonLabel === this.editOnboardData.nextCTAButtonLabel &&
          val.imageType === this.editOnboardData.imageType &&
          this.uploadImageName === this.editOnboardData.onboardImg.name &&
          val.imageLabel === this.editOnboardData.imageLabel);
      }
      else if (this.editOnboardData) {
        this.disableBottons = (val.nextCTAButtonLabel === this.editOnboardData.nextCTAButtonLabel &&
          val.imageType === this.editOnboardData.imageType &&
          this.uploadImageName === this.editOnboardData.onboardImageDetails.originalname &&
          val.imageLabel === this.editOnboardData.imageLabel);
      }
      else{
        this.disableBottons = true;
      }
      if (imageLabel >= 50 || buttonLabel >= 50 || imageLabel == 0 || buttonLabel == 0) {
        this.disableBottons = true;
      }
    });
    return this.disableBottons;
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
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Uploaded',
      message: 'Betpack onboarding image configuration is updated successfully',
      closeCallback() {
        self.router.navigate(['betpack-market/onboarding-betpack']);
      }
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
 * Load data on page load
 * @returns - {void}
 */
  setValueToForm(isLoading: boolean = true): void {
    this.showHideSpinner()
    this.currentAdditem = this.unsavedOnboardData.find(image => {
      if (this.id === image.id && image.isAdd) {
        return image;
      }
    });
    if (this.currentAdditem) {
      this.buttonChange = true;
      this.editOnboardData = this.currentAdditem;
      this.editOnboard = this.currentAdditem.imageLabel
      this.breadcrumbsData = [{
        label: 'Onboarding',
        url: '/betpack-market/onboarding-betpack'
      }, {
        label: this.currentAdditem.imageLabel,
        url: `/onboarding-betpack/${this.id}`
      }];
      this.uploadImageName = this.currentAdditem.onboardImg.name;
      this.imageToUpload = this.currentAdditem.onboardImg
      this.onboardingEditFormGroup.get('imageType').setValue(this.currentAdditem.imageType);
      this.onboardingEditFormGroup.get('onboardImageDetails').setValue(this.currentAdditem.onboardImg.name);
      this.onboardingEditFormGroup.get('imageLabel').setValue(this.currentAdditem.imageLabel);
      this.onboardingEditFormGroup.get('nextCTAButtonLabel').setValue(this.currentAdditem.nextCTAButtonLabel);
      this.showHideSpinner(false)
    }
    else {
      this.apiClientService.onboardbetpackService().getOnboardImage(this.onboardImageData.id, this.id).map((response: HttpResponse<OnboardModel>) => response.body)
        .subscribe((res: OnboardModel) => {
          if (res.id == this.id) {
            this.editOnboardData = res;
            this.editOnboard = res.imageLabel
            this.breadcrumbsData = [{
              label: 'Onboarding',
              url: '/betpack-market/onboarding-betpack'
            }, {
              label: res.imageLabel,
              url: `/onboarding-betpack/${this.id}`
            }];
            this.uploadImageName = res.onboardImageDetails.originalname;
            this.onboardingEditFormGroup.get('imageType').setValue(res.imageType);
            this.onboardingEditFormGroup.get('onboardImageDetails').setValue(res.onboardImageDetails.originalname);
            this.onboardingEditFormGroup.get('imageLabel').setValue(res.imageLabel);
            this.onboardingEditFormGroup.get('nextCTAButtonLabel').setValue(res.nextCTAButtonLabel);
            this.showHideSpinner(false)
          }
        })
    }
  }

  /**
 * Upload File.
 * @returns - {void}
 */
  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/png', 'image/jpeg'];

    this.uploadImageName = file.name;
    this.imageToUpload = file;
    this.disableBottons =  this.uploadImageName === this.onboardingEditFormGroup.get('onboardImageDetails').value 
    if (supportedTypes.indexOf(fileType) === -1) {
      if(this.checkImage){
        this.imageUploadInput.nativeElement.value = '';
        this.uploadImageName = '';
        this.imageToUpload = undefined;
        this.disableBottons = true;
      }
      else{
      this.setValueToForm();
      }
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"jpeg\" and \"png\".'
      });
      return;
    }
  }

  /**
  * Upload File.
  * @returns - {void}
  */
  uploadImageFile(event): void {
    this.imageUploadInput.nativeElement.click();
  }

  /**
 * Remove Uploaded File.
 * @returns - {void}
 */
  removeMainImage(event): void {
    if(event.target.classList[0] === 'main-image-btn'){
    this.imageUploadInput.nativeElement.value = '';
    this.uploadImageName = '';
    this.imageToUpload = undefined;
    this.disableBottons = true;
    this.checkImage = true;
    }
  }

  /**
 * prepare form data.
 * @returns - {void}
 */
  createEditImageData(): void {
    this.formData = this.onboardingEditFormGroup.getRawValue();
    this.editOnboardFormData = new FormData()
    this.editOnboardFormData.append('imageLabel', this.formData.imageLabel);
    this.editOnboardFormData.append('imageType', this.formData.imageType);
    this.editOnboardFormData.append('nextCTAButtonLabel', this.formData.nextCTAButtonLabel);
    this.imageToUpload ? this.editOnboardFormData.append('onboardImg', this.imageToUpload) : this.editOnboardFormData.delete('onboardImg');
    if (this.editOnboardData.id) {
      this.editOnboardFormData.append('onboardImageDetails.filename', this.editOnboardData.onboardImageDetails.filename);
      this.editOnboardFormData.append('onboardImageDetails.filetype', this.editOnboardData.onboardImageDetails.filetype);
      this.editOnboardFormData.append('onboardImageDetails.originalname', this.editOnboardData.onboardImageDetails.originalname);
      this.editOnboardFormData.append('onboardImageDetails.path', this.editOnboardData.onboardImageDetails.path);
      this.editOnboardFormData.append('onboardImageDetails.size', this.editOnboardData.onboardImageDetails.size);

    }
    return this.editOnboardFormData;
  }

  /**
   * Add edit data to table.
   * @returns - {void}
   */
  addChanges(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'To save onboard image',
      message: 'Click on save changes in landing page to save the added image',
      closeCallback() {
        self.router.navigate(['betpack-market/onboarding-betpack']);
      }
    });
    this.formData = this.onboardingEditFormGroup.getRawValue();
    this.constructOnboardData = {
      id: this.id,
      imageType: this.formData.imageType,
      isAdd: true,
      onboardImg: this.imageToUpload,
      imageLabel: this.formData.imageLabel,
      nextCTAButtonLabel: this.formData.nextCTAButtonLabel
    },
      this.betpackOnboardService.setOnboardData(this.constructOnboardData)
  }

  /**
 * Save splash data form.
 * @returns - {void}
 */
  saveChanges(): void {
    this.dialogService.showConfirmDialog({
      title: 'Save Onboard',
      message: 'Are you sure you want to save Onboarding image configuration?',
      yesCallback: () => {
        this.sendSaveRequest();
      }
    });
  }
  sendSaveRequest(isLoading: boolean = true): void {
    this.showHideSpinner()
    this.apiClientService.onboardbetpackService().putOnboardImage(this.createEditImageData(), this.onboardImageData.id, this.id).subscribe((res) => {
      if (res) {
        this.showHideSpinner(false)
        this.uploadNotify();
      }
    }, error => {
      this.showHideSpinner(false)
      this.errorNotify(error);
    });
  }

  /**
 * Revert splash data form.
 * @returns - {void}
 */
  revertChanges(): void {
    this.setValueToForm()
  }

  /**
 * Remove splash data form.
 * @returns - {void}
 */
  public remove(): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Onboard Betpack`,
      message: `Are you sure you want to remove Betpack Onboarded Image?`,
      yesCallback: () => {
        this.removeRequest()
      }
    });
  }
  removeRequest(): void {
    this.apiClientService.onboardbetpackService().deleteOnboardImage(this.onboardImageData.id, this.id).subscribe((res) => {
      if(res){
            this.router.navigate(['betpack-market/onboarding-betpack']);
      }
    });
  }
}

