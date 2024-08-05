import { Breadcrumb } from './../../client/private/models/breadcrumb.model';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PromotionsAPIService } from '../service/promotions.api.service';
import { Promotion } from '../../client/private/models/promotion.model';
import { SportCategory } from '../../client/private/models/sportcategory.model';
import { Competition } from '../../client/private/models/competition.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { DateRange } from '../../client/private/models/dateRange.model';
import { BrandService } from '../../client/private/services/brand.service';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { FormControl, Validators } from '@angular/forms';
import { ErrorService } from '../../client/private/services/error.service';
import { MatSelectChange } from '@angular/material/select';
import { BetPackValidationService } from '@app/promotions/service/bet-pack-validation.service';
import { FreeRideValidationServiceService } from '@app/promotions/service/free-ride-validation-service.service';
import { ApiClientService } from '@app/client/private/services/http';
import { PromotionsNavigationGroup } from '@app/client/private/models/promotions-navigation.model';

@Component({
  selector: 'create-promotion-page',
  templateUrl: './create.promotion.page.component.html'
})
export class CreatePromotionComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  promotion: Promotion = {
    // values will be set from from
    title: '',
    promotionId: null,
    openBetId: '',
    popupTitle: '',
    promoKey: '',
    description: '',
    vipLevelsInput: '',
    requestId: '',
    validityPeriodStart: '',
    validityPeriodEnd: '',
    showToCustomer: 'both',
    isSignpostingPromotion: false,

