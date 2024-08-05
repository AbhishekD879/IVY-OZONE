import { Component, OnInit, ViewChild } from "@angular/core";
import { DataTableColumn, SportCategory} from "@app/client/private/models";
import { GlobalLoaderService } from "@app/shared/globalLoader/loader.service";
import { ActivatedRoute, Params } from "@angular/router";
import { map, switchAll } from "rxjs/operators";
import { ApiClientService } from "@app/client/private/services/http";
import { forkJoin } from "rxjs-compat/observable/forkJoin";
import { SportTab } from "@app/client/private/models/sporttab.model";
import { HttpResponse } from "@angular/common/http";
import { AppConstants } from "@app/app.constants";
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActionButtonsComponent } from "@app/shared/action-buttons/action-buttons.component";
import { INSIGHTS_DEFAULT_DATA } from "./insights-mock";
import { InsightsService } from "../insights.service";
import { DialogService } from '@root/app/shared/dialog/dialog.service';
 
@Component({
  selector: "app-insights",
  templateUrl: "./insights.component.html",
})
export class InsightsComponent implements OnInit {
  breadcrumbsData: any = [];
  treingBetsTabMock: any;
  insightsTable: any=[];
  sportTab:SportTab;
  public insightsDatatable: boolean = true;
  showCmsTable:boolean;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: "Tab Name",
      property: "trendingTabName",
      link: {
        hrefProperty: "href",
      },
      type: "link",
      width: 2,
    },
    {
      name: "Enabled",
      property: "enable",
      type: "boolean",
      width: 1,
    },
  ];

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private insightsService:InsightsService,
    private dialogService: DialogService,
  ) {}


  /**
   * load data with component init
   */
  ngOnInit(): void {
     this.loadInitialData();
  }
  /**
   * load data with component init
   */
  private loadInitialData(): void {
    this.showCmsTable=false;
    this.globalLoaderService.showLoader();
    this.activatedRoute.params
      .pipe(
        map((params: Params) => {
          const sportTab = this.insightsService.getSportTabById(params["sportTabId"]);
          const sportCategory = this.insightsService.getSportCategoryById(params["id"]);
          return forkJoin([sportTab, sportCategory]);
        }),
        switchAll()
      )
      .subscribe(([sportTab, sport]) => {
        this.sportTab = sportTab;
        if (!sportTab?.trendingTabs.length) {
          this.sportTab.trendingTabs = INSIGHTS_DEFAULT_DATA;
        }
        this.createSportTable();
        this.buildBreadCrumbsData(sportTab, sport);
        this.globalLoaderService.hideLoader();
      },
      error => {
        this.dialogService.showNotificationDialog({
          title: 'Error occurred',
          message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
        });
      });
  }
  /**
   * createSportTable
   * @param {Object}sportTab
   */
  private createSportTable() {
    this.insightsTable = [];
    this.sportTab.trendingTabs.forEach((tab) => {
      this.insightsTable.push({
        id:tab.id,
        href: tab && tab.href,
        enable: tab && tab.enabled,
        trendingTabName: tab && tab.trendingTabName,
      });
    });
    this.showCmsTable=true;
  }
  
  insightsTabReorderHandler(newOrder: any): void {
    this.insightsService.newOrder(newOrder)
    .subscribe((data: any) => {
      this.snackBar.open('Sport Tab Order Saved!', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  /**
   * it builds the breadcrumbs
   * @param tab 
   * @param sport 
   */
  private buildBreadCrumbsData(tab: SportTab, sport: SportCategory) {
    this.breadcrumbsData = [
      {
        label: `Sport Categories`,
        url: `/sports-pages/sport-categories`,
      },
      {
        label: sport.imageTitle,
        url: `/sports-pages/sport-categories/${sport.id}`,
      },
      {
        label: "insights Tab",
        url: `/sports-pages/sport-categories/${sport.id}/sport-tab/${tab.id}/insightsTab`,
      },
    ];
  }
  
  /**
   * it handle the save changes and revert changes
   * @param {string} event 
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
   * saveChanges
   * @param message 
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
      this.sportTab = sportTab;
      this.actionButtons.extendCollection(this.sportTab);
      this.snackBar.open(message? message: `Sport Tab is saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    
    },
    error => {
      this.dialogService.showNotificationDialog({
        title: 'Error occurred',
        message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
      });
    });
  }
  /**
   *  to be revert changes 
   */
  public revertChanges(): void {
    this.loadInitialData();
  }
/**
 * isValidForm
 * @param {object} sportTab 
 * @returns boolean
 */
  public isValidForm(sportTab: SportTab): boolean {
    return !!(sportTab.displayName && sportTab.displayName.length > 0 && sportTab.displayName && sportTab.displayName.length <=15) 
  }
}
