import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { MaintenancePage } from '../../client/private/models/maintenancepage.model';
import { ConfirmDialogComponent } from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../client/private/services/brand.service';
import { DateRange } from '../../client/private/models/dateRange.model';

@Component({
  selector: 'add-maintenance-page',
  templateUrl: './add-maintenance-page.component.html',
  styleUrls: ['./add-maintenance-page.component.scss']
})
export class AddMaintenancePageComponent implements OnInit {
  public form: FormGroup;
  public maintenancePage: MaintenancePage;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.maintenancePage = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      validityPeriodEnd: '',
      validityPeriodStart: '',
      name: '',
      desktop: false,
      tablet: false,
      mobile: false,
      targetUri: '',
      brand: this.brandService.brand,
      uriMedium: '',
      uriOriginal: '',
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
    this.form = new FormGroup({
      pageName: new FormControl('', [Validators.required]),
      pageTargetUri: new FormControl('', [Validators.required])
    });
  }

  isValidForm(): boolean {
    return this.maintenancePage.validityPeriodEnd &&
           this.maintenancePage.validityPeriodEnd.length > 0 &&
           this.maintenancePage.validityPeriodStart &&
           this.maintenancePage.validityPeriodStart.length > 0;
  }

  handleDateUpdate(data: DateRange) {
    this.maintenancePage.validityPeriodStart = data.startDate;
    this.maintenancePage.validityPeriodEnd = data.endDate;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  getNewMaintenancePage(): MaintenancePage {
    this.maintenancePage.name = this.form.value.pageName;
    this.maintenancePage.targetUri = this.form.value.pageTargetUri;

    return this.maintenancePage;
  }
}
