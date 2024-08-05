import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';
import { MatSelect } from '@angular/material/select';
import { MatOption } from '@angular/material/core';
import * as _ from 'lodash';

import { marketTypes, SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { FanzoneInclusionList } from '@app/client/private/models/surfaceBet.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { AppConstants,CSPSegmentLSConstants } from '@app/app.constants';
import { ErrorService } from '@app/client/private/services/error.service';
import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';
import { ISegmentModel } from '@app/client/private/models/segment.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';

@Component({
  templateUrl: './highlight-carousel.component.html',
  styleUrls: ['./highlight-carousel.component.scss']
})

export class SportsHighlightCarouselComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('iconUploadInput') private iconUploadInput: ElementRef;
  @ViewChild('select') select: MatSelect;

  public directiveNames: string[] = marketTypes;
  public highlightCarousel: SportsHighlightCarousel = {
    id: null,
    displayFrom: null,
    displayTo: null,
    title: null,
    disabled: true,
    displayOnDesktop: false,
    brand: this.brandService.brand,
    sortOrder: null,
    svgId: '',
    svg: '',
    svgFilename: null,
    inPlay: false,
    typeId: null,
    typeIds: [],
    sportId: 0,
    pageId: null,
    pageType: null,
    limit: null,
    events: [],
    createdBy: null,
    createdAt: null,
    updatedBy: null,
    updatedAt: null,
    updatedByUserName: null,
    createdByUserName: null,
    inclusionList: [],
    exclusionList: [],
    universalSegment: true,
    fanzoneInclusions: [],
    displayMarketType: null
  };

  fanzoneInclusions21st: boolean = true;
  isFZ21stSelected : boolean = false;

  public highlightCarouselList: SportsHighlightCarousel[];
  public breadcrumbsData: Breadcrumb[];
  public form: FormGroup;
  public carouselId: string;
  public sportConfigId: string;
  public routeParams: Params;

  public hubId: string;
  public hubIndex: number;

  public moduleId: string;
  public module: SportsModule;
  public eventError: string;
  public dateRangeError: string;
  public imageToUpload = {
    name: '',
    file: null
  };
  public selectByTypeId: boolean = true;
  public pageTitle: string = 'Highlights Carousel';
  public isIMActive: boolean;
  public isRevert = false;
  segmentsList: ISegmentModel = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };
  isSegmentValid: boolean = false;
  isHomePage: boolean;
  public allSelected = false;
  public fanzoneInclusionList: FanzoneInclusionList[] = [];
  public isFanzoneSportCategory: boolean;
  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private brandService: BrandService,
    private snackBar: MatSnackBar,
    private errorService: ErrorService,
    private sportsModulesService: SportsModulesService,
    private sportsHighlightCarouselsService: SportsHighlightCarouselsService,
    private dialogService: DialogService,
    private segmentStoreService: SegmentStoreService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
    this.isIMActive = this.brandService.isIMActive();
    this.isHomePage = this.segmentStoreService.validateHomeModule();
    this.isSegmentValid = !this.isHomePage;
  }

  public ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.hubId = params['hubId'];
      this.sportConfigId = params['id'];
      this.carouselId = params['carouselId'];
      this.moduleId = params['moduleId'];
      this.pageTitle = this.carouselId ? 'Highlights Carousel:' : 'New Highlights Carousel';
      this.highlightCarousel.displayMarketType = 'PrimaryMarket';
      this.loadInitialData(params);
    });
  }

  public validationHandler(): boolean {
    return this.form.valid && this.isSegmentValid && !this.dateRangeError && (this.isHomePage ? true : !this.eventError);
  }

  public uploadIconHandler(): void {
    this.iconUploadInput.nativeElement.click();
  }

  public handleImageChange(event: { target: { files: File[] } }): void {
    const file = event.target.files[0];
    const fileType = file && file.type;

    if (!file) {
      return;
    }

    if (fileType !== 'image/svg+xml') {
      this.snackBar.open(`Error. Unsupported file type.`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.form.controls.icon.reset();
      return;
    }

    if (this.highlightCarousel.id) {
      this.globalLoaderService.showLoader();
      this.sportsHighlightCarouselsService.uploadIcon(
        this.highlightCarousel.id,
        file
      ).map((response: HttpResponse<SportsHighlightCarousel>) => response.body)
        .subscribe((data: SportsHighlightCarousel) => {
          this.actionButtons.extendCollection(data);
          this.highlightCarousel = this.updateEditableFields(data, this.highlightCarousel);
          this.snackBar.open(`Icon Uploaded.`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
          this.globalLoaderService.hideLoader();
        }, error => {
          this.form.controls.icon.reset();
          this.globalLoaderService.hideLoader();
        });
    } else {
      this.imageToUpload.name = file.name;
      this.imageToUpload.file = file;
    }
  }

  public removeIconHandler(): void {
    if (this.highlightCarousel.id) {
      this.removeIconRequest();
    } else {
      this.form.controls.icon.reset();
      this.imageToUpload.name = '';
      this.imageToUpload.file = undefined;
    }
  }

  public onChangeDirectiveName(value: string): void {
    this.highlightCarousel.displayMarketType = value;
  }

  public toggleActiveStatus(): void {
    this.highlightCarousel.disabled = !this.highlightCarousel.disabled;
    this.validateDate();
  }

  public onDisplayOnDesktopCheck(): void {
    this.highlightCarousel.displayOnDesktop = !this.highlightCarousel.displayOnDesktop;
    this.validateDate();
  }

  public handleDateUpdate(dateRange: DateRange): void {
    const newObj = {
      start: new Date(dateRange.startDate),
      end: new Date(dateRange.endDate)
    };
    this.highlightCarousel.displayFrom = isNaN(newObj.start.getTime()) ? this.highlightCarousel.displayFrom : newObj.start.toISOString();
    this.highlightCarousel.displayTo = isNaN(newObj.end.getTime()) ? this.highlightCarousel.displayTo : newObj.end.toISOString();
    this.validateDate();
    this.validateEvents();
  }

  public validateDate(): boolean {
    this.dateRangeError = null;

    const currentDate = new Date().getTime();
    const startDate = new Date(this.highlightCarousel.displayFrom).getTime();
    const endDate = new Date(this.highlightCarousel.displayTo).getTime();

    if (startDate > endDate && currentDate < endDate) {
      this.dateRangeError = '"Display to" date should be after "Display from" date. Please amend your schedule.';
      return !this.dateRangeError;
    }

    if (currentDate > endDate) {
      this.dateRangeError = '"Display to" date should be in future. Please amend your schedule.';
      return !this.dateRangeError;
    }

    return !this.dateRangeError;
  }

  public validateEvents(): boolean {
    if(this.isHomePage) {
      return;
    }

    // cannot set Type ID, Event ID that is already used in other carousels in same date period
    this.eventError = null;
    if (this.highlightCarousel && this.highlightCarouselList) {
      // get all carousels except current
      const carouselCheckList: SportsHighlightCarousel[] = _.filter(this.highlightCarouselList, el => el.id !== this.carouselId);

      if (this.isTypeIdUsed(carouselCheckList)) {
        this.eventError = `Type ID: ${this.highlightCarousel.typeId} is already used for same period. Please amend your schedule.`;
      }

      const eventsIntersection = this.getEventsIntersection(carouselCheckList);
      if (eventsIntersection && eventsIntersection.length) {
        this.eventError = `Event IDs: ${eventsIntersection.join(', ')} are already used for same period. Please amend your schedule.`;
      }

      return !this.eventError;
    }

    return true;
  }

  public setEventError(value: string): void {
    if(this.isHomePage) {
      return;
    }
    this.eventError = value;
  }

  public isTypeIdUsed(carouselCheckList: SportsHighlightCarousel[]): boolean {
    if (!this.highlightCarousel.typeId) {
      return false;
    }

    const typeId: number = this.highlightCarousel.typeId;
    const currentStart = (new Date(this.highlightCarousel.displayFrom)).getTime();
    const currentEnd = (new Date(this.highlightCarousel.displayTo)).getTime();

    const isEventTypeIdUsed: boolean = typeId && _.some(carouselCheckList, el => {
      const elStart = (new Date(el.displayFrom)).getTime();
      const elEnd = (new Date(el.displayTo)).getTime();
      const matchPeriod: boolean = currentStart < elEnd && currentEnd > elStart;

      return matchPeriod && typeId && el.typeId && el.typeId.toString() === typeId.toString();
    });

    return isEventTypeIdUsed;
  }

  public getEventsIntersection(carouselCheckList: SportsHighlightCarousel[]): string[] {
    if (!this.highlightCarousel.events || !this.highlightCarousel.events.length) {
      return [];
    }

    const currentStart = (new Date(this.highlightCarousel.displayFrom)).getTime();
    const currentEnd = (new Date(this.highlightCarousel.displayTo)).getTime();

    const usedEventIds: string[] = _.reduce(carouselCheckList, (sum: string[], el: SportsHighlightCarousel) => {
      const elStart = (new Date(el.displayFrom)).getTime();
      const elEnd = (new Date(el.displayTo)).getTime();
      const matchPeriod: boolean = currentStart < elEnd && currentEnd > elStart;

      if (matchPeriod) {
        return _.union(sum, el.events || []);
      } else {
        return sum;
      }
    }, []);

    return _.intersection(usedEventIds, this.highlightCarousel.events);
  }

  public changeEventSelection(selectByTypeId: boolean) {
    if (selectByTypeId) {
      this.highlightCarousel.events = null;
    } else {
      this.highlightCarousel.typeId = null;
      this.highlightCarousel.typeIds = null;
    }
    this.setAdditionalFormFields();
    this.eventError = null;
  }

  public get uploadButtonText(): string {
    if (this.highlightCarousel.svgFilename && this.highlightCarousel.svgFilename.filename || this.imageToUpload.name) {
      return 'Change Icon';
    } else {
      return 'Upload Icon';
    }
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

  public save(): void {
    this.validateDate();
    this.validateEvents();

    if (this.dateRangeError || this.eventError) {
      return;
    }

    if (this.carouselId) {
      this.updateRequest();
    } else {
      this.createRequest();
    }
  }

  private updateEditableFields(targetObject: SportsHighlightCarousel, source: SportsHighlightCarousel): SportsHighlightCarousel {
    return _.extend(targetObject,
      _.pick(source, 'title', 'displayFrom ', 'displayTo', 'typeId','typeIds' ,'events', 'limit', 'disabled', 'displayOnDesktop')
    );
  }

  private removeIconRequest() {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsHighlightCarousel().deleteIcon(
      this.highlightCarousel.id
    ).map((response: HttpResponse<SportsHighlightCarousel>) => response.body)
      .subscribe((data: SportsHighlightCarousel) => {
        this.actionButtons.extendCollection(data);
        this.highlightCarousel = this.updateEditableFields(data, this.highlightCarousel);
        this.snackBar.open(`Icon Removed.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.form.controls.icon.reset();
        this.globalLoaderService.hideLoader();
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsHighlightCarousel().delete(this.highlightCarousel.id).subscribe((response) => {
      this.globalLoaderService.hideLoader();
      this.router.navigate([this.getUrlToGoBack]);
    }, error => {
      this.globalLoaderService.hideLoader();
    });
  }

  private createRequest(): void {
    this.globalLoaderService.showLoader();

    if (this.hubIndex) {
      this.highlightCarousel.pageId = this.hubIndex.toString();
      this.highlightCarousel.pageType = 'eventhub';
    } else {
      this.highlightCarousel.pageId = this.module.pageId;
      this.highlightCarousel.pageType = 'sport';
    }
    this.checkIf21stTeamSelected();

    this.sportsHighlightCarouselsService.saveWithIcon(this.highlightCarousel, this.imageToUpload.file)
      .subscribe((carousel: SportsHighlightCarousel) => {
        this.globalLoaderService.hideLoader();
        if (this.isHomePage) {
          this.segmentStoreService.setSegmentValue(carousel, CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL);
          this.router.navigate([this.getUrlToGoBack]);
        } else {
          this.router.navigate([this.getUrlToGoEdit(carousel.id)]);
        }
      }, error => {
        this.errorService.emitError(error);
        this.globalLoaderService.hideLoader();
      });
  }

  private updateRequest(): void {
    this.globalLoaderService.showLoader();
    this.checkIf21stTeamSelected();
    this.apiClientService.sportsHighlightCarousel().update(this.highlightCarousel)
      .map((response: HttpResponse<SportsHighlightCarousel>) => response.body)
      .subscribe((carousel: SportsHighlightCarousel) => {
        this.highlightCarousel = carousel;
        this.actionButtons.extendCollection(this.highlightCarousel);
        if (this.isHomePage) {
          const self = this;
          this.segmentStoreService.setSegmentValue(this.highlightCarousel, CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL);
          this.dialogService.showNotificationDialog({
            title: 'Highlight Carousel',
            message: 'Highlight Carousel is Saved.',
            closeCallback() {
              self.router.navigate([self.getUrlToGoBack]);
            }
          });
        }
        this.globalLoaderService.hideLoader();
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private revert(): void {
    this.loadInitialData(this.routeParams);
    this.isRevert = true;
  }

  private loadInitialData(params: Params): void {
    this.form = null;
    this.globalLoaderService.showLoader();
    if (this.carouselId) {
      // edit
      this.apiClientService.sportsHighlightCarousel().findById(this.carouselId)
        .map((response: HttpResponse<SportsHighlightCarousel>) => response.body)
        .subscribe((highlightCarousel: SportsHighlightCarousel) => {
          this.highlightCarousel = highlightCarousel;
          if(!this.highlightCarousel.displayMarketType) {
            this.highlightCarousel.displayMarketType = 'PrimaryMarket'
          }
          this.isFanzoneSportCategory = this.highlightCarousel.sportId === 160;
          this.isFanzoneSportCategory && this.setupFanzoneInclusions();
          this.setupForm();
          this.getBreadcrumbs(params);
          this.getCarouselList(this.highlightCarousel.sportId);
          if(this.isFanzoneSportCategory && this.highlightCarousel.fanzoneInclusions.length > 0 ){
             if(this.highlightCarousel.fanzoneInclusions.indexOf('FZ001') < 0 ){
              this.fanzoneInclusions21st = false;
             }else {
              this.isFZ21stSelected = true;
             }
          }
        
          this.globalLoaderService.hideLoader();
        }, err => {
          this.globalLoaderService.hideLoader();
        });
    } else {
      // create; module data is needed to set carousel sportId
      this.sportsModulesService.getSingleModuleData(this.moduleId, this.sportConfigId)
        .subscribe((moduleData: [SportsModule, SportCategory]) => {
          this.module = moduleData[0];
          this.highlightCarousel.sportId = this.module.sportId;
          this.isFanzoneSportCategory = this.highlightCarousel.sportId === 160;
          this.isFanzoneSportCategory && this.setupFanzoneInclusions();
          this.getBreadcrumbs(params);
          this.setupForm();
          this.getCarouselList(this.module.sportId);
          this.globalLoaderService.hideLoader();
        }, err => {
          this.globalLoaderService.hideLoader();
        });
    }
  }

  private getCarouselList(sportCategoryId: number): void {
    if (this.hubId) {
      this.sportsHighlightCarouselsService.getHubIndex(this.hubId)
        .subscribe((hubIndex: number) => {
          this.hubIndex = hubIndex;
          // for homepage sportId sould be 0
          this.loadCarousels(hubIndex, 'eventhub');
        });
    } else {
      this.loadCarousels(sportCategoryId, 'sport');
    }

  }

  private loadCarousels(pageId, pageType) {
    this.apiClientService.sportsHighlightCarousel().findAllByBrandAndSport(this.brandService.brand, pageId, pageType)
      .map((response: HttpResponse<SportsHighlightCarousel[]>) => response.body)
      .subscribe((carousels: SportsHighlightCarousel[]) => {
        this.highlightCarouselList = carousels;
        this.validateDate();
        this.validateEvents();
      });
  }

  private setupForm(): void {
    this.selectByTypeId = !(this.highlightCarousel.events && this.highlightCarousel.events.length);
    this.form = new FormGroup({
      title: new FormControl(this.highlightCarousel.title, [Validators.required]),
      disabled: new FormControl(this.highlightCarousel.disabled, []),
      inPlay: new FormControl(this.highlightCarousel.inPlay, []),
      limit: new FormControl(this.highlightCarousel.limit, [Validators.pattern(/^(\d*)$/)]),
      selectByTypeId: new FormControl(this.selectByTypeId, []),
      icon: new FormControl(),
      displayOnDesktop:  new FormControl(this.highlightCarousel.displayOnDesktop, [])
    });
     this.isFanzoneSportCategory && this.form.addControl('fanzoneInclusions', new FormControl(this.highlightCarousel.fanzoneInclusions));
     this.isFanzoneSportCategory && this.form.addControl('fanzoneInclusions21st', new FormControl(this.fanzoneInclusions21st));

    this.segmentsList = {
      exclusionList: this.highlightCarousel.exclusionList,
      inclusionList: this.highlightCarousel.inclusionList,
      universalSegment: this.highlightCarousel.universalSegment
    };
    this.setAdditionalFormFields();
  }

  // switch between event type ID and event ID list form controls
  private setAdditionalFormFields(): void {
    const typeIdControl = this.isFanzoneSportCategory ? 'typeIds': 'typeId'
    this.form.removeControl(typeIdControl);
    this.form.removeControl('events');

    if (this.selectByTypeId) {
      if (this.isFanzoneSportCategory) {
        this.highlightCarousel.typeIds = this.highlightCarousel.typeIds || [];
      }
      this.form.addControl(
        typeIdControl,
        new FormControl(this.highlightCarousel[typeIdControl], [Validators.required])
      );
      !this.isFanzoneSportCategory && this.form.controls[typeIdControl].setValidators(Validators.pattern(/^(\d+)$/));
      this.form.controls[typeIdControl].updateValueAndValidity();
    } else {
      this.highlightCarousel.events = this.highlightCarousel.events || [];
      this.form.addControl(
        'events',
        new FormControl(this.highlightCarousel.events, [Validators.required])
      );
    }
  }

  private getBreadcrumbs(params: Params): void {
    const title: string = this.carouselId ? this.highlightCarousel.title : 'Create';

    this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
      customBreadcrumbs: [
        {
          label: title
        }
      ]
    })
    .subscribe((breadcrumbsData: Breadcrumb[]) => {
      this.breadcrumbsData = breadcrumbsData;
    });
  }

  private get getUrlToGoBack(): string {
    if (this.hubId) {
      return `${this.breadcrumbsData[this.breadcrumbsData.length - 2].url}`;
    }

    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/sports-highlight-carousels/${this.moduleId}`;
    } else {
      return `sports-pages/homepage/sports-module/sports-highlight-carousels/${this.moduleId}`;
    }
  }

  private getUrlToGoEdit(carouselId: string): string {
    if (this.hubId) {
      return `${this.breadcrumbsData[this.breadcrumbsData.length - 2].url}/carousel/edit/${carouselId}`;
    }
    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/sports-highlight-carousels/${this.moduleId}
      /carousel/edit/${carouselId}`;
    } else {
      return `sports-pages/homepage/sports-module/sports-highlight-carousels/${this.moduleId}/carousel/edit/${carouselId}`;
    }
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
    this.highlightCarousel = { ...this.highlightCarousel, ...segmentConfigData };
  }

  setupFanzoneInclusions() {
    this.apiClientService.fanzoneService().getAllFanzones().subscribe(fanzone => {
      const fanzonesList = fanzone.body.map((item) => {
        return {
          active: item.active,
          name: item.name,
          teamId: item.teamId
        };
      });

      this.fanzoneInclusionList = fanzonesList.filter(item => item.teamId != 'FZ001');
      // To handle the select all fanzone scenario
      const intersectFzInclusionList =  _.intersection(_.map(this.fanzoneInclusionList, "teamId"), this.highlightCarousel.fanzoneInclusions);
      this.allSelected = this.fanzoneInclusionList.length === intersectFzInclusionList.length;
    });
  }
  toggleAllSelection(): void {
    if (this.allSelected) {
      this.select.options.forEach((item: MatOption) => item.select());
    } else {
      this.select.options.forEach((item: MatOption) => item.deselect());
    }
  }
  optionClick(): void {
    this.allSelected = !this.select.options.some(option => option.selected === false);
  }

  onselect21stTeam() {
    this.fanzoneInclusions21st = !this.fanzoneInclusions21st;
    this.highlightCarousel.fanzoneInclusions = [];
  }

  checkIf21stTeamSelected(){
    if(this.fanzoneInclusions21st) {
      this.highlightCarousel.fanzoneInclusions = ['FZ001'];
    }
  }
}
