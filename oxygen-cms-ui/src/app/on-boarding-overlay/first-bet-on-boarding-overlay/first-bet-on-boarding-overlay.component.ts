import { ChangeDetectorRef, Component, ElementRef, EventEmitter, HostListener, OnInit, Output, ViewChild } from '@angular/core';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IFirstBetPlacement } from './first-bet-placement-overlay.model';
import { FIRST_BET_PLACEMENT_VALUES, first_bet_placement } from './first-bet-placement-overlay.constants';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { splitTagsEntitiesAndCheckLength } from './valdiaitorMaxLengthCheck';
import { ErrorService } from '@app/client/private/services/error.service';
import { AppConstants } from '@root/app/app.constants';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';

@Component({
  selector: 'app-first-bet-on-boarding-overlay',
  templateUrl: './first-bet-on-boarding-overlay.component.html',
  styleUrls: ['./first-bet-on-boarding-overlay.component.scss']
})
export class FirstBetOnBoardingOverlayComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('inputLimit') inputLimit: ElementRef;

  charLimit = 200;
  firstBetform: FormGroup;
  onBoardingFirstBet: IFirstBetPlacement;
  readonly FIRST_BET: { [key: string]: string } = first_bet_placement;
  checkEndDateEnable: any;
  @Output() onDateUpdate: EventEmitter<DateRange> = new EventEmitter();
  isSetEndDateBtnEnable: boolean;
  uploadBannerIconName: any;
  imageToUpload: File;
  uploadBannerIcon: string;
  removeDate: boolean = true;

  @ViewChild('bannerIconUpload') private bannerIconUpload: ElementRef;

  constructor(private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private cd: ChangeDetectorRef, public formBuilder: FormBuilder,
    public snackBar: MatSnackBar,
    private errorService: ErrorService,
    private globalLoaderService:GlobalLoaderService) {
    this.verifyOnboardingFirstBet = this.verifyOnboardingFirstBet.bind(this);
  }

  ngOnInit(): void {
    this.loadInitialData();
  }

  /**
   * To Verify Onboarding first bet
   * @param {IFirstBetPlacement} termsConditions
   * @returns {boolean}
   */
  verifyOnboardingFirstBet(termsConditions: IFirstBetPlacement): boolean {
    return termsConditions && termsConditions.homePage.title.length > 0 && termsConditions.homePage.button.length > 0 &&
      termsConditions.homePage.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit && termsConditions.homePage.description.length > 0 &&
      termsConditions.button.title.length > 0 && termsConditions.button.rightButtonDesc.length > 0 && termsConditions.button.leftButtonDesc.length > 0 &&
      termsConditions.button.description.length > 0 && termsConditions.button.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.pickYourBet.title.length > 0 &&
      termsConditions.pickYourBet.description.length > 0 && termsConditions.pickYourBet.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.placeYourBet.defaultContent.title.length > 0 &&
      termsConditions.placeYourBet.defaultContent.description.length > 0 && termsConditions.placeYourBet.defaultContent.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.placeYourBet.boost.title.length > 0 &&
      termsConditions.placeYourBet.boost.description.length > 0 && termsConditions.placeYourBet.boost.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betPlaced.defaultContent.title.length > 0 && termsConditions.betPlaced.buttonDesc.length > 0 &&
      termsConditions.betPlaced.defaultContent.description.length > 0 && termsConditions.betPlaced.defaultContent.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betPlaced.winAlert.title.length > 0 &&
      termsConditions.betPlaced.winAlert.description.length > 0 && termsConditions.betPlaced.winAlert.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betSlip.defaultContent.title.length > 0 &&
      termsConditions.betSlip.defaultContent.description.length > 0 && termsConditions.betSlip.defaultContent.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betSlip.boost.title.length > 0 &&
      termsConditions.betSlip.boost.description.length > 0 && termsConditions.betSlip.boost.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betDetails.defaultContent.title.length > 0 &&
      termsConditions.betDetails.defaultContent.description.length > 0 && termsConditions.betDetails.defaultContent.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.betDetails.cashOut.title.length > 0 &&
      termsConditions.betDetails.cashOut.description.length > 0 && termsConditions.betDetails.cashOut.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.addSelection.title.length > 0 &&
      termsConditions.addSelection.description.length > 0 && termsConditions.addSelection.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.myBets.defaultContent.title.length > 0 && termsConditions.myBets.buttonDesc.length > 0 &&
      termsConditions.myBets.defaultContent.description.length > 0 && termsConditions.myBets.defaultContent.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.myBets.cashOut.title.length > 0 &&
      termsConditions.myBets.cashOut.description.length > 0 && termsConditions.myBets.cashOut.description.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < this.charLimit &&
      termsConditions.fileName && ((!this.onBoardingFirstBet.expiryDateEnabled)? !this.endDateValid():this.onBoardingFirstBet.displayTo!=null);

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
    this.apiService.firstBetPlacementService()
      .getDetailsByBrand()
      .subscribe((data: { body: IFirstBetPlacement }) => {
        if (!data.body) {
          this.onBoardingFirstBet = FIRST_BET_PLACEMENT_VALUES;
        } else {
          this.onBoardingFirstBet = data.body;
        } 
        this.createFormGroup();
        this.isExpiryDateChecked();
        this.actionButtons?.extendCollection(this.onBoardingFirstBet);
      }, error => {
        if (error.status === 404) {

          this.onBoardingFirstBet = this.getDefaultValues();
          this.createFormGroup();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  createFormGroup() {
    if(this.onBoardingFirstBet){
    this.firstBetform = new FormGroup({
      homePageTitle: new FormControl(this.onBoardingFirstBet.homePage.title || '', [Validators.required]),
      homePageDesc: new FormControl(this.onBoardingFirstBet.homePage.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
      homePageBtn: new FormControl(this.onBoardingFirstBet.homePage.button || '', [Validators.required]),
      confirmBannerBtnTitle: new FormControl(this.onBoardingFirstBet.button.title || '', [Validators.required]),
      confirmBannerBtnDesc: new FormControl(this.onBoardingFirstBet.button.description, [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
      confirmBannerleftButtonDesc: new FormControl(this.onBoardingFirstBet.button.leftButtonDesc || '', [Validators.required]),
      confirmBannerRightButtonDesc: new FormControl(this.onBoardingFirstBet.button.rightButtonDesc || '', [Validators.required]),
      pickYourBetTitle: new FormControl(this.onBoardingFirstBet.pickYourBet.title || '', [Validators.required]),
      pickYourBetDesc: new FormControl(this.onBoardingFirstBet.pickYourBet.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
      placeYourBetFormGroup: this.formBuilder.group({
        placeYourBetDefaultTitle: new FormControl(this.onBoardingFirstBet.placeYourBet.defaultContent.title || '', [Validators.required]),
        placeYourBetDefaultDesc: new FormControl(this.onBoardingFirstBet.placeYourBet.defaultContent.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        placeYourBetBoostTitle: new FormControl(this.onBoardingFirstBet.placeYourBet.boost.title || '', [Validators.required]),
        placeYourBetBoostDesc: new FormControl(this.onBoardingFirstBet.placeYourBet.boost.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)])
      }),
      addSelectionTitle: new FormControl(this.onBoardingFirstBet.addSelection.title || '', [Validators.required]),
      addSelectionDesc: new FormControl(this.onBoardingFirstBet.addSelection.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
      betPlacedFormGroup: this.formBuilder.group({
        betPlacedDefaultTitle: new FormControl(this.onBoardingFirstBet.betPlaced.defaultContent.title || '', [Validators.required]),
        betPlacedDefaultDesc: new FormControl(this.onBoardingFirstBet.betPlaced.defaultContent.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        betPlacedBtnDesc: new FormControl(this.onBoardingFirstBet.betPlaced.buttonDesc || '', [Validators.required]),
        betPlacedWinAlertTitle: new FormControl(this.onBoardingFirstBet.betPlaced.winAlert.title || '', [Validators.required]),
        betPlacedWinAlertDesc: new FormControl(this.onBoardingFirstBet.betPlaced.winAlert.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)])
      }),
      betSlipFormGroup: this.formBuilder.group({
        betSlipDefaultTitle: new FormControl(this.onBoardingFirstBet.betSlip.defaultContent.title || '', [Validators.required]),
        betSlipDefaultDesc: new FormControl(this.onBoardingFirstBet.betSlip.defaultContent.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        betSlipBoostTitle: new FormControl(this.onBoardingFirstBet.betSlip.boost.title || '', [Validators.required]),
        betSlipBoostDesc: new FormControl(this.onBoardingFirstBet.betSlip.boost.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)])
      }),
      betDetailsFormGroup: this.formBuilder.group({
        betDetailsDefaultTitle: new FormControl(this.onBoardingFirstBet.betDetails.defaultContent.title || '', [Validators.required]),
        betDetailsDefaultDesc: new FormControl(this.onBoardingFirstBet.betDetails.defaultContent.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        betDetailsCashOutTitle: new FormControl(this.onBoardingFirstBet.betDetails.cashOut.title || '', [Validators.required]),
        betDetailsCashOutDesc: new FormControl(this.onBoardingFirstBet.betDetails.cashOut.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)])
      }),
      myBetsFormGroup: this.formBuilder.group({
        myBetsDefaultTitle: new FormControl(this.onBoardingFirstBet.myBets.defaultContent.title || '', [Validators.required]),
        myBetsDefaultDesc: new FormControl(this.onBoardingFirstBet.myBets.defaultContent.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        myBetsCashOutTitle: new FormControl(this.onBoardingFirstBet.myBets.cashOut.title || '', [Validators.required]),
        myBetsCashOutDesc: new FormControl(this.onBoardingFirstBet.myBets.cashOut.description || '', [Validators.required, splitTagsEntitiesAndCheckLength(this.charLimit)]),
        myBetsBtnDesc: new FormControl(this.onBoardingFirstBet.myBets.buttonDesc || '', [Validators.required])
      })
    });
  }
  }

  /**
   * To assign default values
   * @returns {IFirstBetPlacement}
   */
  private getDefaultValues(): IFirstBetPlacement {
    const popup = { ...FIRST_BET_PLACEMENT_VALUES };
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
   * To handle save and edit scenarios
   */
  private save(): void {
    if (this.onBoardingFirstBet.createdAt) {
      this.sendRequest('updateFirstBet');
    } else {
      this.sendRequest('saveFirstBet');
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
  private sendRequest(requestType: string): void {
    this.apiService.firstBetPlacementService()[requestType](this.onBoardingFirstBet)
      .map((response) => response.body)
      .subscribe((data: IFirstBetPlacement) => {
        this.onBoardingFirstBet = data;
        if (this.uploadBannerIcon && requestType === 'saveFirstBet') {
          this.SaveBannerIconUploaded(this.uploadBannerIcon,requestType)
      } else {
        this.finishFirstBetOnBoardingCreation();
      }
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  finishFirstBetOnBoardingCreation(){
    this.actionButtons.extendCollection(this.onBoardingFirstBet);
    if(this.onBoardingFirstBet.createdAt!=''){
    this.dialogService.showNotificationDialog({
      title: 'Success',
      message: 'Your changes have been saved'
    });
    }
  }

  handleDateUpdate(data: DateRange) {
    this.onBoardingFirstBet.displayFrom = new Date(data.startDate).toISOString();
    this.onBoardingFirstBet.displayTo = data.endDate ? new Date(data.endDate).toISOString() : "";
    this.endDateValid();
  }

  updateFirstbetDescription(data: any, firstbetTutorialProperty: any, formControlName: string, formGrpName?: string) {

    const prop = firstbetTutorialProperty.split('.');
    const propertyData = this.onBoardingFirstBet[prop[0]];
    if (firstbetTutorialProperty.split('.')[2]) {
      propertyData[firstbetTutorialProperty.split('.')[1]][firstbetTutorialProperty.split('.')[2]] = data;
    } else {
      propertyData[firstbetTutorialProperty.split('.')[1]] = data;
    }
    formGrpName ? this.firstBetform.get([formGrpName, formControlName]).setValue(data) :
      this.firstBetform.get(formControlName).setValue(data);
    this.cd.detectChanges();
  }

  /**
 * End Date valid check
 */
  public endDateValid(): boolean {
    return this.onBoardingFirstBet?.displayFrom > this.onBoardingFirstBet?.displayTo;
  }

  onEndDateUpdate(endDate: string): void {
    this.onBoardingFirstBet.displayTo = endDate;
  }

  prepareToUploadFile(event) {
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
     this.uploadBannerIcon = file;
     this.onBoardingFirstBet.fileName = file.name;
    const requestType=this.onBoardingFirstBet.id===''?'saveFirstBet':''
    if(requestType !== 'saveFirstBet'){
    this.SaveBannerIconUploaded(file,requestType)
    }
  }

  handleUploadImageClick() {
    const input = this.bannerIconUpload.nativeElement;
    input.click();
  }

  public SaveBannerIconUploaded(file,requestType){
    const formData = new FormData();
    //uploaded file
    formData.append('file', file);
    this.apiService
      .firstBetPlacementService()
      .postFirstBetBulbIcon(this.onBoardingFirstBet.id, formData) 
      .map((uploadResponseData: HttpResponse<IFirstBetPlacement>) => {
            return uploadResponseData && uploadResponseData.body;
          })
          .subscribe((uploadResponseData: IFirstBetPlacement) => {
            if (uploadResponseData && requestType === 'saveFirstBet') {
              this.finishFirstBetOnBoardingCreation();
            }else{
              this.onBoardingFirstBet = _.extend(uploadResponseData, _.pick(this.onBoardingFirstBet, 'isEnable', 'buttonText'));
                this.snackBar.open('Banner Icon Was Uploaded.', 'Ok!', {
                  duration: AppConstants.HIDE_DURATION,
                });
              }

            }
          , (error: HttpErrorResponse) => {
              this.errorService.emitError('FirstBet Onboarding Created, but Image not uploaded. Error: ' + error.error.message);
          });
  }

  public removeBannerIcon(): void {
    const input = this.bannerIconUpload.nativeElement;

    input.value = '';
    this.onBoardingFirstBet.fileName = undefined;
    this.uploadBannerIcon = undefined;
    this.globalLoaderService.showLoader();
    this.apiService
      .firstBetPlacementService()
      .removeFirstBetBulbIcon(this.onBoardingFirstBet.id)
      .map((bannerResponse: HttpResponse<IFirstBetPlacement>) => {
        return bannerResponse.body;
      })
      .subscribe((firstBetBulbIcon: IFirstBetPlacement) => {
        this.onBoardingFirstBet = _.extend(firstBetBulbIcon, _.pick(this.onBoardingFirstBet, 'isEnable', 'imageLabel', 'buttonText'));
        this.snackBar.open('Banner Icon Was Removed.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  getButtonName(fileName): string {
    return fileName && fileName.length > 0 ? 'Change File' : 'Upload File';
  }

  @HostListener('input') input() {
    let value = this.inputLimit.nativeElement.value;
    if (value.length > 2) {
      this.inputLimit.nativeElement.value =
        this.inputLimit.nativeElement.value.substr(0, 2);
      return;
    }
  }

  isExpiryDateChecked()
   {
    this.removeDate = false;
    this.checkEndDateEnable = this.onBoardingFirstBet.expiryDateEnabled;
    this.isSetEndDateBtnEnable = this.onBoardingFirstBet.expiryDateEnabled;
    setTimeout(() => {
      this.removeDate = true;
    }, 0);
  }

}
