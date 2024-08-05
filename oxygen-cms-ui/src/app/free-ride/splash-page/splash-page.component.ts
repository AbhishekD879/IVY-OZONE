import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup } from '@angular/forms';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '../../shared/dialog/dialog.service';
import { FreeRideAPIService } from '../services/free-ride.api.service';
import { FreeRideSplashPageModel } from './model/splash-page.model';

@Component({
  selector: 'app-splash-page',
  templateUrl: './splash-page.component.html',
  styleUrls: ['./splash-page.component.scss']
})
export class SplashPageComponent implements OnInit {
  splashFormGroup: FormGroup;
  splashFormData = new FormData();
  bannerImage: string;
  splashImage: string;
  freeRideLogo: string;
  disableSaveBtn: boolean;
  responseData: FreeRideSplashPageModel;
  constructor(
    private dialogService: DialogService,
    private freeRideService: FreeRideAPIService,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.createFormGorup();
    this.loadSplashData();
    this.splashFormGroup.valueChanges.subscribe((val) => {
      this.disableSaveBtn = val.welcomeMsg === this.responseData.welcomeMsg &&
        val.termsAndConditionLink === this.responseData.termsAndConditionLink && val.buttonText === this.responseData.buttonText &&
        val.termsAndConditionHyperLinkText === this.responseData.termsAndConditionHyperLinkText &&
        val.promoUrl === this.responseData.promoUrl &&
        val.isHomePage === this.responseData.isHomePage &&
        val.isBetReceipt === this.responseData.isBetReceipt;
    });
  }

  public createFormGorup(): void {
    this.splashFormGroup = new FormGroup({
      launchBannerName: new FormControl({ value: '', disabled: true }, [Validators.required]),
      splashPageName: new FormControl({ value: '', disabled: true }, [Validators.required]),
      freeRideImg: new FormControl({ value: '', disabled: true }, [Validators.required]),
      welcomeMsg: new FormControl('', [Validators.required, Validators.maxLength(80)]),
      termsAndConditionLink: new FormControl('', [Validators.maxLength(150)]),
      termsAndConditionHyperLinkText: new FormControl('', [Validators.maxLength(150)]),
      buttonText: new FormControl('', [Validators.required, Validators.maxLength(15)]),
      promoUrl: new FormControl('', [Validators.maxLength(15)]),
      isHomePage: new FormControl('false', []),
      isBetReceipt: new FormControl('false', []),
    });
  }

  /**
   * Load data on page load
   * @returns - {void}
   */
  loadSplashData(): void {
    this.freeRideService.getAllSplashData().subscribe((res: FreeRideSplashPageModel) => {
      this.responseData = res;
      this.splashFormGroup.get('launchBannerName').setValue(res.bannerImageFileName);
      this.splashFormGroup.get('splashPageName').setValue(res.splashImageName);
      this.splashFormGroup.get('freeRideImg').setValue(res.freeRideLogoFileName);
      this.splashFormGroup.get('welcomeMsg').setValue(res.welcomeMsg);
      this.splashFormGroup.get('termsAndConditionLink').setValue(res.termsAndConditionLink || '');
      this.splashFormGroup.get('termsAndConditionHyperLinkText').setValue(res.termsAndConditionHyperLinkText || '');
      this.splashFormGroup.get('buttonText').setValue(res.buttonText);
      this.splashFormGroup.get('promoUrl').setValue(res.promoUrl);
      this.splashFormGroup.get('isHomePage').setValue(res.isHomePage);
      this.splashFormGroup.get('isBetReceipt').setValue(res.isBetReceipt);
      this.disableSaveBtn = true;
    });
  }


