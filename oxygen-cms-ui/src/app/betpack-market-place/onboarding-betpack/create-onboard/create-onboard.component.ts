import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models/breadcrumb.model';
import { BetpackOnboardService } from '@root/app/client/private/services/betpack-onboard.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { onboardingConstants } from '../../constants/betpack-market-place.constants';
import { OnboardModel } from '../../model/bet-pack-banner.model';

@Component({
  selector: 'app-create-onboard',
  templateUrl: './create-onboard.component.html',
  styleUrls: ['./create-onboard.component.scss']
})
export class CreateOnboardComponent implements OnInit {
  @ViewChild('imageUploadInput') private imageUploadInput: ElementRef;
  
  public onboardConstats: any = onboardingConstants;
  public constructOnboardData: OnboardModel;
  public onboardingFormGroup: FormGroup;
  public uploadImageName: string;
  public imageToUpload: File;
  public formData: OnboardModel;
  public breadcrumbsData: Breadcrumb[];
  public disableBottons: boolean = false;

  constructor(private formBuilder: FormBuilder,
    private dialogService: DialogService,
    private router: Router,
    private betpackOnboardService: BetpackOnboardService) { }

  ngOnInit(): void {
    this.breadcrumbsData = [{
      label: 'Onboarding',
      url: '/betpack-market/onboarding-betpack'
    }, {
      label: 'Create',
      url: `/onboarding-betpack//create-onboard`
    }];
    this.createFormGorup();
  }

  /**
  * createFormGorup
  * @returns - {void}
  */
  public createFormGorup(): void {
    this.onboardingFormGroup = this.formBuilder.group({
      imageType: new FormControl('', [Validators.required]),
      onboardImg: new FormControl({ value: '', disabled: true }, [Validators.required]),
      imageLabel: new FormControl('', [Validators.required, Validators.maxLength(50)]),
      nextCTAButtonLabel: new FormControl('', [Validators.required, Validators.maxLength(50)]),
    });
  }

  /**
  * check if form is valid.
  * @returns - {boolean}
  */
  isValidForm(): boolean {
    let imageLabel = this.onboardingFormGroup.get('imageLabel').value.length >= 50;
    let buttonLabel = this.onboardingFormGroup.get('nextCTAButtonLabel').value.length >= 50;
    return !this.onboardingFormGroup.valid || imageLabel ||buttonLabel;
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
    this.disableBottons = false;
    if (supportedTypes.indexOf(fileType) === -1) {
      this.onboardingFormGroup.get('onboardImg').setValue('');
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
  uploadImageFile(event) {
    this.imageUploadInput.nativeElement.click();
  }

  /**
   * Remove Uploaded File.
   * @returns - {void}
   */
  removeMainImage(event) {
    if(event.target.classList[0] === 'main-image-btn'){
      this.imageUploadInput.nativeElement.value = '';
      this.uploadImageName = '';
      this.imageToUpload = undefined;
      this.disableBottons = true;
      }
  }

  private generateUuid(): string {
    function S4(): string {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + '-' + S4() + '-' + S4() + '-' + S4() + '-' + S4() + S4() + S4());
  }

  /**
   * Add data to table.
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
    this.formData = this.onboardingFormGroup.getRawValue();
    this.constructOnboardData = {
      id: this.generateUuid(),
      isAdd: true,
      imageType: this.formData.imageType,
      onboardImg: this.imageToUpload,
      imageLabel: this.formData.imageLabel,
      nextCTAButtonLabel: this.formData.nextCTAButtonLabel
    },
      this.betpackOnboardService.setOnboardData(this.constructOnboardData)
  }

  /**
   * Remove splash data form.
   * @returns - {void}
   */
  revertChanges(): void {
    this.onboardingFormGroup.reset()
  }

}
