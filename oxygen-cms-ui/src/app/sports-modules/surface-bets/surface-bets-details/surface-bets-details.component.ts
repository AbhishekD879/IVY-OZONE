import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';
import * as _ from 'lodash';

import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { SurfaceBet, FanzoneInclusionList, SurfaceBetTitle } from '@app/client/private/models/surfaceBet.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { forkJoin } from 'rxjs/observable/forkJoin';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { FracToDecService } from '@app/shared/services/fracToDec/frac-to-dec.service';
import { Price } from '@app/client/private/models/price.model';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { ISegmentModel, ISegmentMsg } from '@app/client/private/models/segment.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { map, startWith } from 'rxjs/operators';
import { MatSelect } from '@angular/material/select';
import { MatOption } from '@angular/material/core';
import { SurfaceBetConstants } from '@app/sports-modules/surface-bets/constants/surface-bet.constants';
import {Observable} from 'rxjs';

@Component({
  templateUrl: './surface-bets-details.component.html',
  styleUrls: ['./surface-bets-details.component.scss']
})

export class SportsSurfaceBetsDetailsComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('iconUploadInput') private iconUploadInput: ElementRef;
  @ViewChild('select') select: MatSelect;

  public surfaceBetConstants: any = SurfaceBetConstants;
  public sportConfigId: string;
  public hubId: string;
  public moduleId: string;
  public allEventHubs: IEventHub[];
  public mappedEventHubs: number[];
  public params: Params;
  public surfaceBet: SurfaceBet = {
    content: null,
    contentHeader: null,
    disabled: true,
    title: null,
    displayFrom: null,
    displayTo: null,
    eventIDs: [],
    selectionId: null,
    categoryIDs: [],
    fanzoneInclusions: [],
    sortOrder: null,
    svg: null,
    svgFilename: null,
    svgBgId: null,
    svgBgImgPath: null,
    price: {
      priceDec: null,
      priceDen: null,
      priceNum: null,
      priceType: null
    },
    references: [],
    highlightsTabOn: false,
    edpOn: false,
    displayOnDesktop: false,
    exclusionList: [],
    inclusionList: [],
    universalSegment: true,
    id: null,
    brand: '',

    createdBy: null,
    createdAt: null,

    updatedBy: null,
    updatedAt: null,

    updatedByUserName: null,
    createdByUserName: null
  };

  public breadcrumbsData: Breadcrumb[];

  public form: FormGroup;
  public surfaceBetId: string;
  public allSurfaceBets: SurfaceBet[];
  public error = null;
  public pageTitle: string = 'Surface Bets';
  public imageToUpload = {
    name: '',
    file: null
  };

  public sportCategories: SportCategory[] = [];
  public fanzoneInclusionList: FanzoneInclusionList[] = [];
  public allSelected = false;
  isIMActive: boolean;
  isSegmentValid: boolean = false;
  selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  segmentsList: ISegmentModel = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };
  public isRevert = false;
  public isHomePage: boolean;
  public isFanzoneSportCategory: boolean;
  surfaceBetTitle: SurfaceBetTitle[] =[];
  filteredSurfaceBetTitle: Observable<SurfaceBetTitle[]>;
  isDropDownVisible : boolean = true;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private brandService: BrandService,
    private snackBar: MatSnackBar,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private fracToDecService: FracToDecService,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
    private dialogService: DialogService,
    private segmentStoreService: SegmentStoreService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
    this.isIMActive = this.brandService.isIMActive();
    this.isHomePage = this.segmentStoreService.validateHomeModule();
    this.isSegmentValid = !this.isHomePage;
  }

  public ngOnInit(): void {
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.SURFACE_BET_TAB) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
    this.activatedRoute.params.subscribe((params: Params) => {
      this.surfaceBetId = params['betId'];
      this.sportConfigId = params['id'];
      this.hubId = params['hubId'];
      this.moduleId = params['moduleId'];
      this.params = params;

      this.pageTitle = this.surfaceBetId ? 'Surface Bet:' : 'New Surface Bet';

      this.loadInitialData();
      this.getSurfaceBetTitle();
    });
  }

  public validationHandler(): boolean {
    return this.form.valid && this.isSegmentValid && (this.isHomePage ? true : !this.error) ;
  }

  public toggleActiveStatus(): void {
    this.surfaceBet.disabled = !this.surfaceBet.disabled;
    this.validateSelection();
  }

  public handleDateUpdate(dateRange: DateRange): void {
    const newObj = {
      start: new Date(dateRange.startDate),
      end: new Date(dateRange.endDate)
    };
    this.surfaceBet.displayFrom = isNaN(newObj.start.getTime()) ? this.surfaceBet.displayFrom : newObj.start.toISOString();
    this.surfaceBet.displayTo = isNaN(newObj.end.getTime()) ? this.surfaceBet.displayTo : newObj.end.toISOString();
    this.validateSelection();
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
    this.setReferences();
    if (this.surfaceBet.id) {
      this.updateRequest();
    } else {
      this.createRequest();
    }
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

    if (this.surfaceBet.id) {
      this.globalLoaderService.showLoader();
      this.sportsSurfaceBetsService.uploadIcon(
        this.surfaceBet.id,
        file
      ).map((response: HttpResponse<SurfaceBet>) => response.body)
        .subscribe((bet: SurfaceBet) => {
          this.setEventAndCategoryIds(bet);
          this.actionButtons.extendCollection(bet);
          this.surfaceBet = this.updateEditableFields(bet, this.surfaceBet);
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
    if (this.surfaceBetId) {
      this.removeIconRequest();
    } else {
      this.iconUploadInput.nativeElement.value = '';
      this.imageToUpload.name = '';
      this.imageToUpload.file = '';
    }
  }

  public get uploadButtonText(): string {
    if (this.surfaceBet.svgFilename && this.surfaceBet.svgFilename.filename || this.imageToUpload.name) {
      return 'Change Icon';
    } else {
      return 'Upload Icon';
    }
  }

  public trackSportById(sport: SportCategory): string {
    return sport.id;
  }

  public setPrice(price: Price): void {
    price.priceType = 'LP';
    if (price.priceNum && price.priceDen) {
      price.priceDec = this.fracToDecService.fracToDec(price.priceNum, price.priceDen) as number;
    } else {
      price.priceDec = null;
    }
  }

  public validateSelection(): void {
    if(this.isHomePage) {
      return;
    }

    let betsWithSameSelection;
    if (this.surfaceBet.disabled) {
      betsWithSameSelection = [];
    } else {
      const currentDate = (new Date()).getTime();
      const currentBetTime = (new Date(this.surfaceBet.displayTo)).getTime();
      betsWithSameSelection = _.filter(this.allSurfaceBets, (bet) => {
        if(!bet.universalSegment && (!bet.inclusionList || bet.inclusionList.length === 0)) {
          return false;
        }
        const betTime = (new Date(bet.displayTo)).getTime();
        return (bet.selectionId && this.surfaceBet.selectionId) 
        && bet.selectionId.toString() === this.surfaceBet.selectionId.toString() 
        && bet.id !== this.surfaceBet.id && betTime >= currentDate && currentBetTime >= currentDate 
        && !bet.disabled;
      });
    }

    if (betsWithSameSelection.length) {
      const selectionIds = betsWithSameSelection.map(el => el.title).join(', ');
      this.error = `This selection ID is already used in: ${selectionIds}`;
    } else {
      this.error = null;
    }
  }

  private setReferences(): void {
    /**
     * to get surface bets on home page need reference
     * */
    _.remove(this.surfaceBet.categoryIDs, el => el === 0);
    if (this.surfaceBet.highlightsTabOn) {
      this.surfaceBet.categoryIDs.push(0);
    }

    // references to EDP
    const eventRefs = _.map(this.surfaceBet.eventIDs, (eventId) => {
      const id = this.surfaceBet.references.find((bet) => bet.refId === eventId)?.id;
      return {
        id: id,
        refId: eventId,
        relatedTo: 'edp',
        enabled: true
      };
    });

    // references to SLP
    const sportRefs = _.map(this.surfaceBet.categoryIDs, (categoryId) => {
      const sportId = this.surfaceBet.references.find((bet) => bet.refId === categoryId.toString())?.id;
      const sortOrder = this.surfaceBet.references.find((bet) => bet.refId === categoryId.toString())?.sortOrder;
      return {
        id: sportId,
        refId: categoryId.toString(),
        relatedTo: 'sport',
        enabled: true,
        sortOrder: sortOrder
      };
    });

    const eventHubRefs = _.map(this.mappedEventHubs, (eventHubIndex: number) => {
      const eventId = this.surfaceBet.references.find((bet) => bet.refId === eventHubIndex.toString())?.id
      const sortOrder = this.surfaceBet.references.find((bet) => bet.refId === eventHubIndex.toString())?.sortOrder
      return {
        id: eventId,
        refId: eventHubIndex.toString(),
        relatedTo: 'eventhub',
        enabled: true,
        sortOrder: sortOrder
      };
    });

    this.surfaceBet.references = [
      ...eventRefs,
      ...sportRefs,
      ...eventHubRefs
    ];
  }

  private removeIconRequest(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().deleteIcon(
      this.surfaceBet.id
    ).map((response: HttpResponse<SurfaceBet>) => response.body)
      .subscribe((data: SurfaceBet) => {
        this.surfaceBet = this.updateEditableFields(data, this.surfaceBet);
        this.snackBar.open(`Icon Removed.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().delete(this.surfaceBet.id).subscribe((response) => {
      this.globalLoaderService.hideLoader();
      this.router.navigate([this.getUrlToGoBack]);
    }, error => {
      this.globalLoaderService.hideLoader();
    });
  }

  private createRequest(): void {
    this.globalLoaderService.showLoader();
    this.sportsSurfaceBetsService.saveWithIcon(this.surfaceBet, this.imageToUpload.file)
      .subscribe((bet: SurfaceBet) => {
        this.globalLoaderService.hideLoader();
        if (this.isHomePage) {
          this.surfaceBet = bet;
          let self = this;
          this.segmentStoreService.setSegmentValue(this.surfaceBet, CSPSegmentLSConstants.SURFACE_BET_TAB);
          this.dialogService.showNotificationDialog({
            title: 'Surface Bet',
            message: 'Surface Bet is Created.',
            closeCallback() {
              self.router.navigate([self.getUrlToGoBack]);
            }
          });
        } else {
          this.router.navigate([this.getUrlToGoEdit(bet.id)]);
        }
      }, error => {
        this.globalLoaderService.hideLoader();
        this.snackBar.open(`Sports Surface Bet creation Error!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  private updateRequest(): void {
    this.globalLoaderService.showLoader();
    let self = this;
    this.apiClientService.sportsSurfaceBets().update(this.surfaceBet)
      .map((response: HttpResponse<SurfaceBet>) => response.body)
      .subscribe((bet: SurfaceBet) => {
        this.surfaceBet = bet;
        this.setEventAndCategoryIds(bet);
        this.actionButtons.extendCollection(this.surfaceBet);
        if(this.isHomePage) {
          this.segmentStoreService.setSegmentValue(this.surfaceBet, CSPSegmentLSConstants.SURFACE_BET_TAB);
          this.dialogService.showNotificationDialog({
            title: 'Surface Bet',
            message: 'Surface Bet is Updated.',
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
    this.loadInitialData();
    this.isRevert = true;
  }



   private loadInitialData(): void {
    this.form = null;
    this.globalLoaderService.showLoader();
    forkJoin([
      this.sportsSurfaceBetsService.getSportCategories(),
      this.apiClientService.sportsSurfaceBets().findAllByBrand(this.brandService.brand),
      this.apiClientService.eventHub().getAllEventHubs(),
      this.apiClientService.fanzoneService().getAllFanzones()
    ]).map((response) => {
      const sports = response[0];
      this.isFanzoneSportCategory = this.sportConfigId && response[0].find(sport => sport.id === this.sportConfigId).categoryId === 160;
      const allBets = response[1].body;
      const allEventHubs = response[2];
      const fanzonesList = response[3].body.map((item) => {
        return {
          active: item.active,
          name: item.name,
          teamId: item.teamId
        };
      });
      return {
        sports,
        allBets,
        allEventHubs,
        fanzonesList
      };
    })
      .subscribe(({ sports, allBets, allEventHubs, fanzonesList }) => {
        if (this.surfaceBetId) {
          this.apiClientService.sportsSurfaceBets().findById(this.surfaceBetId).
            subscribe(res => {
              this.surfaceBet = res.body;
              this.setEventAndCategoryIds(this.surfaceBet);
              this.setFormDataAndValidate(sports, allBets, allEventHubs, fanzonesList);
            })
        } else {
          this.surfaceBet.brand = this.brandService.brand;
          this.setFormDataAndValidate(sports, allBets, allEventHubs, fanzonesList);
        }
      }, err => {
        this.globalLoaderService.hideLoader();
      });
  }

  setFormDataAndValidate(sports, allBets, allEventHubs, fanzonesList) {
    this.allEventHubs = allEventHubs;
        this.sportCategories = sports;
        this.allSurfaceBets = allBets;
        this.fanzoneInclusionList = fanzonesList;
        // To handle the select all fanzone scenario
        const intersectFzInclusionList =  _.intersection(_.map(this.fanzoneInclusionList, "teamId"), this.surfaceBet.fanzoneInclusions);
        this.allSelected = this.fanzoneInclusionList.length === intersectFzInclusionList.length;
        this.validateSelection();
        this.setupForm();
        this.getBreadcrumbs(this.params);
        this.globalLoaderService.hideLoader();
  }
  async getSBItem() {
    let response = await this.apiClientService.sportsSurfaceBets().
      findById(this.surfaceBetId).pipe(map(res => res.body)).toPromise();
    return response;
  }

  private setEventAndCategoryIds(bet: SurfaceBet): void {
    if (bet && bet.references) {
      bet.categoryIDs = _.map(_.filter(bet.references, item => item.relatedTo === 'sport' && item.enabled), el => parseInt(el.refId, 10));
      bet.eventIDs = _.map(_.filter(bet.references, item => item.relatedTo === 'edp' && item.enabled), el => el.refId);
      this.mappedEventHubs = _.map(
        _.filter(bet.references, item => item.relatedTo === 'eventhub' && item.enabled),
        el => parseInt(el.refId, 10)
      );
    }
  }

  private setupForm(): void {
    const pricePattern = '^[1-9][0-9]*';

    this.form = new FormGroup({
      eventIDs: new FormControl(this.surfaceBet.eventIDs, []),
      title: new FormControl(this.surfaceBet.title, [Validators.required]),
      content: new FormControl(this.surfaceBet.content, []),
      contentHeader: new FormControl(this.surfaceBet.contentHeader, []),
      selectionId: new FormControl(this.surfaceBet.selectionId, [Validators.required]),
      priceNum: new FormControl(this.surfaceBet.price.priceNum, [Validators.pattern(pricePattern)]),
      priceDen: new FormControl(this.surfaceBet.price.priceDen, [Validators.pattern(pricePattern)]),
      categoryIDs: new FormControl(this.surfaceBet.categoryIDs, []),
      mappedEventHubs: new FormControl(this.mappedEventHubs, []),
      icon: new FormControl(),
      highlightsTabOn: new FormControl(this.surfaceBet.highlightsTabOn, []),
      edpOn: new FormControl(this.surfaceBet.edpOn, []),
      displayOnDesktop:  new FormControl(this.surfaceBet.displayOnDesktop, [])
    });
    this.isFanzoneSportCategory && this.form.addControl('fanzoneInclusions', new FormControl(this.surfaceBet.fanzoneInclusions, [Validators.required]));
    this.segmentsList = {
      exclusionList: this.surfaceBet.exclusionList,
      inclusionList: this.surfaceBet.inclusionList,
      universalSegment: this.surfaceBet.universalSegment
    };

    this.form.patchValue({title : ''});
    this.form.patchValue({title : this.surfaceBet.title});
    this.updateSurfaceBetTitle();
  }

/**
 * Update SurfaceBetTitle on based of the API response surfaceBetTitle
 */
  updateSurfaceBetTitle(){
    this.filteredSurfaceBetTitle = this.form?.get('title')?.valueChanges
    .pipe(
      startWith<string>(''),
      map(name => {
      let title = this.form?.get('title').value;
      return  title ? this.filterDropDown(title) : this.surfaceBetTitle.slice();
     })
      );
  }

  /**
   * Handles logic for filtering the drop down list 
   * @param {string} name
   * @returns - {SurfaceBetTitle[]} 
  */
  private filterDropDown(name : string): SurfaceBetTitle[] {
    const filterValue = name.toLowerCase();
    return this.surfaceBetTitle.filter(option => option.title.toLowerCase().indexOf(filterValue) === 0);
  }

  private updateEditableFields(targetObject: SurfaceBet, source: SurfaceBet): SurfaceBet {
    return _.extend(targetObject,
      _.pick(source, ['title', 'displayFrom ', 'displayTo', 'eventIDs', 'disabled', 'highlightsTabOn', 'edpOn', 'displayOnDesktop', 'content',
        'selectionId', 'categoryIDs', 'price', 'references'])
    );
  }

  private getBreadcrumbs(params: Params): void {
    const title: string = this.surfaceBet.id ? this.surfaceBet.title : 'Create';

    this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
      customBreadcrumbs: [
        {
          label: title
        }
      ]
    }).subscribe((breadcrumbsData: Breadcrumb[]) => {
      this.breadcrumbsData = breadcrumbsData;
    });
  }

  private getUrlToGoEdit(betId: string): string {
    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/surface-bets/${this.moduleId}/bet/edit/${betId}`;
    } else if (this.hubId) {
      return `sports-pages/event-hub/${this.hubId}/sports-module/surface-bets/${this.moduleId}/bet/edit/${betId}`;
    } else {
      return `sports-pages/homepage/sports-module/surface-bets/${this.moduleId}/bet/edit/${betId}`;
    }
  }

  private get getUrlToGoBack(): string {
    if (this.sportConfigId) {
      return `sports-pages/sport-categories/${this.sportConfigId}/sports-module/surface-bets/${this.moduleId}`;
    } else if (this.hubId) {
      return `sports-pages/event-hub/${this.hubId}/sports-module/surface-bets/${this.moduleId}`;
    } else {
      return `sports-pages/homepage/sports-module/surface-bets/${this.moduleId}`;
    }
  }

  /**
   * updates issegmentvalid true/false on child form changes
  */
  isSegmentFormValid(val: boolean): void {
    this.isSegmentValid = val;
  }

  /**
   * Highlights checkbox will be checked automatically when displayOnDesktop is checked
   */
  onDisplayOnDesktopCheck(): void{
    if(this.surfaceBet.displayOnDesktop){
      this.surfaceBet.highlightsTabOn = true;
    }
  }
  /*
   * Handles logic for child emitted data.
  */
  modifiedSegmentsHandler(data: ISegmentModel): void {
    this.isRevert = false;
    this.surfaceBet = { ...this.surfaceBet, ...data };
  }

  /*** Handles remove icon visibility ***/
  enableRemoveIconBtn(): boolean {
    return (this.surfaceBet.svgFilename && this.surfaceBet.svgFilename.filename) || this.imageToUpload.name ? true : false;
  }

  toggleAllSelection(): void {
    if (this.allSelected) {
      this.select.options.forEach((item: MatOption) => item.select());
    } else {
      this.select.options.forEach((item: MatOption) => item.deselect());
    }
  }
  optionClick(): void {
    this.allSelected = !this.select.options.some(option => option.selected  ===  false);
  }

 /**
   * Handles logic for deleting the Surface Bet Title 
   * @param {string} id
   * @returns - {void} 
  */
  deleteTitle(event: any,id:string): void{
    event.preventDefault();
    event.stopPropagation();
    this.dialogService.showConfirmDialog({
      title: 'Do you want to delete the surface bet title?',
      yesCallback: () => {
        this.sendRemoveRequest(id);
      }
    });
  }

  /**
   * send Remove Request for SurfaceBetTitle
   * @param id 
   */
  sendRemoveRequest(id : string) {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().deleteSurfaceBetTitle(
      this.brandService.brand,id
    ).subscribe((response) => {
      this.globalLoaderService.hideLoader();
      this.getSurfaceBetTitle();
    }, error => {
      this.globalLoaderService.hideLoader();
    });
  }
/**
   * Handles logic for getting Surface Bet Title 
   * @returns - {void} 
  */
  getSurfaceBetTitle() : void{
    this.apiClientService.sportsSurfaceBets().getSurfaceBetTitle(this.brandService.brand)
    .map((response: HttpResponse<SurfaceBetTitle[]>) => response.body)
    .subscribe((title: SurfaceBetTitle[]) => {
    this.surfaceBetTitle = title;
    this.updateSurfaceBetTitle();
    }, error => {
      this.globalLoaderService.hideLoader();
    });
  }

/**
 * Toggle Dropdowm sign
 */
  toggleDropDown(){
    this.isDropDownVisible = false;
  }

/**
 * Handle drop down sign if autoComplete div is open
 */
  handleOpen(){
    this.isDropDownVisible = false;
  }

 /**
 * Handle drop down sign if autoComplete div is closed
 */
  handleClosed(){
    this.isDropDownVisible = true;
  }
}
