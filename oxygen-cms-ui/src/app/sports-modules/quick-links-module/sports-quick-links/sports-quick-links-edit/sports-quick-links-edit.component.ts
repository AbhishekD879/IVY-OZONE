import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { mergeMap } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import * as _ from 'lodash';
import { MatSelect } from '@angular/material/select';
import { MatOption } from '@angular/material/core';

import { SportQuickLinksService } from '../sport-quick-links.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SportsQuickLink } from '@app/client/private/models/sportsquicklink.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { ISegmentModel, ISegmentMsg } from '@app/client/private/models/segment.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { FanzoneInclusionList } from '@app/client/private/models/surfaceBet.model';

@Component({
  templateUrl: './sports-quick-links-edit.component.html',
  styleUrls: ['./sports-quick-links-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class SportsQuickLinksEditComponent implements OnInit {
  public sportsQuickLink: SportsQuickLink;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  public maxLinksAmount: number;
  public isLinkVlid: boolean = true;
  public error: string;
  public isRevert = false;
  public isHomePage: boolean;

  currentSportConfigId: string;
  currentLinkId: string;
  currentModuleId: string;
  hubId: string;
  hubIndex: number;
  isIMActive: boolean;
  segmentsList: ISegmentModel;
  isSegmentValid: boolean = false;
  selectedQuickLink:SportsQuickLink;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public isFanzoneSportCategory: boolean;
  public fanzoneInclusionList: FanzoneInclusionList[] = [];
  public allSelected = false;
  @ViewChild('select') select: MatSelect;
  @ViewChild('actionButtons') actionButtons;

  private sportsQuickLinkList: SportsQuickLink[];
  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private sportQuickLinksService: SportQuickLinksService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private brandService: BrandService,
    private segmentStoreService: SegmentStoreService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
    this.isIMActive = this.brandService.isIMActive();
    this.isHomePage = this.segmentStoreService.validateHomeModule();
    this.isSegmentValid = !this.isHomePage;
  }

  ngOnInit(): void {
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.SPORTS_QUICK_LINK) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];
      this.currentSportConfigId = params['id'];
      this.currentLinkId = params['linkId'];
      this.currentModuleId = params['moduleId'];

      this.apiClientService.sportsQuickLink()
        .findOne(params['linkId'])
        .map((data: HttpResponse<SportsQuickLink>) => {
          this.selectedQuickLink = data.body;
          return this.selectedQuickLink;
        })
        .pipe(mergeMap((sportsQuickLink: SportsQuickLink) => {
          // load all QL to validate vurrent link schedule time
          return this.loadAllLinksForSport(sportsQuickLink.sportId.toString(), sportsQuickLink.id);
        }))
        .pipe(mergeMap((sportsQuickLink: SportsQuickLink) => {  // set breadcrumbs
          const title: string = sportsQuickLink.title;

          return this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
            customBreadcrumbs: [
              {
                label: title
              }
            ]
          })
            .map((breadcrumbsData: Breadcrumb[]) => {
              this.breadcrumbsData = breadcrumbsData;
              return sportsQuickLink;
            });
        }))
        .subscribe((sportsQuickLink: SportsQuickLink) => {
          this.sportsQuickLink = sportsQuickLink;
          this.maxLinksAmount = this.sportQuickLinksService.maxLinksAmount;
          this.validateLink();

          this.form = new FormGroup({
            title: new FormControl(this.sportsQuickLink.title, [Validators.required]),
            destination: new FormControl(this.sportsQuickLink.destination, [
              Validators.required,
              Validators.pattern('^(http|https):\/\/(.*)')
            ]),
            disabled: new FormControl(this.sportsQuickLink.disabled),
            validityPeriodStart: new FormControl(this.sportsQuickLink.validityPeriodStart),
            validityPeriodEnd: new FormControl(this.sportsQuickLink.validityPeriodEnd)
          });
          this.segmentsList = {
            exclusionList: this.sportsQuickLink.exclusionList,
            inclusionList: this.sportsQuickLink.inclusionList,
            universalSegment: this.sportsQuickLink.universalSegment
            };

            this.isFanzoneSportCategory = this.sportsQuickLink.sportId === 160;
            this.isFanzoneSportCategory && this.setupFanzoneInclusions();
            this.isFanzoneSportCategory && this.form.addControl('fanzoneInclusions', new FormControl(this.sportsQuickLink.fanzoneInclusions, [Validators.required]));

          this.globalLoaderService.hideLoader();
        }, error => {
          this.globalLoaderService.hideLoader();
        });
    });
  }

  loadAllLinksForSport(sportId: string, linkId: string): Observable<SportsQuickLink> {
    let pageType = 'sport';

    if (this.hubId) {
      pageType = 'eventhub';

      return this.sportQuickLinksService.getHubIndex(this.hubId)
        .pipe(mergeMap((hubIndex: number) => {
          this.hubIndex = hubIndex;
          return this.loadQuickLinks(hubIndex.toString(), pageType, linkId);
        }));
    }

    return this.loadQuickLinks(sportId, pageType, linkId);
  }

  loadQuickLinks(pageId: string, pageType: string, linkId: string): Observable<SportsQuickLink> {
    if(pageType == 'eventhub') {
    return this.sportQuickLinksService.loadQuickLinks(pageId, pageType)
      .map((sportsQuickLinkList: SportsQuickLink[]) => {
        this.sportsQuickLinkList = sportsQuickLinkList;
        return this.selectedQuickLink; // Creating object to store the individual quick link data to display segmented data without universal in array.
      });
    } else {
     return this.sportQuickLinksService.loadSegmentQuickLinks(this.selectedSegment, pageId, pageType)
     .map((sportsQuickLinkList: SportsQuickLink[])  => {
      this.sportsQuickLinkList = sportsQuickLinkList;
      return this.selectedQuickLink; // Creating object to store the individual quick link data to display segmented data without universal in array.
     })
    }
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsQuickLink()
      .update(this.sportsQuickLink)
      .map((data: HttpResponse<SportsQuickLink>) => {
        return data.body;
      })
      .subscribe((data: SportsQuickLink) => {
        const self = this;
        this.sportsQuickLink = data;
        this.actionButtons.extendCollection(this.sportsQuickLink);
        this.segmentStoreService.setSegmentValue(this.sportsQuickLink, CSPSegmentLSConstants.SPORTS_QUICK_LINK);
        this.dialogService.showNotificationDialog({
          title: 'Sports Quick Link',
          message: 'Sports Quick Link is Saved.',
          closeCallback() {
            if(self.isHomePage) {
            self.router.navigate([`/sports-pages/homepage/sports-module/sports-quick-links`, self.currentModuleId]);
            }
          }
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
    this.isRevert = true;
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsQuickLink()
      .delete(this.sportsQuickLink.id)
      .subscribe(() => {
        const urlToGoBack = this.getUrlToGoBack();
        this.globalLoaderService.hideLoader();
        this.router.navigate([urlToGoBack]);
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  getUrlToGoBack() {
    if (this.hubId) {
      return `${this.breadcrumbsData[this.breadcrumbsData.length - 2].url}`;
    }

    if (this.currentSportConfigId) {
      return `sports-pages/sport-categories/${this.currentSportConfigId}/sports-module/sports-quick-links/${this.currentModuleId}`;
    } else {
      return `sports-pages/homepage/sports-module/sports-quick-links/${this.currentModuleId}`;
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

  uploadIconHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsQuickLink()
      .uploadIcon(this.sportsQuickLink.id, file)
      .map((data: HttpResponse<SportsQuickLink>) => {
        return data.body;
      })
      .subscribe((data: SportsQuickLink) => {
        this.sportsQuickLink = _.extend(data,
          _.pick(this.sportsQuickLink, 'title', 'destination', 'validityPeriodEnd', 'validityPeriodStart')
        );
        this.snackBar.open(`Icon Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeIconHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsQuickLink()
      .removeIcon(this.sportsQuickLink.id)
      .map((data: HttpResponse<SportsQuickLink>) => {
        return data.body;
      })
      .subscribe((data: SportsQuickLink) => {
        this.sportsQuickLink = _.extend(data,
          _.pick(this.sportsQuickLink, 'title', 'destination', 'validityPeriodEnd', 'validityPeriodStart')
        );
        this.snackBar.open(`Icon Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  validateLink() {
    if (!this.isHomePage) {
      const listWithNewLink: SportsQuickLink[] = _.cloneDeep(this.sportsQuickLinkList);
      _.extend(_.find(listWithNewLink, link => link.id === this.sportsQuickLink.id), this.sportsQuickLink);

      this.isLinkVlid = this.sportQuickLinksService.isValidLink(this.sportsQuickLink, listWithNewLink);
    }
  }

  linkStateChange() {
    this.sportsQuickLink.disabled = !this.sportsQuickLink.disabled;
    this.validateLink();
  }

  validationHandler() {
    return this.form && this.form.valid && this.isLinkVlid && this.isSegmentValid;
  }

  handleDateUpdate(data: DateRange) {
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

  /*
  * Handles logic for child emitted data.
  */
  modifiedSegmentsHandler(data: ISegmentModel): void {
    this.isRevert = false;
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
