import { ChangeDetectorRef, Component, OnInit,AfterViewChecked } from '@angular/core';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '../../shared/dialog/dialog.service';
import { BannerModel } from '../model/bet-pack-banner.model';
import { HttpResponse } from '@angular/common/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { IMAGE_MANAGER_SVG_ID_PATTERN } from '@app/image-manager/constants/image-manager.constant';
import * as _ from 'lodash';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';


@Component({
  selector: 'banner',
  templateUrl: './banner.component.html',
  styleUrls: ['./banner.component.scss']
})
export class BannerComponent implements OnInit,AfterViewChecked{

  bannerFormGroup: FormGroup;
  bannerFormData = new FormData(); 
  disableSaveBtn: boolean;
  charLimit = 70;
  limitExceeded: boolean;
  marketPlaceImageFileName:any={}
  marketPlaceBgImageFileName:any={}
  reviewPageBgImageFileName:any={}
  reviewPageImageFileName:any={}
  expiresInIconImage:any={}
  InitialValue:any
  hideAction=false
  constructor(
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private brandService: BrandService,
    private cd: ChangeDetectorRef,
    private fb: FormBuilder,
    private globalLoaderService:GlobalLoaderService
  ) {
    this.createFormGorup();
  }

  ngOnInit(): void {
    this.loadSplashData();
  } 
  public createFormGorup(): void {
    this.bannerFormGroup = this.fb.group({
      bannerImage: [null],
      bannerImageUpload: [null],
      bannerImageFileName: [null, [Validators.required]],
      welcomeMsg: ['', [Validators.required,Validators.maxLength(70)]],
      termsAndCondition: ['', [Validators.required, Validators.maxLength(70)]],
      termsAndConditionLink: ['', [Validators.required]],
      enabled: [false],
      bannerTextDescInMarketPlacePage: ['', [Validators.required]],
      bannerTextDescInReviewPage: ['', [Validators.required]],
      bannerActiveInMarketPlace: [false],
      bannerActiveInReviewPage: [false],
      expiresInActive: [false],
      expiresInText: ['',[ Validators.required,Validators.maxLength(70)]],
      id: [''],
      createdBy: [''],
      updatedBy: [''],
      updatedAt: [''],
      brand: [this.brandService.brand],
      createdAt: [''],
      updatedByUserName: [''],
      createdByUserName: [''],
    });
  }

  ngAfterViewChecked(){
    if(this.hideAction){
      this.bannerFormGroup.get('marketPlaceImageFileName').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
      this.bannerFormGroup.get('marketPlaceBgImageFileName').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
      this.bannerFormGroup.get('reviewPageBgImageFileName').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
      this.bannerFormGroup.get('reviewPageImageFileName').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
      this.bannerFormGroup.get('expiresInIconImage').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
    }
    }

  /**
   * Load data on page load
   * @returns - {void}
   */
  loadSplashData() {
    this.globalLoaderService.showLoader()
    this.apiClientService.betpackService().getBannerData().map((response: HttpResponse<BannerModel>) => response.body)
      .subscribe((res: any) => {
        this.globalLoaderService.hideLoader();
        this.hideAction=true   
        if(res){
          this.bannerFormGroup.patchValue(res);
        }
      },error=>{
        this.globalLoaderService.hideLoader();
        this.errorNotify(error);

      }
      );
  }

