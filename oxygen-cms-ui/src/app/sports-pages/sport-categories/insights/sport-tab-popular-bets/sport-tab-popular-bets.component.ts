import { ChangeDetectorRef, Component, EventEmitter, OnChanges, OnInit, Output, ViewChild } from "@angular/core";
import { FormGroup, Validators, FormControl } from '@angular/forms';
import { MatDialog, MatDialogRef } from "@angular/material/dialog";
import { SportTab } from "@app/client/private/models/sporttab.model";
 import {map, switchAll} from 'rxjs/operators';
import { Breadcrumb, DataTableColumn } from "@app/client/private/models";
import { ISportTabPopularBetsFilter, SportTabFilterInstance } from "@app/client/private/models/sporttabFilters.model";
import { DialogService } from "@app/shared/dialog/dialog.service";
import { PopularBetFiltersCreateComponent } from "../popular-bet-filters-create/popular-bet-filters-create.component";
import { AppConstants } from "@app/app.constants";
import { TinymceComponent } from "@app/shared/tinymce/tinymce.component";
import { CmsAlertComponent } from "@app/shared/cms-alert/cms-alert.component";
import { FILTER_FEILDS } from "./sport-tab-popular-bets-filter.constants";
import * as _ from "lodash";
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ActivatedRoute, Params} from '@angular/router';
import {ApiClientService} from '@app/client/private/services/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {forkJoin} from 'rxjs/observable/forkJoin';
import { ActionButtonsComponent } from "@app/shared/action-buttons/action-buttons.component";
import { HttpResponse } from "@angular/common/http";
import {SportCategory} from '@app/client/private/models/sportcategory.model';
import { SPORT_TAB_FILTERS_CONFIG } from "../../sport-tab-filters/sport-tab-filters.config";
import { InsightsService } from "../insights.service";
import { INSIGHTS_DEFAULT_DATA } from "../inisghts-tab/insights-mock";

@Component({
  selector: "sport-tab-popular-bets",
  templateUrl: "./sport-tab-popular-bets.component.html",
  styleUrls: ["./sport-tab-popular-bets.component.scss"],
})
export class SportTabPopularBetsComponent implements OnChanges, OnInit {

  form: FormGroup;
  @Output() updatedFilterData = new EventEmitter<any>();
  @Output() changedPopularBetsData = new EventEmitter<any>();
  @ViewChild('requestError') private requestError: CmsAlertComponent;
  @ViewChild('informationTextEditor') informationTextEditor: TinymceComponent;

  filterItem = [];
  showMarketSwitcher: boolean = false;
  filtersList: SportTabFilterInstance<any>[] = [];
  searchField: string = '';
  isMarketsEdited: boolean;
  sortByFiltersColumns: Array<DataTableColumn> = FILTER_FEILDS;
  timeFitersColumns: Array<DataTableColumn> = FILTER_FEILDS;
  private readonly filtersConfig = SPORT_TAB_FILTERS_CONFIG;
  private readonly sportTabId = 'popular_bets';
  eventStartsFilter: boolean;
  updatingPopularTimeFilters: boolean = false;
  sportParams: Params;
  public breadcrumbsData: Breadcrumb[];
  public sportTab: SportTab | any;
  populrBetsData: any;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  isLoading = false;
  isDefaultValueEmpty:boolean = true;
  
  constructor(
    private dialogService: DialogService,
    private dialog: MatDialog,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private changeDetectorRef: ChangeDetectorRef,
    private insightsService:InsightsService
   ) {
     this.validationHandler = this.validationHandler.bind(this);
   }

