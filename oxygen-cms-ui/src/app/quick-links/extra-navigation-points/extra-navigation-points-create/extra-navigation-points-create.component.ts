
import { Component, OnInit} from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {
  DateRange,
  ModuleRibbonTab,
  SportCategory,
  Competition,
  ExtraNavigationPoint
} from '../../../client/private/models';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { ExtraNavigationPointsApiService } from '@app/quick-links/extra-navigation-points/extra-navigation-points-api.service';
import { TitleOptions } from '@app/client/private/models/navigationpoint.model';


@Component({
  templateUrl: './extra-navigation-points-create.component.html'
})
export class ExtraNavigationPointsCreateComponent implements OnInit {

  public form: FormGroup;
  public extraNavigationPoint: ExtraNavigationPoint;
  public homeTabs: ModuleRibbonTab[] = [];
  public sportCategories: SportCategory[] = [];
  public bigCompetitions: Competition[] = [];
  public titleOptions: TitleOptions[] = [
    {
      key: 'bgImage', 
      value: 'Bg Image Right Alignment', 
      config: {
        title: { maxLength: 20 },
        description: { maxLength: 27 },
        shortDescription: { coral: { maxLength: 64 }, lads: { maxLength: 64 } }
      }
    }
  ];

  constructor(
    private extraNavigationPointsApiService: ExtraNavigationPointsApiService,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.maxLength(27)]),
      shortDescription: new FormControl(''),      
      homeTabs: new FormControl('', []),
      sportCategories: new FormControl('', []),
      competitions: new FormControl('', []),
      featureTag: new FormControl('', []),
      bgImageUrl: new FormControl('',[]),
    });

    this.extraNavigationPoint = {
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
      bgAlignmentEnabled : true,
      enabled: false,
      targetUri: '',
      title: '',
      description: '',
      shortDescription:'',
      validityPeriodEnd: '',
      validityPeriodStart: '',
      featureTag: ''
    };

    this.extraNavigationPointsApiService.getLandingPages()
      .subscribe(([homeTabs, sportCategories, competitions]: [ModuleRibbonTab[], SportCategory[], Competition[]]) => {
        this.homeTabs = homeTabs;
        this.sportCategories = sportCategories;
        this.bigCompetitions = competitions;
      });
    this.changePreferance(); 
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public handleDateUpdate(data: DateRange): void {
    this.extraNavigationPoint.validityPeriodStart = data.startDate;
    this.extraNavigationPoint.validityPeriodEnd = data.endDate;
  } 

  changePreferance() {
    this.extraNavigationPoint.bgAlignmentEnabled = !this.extraNavigationPoint.bgAlignmentEnabled;
    if (this.extraNavigationPoint.bgAlignmentEnabled) {
      this.extraNavigationPoint.competitionId = [];
      this.extraNavigationPoint.categoryId = [];
      this.form.controls.title.setValidators([Validators.maxLength(this.titleOptions[0].config.title.maxLength)]);
      this.form.controls.title.updateValueAndValidity();
      this.form.controls.shortDescription.setValidators([Validators.maxLength(this.titleOptions[0].config.shortDescription.lads.maxLength)]);
      this.form.controls.shortDescription.updateValueAndValidity();
      this.form.controls.bgImageUrl.enable();
      this.form.controls.description.enable();
     
    } else {
      this.form.controls.title.setValidators([Validators.maxLength(25)]);
      this.form.controls.title.updateValueAndValidity();
      this.form.controls.shortDescription.setValidators([Validators.maxLength(45)]);
      this.form.controls.shortDescription.updateValueAndValidity();  
      this.form.controls.bgImageUrl.disable();
      this.form.controls.bgImageUrl.setValue("");
      this.form.controls.description.disable();
      this.form.controls.description.setValue("");
    }
  }

  public isMaxLengthReached(name: string): boolean {
    const control = this.form.controls[name];
    const isTouched = control && (control.dirty || control.touched);

    return isTouched && control.errors && control.errors.maxlength;
  }
}