  /**
   * Uplad File.
   * @returns - {void}
   */
  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/png', 'image/jpeg', 'image/svg', 'image/svg+xml'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"jpeg\" and \"png\".'
      });

      return;
    }
    if (event.target.id === 'upload-launch-banner') {
      this.splashFormGroup.get('launchBannerName').setValue(file.name);
      this.bannerImage = file;
    } else if (event.target.id === 'upload-splash-page') {
      this.splashFormGroup.get('splashPageName').setValue(file.name);
      this.splashImage = file;
    } else {
      this.splashFormGroup.get('freeRideImg').setValue(file.name);
      this.freeRideLogo = file;
    }
    this.disableSaveBtn = this.responseData.bannerImageFileName === this.splashFormGroup.get('launchBannerName').value
                        && this.responseData.splashImageName === this.splashFormGroup.get('splashPageName').value
                        && this.responseData.freeRideLogoFileName === this.splashFormGroup.get('freeRideImg').value;
  }
  handleUploadImageClick(event) {
    const input = event.target.previousElementSibling.querySelector('input');
    input.click();
  }

  /**
   * Remove Uploaded File.
   * @returns - {void}
   */
  removeMainImage(event): void {
    if (event.target.classList[0] === 'launch-image-btn') {
      this.splashFormGroup.get('launchBannerName').setValue('');
      this.bannerImage = undefined;
      this.disableSaveBtn = true;
    } else if (event.target.classList[0] === 'splash-image-btn') {
      this.splashFormGroup.get('splashPageName').setValue('');
      this.splashImage = undefined;
      this.disableSaveBtn = true;
    } else {
      this.splashFormGroup.get('freeRideImg').setValue('');
      this.freeRideLogo = undefined;
      this.disableSaveBtn = true;
    }
  }

  /**
  * check if form is valid.
  * @returns - {boolean}
  */
  disableSave(): boolean {
    return !this.splashFormGroup.valid || this.splashFormGroup.get('launchBannerName').value === ''
      || this.splashFormGroup.get('splashPageName').value === '' || this.splashFormGroup.get('freeRideImg').value === '';
  }

  /**
   * prepare form data.
   * @returns - {void}
   */

  constructFormData(): FormData {
    this.splashFormData = new FormData();
    this.splashImage ? this.splashFormData.append('splashImg', this.splashImage) : this.splashFormData.delete('splashImg');
    this.freeRideLogo ? this.splashFormData.append('freeRideLogoImg', this.freeRideLogo) : this.splashFormData.delete('freeRideLogoImg');
    this.bannerImage ? this.splashFormData.append('bannerImg', this.bannerImage) : this.splashFormData.delete('bannerImg');
    this.splashFormData.append('brand', this.responseData.brand);
    this.splashFormData.append('welcomeMsg', this.responseData.welcomeMsg);
    this.splashFormData.append('termsAndConditionLink', this.responseData.termsAndConditionLink);
    this.splashFormData.append('termsAndConditionHyperLinkText', this.responseData.termsAndConditionHyperLinkText);
    this.splashFormData.append('buttonText', this.responseData.buttonText);
    this.splashFormData.append('promoUrl', this.responseData.promoUrl);
    this.splashFormData.append('isHomePage', this.responseData.isHomePage.toString());
    this.splashFormData.append('isBetReceipt', this.responseData.isBetReceipt.toString());
    if (this.responseData.id) {
      this.splashFormData.append('id', this.responseData.id);
      this.splashFormData.append('splashImageName', this.responseData.splashImageName);
      this.splashFormData.append('splashImage.filename', this.responseData.splashImage.filename);
      this.splashFormData.append('splashImage.originalname', this.responseData.splashImage.originalname);
      this.splashFormData.append('splashImage.path', this.responseData.splashImage.path);
      this.splashFormData.append('bannerImageFileName', this.responseData.bannerImageFileName);
      this.splashFormData.append('bannerImage.filename', this.responseData.bannerImage.filename);
      this.splashFormData.append('bannerImage.originalname', this.responseData.bannerImage.originalname);
      this.splashFormData.append('bannerImage.path', this.responseData.bannerImage.path);
      this.splashFormData.append('freeRideLogoFileName', this.responseData.freeRideLogoFileName);
      this.splashFormData.append('freeRideLogo.filename', this.responseData.freeRideLogo.filename);
      this.splashFormData.append('freeRideLogo.originalname', this.responseData.freeRideLogo.originalname);
      this.splashFormData.append('freeRideLogo.path', this.responseData.freeRideLogo.path);
    }
    return this.splashFormData;
  }


  /**
   * Save splash data form.
   * @returns - {void}
   */

  saveChanges(): void {
    this.responseData.brand = this.brandService.brand;
    this.responseData = { ...this.responseData, ...this.splashFormGroup.value };
    this.freeRideService.splashData(this.constructFormData(), this.responseData?.id).subscribe((res: FreeRideSplashPageModel) => {
      if (res) {
        this.dialogService.showNotificationDialog({
          title: 'Uploaded',
          message: 'Your Data is uploaded successfully'
        });
        this.disableSaveBtn = true;
      }
    }, error => {
      this.dialogService.showNotificationDialog({
        title: 'Error',
        message: error
      });
    });
  }

}