  ngOnInit(): void {
    this.loadInitialData();
  }
/**
 * to be create popular bets form
 */
  createPopularBetsFormGroup(){
    const popularTab = this.populrBetsData && this.populrBetsData?.popularTabs;
    this.form = new FormGroup({
      enabled: new FormControl(popularTab[0].enabled || false, []),
      showNewFlag: new FormControl(popularTab[0].showNewFlag || false, []),
      popularTabName: new FormControl(popularTab[0].popularTabName || 'Popular_tab'),
      trendingTabName: new FormControl(this.populrBetsData.trendingTabName || '', [Validators.required,Validators.maxLength(15)]),
      headerDisplayName: new FormControl(popularTab[0].headerDisplayName || '', [Validators.required,Validators.maxLength(15)]),
      startsInText: new FormControl(popularTab[0].startsInText || '', [Validators.required,Validators.maxLength(25)]),
      backedInLastText: new FormControl(popularTab[0].backedInLastText || '', [Validators.required,Validators.maxLength(25)]),
      showMoreText: new FormControl(popularTab[0].showMoreText || '', [Validators.required,Validators.maxLength(15)]),
      showLessText: new FormControl(popularTab[0].showLessText || '', [Validators.required,Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(popularTab[0].backedUpTimesText || '', [Validators.required,Validators.maxLength(30)]),
      informationTextDesc: new FormControl( popularTab[0].informationTextDesc || '', [Validators.required]),
      numbOfDefaultPopularBets: new FormControl(popularTab[0].numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      numbOfShowMorePopularBets: new FormControl(popularTab[0].numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(15)]),
      priceRange: new FormControl(popularTab[0].priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      noPopularBetsMsg: new FormControl(popularTab[0].noPopularBetsMsg || '', [Validators.required, Validators.maxLength(100)]),
      lastUpdatedTime: new FormControl( popularTab[0].lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      betSlipBarBetsAddedDesc: new FormControl(popularTab[0].betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(popularTab[0].betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarDesc: new FormControl(popularTab[0].betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(popularTab[0].betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText:  new FormControl(popularTab[0].suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(popularTab[0].suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      backedInLastFilter: new FormControl(popularTab[0].backedInLastFilter || []),
      eventStartsFilter: new FormControl(popularTab[0].eventStartsFilter || []),
      enableAddToBetSlipBar: new FormControl(popularTab[0].enableAddToBetSlipBar || true,[]),
      enableBackedUpTimes: new FormControl(popularTab[0].enableBackedUpTimes || true,[]),
      enableArrowIcon: new FormControl(popularTab[0].enableArrowIcon || true,[])
    });
  }
  /**
   * it detectes the every change
   */
  ngOnChanges(): void {
     this.showMarketSwitcherTable();
 }
  
  /**
   * it loads the initial data 
   * loadInitialData()
   */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute
      .params
      .pipe(
        map((params: Params) => {
          this.sportParams = params;
          const sportTab = this.insightsService.getSportTabById(params["sportTabId"]);
          const sportCategory = this.insightsService.getSportCategoryById(params["id"]);
          return forkJoin([sportTab, sportCategory]);
        }),
        switchAll())
      .subscribe(([sportTab, sport]) => {
        this.buildBreadCrumbsData(sportTab, sport);
        this.sportTab = this.normalizeTab(sportTab);
        if (!this.sportTab.trendingTabs.length) {
          this.sportTab.trendingTabs = INSIGHTS_DEFAULT_DATA;
        }
        this.populrBetsData = this.sportTab?.trendingTabs?.find((tab)=> tab.headerDisplayName.toLowerCase() === this.sportTabId);
        this.createPopularBetsFormGroup(); 
        if (this.informationTextEditor) {
          this.informationTextEditor.update(this.populrBetsData.popularTabs[0].informationTextDesc);
        }
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.showMarketSwitcherTable();
      });
   }
/**
 * 
 * @param {object}sportTab 
 * @returns {object} 
 */
  private normalizeTab(sportTab: SportTab): SportTab {
    Object.keys(this.filtersConfig).forEach((filterName: string) => {
      const config = this.filtersConfig[filterName];

      if (config && config.tabs && config.tabs.indexOf(sportTab.name) >= 0) {
        if (!sportTab.filters) { sportTab.filters = {}; }
        if (!sportTab.filters[filterName]) { sportTab.filters[filterName] = {}; }
        if (!sportTab.filters[filterName].values) {
          sportTab.filters[filterName].values = [];
          sportTab.filters[filterName].enabled = false;
        }
      }
    });

    return sportTab;
  }
  /**
   * saveChanges
   * @param {message} message 
   */

  public saveChanges(message?): void {
      this.submitChanges(message);
  }
  public submitChanges(message?): void {
    this.apiClientService
    .sportTabService()
    .edit(this.sportTab)
    .map((data: HttpResponse<SportTab>) => data.body)
    .subscribe((sportTab: SportTab) => {
      this.isMarketsEdited = false;
      this.sportTab = this.normalizeTab(sportTab);
      this.populrBetsData = this.sportTab?.trendingTabs?.find((tab)=> tab.headerDisplayName.toLowerCase() === this.sportTabId);
      this.actionButtons.extendCollection(this.sportTab);
      this.snackBar.open(message? message: `Sport Tab is saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.showMarketSwitcherTable();
    });
  }

  /**
   * to revert active changes
   */
  public revertChanges(): void {
    this.loadInitialData();
  }
  /**
   * it handle the save changes and revert changes
   * @param event {string}
   */
  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * it builds breadcrumbs 
   * @param  {string} tab it contained the tab id 
   * @param  {Object} sport
   */

  private buildBreadCrumbsData(tab: SportTab, sport: SportCategory) {
    this.breadcrumbsData = [{
      label: `Sport Categories`,
      url: `/sports-pages/sport-categories`
    }, {
      label: sport.imageTitle,
      url: `/sports-pages/sport-categories/${sport.id}`
    },
    {
      label: "insights Tab",
      url:`/sports-pages/sport-categories/${sport.id}/sport-tab/${tab.id}/insightsTab`,
    },
    {
      label: tab.displayName,
      url: `/sports-pages/sport-categories/${sport.id}/sport-tab/${tab.id}/insightsTab/insights-popular`
    }];
  }

  /**
   * Update Information text Blurb message
   * @param {string}  newBlurbText
   * @param {string} field
   */
  public updateInfoTxtData(data: string) {
    this.form.get('informationTextDesc').setValue(data);
    this.changeDetectorRef.detectChanges();
    return this.populrBetsData.popularTabs[0].informationTextDesc = data;
  }

  /*
  *form controls
   */
  get formControls() {
    return this.form?.controls;
  }

  /**
   * Popular bets filter tables update
   * @param filterType 
   * @param pageType 
   * @param sportDatafilter 
   */
  public updatePopularBetFilter( filterType: string, pageType: string, sportDatafilter?: ISportTabPopularBetsFilter): void {
    this.eventStartsFilter = filterType === 'eventStartsFilter';
    const filterIndex = sportDatafilter && this.populrBetsData.popularTabs[0][filterType].indexOf(sportDatafilter);
    const isEdit = pageType === 'edit';
    let data: any = {
      sportFilterData: this.populrBetsData.popularTabs[0][filterType],
      pageType: pageType,
      title: this.eventStartsFilter ? 'Event Start Time Filter' : 'Backed In Last Filter',
     };
    if (isEdit) {
      data.filter = sportDatafilter;
      data.index = filterIndex;  
    }
    const dialogRef = this.dialog.open(PopularBetFiltersCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: data,
    });
    this.updatingPopularTimeFilters = true;
    this.emitDataOnClose(dialogRef, this.populrBetsData.popularTabs[0][filterType], filterType, isEdit, filterIndex);
  }

  /**
   * on popup close, it enters the table data
   * @param dialogRef 
   * @param sportTabFilters 
   * @param filterType 
   * @param isEdit 
   * @param filterIndex 
   */
  private emitDataOnClose(dialogRef: MatDialogRef<PopularBetFiltersCreateComponent>, sportTabFilters: ISportTabPopularBetsFilter[], filterType: string, isEdit: boolean, filterIndex: number): void {
    dialogRef.afterClosed().subscribe((filterObj) => { 
      if (filterObj) {
        filterObj.time = Number(filterObj.time);
        let indexDup;
        indexDup = sportTabFilters.findIndex((item) => { 
        return item.displayName === filterObj.displayName || ( item.time === filterObj.time && item.isTimeInHours === filterObj.isTimeInHours)
        });
        //it makes the only one default value in the table
        sportTabFilters.forEach((val, i) => {
          if (val.time == filterObj.time) {
            val.isDefault = filterObj.isDefault;
          } else {
            if (filterObj.isDefault == false) {
              return;
            }
            val.isDefault = false;
          }
        });
        // it does not allow the duplicate fields in the table
        if ((indexDup >= 0 && !isEdit) || (indexDup !== filterIndex && indexDup >= 0)) {
          this.requestError.showError(`Fliter with same properties exist!`);
        } else {
          !isEdit ? sportTabFilters.push(filterObj): sportTabFilters[filterIndex] = filterObj;
          this.populrBetsData.popularTabs[0][filterType] = sportTabFilters;
         }
         this.defaultValidationHandler();
      }
      this.updatingPopularTimeFilters = false;
    });
  }
  // without having default filed in the table formvalidation never allow to save 
  public defaultValidationHandler(){
    let eventStartDefault = this.populrBetsData.popularTabs[0].eventStartsFilter.find(val => val.isDefault == true);
    let backedDefault  = this.populrBetsData.popularTabs[0].backedInLastFilter.find(val => val.isDefault == true);
    this.isDefaultValueEmpty = eventStartDefault && backedDefault ? true : false ;
    (eventStartDefault === undefined) || (backedDefault === undefined)  ?  this.requestError.showError(`Please add atleast one default filter in the Table!`) : '';
  }

  /**
   * removed filter table data
   */
  public removeFilter(filterItem: ISportTabPopularBetsFilter, filterType: string): void {
    const notificationMessage = 'Are You Sure You Want to Remove Filter ?';
    this.updatingPopularTimeFilters = true;
    this.dialogService.showConfirmDialog({
      title: 'Remove',
      message: notificationMessage,
      yesCallback: (): void => {
        const index = this.populrBetsData.popularTabs[0][filterType].indexOf(filterItem);
        this.populrBetsData.popularTabs[0][filterType].splice(index, 1);
        this.updatingPopularTimeFilters = false;
        this.defaultValidationHandler();
       },
      noCallback: (): void => {
        this.updatingPopularTimeFilters = false;
      }
    });
  }

  /**
   * enabled popularbets check for table
   */
  public showMarketSwitcherTable(): void {
    this.showMarketSwitcher = false;
    setTimeout(() => {
      const tabs = AppConstants.POPULAR_BETS;
      this.showMarketSwitcher = tabs.indexOf(this.sportTab.name.toLocaleLowerCase()) !== -1;
    }, 1);
  }

  /**
   * Reorder table data
   * @param reOrderedData 
   * @param filterType 
   */
  public reorderHandler(reOrderedData, filterType): void {
    // Added logic to override the previous data and only consider the indexes from the emmited data
    this.populrBetsData.popularTabs[0][filterType] = reOrderedData;
   }
 
   // form validation and default field validation must be considered here 
   public validationHandler(): boolean {
    return this.form && this.form.valid && this.isDefaultValueEmpty;
  }
}
