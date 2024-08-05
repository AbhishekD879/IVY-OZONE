import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Offer } from '../../../../client/private/models/offer.model';
import { OfferModule } from '../../../../client/private/models/offermodule.model';
import { OfferModuleAPIService } from '../../../service/offer-module.api.service';
import { OffersAPIService } from '../../../service/offers.api.service';
import { DialogService } from '../../../../shared/dialog/dialog.service';
import { HttpResponse } from '@angular/common/http';
import { Breadcrumb } from '../../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'offer-page',
  templateUrl: './offer.page.component.html',
  styleUrls: ['./offer.page.component.scss']
})
export class OfferPageComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  offerModulesData: OfferModule[] = [];
  getDataError: string;
  offer: Offer;
  id: string;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private offerModuleAPIService: OfferModuleAPIService,
    private offersAPIService: OffersAPIService
  ) {}

  /**
   * Checks whether offer data are provided correctly
   */
  isValidModel(offer: Offer): boolean {
    const vipLevelsData = offer.vipLevelsInput;
    return offer.name.length > 0 &&
           offer.targetUri.length > 0 &&
           offer.displayTo.length > 0 &&
           offer.displayFrom.length > 0 &&
           offer.module.length > 0 &&
           (vipLevelsData.length === 0 || (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(',', ''), 10))));
  }

    /**
   * Handle data comes from dataTime component, set offer property
   * @param {string} data - date after apllying toISOString();
   */
  handleDateUpdate(data): void {
    this.offer.displayFrom = data.startDate;
    this.offer.displayTo = data.endDate;
  }

    /**
   * Upload file on input change event.
   * @param event
   */
  uploadFile(formData: FormData): void {
    this.offersAPIService
        .postNewOfferImage(this.offer.id, formData)
        .subscribe((data: any) => {
          this.offer.image = data.body.image;

          this.snackBar.open('Image Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  /**
   * Reset chosen image
   */
  removeFile() {
    this.offersAPIService.removeOfferImage(this.offer.id)
    .subscribe((data: any) => {
      this.offer.image.filename = '';

      this.snackBar.open('Image Was Removed.', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  /**
   * Reset changes appplied to offer
   */
  revertOfferChanges() {
    this.loadInitialData();
  }

    /**
   * Send DELETE API request
   * @param {Offer} offer
   */
  sendRemoveRequest(offer: Offer) {
    this.offersAPIService.deleteOffer(offer.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Offer is Removed.'
        });
        this.router.navigate(['/offers/offers']);
      });
  }

  /**
   * handle deleting offer
   * @param {Offer} offer
   */
  removeOffer() {
    this.sendRemoveRequest(this.offer);
  }

  /**
   * Make PUT request to server to update
   */
  saveOfferChanges() {
    this.offersAPIService.putOfferChanges(this.offer)
      .map((response: HttpResponse<Offer>) => {
        return response.body;
      })
      .subscribe((data: Offer) => {
        this.offer = data;
        this.actionButtons.extendCollection(this.offer);
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'Offer Changes are Saved.'
        });
      });
  }

  public getLink(): string {
    return `/offers/offer-modules/${this.offer.module}`;
  }

  /**
   * Load offer data
   */
  loadOfferData() {
    this.offersAPIService.getSingleOffersData(this.id)
      .subscribe((data: HttpResponse<Offer>) => {
        this.offer = data.body;
        this.breadcrumbsData = [{
          label: `Offers`,
          url: `/offers/offers`
        }, {
          label: this.offer.name,
          url: `/offers/offers/${this.offer.id}`
        }];
      }, error => {
        this.getDataError = error.message;
      });
  }

  /**
   * Load initial data to initialize component
   */
  loadInitialData() {
    this.offerModuleAPIService.getOfferModulesData()
      .subscribe((data: HttpResponse<OfferModule[]>) => {
        this.offerModulesData = data.body;
      }, error => {
        this.getDataError = error.message;
      });

    this.loadOfferData();
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeOffer();
        break;
      case 'save':
        this.saveOfferChanges();
        break;
      case 'revert':
        this.revertOfferChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public onShowToCustomerChange(value: string): void {
    this.offer.showOfferTo = value;
  }

  public onShowOnCustomerChange(value: string): void {
    this.offer.showOfferOn = value;
  }
}
