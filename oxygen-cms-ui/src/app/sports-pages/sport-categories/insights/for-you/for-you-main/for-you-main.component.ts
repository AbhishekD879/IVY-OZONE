import { Component, OnInit, ViewChild } from '@angular/core';
import { Breadcrumb, DataTableColumn , SportCategory } from '@root/app/client/private/models';
import { GlobalLoaderService } from "@app/shared/globalLoader/loader.service";
import { ActivatedRoute, Params } from "@angular/router";
import { map, switchAll } from "rxjs/operators";
import { ApiClientService } from "@app/client/private/services/http";
import { forkJoin } from "rxjs-compat/observable/forkJoin";
import { IsportTable, SportTab, trendingTabs } from "@root/app/client/private/models/sporttab.model";
import { HttpResponse } from "@angular/common/http";
import { ActionButtonsComponent } from '@root/app/shared/action-buttons/action-buttons.component';
import { INSIGHTS_DEFAULT_DATA } from '../../inisghts-tab/insights-mock';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';
import { InsightsService } from '../../insights.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';

@Component({
  selector: 'foryou-main',
  templateUrl: './for-you-main.component.html',
})

export class foryoumainComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  breadcrumbsData: Breadcrumb[];
  sportTab:SportTab;
  foryouSportTable:IsportTable[];
  readonly sportTabId = 'insights-forYou';
  forYouBets : trendingTabs;
  isUntiedSport:boolean = false;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: "Module",
      property: "tabname",
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
   ) {
  }

  ngOnInit(): void {
    this.loadInitialData();
  }

  private loadInitialData(): void {
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
        this.buildBreadCrumbsData(sportTab, sport);
        this.sportTab = sportTab;
        if(!sportTab?.trendingTabs.length){
          this.sportTab.trendingTabs = INSIGHTS_DEFAULT_DATA;
        }
        this.forYouBets = sportTab.trendingTabs.find(tab => tab.href === this.sportTabId);
        this.createForyouSportTable();
        this.globalLoaderService.hideLoader();
      },
      error => {
        this.dialogService.showNotificationDialog({
          title: 'Error occurred',
          message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  private createForyouSportTable() {
    this.foryouSportTable = [];
    this.forYouBets.popularTabs.forEach((tab) => {
      const tabHref = `${tab.href}/${tab?.id}`;
      this.foryouSportTable.push({
        href: tab && tabHref,   
        enable: tab && tab.enabled,
        tabname: tab && tab.headerDisplayName,
      });
    });
   }

  sportTabReorderHandler(event) {}

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
      {
        label: "foryou main",
        url: `/sports-pages/sport-categories/${sport.id}/sport-tab/${tab.id}/insightsTab/insights-forYou`,
      },
  ];
  }

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
  revertChanges() {
    this.loadInitialData();
  }
  public saveChanges(message?): void {
      this.submitChanges(message);
  }
  private submitChanges(message?): void {
    this.apiClientService
    .sportTabService()
    .edit(this.sportTab)
    .map((data: HttpResponse<SportTab>) => data.body)
    .subscribe((sportTab: SportTab) => {
      this.sportTab = sportTab;
      this.forYouBets = sportTab.trendingTabs.find(tab => tab.href === this.sportTabId);   
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
   * isValidForm
   * @param sportTab 
   * @returns {boolean} 
  */
  public isValidForm(sportTabData: SportTab): boolean {
    const forYouBets = sportTabData.trendingTabs.find(tab => tab.href === 'insights-forYou');
    return forYouBets && forYouBets.trendingTabName.length > 0 && forYouBets.trendingTabName.length <= 15;   
  }

}
