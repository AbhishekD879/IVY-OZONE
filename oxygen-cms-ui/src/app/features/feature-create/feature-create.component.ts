import { Component, OnInit } from '@angular/core';
import { Feature } from '../../client/private/models/feature.model';
import { BrandService } from '../../client/private/services/brand.service';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { DateRange } from '../../client/private/models/dateRange.model';

@Component({
  selector: 'app-feature-create',
  templateUrl: './feature-create.component.html',
  styleUrls: ['./feature-create.component.scss']
})
export class FeatureCreateComponent implements OnInit {
  public feature: Feature;

  constructor(
    private brandService: BrandService,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
  ) { }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  ngOnInit(): void {
    this.feature = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      title_brand: '',
      sortOrder: -1,
      heightMedium: -1,
      widthMedium: -1,
      uriMedium: '',
      validityPeriodEnd: '',
      validityPeriodStart: '',
      shortDescription: '',
      title: '',
      vipLevels: [],
      lang: '',
      brand: this.brandService.brand,
      showToCustomer: 'both',
      disabled: false,
      description: '',
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      },
    };
  }

  public getFeature(): Feature {
    return this.feature;
  }

  public isValidFeature(): boolean {
    return !!(this.feature.title &&
              this.feature.title.length > 0 &&
              this.feature.validityPeriodStart && this.feature.validityPeriodStart.length > 0 &&
              this.feature.validityPeriodEnd && this.feature.validityPeriodEnd.length > 0);
  }

  public update(desc: string): void {
    this.feature.description = desc;
  }

  public handleDateUpdate(data: DateRange): void {
    this.feature.validityPeriodStart = data.startDate;
    this.feature.validityPeriodEnd = data.endDate;
  }

  public onShowToCustomerChange(value: string): void {
    this.feature.showToCustomer = value;
  }
}
