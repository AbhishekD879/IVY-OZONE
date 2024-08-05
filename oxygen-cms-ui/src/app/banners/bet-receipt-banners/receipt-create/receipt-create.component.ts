import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';

import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';
import { DateRange } from '../../../client/private/models/dateRange.model';

@Component({
  selector: 'app-receipt-create',
  templateUrl: './receipt-create.component.html',
  styleUrls: ['./receipt-create.component.scss']
})
export class ReceiptCreateComponent implements OnInit {

  public banner;
  public type: string;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private router: Router,
  ) {
  }

  ngOnInit() {
    const type = this.router.url.split('/')[3];
    this.type = type.charAt(0).toUpperCase() + type.slice(1);
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
      disabled: false,
      brand: this.brandService.brand,
      uriMedium: undefined,
      uriOriginal: undefined,
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
  }

  public handleDateUpdate(data: DateRange): void {
    this.banner.validityPeriodStart = data.startDate;
    this.banner.validityPeriodEnd = data.endDate;
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public getBanner(): any {
    return this.banner;
  }

  public isValidBanner(): boolean {
    return !!(this.banner.name &&
              this.banner.name.length > 0 &&
              this.banner.validityPeriodStart && this.banner.validityPeriodStart.length > 0 &&
              this.banner.validityPeriodEnd && this.banner.validityPeriodEnd.length > 0);
  }

}

