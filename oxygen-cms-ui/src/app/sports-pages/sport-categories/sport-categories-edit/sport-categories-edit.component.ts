import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {SportCategory, TARGET_URI_PATTERN, GREYHOUNDS_SPORT, HORSE_RACING_SPORT, AggregatedMarket} from '@app/client/private/models/sportcategory.model';
import {ApiClientService} from '@app/client/private/services/http';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {AppConstants} from '@app/app.constants';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {SportsModule} from '@app/client/private/models/homepage.model';
import {SportsModulesService} from '@app/sports-modules/sports-modules.service';
import {Order} from '@app/client/private/models/order.model';
import {SportTab} from '@app/client/private/models/sporttab.model';
import {SportCategoryService} from '@app/client/private/services/http/menu/sportCategory.service';
import {Tier} from '@app/client/private/models/tier.enum';
import { ISegmentModel } from '@app/client/private/models/segment.model';


@Component({
  templateUrl: './sport-categories-edit.component.html',
  styleUrls: ['./sport-categories-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class SportCategoriesEditComponent implements OnInit {
  private readonly sportCategoryService: SportCategoryService;
  public modulesData: Array<SportsModule> = [];
  public sportTabData: Array<SportTab> = [];

  public sportCategory: SportCategory;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public expandGeneralSettings: boolean;
  public initialFormState: SportCategory;
  public isIMActive: boolean;
  sportsWithMultiMarkets = [1, 6, 30, 31];
  public isShowInplayConfig: boolean = false;

  segmentsList: ISegmentModel = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };
  public isRevert = false;
  isSegmentValid: boolean = false;
  isMarketAllowed:boolean = false;

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Module',
      property: 'title',
      link: {
        hrefProperty: 'href'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Enabled',
      property: 'disabled',
      type: 'boolean',
      isReversed: true,
      width: 1
    }
  ];

  sportTabColumns: Array<DataTableColumn> = [
    {
      name: 'Tab Name',
      property: 'displayName',
      link: {
        hrefProperty: 'href'
      },
      type: 'link'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Check events',
      property: 'checkEvents',
      type: 'boolean'
    },
    {
      name: 'Has events',
      property: 'hasEvents',
      type: 'boolean'
    }
  ];

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private sportsModulesService: SportsModulesService,
    private brandService: BrandService
  ) {
    this.isValidForm = this.isValidForm.bind(this);
    this.sportCategoryService = apiClientService.sportCategory();
    this.isIMActive = this.brandService.isIMActive();
  }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.sportCategory = null;
    this.globalLoaderService.showLoader();
    this.activatedRoute.queryParams.subscribe((params: Params) => {
      this.expandGeneralSettings = params['expanded'];
    });
    this.activatedRoute.params.subscribe((params: Params) => {
      this.sportCategoryService
        .findOne(params['id'])
        .map((data: HttpResponse<SportCategory>) => {
          return data.body;
        })
        .subscribe((sportCategory: SportCategory) => {
          if(sportCategory.categoryId == 16){
            this.isShowInplayConfig = true;
          }
          this.sportCategory = sportCategory;
          if (!this.sportCategory.inplaySportModule) {
            this.sportCategory.inplaySportModule = {
              enabled: false,
              inplayCount: 10
            };
          }
          if (!this.sportCategory.inplayStatsConfig) {
            this.sportCategory.inplayStatsConfig ={
              showStatsWidget:false,
              note:`Please note: Stats widget league are configured in System Configurations CouponStatsWidget Table`
            }
          }
          this.sportCategory.isRealSport = (() => {
            return this.sportCategory.tier === Tier.TIER_1 || this.sportCategory.tier === Tier.TIER_2;
          });
          this.isMarketAllowed = this.sportsWithMultiMarkets.indexOf(this.sportCategory.categoryId) > -1;
          this.sportCategory.isFRRealSport = (() => {
            return this.sportCategory.tier === Tier.TIER_1 || this.sportCategory.tier === Tier.TIER_2
            || this.sportCategory.categoryId === GREYHOUNDS_SPORT || this.sportCategory.categoryId === HORSE_RACING_SPORT;
          });
          const categoryIdValidator = this.sportCategory.isRealSport() ? [Validators.required] : [];
          const targetUriValidators = this.sportCategory.isRealSport() ? [Validators.required, Validators.pattern(TARGET_URI_PATTERN)] : [];
          this.form = new FormGroup({
            imageTitle: new FormControl(this.sportCategory.imageTitle, [Validators.required]),
            categoryId: new FormControl(this.sportCategory.categoryId, categoryIdValidator),
            ssCategoryCode: new FormControl(this.sportCategory.ssCategoryCode, [Validators.required]),
            outrightSport: new FormControl(this.sportCategory.outrightSport, []),
            multiTemplateSport: new FormControl(this.sportCategory.multiTemplateSport, []),
            oddsCardHeaderType: new FormControl(this.sportCategory.oddsCardHeaderType, []),
            typeIds: new FormControl(this.sportCategory.typeIds, []),
            dispSortNames: new FormControl(this.sportCategory.dispSortNames, []),
            primaryMarkets: new FormControl(this.sportCategory.primaryMarkets, []),
            alt: new FormControl(this.sportCategory.alt, []),
            targetUri: new FormControl(this.sportCategory.targetUri, targetUriValidators),
            disabled: new FormControl(!this.sportCategory.disabled, []),
            inApp: new FormControl(this.sportCategory.inApp, []),
            showInPlay: new FormControl(this.sportCategory.showInPlay, []),
            showInHome: new FormControl(this.sportCategory.showInHome, []),
            showInAZ: new FormControl(this.sportCategory.showInAZ, []),
            showScoreboard: new FormControl(this.sportCategory.showScoreboard, []),
            scoreBoardUri: new FormControl(this.sportCategory.scoreBoardUri, []),
            isTopSport: new FormControl(this.sportCategory.isTopSport, []),
            showFreeRideBanner: new FormControl(this.sportCategory.showFreeRideBanner, []),
            messageLabel: new FormControl(this.sportCategory.messageLabel, [Validators.maxLength(100)]),
            topMarkets : new FormControl(this.sportCategory.topMarkets, []),
            isReactionsEnabled : new FormControl(this.sportCategory.isReactionsEnabled, []),
            showStatsWidget : new FormControl(this.sportCategory?.inplayStatsConfig?.showStatsWidget, [])
          });

          this.breadcrumbsData = [{
            label: `Sport Categories`,
            url: `/sports-pages/sport-categories`
          }, {
            label: this.sportCategory.imageTitle,
            url: `/sports-pages/sport-categories/${this.sportCategory.id}`
          }];

          this.modulesData = [];
          this.sportTabData = [];
          if (this.sportCategory.categoryId) {
            this.sportsModulesService.getModulesData('sport', this.sportCategory.categoryId)
              .subscribe((modulesData: SportsModule[]) => {
                this.modulesData = modulesData;
              });
            this.apiClientService.sportTabService()
              .findAllByBrandAndSportId(this.sportCategory.brand, this.sportCategory.categoryId)
              .map((response: HttpResponse<SportTab[]>) => {
                return this.addSportTabHref(response.body);
              })
              .subscribe((sportTabs: SportTab[]) => {
                sportTabs.forEach((tab, ind)=> {
                  sportTabs[ind].href = tab.name.toLocaleLowerCase() == 'popularbets' ? `${tab.href}/insightsTab` : tab.href;
                });
                this.sportTabData = sportTabs;
              });
          } else {
            this.expandGeneralSettings = true;
          }
          this.initialFormState = { ...this.form.value };
          this.globalLoaderService.hideLoader();
          this.onFormGroupChanges();
          this.segmentsList = {
            exclusionList: this.sportCategory.exclusionList,
            inclusionList: this.sportCategory.inclusionList,
            universalSegment: this.sportCategory.universalSegment
          };
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  onFormGroupChanges(): void {
    const subscr = this.form.valueChanges.subscribe(val => {
      if (this.form.get('svgId')) {
        this.initialFormState = { ...this.form.value };
        subscr.unsubscribe();
      }
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.sportCategoryService
      .update(this.sportCategory)
      .map((data: HttpResponse<SportCategory>) => {
        return data.body;
      })
      .subscribe((data: SportCategory) => {
        this.sportCategory = data;
        this.sportCategory.isRealSport = (() => {
          return this.sportCategory.tier === Tier.TIER_1 || this.sportCategory.tier === Tier.TIER_2;
        });
        this.sportCategory.isFRRealSport = (() => {
          return this.sportCategory.tier === Tier.TIER_1 || this.sportCategory.tier === Tier.TIER_2
          || this.sportCategory.categoryId === GREYHOUNDS_SPORT || this.sportCategory.categoryId === HORSE_RACING_SPORT;
        });
        this.actionButtons.extendCollection(this.sportCategory);
        this.dialogService.showNotificationDialog({
          title: 'Sport Category',
          message: 'Sport Category is Saved.'
        });
        this.initialFormState = { ...this.form.value };
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
    this.isRevert = true;
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.sportCategoryService
      .delete(this.sportCategory.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/sports-pages/sport-categories/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
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

  uploadImageHandler(file): void {
    const observableFunction = this.sportCategoryService.uploadImage.bind(this.sportCategoryService, this.sportCategory.id, file);
    this.popup('Image Uploaded.', observableFunction);
  }

  removeImageHandler(): void {
    const observableFunction = this.sportCategoryService.removeImage.bind(this.sportCategoryService, this.sportCategory.id);
    this.popup('Image Deleted.', observableFunction);
  }

  uploadIconHandler(file): void {
    const observableFunction = this.sportCategoryService.uploadIcon.bind(this.sportCategoryService, this.sportCategory.id, file);
    this.popup('Icon Uploaded.', observableFunction);
  }

  removeIconHandler(): void {
    const observableFunction = this.sportCategoryService.removeIcon.bind(this.sportCategoryService, this.sportCategory.id);
    this.popup('Icon Deleted.', observableFunction);
  }

  uploadSvgHandler(file): void {
    const observableFunction = this.sportCategoryService.uploadSvg.bind(this.sportCategoryService, this.sportCategory.id, file);
    this.popup('Svg Uploaded.', observableFunction);
  }

  removeSvgHandler(): void {
    const observableFunction = this.sportCategoryService.removeSvg.bind(this.sportCategoryService, this.sportCategory.id);
    this.popup('Svg Deleted.', observableFunction);
  }

  private popup(message, observableFunction): void {
    this.globalLoaderService.showLoader();
    observableFunction()
      .map((data: HttpResponse<SportCategory>) => {
        return data.body;
      })
      .subscribe((data: SportCategory) => {
        this.sportCategory = _.extend(data, _.pick(this.sportCategory, 'imageTitle', 'categoryId',
          'ssCategoryCode', 'tier', 'alt', 'targetUri', 'scoreBoardUri'));
        this.snackBar.open(message, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  sportTabReorderHandler(newOrder: Order): void {
    this.apiClientService.sportTabService().postNewOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('Sport Tab Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  reorderHandler(newOrder: Order): void {
    this.sportsModulesService.updateModulesOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New Homepage Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  isValidForm(): boolean {
    return this.form.valid && this.isSegmentValid;
  }

  addSportTabHref(tabs: SportTab[]): SportTab[] {
    const updatedTabsData = [];
    tabs.forEach((tab: SportTab) => {
      const tabHref = `sport-tab/${tab.id}`;
      updatedTabsData.push({
        ...tab,
        href: tabHref
      });
    });
    return updatedTabsData;
  }

  canDeactivate(): boolean {
    return _.isEqual(this.initialFormState, this.form.value);
  }

  /**
   * updates issegmentvalid true/false on child form changes
  */
     isSegmentFormValid(val: boolean): void {
      this.isSegmentValid = val;
    }

  /*
   * Handles logic for child emitted data.
  */
  modifiedSegmentsHandler(segmentsData: ISegmentModel): void {
    this.isRevert = false;
    this.sportCategory = { ...this.sportCategory, ...segmentsData };
  }
  topMarkets(event) {
    var tmInput = event.target.value.replaceAll('|,|', ',').replaceAll(':', ',').replaceAll('|', '').replaceAll(' ', '').toLowerCase();
    const toFindDuplicates = arry => arry.filter((item, index) => arry.indexOf(item) !== index)
    const duplicateElementa = toFindDuplicates(tmInput.split(','));
    if (duplicateElementa.length >= 1) {
      this.form.controls['topMarkets'].setErrors({ 'incorrect': true });
      return;
    }
    else {
      this.form.controls['topMarkets'].setErrors(null);
      this.sportCategory.aggrigatedMarkets = [];
      var markets = event.target.value.split('|,|');
      for (var i = 0; i < markets.length; i++) {
        var topMarketsValue = markets[i].replaceAll('|', '').split(':');
        if (topMarketsValue[1].split(',').length > 3) {
          this.form.controls['topMarkets'].setErrors({ 'incorrect': true });
          break;
        }
        var titles = topMarketsValue[1].split(',').map(element => element.trim());
      var topMarketsObj: AggregatedMarket = {marketName:'',titleName:''};
        topMarketsObj.marketName = topMarketsValue[0].trim();
        topMarketsObj.titleName = titles.join(',');
        this.sportCategory.aggrigatedMarkets[i] = topMarketsObj;
      }
    }
  }
}
