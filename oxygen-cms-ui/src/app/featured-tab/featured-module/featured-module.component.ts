import { Brand } from '@app/client/private/models/brand.model';
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { FeaturedTabModule } from '@app/client/private/models/featuredTabModule';
import { DataSelection, EventsSelectionSetting } from '@app/client/private/models/homemodule.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { AppConstants, CSPSegmentLSConstants } from '@app/app.constants';

import { FeaturedModuleEventsRequest } from '@app/client/private/models/featuredModuleEventsRequest';
import { BrandService } from '@app/client/private/services/brand.service';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { ISegmentModel } from '@app/client/private/models/segment.model';
import { SegmentStoreService } from '@root/app/client/private/services/segment-store.service';
import { Location } from '@angular/common';
enum selectEventsTypes {
  Category = 'Category',
  Class = 'Class',
  Type = 'Type',
  Team = 'Team',
  RaceTypeId = 'Race Type id',
  RacingGrid = 'Racing Grid',
  Selection = 'Selection',
  Event = 'Event',
  Market = 'Market',
  'Enhanced Multiples' = 'Enhanced Multiples'
}

@Component({
  selector: 'app-featured-module',
  templateUrl: './featured-module.component.html',
  styleUrls: ['./featured-module.component.scss']
})
export class FeaturedModuleComponent implements OnInit {
  public isLoading: boolean = false;
  public pageType: string;
  public featuredTabModule: FeaturedTabModule;
  public publishedDevices: Brand[];

  public additionalOptionsDisabled: boolean = false;
  public badgeInputEnabled: boolean = false;
  public groupBySportCheckboxEnabled: boolean = false;

  public selectEventsTypesEnum: any = selectEventsTypes;
  public selectEventsTypeOptions: string[] = Object.keys(selectEventsTypes);

  public eventsSelection: any[] = [];

  public breadcrumbsData: Breadcrumb[];
  public warningMessage: string;
  public isRevert = false;
  public isHomePage: boolean;
  @ViewChild('actionButtons')
  public actionButtons;
  public hubId: string;
  segmentsList: ISegmentModel;
  isSegmentValid: boolean = false;

  constructor(
    public snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private errorService: ErrorService,
    private segmentStoreService: SegmentStoreService,
    private location: Location
  ) {
    this.isValidModel = this.isValidModel.bind(this);
    let path = this.location.path();
    this.isHomePage =  path.includes('featured-modules') && !path.includes('event-hub');
    this.isSegmentValid = !this.isHomePage;
  }

  ngOnInit() {
    this.loadInitialData();
  }

  /**
   * For page state 'add', create new module.
   */
  createEmptyFeaturedModule(hubData?: IEventHub): void {
    this.featuredTabModule = {
      badge: '',
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,

      data: [],
      dataSelection: {
        selectionId: '',
        selectionType: this.selectEventsTypeOptions[0]
      },
      displayOrder: null,
      eventsSelectionSettings: {
        from: new Date().toISOString(),
        to: new Date(new Date().setHours(24)).toISOString(),
        autoRefresh: false
      },
      footerLink: {
        text: '',
        url: ''
      },
      id: null,
      maxRows: 3,
      maxSelections: 3,
      navItem: 'Featured',
      publishToChannels: this.brandService.brandsList
        .filter(brand => brand.brandCode === this.brandService.brand)
        .map(brand => brand.brandCode),
      publishedDevices: {},
      showExpanded: false,
      groupedBySport: true,
      title: '',
      totalEvents: 0,
      version: 0,
      visibility: {
        displayFrom: new Date().toISOString(),
        displayTo: new Date(new Date().setHours(24)).toISOString(),
        enabled: true
      },
      personalised: false,
      pageId: (hubData ? hubData.indexNumber.toString() : '0'),
      pageType: (hubData ? 'eventhub' : 'sport'),
      inclusionList: [],
      exclusionList: [],
      universalSegment: true
    };

    this.segmentsList = {
      exclusionList: this.featuredTabModule.exclusionList,
      inclusionList: this.featuredTabModule.inclusionList,
      universalSegment: this.featuredTabModule.universalSegment
    };

    this.featuredTabModule.publishToChannels.forEach( brand => {
      this.featuredTabModule.publishedDevices[brand] = {desktop: true, tablet: true, mobile: true};
    });
  }

