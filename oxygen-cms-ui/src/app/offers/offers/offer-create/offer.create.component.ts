import { DateRange } from './../../../client/private/models/dateRange.model';
import { Component, OnInit } from '@angular/core';
import {Offer} from '../../../client/private/models/offer.model';
import {OfferModule} from '../../../client/private/models/offermodule.model';
import {ConfirmDialogComponent} from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import { OfferModuleAPIService } from '../../service/offer-module.api.service';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  selector: 'offer-create-dialog',
  templateUrl: './offer.create.component.html',
  styleUrls: ['./offer.create.component.scss']
})
export class OfferCreateComponent implements OnInit {
  offerModulesData: OfferModule[] = [];
  getDataError: string;
  newOffer: Offer;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private offerModuleAPIService: OfferModuleAPIService,
    private brandService: BrandService
  ) {}

  /**
   * Checks whether offer data are provided correctly
   */
  isValidModel() {
    return this.newOffer.name.length > 0 &&
        this.newOffer.targetUri.length > 0 &&
        this.newOffer.displayTo.length > 0 &&
        this.newOffer.displayFrom.length > 0 &&
        new Date(this.newOffer.displayFrom) < new Date(this.newOffer.displayTo) &&
        this.newOffer.module.length > 0 &&
        this.isVipLevelValid();
  }

  /**
   * Closes modal windo
   */
  closeDialog() {
    this.dialogRef.close();
  }

  /**
   * Check whether vipLevelsInput data is valid
   */
  isVipLevelValid() {
    const vipLevelsData = this.newOffer.vipLevelsInput;
    return vipLevelsData.length === 0 ||
      (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(',', ''), 10)));
  }

    /**
   * Handle data comes from dataTime component, set offer property
   * @param {string} data - date after apllying toISOString();
   * @param {string} propertyToUpdate - offer property to set date to it
   */
  handleDateUpdate(data: DateRange) {
    this.newOffer.displayFrom = data.startDate;
    this.newOffer.displayTo = data.endDate;
  }

  /**
   * Set showOfferTo value of Offer
   * @param variant
   */
  setShowToCustomer(variant) {
    this.newOffer.showOfferTo = variant;
  }

  /**
   * Set model value of Offer
   * @param moduleId
   */
  setModule(moduleId) {
    this.newOffer.module = moduleId;
  }
  /**
   * Initialie offer with default values
   */
  initializeOffer() {
    this.newOffer = {
      // values will be set from form
      vipLevelsInput: '',
      module: '',
      targetUri: '',
      displayTo: '',
      displayFrom: '',
      name: '',
      showOfferTo: 'existing',
      showOfferOn: 'both',
      // default automatically created values
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      sortOrder: 0,
      vipLevels: [],
      brand: this.brandService.brand,
      disabled: false,
      useDirectImageUrl: false,
      directImageUrl: '',
      imageUri: '',
      image: undefined,
      moduleName: '',
      updatedByUserName: '',
      createdByUserName: ''
    };
  }

  ngOnInit() {
    this.initializeOffer();
    this.offerModuleAPIService.getOfferModulesData(false)
      .subscribe((data: any) => {
        this.offerModulesData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }
}
