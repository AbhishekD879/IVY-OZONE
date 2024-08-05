import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { forkJoin } from 'rxjs/observable/forkJoin';

import { DialogService } from '../../../shared/dialog/dialog.service';
import {
  NavigationPoint,
  DateRange,
  Breadcrumb,
  ModuleRibbonTab,
  SportCategory,
  Competition
} from '../../../client/private/models';
import { NavigationPointsApiService } from '../navigation-points.api.service';
import { ISegmentModel } from '@app/client/private/models/segment.model'; 
import { AppConstants, CSPSegmentLSConstants,Brand } from '@app/app.constants';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ThemeArray, TitleOptions } from '@root/app/client/private/models/navigationpoint.model';

@Component({
  templateUrl: './navigation-points-edit.component.html',
  providers: [
    DialogService
  ]
})
export class NavigationPointsEditComponent implements OnInit {
  public themesArray: ThemeArray[] = [];
  public titleOptions: TitleOptions[] = [
    {
      key: 'center',
      value: 'Center Alignment',
      config: {
        title: { maxLength: 40 },
        description: { maxLength: 65 }
      }
    },
    {
      key: 'right', 
      value: 'Right Alignment', 
      config: {
        title: { maxLength: 12 },
        description: { maxLength: 25 },
        shortDescription: { coral: { maxLength: 38 }, lads: { maxLength: 42 } }
      }
    },
    
  ];
  public navigationPoint: NavigationPoint;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public homeTabs: ModuleRibbonTab[] = [];
  public sportCategories: SportCategory[] = [];
  public bigCompetitions: Competition[] = [];
  public isRevert = false;
  segmentsList: ISegmentModel;
  isSegmentValid: boolean = false;
  alignment: string= 'center';
  isBrandLads: boolean = false;
  typeAddEdit: string = '';
  @ViewChild('actionButtons') actionButtons;
  bgImage : string;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private navigationPointsApiService: NavigationPointsApiService,
    private dialogService: DialogService,
    private segmentStoreService: SegmentStoreService,
    private brandService:BrandService,
    private globalLoaderService:GlobalLoaderService
  ) {  this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;

    this.isBrandLads && this.titleOptions.push(
      {
        key: 'bgImage', 
        value: 'Bg Image Right Alignment', 
        config: {
          title: { maxLength: 20 },
          description: { maxLength: 27 },
          shortDescription: { coral: { maxLength: 64 }, lads: { maxLength: 64 } }
        }
      }
    )
  
    this.activatedRoute.params.subscribe((params: Params) => {
      const landingPages$ = this.navigationPointsApiService.getLandingPages();
      if (!params['id']) {
        this.typeAddEdit = "ADD";
        this.navigationPoint = {
          message: null,
          categoryId: [],
          competitionId: [],
          homeTabs: [""],
          enabled: false,
          targetUri: "",
          title: "",
          bgImageUrl: "",
          description: "",
          validityPeriodEnd: "",
          validityPeriodStart: "",
          shortDescription: "",
          ctaAlignment: "",
          themes: null,
          id: "",
          brand: "",
          createdBy: "",
          createdAt: '',
          updatedBy: "",
          updatedAt: "",
          updatedByUserName: "",
          createdByUserName: "",
          inclusionList: [],
          exclusionList: [],
          universalSegment: true
        }
        landingPages$
          .subscribe(([homeTabs, sportCategories, competitions]: [ModuleRibbonTab[], SportCategory[], Competition[]]) => {
            this.homeCatTabs(homeTabs, sportCategories, competitions);
          });
        this.navigationPoint['ctaAlignment'] = this.alignment;
        this.initAddEditButton();
      }
      else {
        this.typeAddEdit = "EDIT"
        const navigationPoint$ = this.navigationPointsApiService.getSingleNavigationPoint(params['id'])
          .map((data: HttpResponse<NavigationPoint>) => data.body);
        forkJoin(landingPages$, navigationPoint$)
          .subscribe(([[homeTabs, sportCategories, competitions], navigationPoint]: [[ModuleRibbonTab[], SportCategory[], Competition[]],
            NavigationPoint]) => {
            this.homeCatTabs(homeTabs, sportCategories, competitions);
            this.navigationPoint = navigationPoint;
            this.navigationPoint.ctaAlignment = this.navigationPoint.ctaAlignment || 'center';
            this.alignment = this.navigationPoint.ctaAlignment || 'center';
           
            this.initAddEditButton();
          });
      }
    });
  }

  getCTAalignment (event) {
    const themesArray =[];
    if(event.value === 'bgImage' && this.isBrandLads) {
      this.navigationPoint.competitionId = [];
      this.navigationPoint.categoryId = [];
      this.form.controls.bgImageUrl.setValidators([Validators.required]);
      let themesCount:number = 1;
      for (let i = 1; i <= themesCount ; i++) {
        themesArray.push({ key: `theme_${i}`, value: `theme ${i}` });
      }
    } else {
      let themesCount:number =  this.isBrandLads ? 4 : 6;
      for (let i = 1; i <= themesCount ; i++) {
         themesArray.push({ key: `theme_${i}`, value: `theme ${i}` })
      }
    }
    this.themesArray = themesArray;
    this.form.controls.bgImageUrl.setValue("");
    this.form.controls.bgImageUrl.setValidators([]);
  }
   /**
   * gets hometabs,sportcategories,bigcompetitions from respective models
   */
  private homeCatTabs(homeTabs: ModuleRibbonTab[], sportCategories: SportCategory[], competitions: Competition[]) {
    this.homeTabs = homeTabs;
    this.sportCategories = sportCategories;
    this.bigCompetitions = competitions;
  }
   /**
   * updated the super button page with center and right alignment
   */
  private initAddEditButton() {

    const defaultFormConfig = this.titleOptions.find(option => option.key === this.alignment);
    this.form = new FormGroup({
      title: new FormControl('', [Validators.required, Validators.maxLength(defaultFormConfig.config.title.maxLength)]),
      bgImageUrl : new FormControl('',[]),
      targetUri: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.maxLength(defaultFormConfig.config.description.maxLength)]),
      homeTabs: new FormControl('', []),
      sportCategories: new FormControl('', []),
      competitions: new FormControl('', []),
      ctaAlignment: new FormControl(this.alignment,[Validators.required]),
      shortDescription: new FormControl(''),
      themes: new FormControl('',[Validators.required])
    });
    this.form.controls.ctaAlignment.valueChanges.subscribe((value) => {
      this.form.patchValue({
        shortDescription: ''
      })
      const formConfig = this.titleOptions.find(option => option.key === value);
      this.alignment = value;
      this.bgImage = this.navigationPoint.bgImageUrl;
      this.updateControl('title');
      this.updateControl('description');
      this.updateControl('shortDescription');

      this.form.controls.title.setValidators([Validators.maxLength(formConfig.config.title.maxLength)]);
      this.form.controls.title.updateValueAndValidity();

      this.form.controls.description.setValidators([Validators.maxLength(formConfig.config.description.maxLength)]);
      this.form.controls.description.updateValueAndValidity();

      if (formConfig.config.shortDescription) {
        if (!this.isBrandLads) {
          this.form.controls.shortDescription.setValidators([Validators.maxLength(formConfig.config.shortDescription.coral.maxLength)]);
          this.form.controls.shortDescription.updateValueAndValidity();
        } else {
          this.form.controls.shortDescription.setValidators([Validators.maxLength(formConfig.config.shortDescription.lads.maxLength)]);
          this.form.controls.shortDescription.updateValueAndValidity();
        }
      }
   

      this.getCTAalignment ({value})
    });

    this.segmentsList = {
      exclusionList: this.navigationPoint?.exclusionList,
      inclusionList: this.navigationPoint?.inclusionList,
      universalSegment: this.navigationPoint?.universalSegment
    };
    this.formBreadcrumbs();
    this.globalLoaderService.hideLoader()
    this.navigationPoint['brand'] = this.brandService.brand;
  }

  updateControl(name: string) {
    this.form.controls[name].clearValidators();
    this.form.controls[name].updateValueAndValidity();
  }
  
  private formBreadcrumbs(): void {
      this.breadcrumbsData = [{
        label: 'Super Buttons',
        url: '/quick-links/navigation-points'
      }, {
        label: this.typeAddEdit == 'ADD' ? 'Create' : this.navigationPoint?.title,
        url: this.typeAddEdit == 'ADD' ? `/quick-links/navigation-points/add` : `/quick-links/navigation-points/${this.navigationPoint.id}`
      }];
  }
  private createUpdateNavigationPoint() {
    if (this.typeAddEdit === 'ADD') {
      return this.navigationPointsApiService.createNavigationPoint(this.navigationPoint);
    } else {
      return this.navigationPointsApiService.updateNavigationPoint(this.navigationPoint)
    }
  }
  private save(): void {
    this.createUpdateNavigationPoint().map((data: HttpResponse<NavigationPoint>) => data.body)
      .subscribe((data: NavigationPoint) => {
        const self = this;
        this.navigationPoint = data;
        this.formBreadcrumbs();
        this.actionButtons.extendCollection(this.navigationPoint);
        this.segmentStoreService.setSegmentValue(this.navigationPoint, CSPSegmentLSConstants.SUPER_BUTTON);
        this.dialogService.showNotificationDialog({
          title: AppConstants.SUPER_BUTTON_SAVING,
          message: AppConstants.SUPER_BUTTON_SAVED,
          closeCallback() {
            self.router.navigate([`/quick-links/navigation-points`]);
          }
        });
        });
  }

  private revert(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.navigationPointsApiService.getSingleNavigationPoint(params['id'])
        .map((data: HttpResponse<NavigationPoint>) => data.body)
        .subscribe((navigationPoint: NavigationPoint) => {
          this.navigationPoint = navigationPoint;
             if(!this.navigationPoint?.ctaAlignment){
              this.navigationPoint.ctaAlignment = 'center';
             }
          this.segmentsList = {
            exclusionList: this.navigationPoint.exclusionList,
            inclusionList: this.navigationPoint.inclusionList,
            universalSegment: this.navigationPoint.universalSegment 
          };
        });
    });
    this.isRevert = true;
  }

  private remove(): void {
    this.navigationPointsApiService.deleteNavigationPoint(this.navigationPoint.id)
      .subscribe(() => {
        this.router.navigate(['/quick-links/navigation-points/']);
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
    this.navigationPoint.validityPeriodStart = data.startDate;
    this.navigationPoint.validityPeriodEnd = data.endDate;
  }

  public isMaxLengthReached(name: string): boolean {
    const control = this.form.controls[name];

    return control.errors && control.errors.maxlength;
  }

  /*
  *Disables save button based upon the return type
   */
  public validationHandler(): boolean {
    return this.form.valid && this.isSegmentValid;
  }

  /**
   * updates issegmentvalid true/false on child form changes
  */
  isSegmentFormValid(isValid: boolean): void {
    this.isSegmentValid = isValid;
  }

  /*
   * Handles logic for child emitted data. 
  */
  modifiedSegmentsHandler(segmentConfigData: ISegmentModel): void {
    this.isRevert = false;
    this.navigationPoint = { ...this.navigationPoint, ...segmentConfigData };
  }
}