  /**
   * Upload File.
   * @returns - {void}
   */
  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/svg+xml', 'image/gif', 'image/png', 'image/jpeg', 'image/svg'];
    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"jpeg\",\"gif\",\"png\" and \"svg\".'
      });
      return;
    }
    if (event.target.id === 'upload-banner') {
      this.disableSaveBtn = this.bannerFormGroup.get('bannerImageFileName').value===file.name;
       /*istanbul ignore else*/
      if(!this.disableSaveBtn){
        this.bannerFormGroup.patchValue({ bannerImageFileName: file.name });
        this.bannerFormGroup.patchValue({ bannerImageUpload: file });
      }

    }
    
  }

  /**
  * Upload File.
  * @returns - {void}
  */
  public handleUploadImageClick(event): void {
    const input = event.target.previousElementSibling.querySelector('input');
    input.click();
  }

  /**
   * This updates the banner message
   * @param data
   */
  updateBannerMsg(data: string, key: string): void {
    this.bannerFormGroup.get(key).setValue(data);
    this.cd.detectChanges();
  }

  /**
   * Updates the limit exceeds flag
   * @param - {string} msg
   * @returns - {void}
   */
  patchLimitError(msg: string,key:string): void {
    if(msg){
    this.bannerFormGroupControls[key].setErrors({maxLength:true})
    }

  }

  /**
   * Remove Uploaded File.
   * @returns - {void}
   */
  removeMainImage(event): void {
    if (event.target.classList[0] === 'launch-image-btn') {
      this.bannerFormGroup.patchValue({ bannerImageFileName: null });
       /*istanbul ignore else*/
      if(this.bannerFormGroupControls['bannerImageUpload']){
        this.bannerFormGroup.patchValue({ bannerImageUpload: null });
      }
      this.disableSaveBtn = true;
    }
  }
   /**
  * getter for baner form control
  * @returns - {formControl}
  */
  get bannerFormGroupControls() {
    return this.bannerFormGroup.controls;
  }


  /**
  * check if form is valid.
  * @returns - {boolean}
  */
  isValid() {
    return !this.bannerFormGroup.valid ||! this.bannerFormGroup.get('bannerImageFileName').value||this.disableSaveBtn;
  }
   /**
  * check if form is valid.
  * @returns - {void}
  */
  uploadNotify() {
    this.dialogService.showNotificationDialog({
      title: 'Uploaded',
      message: 'Your Changes Are Saved Succesfully'
    });
    this.disableSaveBtn = true;
  }
   /**
  * check if form is valid.
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
    let bannerFormData = new FormData();
   this.bannerFormGroupControls.bannerImageUpload?.value? bannerFormData.append('bannerImg', this.bannerFormGroupControls.bannerImageUpload.value) : bannerFormData.delete('bannerImg');
    bannerFormData.append('brand', this.bannerFormGroupControls.brand.value);
    bannerFormData.append('welcomeMsg', this.bannerFormGroupControls.welcomeMsg.value);
    bannerFormData.append('termsAndConditionLink', this.bannerFormGroupControls.termsAndConditionLink.value);
    bannerFormData.append('termsAndCondition', this.bannerFormGroupControls.termsAndCondition.value);
    bannerFormData.append('enabled', this.bannerFormGroupControls.enabled.value);
    bannerFormData.append('bannerTextDescInMarketPlacePage', this.bannerFormGroupControls.bannerTextDescInMarketPlacePage.value);
    bannerFormData.append('bannerTextDescInReviewPage', this.bannerFormGroupControls.bannerTextDescInReviewPage.value);
    bannerFormData.append('bannerActiveInMarketPlace', this.bannerFormGroupControls.bannerActiveInMarketPlace.value);
    bannerFormData.append('bannerActiveInReviewPage', this.bannerFormGroupControls.bannerActiveInReviewPage.value);
    bannerFormData.append('marketPlaceBgImageFileName', this.bannerFormGroupControls.marketPlaceBgImageFileName.value);
    bannerFormData.append('marketPlaceImageFileName', this.bannerFormGroupControls.marketPlaceImageFileName.value);
    bannerFormData.append('reviewPageBgImageFileName', this.bannerFormGroupControls.reviewPageBgImageFileName.value);
    bannerFormData.append('reviewPageImageFileName', this.bannerFormGroupControls.reviewPageImageFileName.value);
    bannerFormData.append('expiresInActive', this.bannerFormGroupControls.expiresInActive.value);
    bannerFormData.append('expiresInIconImage', this.bannerFormGroupControls.expiresInIconImage.value);
    bannerFormData.append('expiresInText', this.bannerFormGroupControls.expiresInText.value);

    if (this.bannerFormGroupControls.id.value) {
      bannerFormData.append('id', this.bannerFormGroupControls.id.value);
      bannerFormData.append('bannerImageFileName', this.bannerFormGroupControls.bannerImageFileName.value);
      bannerFormData.append('bannerImage.filename', this.bannerFormGroupControls.bannerImage.value?.filename);
      bannerFormData.append('bannerImage.originalname', this.bannerFormGroupControls.bannerImage.value?.originalname);
      bannerFormData.append('bannerImage.path', this.bannerFormGroupControls.bannerImage.value?.path);
      bannerFormData.append('id', this.bannerFormGroupControls.id.value);
    }
    return bannerFormData;
  }
  /**
   * Save splash data form.
   * @returns - {void}
   */
  saveChanges(): void {
    this.hideAction= false;
    this.globalLoaderService.showLoader();

    if (this.bannerFormGroupControls.id.value) {
      this.apiClientService.betpackService().putBannerData(this.constructFormData(), this.bannerFormGroupControls.id.value).subscribe((res) => {
        if (res) {
          this.bannerFormGroup.patchValue(res);
          this.hideAction= true;
        this.globalLoaderService.hideLoader();
          this.uploadNotify();
        }
      }, error => {
        this.errorNotify(error);
        this.globalLoaderService.hideLoader();

      });
    } else {
      this.apiClientService.betpackService().postBannerData(this.constructFormData()).subscribe((res) => {
        if (res) {
          this.bannerFormGroup.patchValue(res);
          this.hideAction= true;
          this.globalLoaderService.hideLoader();
          this.uploadNotify();
        }
      }, error => {
        this.errorNotify(error);
        this.globalLoaderService.hideLoader();
      });
    }
  }
 

  triggrExpiresActive(event){
    !this.bannerFormGroupControls.expiresInActive.value&&this.bannerFormGroup.patchValue({ expiresInActive: event.checked })
  }
  actionsHandler(event){
    switch(event){
    case  'revert':
      this.loadSplashData();
    break;
    case  'save':
      this.saveChanges();
    break
    default:
      break;
    }
  }
}
