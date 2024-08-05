import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Football3DBanner } from '../../../client/private/models/football3dbanner.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';
import { DateRange } from '../../../client/private/models/dateRange.model';

@Component({
  selector: 'app-banners-create',
  templateUrl: './banners-create.component.html',
  styleUrls: ['./banners-create.component.scss']
})
export class BannersCreateComponent implements OnInit {

  public banner: Football3DBanner;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {
  }

  ngOnInit() {
    this.banner = {
      id: undefined,
      updatedBy: undefined,
      updatedAt: undefined,
      createdBy: undefined,
      createdAt: undefined,
      sortOrder: undefined,
      validityPeriodEnd: '',
      validityPeriodStart: '',
      description: '',
      targetUri: '',
      name: '',
      displayDuration: 5,
      disabled: false,
      brand: this.brandService.brand,
      uriMedium: undefined,
      uriOriginal: undefined,
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      updatedByUserName: '',
      createdByUserName: ''
    };
  }

  public handleDateUpdate(data: DateRange): void {
    this.banner.validityPeriodStart = data.startDate;
    this.banner.validityPeriodEnd = data.endDate;
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public getFootballBanner(): Football3DBanner {
    return this.banner;
  }

  public isValidBanner(): boolean {
    return !!(this.banner.name &&
              this.banner.name.length > 0 &&
              this.banner.validityPeriodStart && this.banner.validityPeriodStart.length > 0 &&
              this.banner.validityPeriodEnd && this.banner.validityPeriodEnd.length > 0);
  }

}