  /**
   * Handle SelectionType change
   * Copied from old CMS
   */
  checkSelectionType(): void {
    switch (this.featuredTabModule.dataSelection.selectionType) {
      case 'Market':
        this.warningMessage = 'Note: Only <b>primary markets</b>, <b>outright markets</b>, <b>Win or Each Way markets</b> are supported.';
        this.featuredTabModule.maxSelections = 0;
        break;
      case 'Event':
        this.warningMessage = 'Note: <b>Racing events</b> are not supported.';
        break;
      default:
        this.warningMessage = null;
    }

    if (this.featuredTabModule.dataSelection.selectionType === 'RacingGrid') {
      this.featuredTabModule.dataSelection.selectionId = '21';
      this.additionalOptionsDisabled = true;
    } else {
      this.additionalOptionsDisabled = false;
    }

    if (this.featuredTabModule.dataSelection.selectionType === 'Selection') {
      this.badgeInputEnabled = true;
    } else {
      this.badgeInputEnabled = false;
      this.featuredTabModule.badge = '';
    }

    if (this.featuredTabModule.dataSelection.selectionType === 'Event') {
      this.groupBySportCheckboxEnabled = true;
    } else {
      this.groupBySportCheckboxEnabled = false;
    }
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleVisibilityDateUpdate(data: DateRange): void {
    this.featuredTabModule.visibility.displayFrom = data.startDate;
    this.featuredTabModule.visibility.displayTo = data.endDate;
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleSelectionSettingsDateUpdate(data: DateRange): void {
    this.featuredTabModule.eventsSelectionSettings.from = data.startDate;
    this.featuredTabModule.eventsSelectionSettings.to = data.endDate;
  }

  /**
   * check current publish brand state
   * @param {string} brandName
   * @return {boolean}
   */
  getBrandPublishState(brandName: string): boolean {
    return this.featuredTabModule.publishToChannels.indexOf(brandName) >= 0;
  }

  /**
   * Toggle brand publish state.
   * @param event
   * @param {string} brandName
   */
  toggleBrandPublishSate(event: any, brandName: string) {
    const publishedBrandsList: string[] = this.featuredTabModule.publishToChannels;
    const indexInList: number = publishedBrandsList.indexOf(brandName);

    if (indexInList >= 0) {
      publishedBrandsList.splice(indexInList, 1);
      this.deactivateDevices(brandName);
    } else {
      publishedBrandsList.push(brandName);
      this.activateDevices(brandName);
    }
  }

  /**
   * Select All/Deselect All buttons logic.
   * @param {boolean} isSelected
   */
  setAllBrandsPublishState(isSelected: boolean): void {
    this.publishedDevices.forEach(brandData => {
      const brandName: string = brandData.brandCode;

      if (isSelected === true) {
        this.activateDevices(brandName);
      }

      if (isSelected === false) {
        this.deactivateDevices(brandName);
      }
    });
  }

  /**
   * set flags for all devices
   * @param {string} brandName
   */
  activateDevices(brandName: string): void {
    const brandDevices = this.featuredTabModule.publishedDevices[brandName];

    brandDevices.desktop = true;
    brandDevices.tablet = true;
    brandDevices.mobile = true;
  }

  /**
   * set flags for all devices
   * @param {string} brandName
   */
  deactivateDevices(brandName: string): void {
    const brandDevices = this.featuredTabModule.publishedDevices[brandName];

    brandDevices.desktop = false;
    brandDevices.tablet = false;
    brandDevices.mobile = false;
  }

  /**
   * Load Events list from server.
   * According to type, id and on Date range.
   */
  reloadOpenBetData(): void {
    const selectionData: DataSelection = this.featuredTabModule.dataSelection;
    const selectionTime: EventsSelectionSetting = this.featuredTabModule.eventsSelectionSettings;
    const openbetRequest: FeaturedModuleEventsRequest = {
      selectionType: selectionData.selectionType,
      selectionId: selectionData.selectionId,
      dateFrom: selectionTime.from,
      dateTo: selectionTime.to
    };

    this.showHideSpinner();

    this.apiClientService
     .featuredTabModules()
     .loadOpenbetEvents(openbetRequest)
     .subscribe((data: any) => {
       this.showHideSpinner(false);

       if (data.body.errors) {
         this.errorService.emitError(data.body.message);
         return;
       }

       this.eventsSelection = data.body;

       this.snackBar.open('OPENBET EVENTS LOADED!!', 'OK!', {
         duration: AppConstants.HIDE_DURATION
       });
     }, (error) => {
       this.showHideSpinner(false);
       this.errorService.emitError(error.message);
     });
  }

  /**
   * Move loadded openbet events data to Module data.
   * recalculate total events couter
   */
  applyOpenbetData() {
    if (this.featuredTabModule.maxRows) {
      this.featuredTabModule.data = this.eventsSelection.slice(0, this.featuredTabModule.maxRows);
    } else {
      this.featuredTabModule.data = this.eventsSelection;
    }
    this.featuredTabModule.totalEvents = this.featuredTabModule.data.length;
  }

  /**
   * clear all mapped events
   */
  removeModuleEvents(): void {
    this.featuredTabModule.data = [];
  }

  /**
   * Show confirmation dialog and create module.
   */
  createModule() {
    this.dialogService.showConfirmDialog({
      title: `Create module: ${this.featuredTabModule.title}`,
      message: `Do You Want to Create module?`,
      yesCallback: () => {
        this.sendNewModuleInformation();
      }
    });
  }

  /**
   * Send create module API request.
   */
  sendNewModuleInformation() {
    this.showHideSpinner(true);
    this.apiClientService.featuredTabModules()
      .add(this.featuredTabModule)
      .subscribe(data => {
        this.featuredTabModule.id = data.body.id;
        let self = this;
        this.segmentStoreService.setSegmentValue(this.featuredTabModule ,CSPSegmentLSConstants.FEATURED_TAB_MODULE);
        this.showHideSpinner(false);
        this.dialogService.showNotificationDialog({
          title: 'Create Completed',
          message: 'Featured Tab Module is Successfully Created.',
          closeCallback() {
            if(self.isHomePage) {
              self.router.navigate(['/featured-modules']);
            } else {
              self.navigateTo(self.featuredTabModule.id);
            }
          }
        });
      });
  }

  /**
   * Send API request to Update module data.
   */
  updateModule() {
    this.featuredTabModule.navItem = 'Featured';

    this.apiClientService.featuredTabModules()
      .edit(this.featuredTabModule)
      .map((module: HttpResponse<FeaturedTabModule>) => module.body)
      .subscribe((data: FeaturedTabModule) => {
        const self = this;
        this.featuredTabModule = data;
        this.actionButtons.extendCollection(this.featuredTabModule);
        this.segmentStoreService.setSegmentValue(this.featuredTabModule ,CSPSegmentLSConstants.FEATURED_TAB_MODULE);
        this.dialogService.showNotificationDialog({
          title: 'Update Completed',
          message: 'Featured Tab Module Changes are Saved.',
          closeCallback() {
            if(self.isHomePage) {
            self.router.navigate(['/featured-modules']);
            }
          }
        });
      });
  }

  /**
   * Send server API request to delete module
   */
  removeModule() {
    this.apiClientService.featuredTabModules()
      .remove(this.featuredTabModule.id)
      .subscribe(data => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Module is Removed.'
        });

        this.navigateTo();
      });
  }

  /**
   * Reload module data from server
   */
  revertChanges() {
    this.loadInitialData();
    this.isRevert = true;
  }

  /**
   * Initial data Loading method
   * Get module data from sevrer or create new module object
   */
  private loadInitialData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];
      this.publishedDevices = this.brandService.brandsList.filter(brand => brand.brandCode === this.brandService.brand);
      this.pageType = params.id ? 'edit' : 'add';

      if (this.pageType === 'edit') {
        this.showHideSpinner();
        this.apiClientService
            .featuredTabModules()
            .getById(params.id)
            .map((moduleResponse: HttpResponse<FeaturedTabModule>) => {
              return moduleResponse.body;
            })
            .subscribe((featuredModule: FeaturedTabModule) => {
              this.featuredTabModule = featuredModule;              
              this.segmentsList = {
                exclusionList: this.featuredTabModule.exclusionList,
                inclusionList: this.featuredTabModule.inclusionList,
                universalSegment: this.featuredTabModule.universalSegment
              };

              if (this.actionButtons) {
                this.actionButtons.extendCollection(this.featuredTabModule);
              }

              this.eventsSelection = this.featuredTabModule.data.filter((item, index) => index < 10);
              this.initBreadcrumbs(params);
              this.checkSelectionType();
              this.showHideSpinner(false);
            }, () => {
              this.showHideSpinner(false);
              this.router.navigate(['/featured-modules']);
            });
      } else {
        this.initBreadcrumbs(params);
        if (this.hubId) {
          this.apiClientService.eventHub().getEventHubById(this.hubId)
            .subscribe((hubData: IEventHub) => {
              this.createEmptyFeaturedModule(hubData);
            });
        } else {
          this.createEmptyFeaturedModule();
        }
      }
    });
  }

  /**
   * Init bredcrumbs paths data to view.
   */
  initBreadcrumbs(params: Params) {
    const isEdit = this.pageType === 'edit';
    if (this.hubId) {
      this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
        customBreadcrumbs: [
          {
            label: isEdit ? this.featuredTabModule.title : 'create'
          }
        ]
      }).subscribe((breadcrubs: Breadcrumb[]) => {
        this.breadcrumbsData = breadcrubs;
      });
    } else {
      this.breadcrumbsData = [{
        label: `Featured Tab Modules`,
        url: `/featured-modules`
      }, {
        label: isEdit ? this.featuredTabModule.title : 'create',
        url: isEdit ? `/featured-modules/edit/${this.featuredTabModule.id}` : '/featured-modules/add'
      }];
    }
  }

  /**
   * Base model validation with checking required fields.
   * @return {boolean}
   */
  public isValidModel(): boolean {
    return this.featuredTabModule && this.featuredTabModule.title.length > 0 &&
      this.featuredTabModule.dataSelection.selectionType.length > 0 &&
      this.featuredTabModule.dataSelection.selectionId.length > 0 &&
      this.featuredTabModule.publishToChannels.length > 0 &&
      this.isSegmentValid;
  }

  /**
   * Validate seletion type before activate "Reload" button.
   * @return {boolean}
   */
  public canReloadEvents(): boolean {
    return this.featuredTabModule.dataSelection.selectionId.length > 0;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeModule();
        break;
      case 'save':
        this.updateModule();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Validate input with type of number to not set value less than 1.
   */
  validateMinValue(e): boolean {
    if ((e.keyCode < 48 || e.keyCode > 57) ||
      (e.target.value.length === 0 && e.keyCode === 48)) {
      return false;
    }
  }

  /**
   * Auto Navigate to creted module with Id
   * Auto Navigate back when module deleted
   * @param moduleId
   */
  navigateTo(moduleId?: string): void {
    let linkToNavigate = '';
    const moduleUrl = `${this.breadcrumbsData[this.breadcrumbsData.length - 2].url}`;
    if (moduleId) {
      if (this.hubId) {
        linkToNavigate = `${moduleUrl}/featured-modules/edit/${this.featuredTabModule.id}`;
      } else {
        linkToNavigate = `/featured-modules/edit/${this.featuredTabModule.id}`;
      }
     } else {
      if (this.hubId) {
        linkToNavigate = moduleUrl;
      } else {
        linkToNavigate = '/featured-modules';
      }
    }
    this.router.navigate([linkToNavigate]);
  }

  handleGroupBySportChange(): void {
    this.featuredTabModule.groupedBySport = !this.featuredTabModule.groupedBySport;
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
    this.featuredTabModule = { ...this.featuredTabModule, ...segmentConfigData };
  }
}
