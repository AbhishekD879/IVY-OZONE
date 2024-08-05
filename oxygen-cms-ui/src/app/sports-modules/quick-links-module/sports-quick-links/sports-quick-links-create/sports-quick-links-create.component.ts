import { Component, ElementRef, Inject, OnInit, ViewChild } from '@angular/core';
import { MatSelect } from '@angular/material/select';
import { MatOption } from '@angular/material/core';

import { FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

import { SportQuickLinksService } from '../sport-quick-links.service';
import { ICreatedLinkData } from '../models/sports-quick-links.models';
import { SportsQuickLink } from '@app/client/private/models/sportsquicklink.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { DateRange } from '@app/client/private/models/dateRange.model';
import * as _ from 'lodash';
import { ISegmentModel } from '@app/client/private/models/segment.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { CmsAlertComponent } from '@app/shared/cms-alert/cms-alert.component';
import { ApiClientService } from '@app/client/private/services/http';
import { FanzoneInclusionList } from '@app/client/private/models/surfaceBet.model';

@Component({
  templateUrl: './sports-quick-links-create.component.html',
  styleUrls: ['./sports-quick-links-create.component.scss']
})
export class SportsQuickLinksCreateComponent implements OnInit {
  @ViewChild('quickLinkSvgUpload') private quickLinkSvgUpload: ElementRef;
  @ViewChild('requestError') private requestError: CmsAlertComponent;

  sportsQuickLinksList: SportsQuickLink[] = [];
  segmentsList: ISegmentModel;
  isSegmentValid: boolean = false;

  sportsQuickLink: SportsQuickLink = {
    // default automatically created values
    id: 'default',
    updatedBy: null,
    updatedAt: null,
    createdBy: null,
    createdAt: null,
    updatedByUserName: null,
    createdByUserName: null,

    sportId: 0,
    pageId: '',
    pageType: 'sport',
    brand: this.brandService.brand,
    disabled: true,
    sortOrder: null,
    destination: '',
    title: '',
    validityPeriodEnd: '',
    validityPeriodStart: '',
    svg: '',
    svgFilename: {
      filename: '',
      path: '',
      size: 0,
      filetype: '',
    },
    inclusionList: [],
    exclusionList: [],
    universalSegment: true,
    fanzoneInclusions: []
  };

  uploadImageName: string;
  imageToUpload: File;

  disabled: FormControl;
  title: FormControl;
  destination: FormControl;
  fanzoneInclusions: FormControl;
  maxLinksAmount: number;
  islinkPeriodValid: boolean = true;
  isIMActive: boolean;
  public isHomePage: boolean;
  public isFanzoneSportCategory: boolean;
  public fanzoneInclusionList: FanzoneInclusionList[] = [];
  public allSelected = false;
  @ViewChild('select') select: MatSelect;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private sportQuickLinksService: SportQuickLinksService,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private segmentStoreService: SegmentStoreService,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
  ) {
    this.disabled = new FormControl('', [Validators.required]);
    this.title = new FormControl('', [Validators.required]);
    this.destination = new FormControl('', [Validators.required]);
    this.isIMActive = this.brandService.isIMActive();
    this.isHomePage = this.segmentStoreService.validateHomeModule();
    this.isSegmentValid = !this.isHomePage;
  }

  ngOnInit() {

    const providedSportId = this.data.data && this.data.data.id;
    const hubIndex = this.data.data && this.data.data.hubIndex;
    this.sportsQuickLinksList = this.sportQuickLinksService.currentLinksList;
    this.maxLinksAmount = this.sportQuickLinksService.maxLinksAmount;

    this.segmentsList = {
      inclusionList: [],
      exclusionList: [],
      universalSegment: this.sportsQuickLink.universalSegment
    };

    if (providedSportId !== undefined) {
      this.sportsQuickLink.sportId = this.data.data.id;
      this.sportsQuickLink.pageId = this.data.data.id;
      this.sportsQuickLink.pageType = 'sport';
    }

    if (hubIndex) {
      this.sportsQuickLink.sportId = parseInt(hubIndex, 10);
      this.sportsQuickLink.pageId = hubIndex;
      this.sportsQuickLink.pageType = 'eventhub';
    }
    this.isFanzoneSportCategory = this.sportsQuickLink.sportId === 160;
    this.isFanzoneSportCategory && this.setupFanzoneInclusions();
    if (this.isFanzoneSportCategory) {
      this.fanzoneInclusions = new FormControl([], [Validators.required]);
    } 
  }

  get newLinkData(): ICreatedLinkData {
    return {
      link: this.sportsQuickLink,
      imageToUpload: this.imageToUpload
    };
  }

  isInValidDestinationUrl(): boolean {
    return this.sportsQuickLink.destination.length > 0 &&
      !(this.sportsQuickLink.destination.match(/^http:\/\//) ||
        this.sportsQuickLink.destination.match(/^https:\/\//));
  }

  linkStateChange(): void {
    this.sportsQuickLink.disabled = !this.sportsQuickLink.disabled;
    this.validateLink();
  }

  hadleUploadImageClick(): void {
    const input = this.quickLinkSvgUpload.nativeElement;

    input.click();
  }

  removeMainImage(): void {
    const input = this.quickLinkSvgUpload.nativeElement;

    input.value = '';

    this.uploadImageName = undefined;
    this.imageToUpload = undefined;
  }

  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file && file.type;

    if (!file) {
      return;
    }

    if (fileType !== 'image/svg+xml') {
      console.log('Error. Unsupported file type.', fileType);
      return;
    }

    this.uploadImageName = file.name;
    this.imageToUpload = file;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  validateLink(): void {
    if (!this.isHomePage) {
      const listWithNewLink: SportsQuickLink[] = _.cloneDeep(this.sportsQuickLinksList);

      listWithNewLink.push(this.sportsQuickLink);

      this.islinkPeriodValid = this.sportQuickLinksService.isValidLink(this.sportsQuickLink, listWithNewLink);
    }
  }

  handleDateUpdate(data: DateRange): void {
    this.sportsQuickLink.validityPeriodStart = data.startDate;
    this.sportsQuickLink.validityPeriodEnd = data.endDate;
    this.validateLink();
  }

  /**
  * updates issegmentvalid true/false on child form changes
  */
  isSegmentFormValid(val: boolean): void {
    this.isSegmentValid = val;
  }

  createQuickLink(createdSportsQuickLinkData: ICreatedLinkData) {
    this.globalLoaderService.showLoader();
    this.sportQuickLinksService.saveNewQuickLink(createdSportsQuickLinkData.link, createdSportsQuickLinkData.imageToUpload)
      .subscribe((savedSportsQuickLink: SportsQuickLink) => {
        let quickLinkObj = {
          createdSportsQuickLinkData: createdSportsQuickLinkData,
          savedSportsQuickLink: savedSportsQuickLink
        }
        this.globalLoaderService.hideLoader();
        this.dialogRef.close(quickLinkObj);
      }, (errorMsg) => {
        this.globalLoaderService.hideLoader();
          this.requestError.showError(errorMsg.error);
      });
  }

  /*)
  * Handles logic for child emitted data.
  */
  modifiedSegmentsHandler(data: ISegmentModel): void {
    this.sportsQuickLink = { ...this.sportsQuickLink, ...data };
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
      this.fanzoneInclusionList = fanzonesList;
      // To handle the select all fanzone scenario
      const intersectFzInclusionList =  _.intersection(_.map(this.fanzoneInclusionList, "teamId"), this.sportsQuickLink.fanzoneInclusions);
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
    this.allSelected = !this.select.options.some(option => option.selected  ===  false);
  }
}
