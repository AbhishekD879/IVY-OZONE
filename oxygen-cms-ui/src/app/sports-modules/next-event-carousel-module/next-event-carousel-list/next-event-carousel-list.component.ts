import { Component, Input, OnInit } from "@angular/core";
import * as _ from "lodash";
import { DataTableColumn } from "@app/client/private/models/dataTableColumn";
import { Order } from "@app/client/private/models/order.model";
import { HttpResponse } from "@angular/common/http";
import { ApiClientService } from "@app/client/private/services/http";
import { DialogService } from "@app/shared/dialog/dialog.service";
import { GlobalLoaderService } from "@app/shared/globalLoader/loader.service";
import { ErrorService } from "@app/client/private/services/error.service";
import {
  AppConstants,
  CSPSegmentConstants,
  CSPSegmentLSConstants,
} from "@app/app.constants";
import { MatSnackBar } from "@angular/material/snack-bar";
import { BrandService } from "@app/client/private/services/brand.service";
import { ActivatedRoute, Params } from "@angular/router";
import { SegmentStoreService } from "@app/client/private/services/segment-store.service";
import { ISegmentMsg } from "@root/app/client/private/models/segment.model";
import { SportsNextEventCarousel } from "@app/client/private/models/sportsNextEventCarousel.model";

@Component({
  selector: "app-next-event-carousel-list",
  templateUrl: "./next-event-carousel-list.component.html",
  styleUrls: ["./next-event-carousel-list.component.scss"],
})
export class NextEventCarouselListComponent implements OnInit {
  @Input() sportId: number = 0;

  public searchField: string;
  public segmentChanged: boolean = false;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public error: string;
  public orderMessage: string;

  public nextEventCarousels: SportsNextEventCarousel[];
  public moduleId: string;
  public dataTableColumns: DataTableColumn[] = [];
  public searchableProperties: Array<string> = ["title"];
  public eventHubDataTableColumns: DataTableColumn[];
  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private snackBar: MatSnackBar,
    private brandService: BrandService,
    private activatedRoute: ActivatedRoute,
    private segmentStoreService: SegmentStoreService
  ) {}

  public ngOnInit(): void {
    this.setDataTableColumns();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.segmentStoreService.validateSegmentValue();
      this.segmentStoreService
        .getSegmentMessage()
        .subscribe((segmentMsg: ISegmentMsg) => {
          if (
            segmentMsg.segmentModule ===
            CSPSegmentLSConstants.NEXT_EVENT_CAROUSEL
          ) {
            this.selectedSegment = segmentMsg.segmentValue;
          }
        });
      this.loadCarouselsBySegment();
    });
  }


  public removeHandler(nextEventCarousel: SportsNextEventCarousel): void {
    this.dialogService.showConfirmDialog({
      title: "Next Event Carousel",
      message: "Are You Sure You Want to Remove Next Event Carousel?",
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService
          .sportsNextEventCarousel()
          .delete(nextEventCarousel.id)
          .subscribe(
            () => {
              _.remove(this.nextEventCarousels, { id: nextEventCarousel.id });
              this.globalLoaderService.hideLoader();
            },
            (error) => {
              this.errorService.emitError(error.message);
              this.globalLoaderService.hideLoader();
            }
          );
      },
    });
  }

  public reorderHandler(order: Order): void {
    this.apiClientService
      .sportsNextEventCarousel()
      .reorder(order)
      .subscribe(() => {
        this.snackBar.open(`Next Event Carousel order saved!`, "Ok!", {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }


  private loadCarouselsBySegment(): void {

    this.globalLoaderService.showLoader();
    this.moduleId = this.activatedRoute.snapshot.paramMap.get("moduleId");
    this.segmentStoreService.validateSegmentValue();
    this.segmentStoreService
      .getSegmentMessage()
      .subscribe((segmentMsg: ISegmentMsg) => {
        if (
          segmentMsg.segmentModule === CSPSegmentLSConstants.NEXT_EVENT_CAROUSEL
        ) {
          this.selectedSegment = segmentMsg.segmentValue;
        }
      });
    this.apiClientService
      .sportsNextEventCarousel()
      .findAllByBrand(this.brandService.brand)
      .subscribe(
        (nextEventCarousel: HttpResponse<SportsNextEventCarousel[]>) => {
          this.nextEventCarousels = nextEventCarousel.body;
          this.orderMessage = this.nextEventCarousels.length
            ? this.nextEventCarousels[0].message
            : "";
          this.segmentChanged = true;
          this.globalLoaderService.hideLoader();
        },
        (error) => {
          this.error = error.message;
          this.globalLoaderService.hideLoader();
        }
      );
  }

  private setDataTableColumns(): void {
    this.eventHubDataTableColumns = [
      {
        name: "Title",
        property: "title",
        link: {
          hrefProperty: "id",
          path: "carousel/edit",
        },
        type: "link",
      },
      {
        name: "Display events",
        property: "limit"
      },
      {
        name: "Enabled",
        property: "disabled",
        type: "boolean",
        isReversed: true,
      },
    ];
   this.dataTableColumns = this.eventHubDataTableColumns;
  }
}
