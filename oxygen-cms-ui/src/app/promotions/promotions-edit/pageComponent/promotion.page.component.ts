import { TinymceComponent } from './../../../shared/tinymce/tinymce.component';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PromotionsAPIService } from '../../service/promotions.api.service';
import { Promotion } from '../../../client/private/models/promotion.model';
import { SportCategory } from '../../../client/private/models/sportcategory.model';
import { Competition } from '../../../client/private/models/competition.model';
import { DialogService } from '../../../shared/dialog/dialog.service';
import { DateRange } from '../../../client/private/models/dateRange.model';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { MatSelectChange } from '@angular/material/select';
import { BetPackValidationService } from '@app/promotions/service/bet-pack-validation.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { FreeRideValidationServiceService } from '@app/promotions/service/free-ride-validation-service.service';
import { PromotionsNavigationGroup } from '@app/client/private/models/promotions-navigation.model';
import * as _ from 'lodash';

// @ts-ignore
declare var tinymce: any;

@Component({
  selector: 'promotion-page',
  templateUrl: './promotion.page.component.html',
  styleUrls: ['./promotion.page.component.scss']
})
export class PromotionPageComponent implements OnInit {
  sportCategories: SportCategory[] = [];
  competitions: Array<Competition> = [];
  promotionNavigation: Array<PromotionsNavigationGroup> = [];
  promotion: Promotion;
  id: string;
  public breadcrumbsData: Breadcrumb[];

  @ViewChild('actionButtons') actionButtons;
  @ViewChild('description') editor: TinymceComponent;
  @ViewChild('htmlMarkup') hEditor: TinymceComponent;
  @ViewChild('promotionText') tEditor: TinymceComponent;
  @ViewChild('congrats') cEditor: TinymceComponent;

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private promotionsAPIService: PromotionsAPIService,
    private betPackValidationService: BetPackValidationService,
    private freeRideValidationServiceService: FreeRideValidationServiceService,
    private apiClientService: ApiClientService,
    private errorService: ErrorService
  ) {
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

  /**
   * load current promotion data
   */
  loadPromotion() {
    this.promotionsAPIService.getSinglePromotionData(this.id)
      .subscribe((data: any) => {
        this.promotion = _.extend(data.body, _.pick(this.promotion, 'disabled', 'isSignpostingPromotion',
          'categoryId', 'title', 'promoKey', 'shortDescription',
          'promotionId', 'openBetId',
          'description', 'eventLevelFlag', 'marketLevelFlag',
          'overlayBetNowUrl', 'vipLevels', 'vipLevelsInput', 'requestId', 'showToCustomer', 'htmlMarkup',
          'promotionText', 'betPack', 'validityPeriodEnd', 'validityPeriodStart', 'popupTitle'));
          this.breadcrumbsData = [{
          label: `Promotions`,
          url: `/promotions`
        }, {
          label: this.promotion.title,
          url: `/promotions/edit/${this.promotion.id}`
        }];
        if (this.editor && this.hEditor) {
          this.editor.update(this.promotion.description);
          this.hEditor.update(this.promotion.htmlMarkup);
        }
        if (this.tEditor) {
          this.tEditor.update(this.promotion.promotionText);
        }
        if (this.cEditor) {
          this.cEditor.update(this.promotion.betPack.congratsMsg);
        }
      }, error => {
        this.router.navigate(['/promotions']);
      });
  }

  loadInitialData() {
    // load current promotion data
    this.loadPromotion();

    // load sport categories to map promotion
    this.promotionsAPIService
      .getSportCategories()
      .subscribe((data: any) => {
        this.sportCategories = data.body;
      });

    // load competitions to map promotion
    this.promotionsAPIService
      .getCompetitions()
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

  /**
   * Upload file on input change event.
   * @param event
   */
  uploadFile(formData: FormData): void {
    this.promotionsAPIService.postNewPromotionImage(this.promotion.id, formData)
      .subscribe((data: any) => {
        // update uploaded image name to show inside input
        this.promotion.uriMedium = data.body.uriMedium;
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'New Image is Uploaded.'
        });
      });
  }

  removeFile() {
    this.promotionsAPIService
      .removePromotionImage(this.promotion.id)
      .subscribe((data: any) => {
        this.promotion.uriMedium = '';
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Image is Removed.'
        });
      });
  }

  hadleUploadImageClick(event) {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  revertPromotionChanges() {
    this.loadInitialData();
  }

  setCategoryId(event: MatSelectChange): void {
    this.promotion.categoryId = event.value;
  }

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

  /**
   * Send DELETE API request
   * @param {Promotion} promotion
   */
  removePromotion() {
    this.promotionsAPIService.deletePromotion(this.promotion.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Promotion is Removed.'
        });
        this.router.navigate(['/promotions']);
      });
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

  /**
   * Make PUT request to server to update
   */
  savePromotionChanges() {
    if (this.promotion.isSignpostingPromotion && (this.promotion.popupTitle === undefined ||
      this.promotion.popupTitle === '' || this.promotion.promotionText === '')) {
      this.dialogService.showNotificationDialog({
        title: 'Warning',
        message: `Signposting Promotion is enabled.
          You have to fill ${this.promotion.popupTitle === undefined || this.promotion.popupTitle === '' ?
            'Popup Title, ' : ''}
          ${this.promotion.promotionText === '' ? 'Popup Text' : ''}`,
      });
    } else {
      if (this.promotion.promotionId !== null && this.promotion.promotionId.length === 0) {
        this.promotion.promotionId = null;
      }
      if (this.promotion.useDirectFileUrl && this.promotion.uriMedium) {
        this.promotion.uriMedium = null;
      } else if (!this.promotion.useDirectFileUrl && this.promotion.directFileUrl) {
        this.promotion.directFileUrl = null;
      }
      if (this.betPackValidationService.isBetPackDetailsValid(this.promotion) &&
      this.freeRideValidationServiceService.isFreeRideDetailsValid(this.promotion)) {
        this.promotionsAPIService
          .putPromotionChanges(this.promotion)
          .map((response) => {
            return response.body;
          })
          .subscribe((data: any) => {
            this.promotion = data;
            this.actionButtons.extendCollection(this.promotion);
            this.dialogService.showNotificationDialog({
              title: 'Upload Completed',
              message: 'Promotion Changes are Saved.'
            });
          },(error: HttpErrorResponse) => {
            this.router.navigate([`promotions/promotion/${this.promotion.id}`]).then(() => {
              this.errorService.emitError(error.error.message);
            });
          });
      }
    }
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');

    this.loadInitialData();
  }

  public isValidForm(promotion: Promotion): boolean {
    return promotion.title && promotion.title.length > 0;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removePromotion();
        break;
      case 'save':
        this.savePromotionChanges();
        break;
      case 'revert':
        this.revertPromotionChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
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
