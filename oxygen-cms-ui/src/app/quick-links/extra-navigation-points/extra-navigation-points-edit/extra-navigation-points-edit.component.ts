import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { forkJoin } from 'rxjs/observable/forkJoin';

import { DialogService } from '../../../shared/dialog/dialog.service';
import {
  DateRange,
  Breadcrumb,
  ModuleRibbonTab,
  SportCategory,
  Competition,
  ExtraNavigationPoint
} from '../../../client/private/models';
import { AppConstants } from '@app/app.constants';
import { ExtraNavigationPointsApiService } from '@app/quick-links/extra-navigation-points/extra-navigation-points-api.service';
import { TitleOptions } from '@app/client/private/models/navigationpoint.model';

@Component({
  templateUrl: './extra-navigation-points-edit.component.html',
  providers: [
    DialogService
  ]
})
export class ExtraNavigationPointsEditComponent implements OnInit {

  public extraNavigationPoint: ExtraNavigationPoint;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public homeTabs: ModuleRibbonTab[] = [];
  public sportCategories: SportCategory[] = [];
  public bigCompetitions: Competition[] = [];
  public isRevert = false;
  @ViewChild('actionButtons') actionButtons;
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
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private ExtraNavigationPointsApiService: ExtraNavigationPointsApiService,
    private dialogService: DialogService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      const landingPages$ = this.ExtraNavigationPointsApiService.getLandingPages();
      const extraNavigationPoint$ = this.ExtraNavigationPointsApiService.getSingleNavigationPoint(params['id'])
        .map((data: HttpResponse<ExtraNavigationPoint>) => data.body);

      forkJoin(landingPages$, extraNavigationPoint$)
        .subscribe(([[homeTabs, sportCategories, competitions], extraNavigationPoint]: [[ModuleRibbonTab[], SportCategory[], Competition[]],
          ExtraNavigationPoint]) => {
          this.homeTabs = homeTabs;
          this.sportCategories = sportCategories;
          this.bigCompetitions = competitions;
          this.extraNavigationPoint = extraNavigationPoint;

          this.form = new FormGroup({
            title: new FormControl('', [Validators.required]),
            targetUri: new FormControl('', [Validators.required]),
            description: new FormControl('', [Validators.maxLength(27)]),
            shortDescription : new FormControl (''),
            homeTabs: new FormControl('', []),
            sportCategories: new FormControl('', []),
            competitions: new FormControl('', []),
            featureTag: new FormControl('', []),
            bgImageUrl: new FormControl('',[]),
            bgAlignmentEnabled : new FormControl('',[])
          });
          this.changebgAlignPreferance({checked : extraNavigationPoint.bgAlignmentEnabled });
          this.formBreadcrumbs();
        });
    });
  }

  private formBreadcrumbs(): void {
    this.breadcrumbsData = [{
      label: 'Special Super Buttons',
      url: '/quick-links/extra-navigation-points'
    }, {
      label: this.extraNavigationPoint.title,
      url: `/quick-links/extra-navigation-points/${this.extraNavigationPoint.id}`
    }];
  }

  private save(): void {
    this.ExtraNavigationPointsApiService.updateNavigationPoint(this.extraNavigationPoint)
      .map((data: HttpResponse<ExtraNavigationPoint>) => data.body)
      .subscribe((data: ExtraNavigationPoint) => {
        const self = this;
        this.extraNavigationPoint = data;
        this.formBreadcrumbs();
        this.actionButtons.extendCollection(this.extraNavigationPoint);
        this.dialogService.showNotificationDialog({
          title: AppConstants.SPECIAL_SUPER_BUTTON_SAVING,
          message: AppConstants.SPECIAL_SUPER_BUTTON_SAVED,
          closeCallback() {
            self.router.navigate([`/quick-links/extra-navigation-points`]);
          }
        });
      });
  }

  private revert(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.ExtraNavigationPointsApiService.getSingleNavigationPoint(params['id'])
        .map((data: HttpResponse<ExtraNavigationPoint>) => data.body)
        .subscribe((extraNavigationPoint: ExtraNavigationPoint) => {
          this.extraNavigationPoint = extraNavigationPoint;
        });
    });
    this.isRevert = true;
  }

  private remove(): void {
    this.ExtraNavigationPointsApiService.deleteNavigationPoint(this.extraNavigationPoint.id)
      .subscribe(() => {
        this.router.navigate(['/quick-links/extra-navigation-points/']);
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public handleDateUpdate(data: DateRange): void {
    this.extraNavigationPoint.validityPeriodStart = data.startDate;
    this.extraNavigationPoint.validityPeriodEnd = data.endDate;
  } 

  public isMaxLengthReached(name: string): boolean {
    const control = this.form.controls[name];
    const isTouched = control && (control.dirty || control.touched);

    return isTouched && control.errors && control.errors.maxlength;
  }
  
  changebgAlignPreferance(event) {
    this.extraNavigationPoint.bgAlignmentEnabled = event.checked;
    if (event.checked) {
      this.extraNavigationPoint.competitionId = [];
      this.extraNavigationPoint.categoryId = [];
      this.form.controls.title.setValidators([Validators.maxLength(this.titleOptions[0].config.title.maxLength)]);
      this.form.controls.shortDescription.setValidators([Validators.maxLength(this.titleOptions[0].config.shortDescription.lads.maxLength)]);
      this.form.controls.bgImageUrl.enable();
      this.form.controls.bgImageUrl.setValidators([Validators.required]);
      this.form.controls.description.enable();
      this.form.controls.title.updateValueAndValidity();
    } else {
      this.form.controls.bgImageUrl.disable();
      this.form.controls.bgImageUrl.setValue("");
      this.form.controls.title.setValidators([Validators.maxLength(25)]);
      this.form.controls.shortDescription.setValidators([Validators.maxLength(45)]);
      this.form.controls.title.updateValueAndValidity();
      this.form.controls.description.disable();
      this.form.controls.description.setValue("");
    }
  }

  /*
  *Disables save button based upon the return type
   */
  public validationHandler(): boolean {
    return this.form.valid;
  } 
}
