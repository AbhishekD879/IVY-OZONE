import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { HRQuickLink } from '@app/client/private/models/hrquicklink.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { DateRange } from '@app/client/private/models/dateRange.model';

@Component({
  templateUrl: './hr-quick-links-create.component.html',
  styleUrls: ['./hr-quick-links-create.component.scss']
})
export class HrQuickLinksCreateComponent implements OnInit {

  public form: FormGroup;
  public hrQuickLink: HRQuickLink;
  public raceTypes: Array<string> = ['horse racing', 'greyhound racing'];
  public linkTypes: Array<string> = ['url', 'selection'];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.hrQuickLink = {
      id: '',
      brand: this.brandService.brand,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      body: '',
      disabled: false,
      heightMedium: 0,
      lang: '',
      linkType: '',
      raceType: '',
      sortOrder: 0,
      target: '',
      title: '',
      uriMedium: '',
      validityPeriodEnd: '',
      validityPeriodStart: '',
      widthMedium: 0,
      filename: {
        filename: '',
        path: '',
        size: 0,
        filetype: '',
      }
    };
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      body: new FormControl('', [Validators.required]),
      raceType: new FormControl('', [Validators.required]),
      linkType: new FormControl('', [Validators.required]),
      target: new FormControl('', [Validators.required])
    });
  }

  getHRQuickLink(): HRQuickLink {
    const form = this.form.value;
    this.hrQuickLink.title = form.title;
    this.hrQuickLink.body = form.body;
    this.hrQuickLink.target = form.target;
    return this.hrQuickLink;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  onRaceTypeChanged(): void {
    this.hrQuickLink.raceType = this.form.value.raceType;
  }

  onLinkTypeChanged(): void {
    this.hrQuickLink.linkType = this.form.value.linkType;
  }

  handleDateUpdate(data: DateRange) {
    this.hrQuickLink.validityPeriodStart = data.startDate;
    this.hrQuickLink.validityPeriodEnd = data.endDate;
  }
}
