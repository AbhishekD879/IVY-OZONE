import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'lodash';

import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { Order } from '@app/client/private/models/order.model';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { HttpResponse } from '@angular/common/http';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActivatedRoute, Params } from '@angular/router';
import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';

@Component({
  selector: 'sports-highlight-carousels',
  templateUrl: './highlight-carousel-list.component.html',
  styleUrls: ['./highlight-carousel-list.component.scss']
})

export class SportsHighlightCarouselListComponent implements OnInit {
  @Input() sportId: number = 0;

  public searchField: string;
  public segmentChanged: boolean = false;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public error: string;

  public hubId: string;
  public orderMessage: string;

  public highlightCarousels: SportsHighlightCarousel[];
  public moduleId: string;
  public dataTableColumns: DataTableColumn[] = [];
  public searchableProperties: Array<string> = [
    'title'
  ];
  public isHomePage: boolean;
  public homePageDataTableColumns: DataTableColumn[];
  public eventHubDataTableColumns: DataTableColumn[];
  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private snackBar: MatSnackBar,
    private brandService: BrandService,
    private activatedRoute: ActivatedRoute,
    private sportsHighlightCarouselsService: SportsHighlightCarouselsService,
    private segmentStoreService: SegmentStoreService
  ) {
    this.isHomePage = this.segmentStoreService.validateHomeModule();
  }

  public ngOnInit(): void {
    this.setDataTableColumns();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];

      if (this.hubId) {
        this.sportsHighlightCarouselsService.getHubIndex(this.hubId)
          .subscribe((hubIndex: number) => {
            // for homepage sportId should be 0
            this.loadCarousels(hubIndex, 'eventhub');
          });
      } else {
        this.segmentStoreService.validateSegmentValue();
        this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
          if (segmentMsg.segmentModule === CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL) {
           this.selectedSegment = segmentMsg.segmentValue;
          }
        });
        this.loadCarouselsBySegment(this.sportId, 'sport');
      }
    });
  }

  public loadCarousels(pageId: number, pageType: string) {
    this.apiClientService.sportsHighlightCarousel().findAllByBrandAndSport(this.brandService.brand, pageId, pageType)
      .map((response: HttpResponse<SportsHighlightCarousel[]>) => response.body)
      .subscribe((carousels) => {
        this.highlightCarousels = carousels;
      }, (error: string) => {
        this.error = error;
      });
  }

  public removeHandler(highlightCarousel: SportsHighlightCarousel): void {
    this.dialogService.showConfirmDialog({
      title: 'Highlights Carousel',
      message: 'Are You Sure You Want to Remove Highlights Carousel?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportsHighlightCarousel()
          .delete(highlightCarousel.id)
          .subscribe(() => {
            _.remove(this.highlightCarousels, { id: highlightCarousel.id });
            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  public reorderHandler(order: Order): void {
    this.apiClientService
      .sportsHighlightCarousel()
      .reorder(order)
      .subscribe(() => {
        this.snackBar.open(`Highlights Carousel order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
  /**
   * get Highlights Carousel list based on segment selection
   * @param segment value
   */
  public segmentHandler(segment: string): void {
    this.globalLoaderService.showLoader();
    this.segmentChanged = false;
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL, segmentValue: segment });

    this.apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment(segment, this.sportId, 'sport').subscribe(
      (data: HttpResponse<SportsHighlightCarousel[]>) => {
        this.highlightCarousels = data.body;
        this.orderMessage = this.highlightCarousels .length ? this.highlightCarousels [0].message : '';
        this.selectedSegment = segment;
        this.segmentChanged = true;
        this.globalLoaderService.hideLoader();
      },
      (error) => {
        this.globalLoaderService.hideLoader();
      }
    );
  }

  private loadCarouselsBySegment(pageId, pageType): void {
    this.globalLoaderService.showLoader();
    this.moduleId = this.activatedRoute.snapshot.paramMap.get('moduleId')
    this.segmentStoreService.validateSegmentValue();
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.HIGHLIGHT_CAROUSEL) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
    this.apiClientService.sportsHighlightCarousel().getHighlightCarouselBySegment(this.selectedSegment, pageId, pageType)
      .subscribe((highlightCarousel:  HttpResponse<SportsHighlightCarousel[]>) => {
        this.highlightCarousels = highlightCarousel.body;
        this.orderMessage = this.highlightCarousels .length ? this.highlightCarousels [0].message : '';
        this.segmentChanged = true;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        this.globalLoaderService.hideLoader();
    });
  }

  private setDataTableColumns(): void {
    this.homePageDataTableColumns = [
      {
        name: 'Title',
        property: 'title',
        link: {
          hrefProperty: 'id',
          path: 'carousel/edit'
        },
        type: 'link'
      },{
        name: 'Segment(s)',
        property: 'inclusionList',
        type: 'array'
      }, {
        name: 'Segment(s) Exclusion',
        property: 'exclusionList',
        type: 'array'
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        name: 'Display in Desktop',
        property: 'displayOnDesktop',
        type: 'boolean'
      },
      {
        name: 'Display from',
        property: 'displayFrom',
        type: 'date'
      },
      {
        name: 'Display to',
        property: 'displayTo',
        type: 'date'
      }
    ];

    this.eventHubDataTableColumns = [
      {
        name: 'Title',
        property: 'title',
        link: {
          hrefProperty: 'id',
          path: 'carousel/edit'
        },
        type: 'link'
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        name: 'Display in Desktop',
        property: 'displayOnDesktop',
        type: 'boolean'
      },
      {
        name: 'Display from',
        property: 'displayFrom',
        type: 'date'
      },
      {
        name: 'Display to',
        property: 'displayTo',
        type: 'date'
      }
    ];

    this.dataTableColumns = this.isHomePage ? this.homePageDataTableColumns : this.eventHubDataTableColumns;
  }
}
