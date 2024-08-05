import { Component, Inject, OnInit } from '@angular/core';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Banner } from '../../../client/private/models/banner.model';
import { DateRange } from '../../../client/private/models/dateRange.model';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  selector: 'banner-create-dialog',
  templateUrl: './banner.create.component.html',
  styleUrls: ['./banner.create.component.scss']
})
export class BannerCreateComponent implements OnInit {
  newBanner: Banner;
  bannersData: Banner[];

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
  ) {}

  isValidModel() {
    return this.newBanner.imageTitle.length > 0 &&
      this.newBanner.validityPeriodStart.length > 0 &&
      this.newBanner.validityPeriodEnd.length > 0 &&
      this.newBanner.showToCustomer && this.newBanner.showToCustomer.length > 0 &&
      this.isNameUniq(this.newBanner.imageTitle);
  }

  isVipLevelValid() {
    const vipLevelsData = this.newBanner.vipLevelsInput || '';
    return vipLevelsData.length === 0 ||
      (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(',', ''), 10)));
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleDateUpdate(data: DateRange) {
    this.newBanner.validityPeriodStart = data.startDate;
    this.newBanner.validityPeriodEnd = data.endDate;
  }

  /**
   * group name should be unique
   * @param bannerName
   */
  isNameUniq(bannerName: string) {
    return this.data.bannersData.every(item => item.imageTitle.toLowerCase() !== bannerName.toLowerCase());
  }

  closeDialog() {
    this.dialogRef.close();
  }

  ngOnInit() {
    this.newBanner = {
      // values will be set from from
      imageTitle: '',
      validityPeriodStart: '',
      validityPeriodEnd: '',
      vipLevelsInput: '',
      showToCustomer: 'both',

      // default automatically created values
      id: undefined,
      alt: undefined,
      brand: this.brandService.brand,
      categoryId: undefined,
      createdAt: undefined,
      createdBy: undefined,
      desktopHeightMedium: undefined,
      desktopTargetUri: undefined,
      desktopUriMedium: undefined,
      desktopUriSmall: undefined,
      desktopWidthMedium: undefined,
      disabled: undefined,
      imageTitle_brand: undefined,
      inApp: undefined,
      lang: undefined,
      sortOrder: undefined,
      targetUri: undefined,
      updatedAt: undefined,
      updatedBy: undefined,
      uriMedium: undefined,
      uriSmall: undefined,
      desktopEnabled: undefined,
      desktopInApp: undefined,
      enabled: undefined,
      desktopFilename: undefined,
      filename: undefined,
      vipLevels: undefined,
      createdByUserName: undefined,
      updatedByUserName: undefined
    };
  }

  public onShowToCustomerChange(value: string): void {
    this.newBanner.showToCustomer = value;
  }
}
