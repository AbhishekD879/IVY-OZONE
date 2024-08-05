import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {
  NavigationPoint,
  DateRange,
  ModuleRibbonTab,
  SportCategory,
  Competition
} from '../../../client/private/models';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { NavigationPointsApiService } from '../navigation-points.api.service';

@Component({
  templateUrl: './navigation-points-create.component.html'
})
export class NavigationPointsCreateComponent implements OnInit {

  public form: FormGroup;
  public navigationPoint: NavigationPoint;
  public homeTabs: ModuleRibbonTab[] = [];
  public sportCategories: SportCategory[] = [];
  public bigCompetitions: Competition[] = [];

  constructor(
    private navigationPointsApiService: NavigationPointsApiService,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required, Validators.maxLength(25)]),
      targetUri: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.maxLength(45)]),
      homeTabs: new FormControl('', []),
      sportCategories: new FormControl('', []),
      competitions: new FormControl('', [])
    });

    this.navigationPoint = {
      id: '',
      brand: this.brandService.brand,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',

      homeTabs: [],
      categoryId: [],
      competitionId: [],
      enabled: false,
      targetUri: '',
      title: '',
      description: '',
      ctaAlignment: '',
      shortDescription: '',
      themes: '',
      validityPeriodEnd: '',
      validityPeriodStart: '',
      inclusionList: [],
      exclusionList: [],
      universalSegment: true
    };

    this.navigationPointsApiService.getLandingPages()
      .subscribe(([homeTabs, sportCategories, competitions]: [ModuleRibbonTab[], SportCategory[], Competition[]]) => {
        this.homeTabs = homeTabs;
        this.sportCategories = sportCategories;
        this.bigCompetitions = competitions;
      });
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public handleDateUpdate(data: DateRange): void {
    this.navigationPoint.validityPeriodStart = data.startDate;
    this.navigationPoint.validityPeriodEnd = data.endDate;
  }

  public isMaxLengthReached(name: string): boolean {
    const control = this.form.controls[name];
    const isTouched = control && (control.dirty || control.touched);

    return isTouched && control.errors && control.errors.maxlength;
  }
}