    // default automatically created values
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    title_brand: '',
    sortOrder: 0,
    heightMedium: 0,
    widthMedium: 0,
    uriMedium: '',
    htmlMarkup: '',
    promotionText: '',
    shortDescription: '',
    vipLevels: [],
    lang: '',
    brand: this.brandService.brand,
    categoryId: [],
    disabled: false,
    updatedByUserName: '',
    createdByUserName: '',
    competitionId: [],
    useDirectFileUrl: false,
    templateMarketName: '',
    blurbMessage: '',
    betPack: {
      isBetPack: false,
      bodyText: '',
      offerId: '',
      triggerIds: '',
      betValue: '',
      lowFundMessage: '',
      notLoggedinMessage: '',
      errorMessage: '',
      congratsMsg: '',
    },
    freeRideConfig: {
      isFreeRidePromo: false,
      errorMessage: '',
      ctaPreLoginTitle: '',
      ctaPostLoginTitle: '',
    }
  };

  sportCategories: Array<SportCategory> = [];
  competitions: Array<Competition> = [];
  promotionNavigation: Array<PromotionsNavigationGroup> = [];
  id: string;

  uploadImageName: string;
  imageToUpload: File;

  title: FormControl;
  promoKey: FormControl;

  constructor(
    private errorService: ErrorService,
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private promotionsAPIService: PromotionsAPIService,
    private brandService: BrandService,
    private betPackValidationService: BetPackValidationService,
    private freeRideValidationServiceService: FreeRideValidationServiceService,
    private apiClientService: ApiClientService,
  ) {
    this.title = new FormControl('', [Validators.required]);
    this.promoKey = new FormControl('', [Validators.required]);
  }

  /**
   * update property, called by child component eventEmitter
   * @param data
   * @param promotionProperty
   */
  updatePromotion(data, promotionProperty) {
    if (promotionProperty.includes('betPack')) {
      const prop = promotionProperty.split('.');
      this.promotion.betPack[prop[1]] = data;
    } else {
      this.promotion[promotionProperty] = data;
    }
  }

  loadInitialData() {
    // load sport categories to map promotion
    this.promotionsAPIService.getSportCategories()
      .map((data: HttpResponse<SportCategory[]>) => data.body)
      .subscribe((data: SportCategory[]) => {
        this.sportCategories = data;
        this.breadcrumbsData = [{
          label: `Promotions`,
          url: `/promotions`
        }, {
          label: 'Create Promotion',
          url: `/promotions/create/`
        }];
      });

    // load competitions to map promotion
    this.promotionsAPIService.getCompetitions()
      .map((data: HttpResponse<Competition[]>) => data.body)
      .subscribe((competitions: Competition[]) => {
        this.competitions = competitions;
      });

    // load Navigations to map Navigation
    this.apiClientService
      .promotionsNavigationsService()
      .findAllByBrand()
        .map((data: HttpResponse<PromotionsNavigationGroup[]>) => {
        return data.body;
      }).subscribe((navigationGroup: any) => {
        this.promotionNavigation = navigationGroup.filter(navigation => navigation.status);
      });
  }

  prepareToUploadFile(event) {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/png', 'image/jpeg'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"jpeg\" and \"png\".'
      });

      return;
    }

    this.uploadImageName = file.name;
    this.imageToUpload = file;
  }

  /**
   * Upload file on input change event.
   * @param file
   */
  uploadFile(file) {
    const formData = new FormData();
    // uploaded file
    formData.append('file', file);
    return this.promotionsAPIService
      .postNewPromotionImage(this.promotion.id, formData);
  }

  hadleUploadImageClick(event) {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeMainImage() {
    this.uploadImageName = undefined;
    this.imageToUpload = undefined;
  }

  setCategoryId(event: MatSelectChange) {
    this.promotion.categoryId = event.value;
  }

  /**
   * Set all chosen competition ids
   * @param event
   */
  setCompetitionId(event: MatSelectChange): void {
    this.promotion.competitionId = event.value;
  }

  /**
   * Set all chosen Navigation ids
   * @param event
   */
   setNavigationId(event: MatSelectChange): void {
      this.promotion.navigationGroupId = event.value;
    }

  isValidModel() {
    return this.title.valid &&
      this.promoKey.valid &&
      this.isVipLevelValid();
  }

  isVipLevelValid() {
    const vipLevelsData = this.promotion.vipLevelsInput || '';
    return vipLevelsData.length === 0 ||
      (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(',', ''), 10)));
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleDateUpdate(data: DateRange) {
    this.promotion.validityPeriodStart = data.startDate;
    this.promotion.validityPeriodEnd = data.endDate;
  }

  finishPromotionCreation() {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Promotion is Created and Stored.',
      closeCallback() {
        self.router.navigate([`promotions/promotion/${self.promotion.id}`]);
      }
    });
  }

  /**
   * Make PUT request to server to update
   */
  savePromotionChanges() {
    const self = this;
    if (this.promotion.isSignpostingPromotion && (this.promotion.popupTitle === '' || this.promotion.promotionText === '')) {
      this.dialogService.showNotificationDialog({
        title: 'Warning',
        message: `Signposting Promotion is enabled.
         You have to fill ${this.promotion.popupTitle === '' ? 'Popup Title, ' : ''}
         ${this.promotion.promotionText === '' ? 'Popup Text' : ''}`,
      });
    } else {
      if (this.promotion.promotionId !== null && this.promotion.promotionId.length === 0) {
        this.promotion.promotionId = null;
      }
      if (!this.promotion.useDirectFileUrl && this.promotion.directFileUrl) {
        this.promotion.directFileUrl = null;
      }
      // TODO refactor this method
      if (this.betPackValidationService.isBetPackDetailsValid(this.promotion) &&
      this.freeRideValidationServiceService.isFreeRideDetailsValid(this.promotion)) {
        this.promotionsAPIService.postNewPromotion(this.promotion)
          .subscribe(data => {
            this.promotion.id = data.body.id;

            if (this.imageToUpload && !this.promotion.useDirectFileUrl) {
              this.uploadFile(this.imageToUpload)
                .map((uploadResponseData: HttpResponse<Promotion>) => {
                  return uploadResponseData && uploadResponseData.body;
                })
                .subscribe((uploadResponseData: Promotion) => {
                  if (uploadResponseData) {
                    this.finishPromotionCreation();
                  }
                }, (error: HttpErrorResponse) => {
                  self.router.navigate([`promotions/promotion/${self.promotion.id}`]).then(() => {
                    this.errorService.emitError('Promotion Created, but Image not uploaded.' + error.error.message);
                  });
                });
            } else {
              this.finishPromotionCreation();
            }
          });
      }
    }
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');

    this.loadInitialData();
  }

  public onShowToCustomerChange(value: string): void {
    this.promotion.showToCustomer = value;
  }

  /*
  Method to clear the Promtion Bet pack if Mark as enabled is unchecked
  @returns :void */
 clearBpData(): void {
   if (!this.promotion?.betPack?.isBetPack) {
        this.promotion.betPack = {
          'isBetPack': false,
          'bodyText': '',
          'congratsMsg': '',
          'offerId': '',
          'triggerIds': '',
          'betValue': '',
          'lowFundMessage': '',
          'notLoggedinMessage': '',
          'errorMessage': ''
        };
      }
    }

    clearFreeRideData(): void {
      if (!this.promotion?.freeRideConfig?.isFreeRidePromo) {
           this.promotion.freeRideConfig = {
            isFreeRidePromo: false,
            errorMessage: '',
            ctaPreLoginTitle: '',
            ctaPostLoginTitle: ''
           };
         }
       }
}
