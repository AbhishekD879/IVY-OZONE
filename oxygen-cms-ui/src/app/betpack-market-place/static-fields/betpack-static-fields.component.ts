import { Component, AfterViewChecked, OnInit } from '@angular/core';
import { StaticFieldModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FormGroup,FormBuilder, Validators } from '@angular/forms';
import { IMAGE_MANAGER_SVG_ID_PATTERN } from '@app/image-manager/constants/image-manager.constant';

@Component({
  selector: 'betpack-static-fields',
  templateUrl: './betpack-static-fields.component.html'
})
export class StaticFieldComponent implements OnInit, AfterViewChecked {
  betPackLabel: StaticFieldModel;
  emptyLabels: boolean = true;
  backgroundImage: string;
  backgroundImageData = new FormData();
  hideAction=false
  bpLables:FormGroup;
  comingSoonSVG:any={}

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private fb:FormBuilder,
  ) { 
   this.buildForm()
  }

  buildForm() {
    this.bpLables = this.fb.group({
      allFilterPillMessage: ['', [Validators.required,Validators.maxLength(100)]],
      isAllFilterPillMessageActive:[false],
      buyButtonLabel: ['', [Validators.required]],
      backgroundImage:[null],
      allFilterPillMessageActive: [false],
      buyBetPackLabel: ['', [Validators.required, Validators.maxLength(20)]],
      backgroundImageFileName: ['', [Validators.required]],
      gotoMyBetPacksLabel: ['', [Validators.required, Validators.maxLength(50)]],
      depositMessage: ['', [Validators.required, Validators.maxLength(100)]],
      kycArcGenericMessage: ['', [Validators.required]],
      useByLabel: ['', [Validators.required, Validators.maxLength(15)]],
      maxBetPackPerDayBannerLabel: ['', [Validators.required, Validators.maxLength(100)]],
      betPackAlreadyPurchasedPerDayBannerLabel: ['', [Validators.required, Validators.maxLength(100)]],
      betPackMarketplacePageTitle: ['', [Validators.required, Validators.maxLength(30)]],
      errorTitle: ['', [Validators.required, Validators.maxLength(50)]],
      errorMessage: ['', [Validators.required, Validators.maxLength(100)]],
      goToBettingLabel: ['', [Validators.required, Validators.maxLength(20)]],
      goBettingURL: ['', [Validators.required]],
      reviewErrorMessage: ['', [Validators.required, Validators.maxLength(100)]],
      reviewErrorTitle: ['', [Validators.required, Validators.maxLength(50)]],
      reviewGoBettingURL: ['', [Validators.required]],
      reviewGoToBettingLabel: ['', [Validators.required, Validators.maxLength(20)]],
      moreInfoLabel: ['', [Validators.required]],
      buyNowLabel: ['', [Validators.required, Validators.maxLength(20)]],
      betPackReview: ['', [Validators.required, Validators.maxLength(20)]],
      maxPurchasedLabel: ['', [Validators.required, Validators.maxLength(25)]],
      limitedLabel: ['', [Validators.required, Validators.maxLength(25)]],
      soldOutLabel: ['', [Validators.required, Validators.maxLength(25)]],
      endingSoonLabel: ['', [Validators.required, Validators.maxLength(25)]],
      expiresInLabel: ['', [Validators.required, Validators.maxLength(25)]],
      endedLabel: ['', [Validators.required, Validators.maxLength(25)]],
      maxOnePurchasedLabel: ['', [Validators.required, Validators.maxLength(25)]],
      brand: [this.brandService.brand,],
      betPackInfoLabel: ['', [Validators.required, Validators.maxLength(25)]],
      lessInfoLabel: ['', [Validators.required]],
      betPackSuccessMessage: ['', [Validators.required, Validators.maxLength(50)]],
      maxPurchasedTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      limitedTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      soldOutTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      endingSoonTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      expiresInTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      endedTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      maxOnePurchasedTooltip: ['', [Validators.required, Validators.maxLength(100)]],
      id: [''],
      updatedBy: [''],
      updatedAt: [''],
      createdBy: [''],
      createdAt: [''],
      updatedByUserName: [''],
      createdByUserName: [''],
      featuredBetPackBackgroundLabel: ['', [Validators.required, Validators.maxLength(25)]],
      serviceError: ['', [Validators.required, Validators.maxLength(50)]],
      goToReviewText: ['', [Validators.required, Validators.maxLength(30)]],
      goToBetbundleText: ['', [Validators.required, Validators.maxLength(30)]],
      isDailyLimitBannerEnabled: [false],
      comingSoon: ['', [Validators.required, Validators.maxLength(25)]],
      sortOrder:[null]
    })
  }
  get bpControls() {
    return this.bpLables?.controls
  }
  ngOnInit() {
    this.load();
  }
  ngAfterViewChecked(){
    this.bpLables.get('comingSoonSvg').setValidators([Validators.required, Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)])
  }
  bpIsValid(){
    return this.bpLables?.invalid
  }
  /**
   * to get the static fields data
   * @returns - {void}
   */
  public load(): void {
    this.apiClientService.betpackService().getLabelsData().map((response: HttpResponse<StaticFieldModel>) => response.body)
      .subscribe((res: StaticFieldModel) => {
        /*istanbul ignore else*/
        if (res) {
          this.bpLables.patchValue(res)
          this.hideAction=true
          this.emptyLabels = false;

        }
      });
  }

  /**
 * to get the saved notification
 * @returns - {void}
 */
  public saveNotify(): void {
    this.dialogService.showNotificationDialog({
      title: `Labels Saving`,
      message: `Labels are Saved.`,
      closeCallback: () => {
        this.load();
      }
    });
  }

  /**
  * to set action items remove,save and revert
  * @param {any} event -;
  * @returns - {void}
  */
  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.load();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }


  /**
  * To save the static fields data
  * @returns - {void}
  */
  public saveChanges(): void {
    this.hideAction=false
    if (this.emptyLabels) {
      this.apiClientService.betpackService().postLabelsData(this.bpLables.value)
        .map((response: HttpResponse<StaticFieldModel>) => response.body)
        .subscribe((res: StaticFieldModel) => {
          this.bpLables.patchValue(res)
          this.hideAction=false
          this.saveNotify();
        });
    } else {
      this.apiClientService.betpackService().putLabelsData(this.bpLables.value)
        .map((response: HttpResponse<StaticFieldModel>) => response.body)
        .subscribe((res: StaticFieldModel) => {
          this.bpLables.patchValue(res)
          this.hideAction=false
          this.saveNotify();
        });
    }
  }


  /**
 * Upload File.
 * @returns - {void}
 */
  public prepareToUploadFile(event): void {
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
    this.bpLables.patchValue({backgroundImageFileName:file.name})
    this.backgroundImage = file;
    this.apiClientService.betpackService().postBackgroundData(this.constructFormData(), this.bpLables.value.id).subscribe(res => {
      this.dialogService.showNotificationDialog({
        title: 'Uploaded',
        message: 'Background Image uploaded Succesfully.'
      });
    });
  }

  /**
   *  Upload File handler.
   * @param {any} event - ;
   * @returns - {void}
   */
  public handleUploadImageClick(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Upload Background Image',
      message: 'Are You Sure You Want to Upload Background Image?',
      yesCallback: () => {
        const input = event.target.previousElementSibling.querySelector('input');
        input.click();
      }
    });
  }
  
  /**
   * Remove Uploaded File.
   * @param {any} event -
   * @returns - {void}
   */
  public removeMainImage(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Background Image',
      message: 'Are You Sure You Want to Remove Background Image?',
      yesCallback: () => {
        this.apiClientService.betpackService().deleteBackgroundData(this.bpLables.value.id)
          .subscribe((res) => {
            this.bpLables.patchValue({backgroundImageFileName:''})
            this.backgroundImage = undefined;
            this.dialogService.showNotificationDialog({
              title: 'Removed',
              message: 'Background Image removed Succesfully.'
            });
          });
      }
    });
  }

  /**
 * prepare form data.
 * @returns - {FormData}
 */
  public constructFormData(): FormData {
    this.backgroundImageData = new FormData();
    this.backgroundImage ? this.backgroundImageData.append('file', this.backgroundImage) : this.backgroundImageData.delete('file');
    return this.backgroundImageData;
  }
}
