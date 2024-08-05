import * as _ from 'lodash';

import { Component, Input, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import { IQuickLinkCreatedData } from '../models/sports-quick-links.models';
import { SportsQuickLink } from '@app/client/private/models/sportsquicklink.model';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { ApiClientService } from '@app/client/private/services/http';
import { ErrorService } from '@app/client/private/services/error.service';
import { SportQuickLinksService } from '../sport-quick-links.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { SportsQuickLinksCreateComponent } from '../sports-quick-links-create/sports-quick-links-create.component';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@app/client/private/models/segment.model';

@Component({
  selector: 'sports-quick-links',
  templateUrl: './sports-quick-links-list.component.html',
  styleUrls: ['sports-quick-links-list.scss']
})
export class SportsQuickLinksListComponent implements OnInit {
  @Input() sportId: number = 0;

  public hubIndex: number;
  public hubId: string;
  public sportsQuickLinks: SportsQuickLink[] = [];
  public error: string;
  public searchField: string = '';
  public segmentChanged: boolean = false;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public moduleId: string;
  public pageId: string;
  public pageType: string
  public dataTableColumns: DataTableColumn[] = [];
  public searchableProperties: Array<string> = [
    'title'
  ];
  public maxLinksAmount: number;
  public isLinksListValid: boolean = true;
  public isHomePage: boolean;
  public homePageDataTableColumns: DataTableColumn[];
  public eventHubDataTableColumns: DataTableColumn[];
  public orderMessage: string;
  public showSegmentDropdown: boolean = true;

  constructor(
    private apiClientService: ApiClientService,
    private sportQuickLinksService: SportQuickLinksService,
    private errorService: ErrorService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private activatedRoute: ActivatedRoute,
    private snackBar: MatSnackBar,
    private segmentStoreService: SegmentStoreService
  ) {
    this.isHomePage = this.segmentStoreService.validateHomeModule();
  }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.setDataTableColumns();

    // This will get the newly added segment and will filter the navigation points.
    this.moduleId = this.activatedRoute.snapshot.paramMap.get('moduleId');
    this.segmentStoreService.validateSegmentValue();
    this.getSegmentValue();

    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];

      this.pageId = this.hubId ? this.hubId : this.sportId.toString();
      this.pageType = this.hubId ? 'eventhub' : 'sport';

      this.getSportQuickLink();
    })
  }

  getSportQuickLink(): void {
    if (this.hubId) {
      this.sportQuickLinksService.getHubIndex(this.pageId)
        .subscribe((hubIndex: number) => {
          this.hubIndex = hubIndex;
          this.loadQuickLinks(hubIndex.toString(), this.pageType);
        });
    } else {
      this.loadQuickLinks(this.pageId, this.pageType);
    }
  }

  loadQuickLinks(pageId: string, pageType: string): void {
    if (!this.hubId) {
      this.loadSegmentedLinks(pageId, pageType);
    } else {
      this.sportQuickLinksService.loadQuickLinks(pageId, pageType)
        .subscribe((sportsQuickLinks: SportsQuickLink[]) => {
          this.maxLinksAmount = this.sportQuickLinksService.maxLinksAmount;
          this.isLinksListValid = this.sportQuickLinksService.isLinksListValid;
          if (this.hubId) {
            this.sportsQuickLinks = sportsQuickLinks;
          }
          this.globalLoaderService.hideLoader();
        }, (error: string) => {
          this.error = error;
          this.globalLoaderService.hideLoader();
        });
    }
  }

  loadSegmentedLinks(pageId: string, pageType: string, segment?: string): void {
    this.sportQuickLinksService.loadSegmentQuickLinks(this.selectedSegment, pageId, pageType).subscribe((quickLinks: SportsQuickLink[]) => {
      this.selectedSegment = segment ? segment : this.selectedSegment;
      this.maxLinksAmount = this.sportQuickLinksService.maxLinksAmount;
      this.isLinksListValid = this.sportQuickLinksService.isLinksListValid;
      this.sportsQuickLinks = quickLinks;
      this.orderMessage = this.sportsQuickLinks.length ? this.sportsQuickLinks[0].message : '';
      this.segmentChanged = true;
      this.showSegmentDropdown = true;
      this.globalLoaderService.hideLoader();
    })
  }

  createSportsQuickLink(): void {
    this.dialogService.showCustomDialog(SportsQuickLinksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Sport Quick Link',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: {
        hubIndex: this.hubIndex,
        pageType: this.hubIndex ? 'eventhub' : 'sport',
        id: this.sportId
      },      
      yesCallback: (createSportData: IQuickLinkCreatedData) => {
        let {createdSportsQuickLinkData, savedSportsQuickLink} = createSportData;
        this.globalLoaderService.showLoader();
            if (this.isHomePage) {
              this.showSegmentDropdown = false;
              this.selectedSegment = savedSportsQuickLink.inclusionList.length !== 0 ? savedSportsQuickLink.inclusionList[0] : CSPSegmentConstants.UNIVERSAL_TITLE;
              this.segmentHandler(this.selectedSegment);
            } else {
              createdSportsQuickLinkData.link.id = savedSportsQuickLink.id;
              this.sportsQuickLinks.push(createdSportsQuickLinkData.link);
            }
            this.globalLoaderService.hideLoader();
            this.snackBar.open(`Sports quick created!`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
      }
    });
  }

  removeHandler(sportsQuickLink: SportsQuickLink): void {
    this.dialogService.showConfirmDialog({
      title: 'Sport Quick Link',
      message: 'Are You Sure You Want to Remove Sport Quick Link?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportsQuickLink()
          .delete(sportsQuickLink.id)
          .subscribe(() => {
            _.remove(this.sportsQuickLinks, { id: sportsQuickLink.id });
            this.sportsQuickLinks = this.sportQuickLinksService.validateLinks(this.sportsQuickLinks);
            this.isLinksListValid = this.sportQuickLinksService.isLinksListValid;

            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(order: Order): void {
    this.apiClientService
      .sportsQuickLink()
      .reorder(order)
      .subscribe(() => {
        this.snackBar.open(`Sports quick link order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  // Gets the navigation points based on Segment selected.
  public segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.SPORTS_QUICK_LINK, segmentValue: segment });
    this.globalLoaderService.showLoader();
    this.loadSegmentedLinks(this.pageId, this.pageType, segment);
  }

  private getSegmentValue(): void {
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.SPORTS_QUICK_LINK) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
  }

  private setDataTableColumns(): void {
    this.homePageDataTableColumns = [
      {
        'name': 'Title',
        'property': 'title',
        'link': {
          hrefProperty: 'id'
        },
        'type': 'link'
      },
      {
        'name': 'Segment(s)',
        'property': 'inclusionList',
        'type': 'array'
      },
      {
        'name': 'Segment(s) Exclusion',
        'property': 'exclusionList',
        'type': 'array'
      },
      {
        name: 'Url',
        property: 'destination',
        width: 2
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        'name': 'Validity Period Start',
        'property': 'validityPeriodStart',
        'type': 'date'
      },
      {
        'name': 'Validity Period End',
        'property': 'validityPeriodEnd',
        'type': 'date'
      }
    ];

    this.eventHubDataTableColumns = [
      {
        'name': 'Title',
        'property': 'title',
        'link': {
          hrefProperty: 'id'
        },
        'type': 'link'
      },
      {
        name: 'Url',
        property: 'destination',
        width: 2
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        'name': 'Validity Period Start',
        'property': 'validityPeriodStart',
        'type': 'date'
      },
      {
        'name': 'Validity Period End',
        'property': 'validityPeriodEnd',
        'type': 'date'
      }
    ];

    this.dataTableColumns = this.isHomePage ? this.homePageDataTableColumns : this.eventHubDataTableColumns;
  }
}
