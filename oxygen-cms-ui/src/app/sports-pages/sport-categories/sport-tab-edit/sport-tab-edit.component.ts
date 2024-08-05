import {Component, OnInit, ViewChild} from '@angular/core';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';
import {ActivatedRoute, Params} from '@angular/router';
import {ApiClientService} from '@app/client/private/services/http';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {HttpResponse} from '@angular/common/http';
import {SportTab, Markets} from '@app/client/private/models/sporttab.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AppConstants} from '@app/app.constants';
import {SportCategory} from '@app/client/private/models/sportcategory.model';
import {map, switchAll} from 'rxjs/operators';
import {Observable} from 'rxjs/Observable';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {SportTabFilter} from '@app/client/private/models/sporttabFilters.model';
import { SPORT_TAB_FILTERS_CONFIG } from '@app/sports-pages/sport-categories/sport-tab-filters/sport-tab-filters.config';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { DialogService } from '@app/shared/dialog/dialog.service'; 

import { Tier } from '@root/app/client/private/models/tier.enum';
@Component({
  selector: 'app-sport-tab-edit',
  templateUrl: './sport-tab-edit.component.html',
  styleUrls: ['./sport-tab-edit.component.scss']
})
export class SportTabEditComponent implements OnInit {

  public isLoading: boolean = false;
  public breadcrumbsData: Breadcrumb[];
  public sportTab: SportTab;
  private readonly filtersConfig = SPORT_TAB_FILTERS_CONFIG;
  public showMarketSwitcher: boolean = false;
  public searchField: string = '';
  public searchableProperties: Array<string> = ['templateMarketName'];
  isAddTable: boolean = false;
  sportParams: any;
  isMarketsEdited: boolean;
  isUntiedSport:boolean=false;
  //Added for market switcher table
  marketSwitcherColumns: Array<DataTableColumn> = [
    {
      name: 'Market Name',
      property: 'templateMarketName',
      type: 'text',
      width: 5
    },
    {
      name: 'Display Name',
      property: 'title',
      type: 'text',
      width: 2
    }
  ]

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.loadInitialData();
  }

  public saveChanges(message?): void {
    if (!this.isMarketsEdited) {
      this.getSportTabById(this.sportParams['sportTabId']).subscribe((sportTab: SportTab) => {
        if (sportTab.marketsNames && sportTab.marketsNames.length > 0) {
          this.sportTab.marketsNames = sportTab.marketsNames;
        }
        this.submitChanges(message);
      });
    } else {
      this.submitChanges(message);
    }
  }

  public submitChanges(message?): void {
    this.apiClientService
    .sportTabService()
    .edit(this.sportTab)
    .map((data: HttpResponse<SportTab>) => data.body)
    .subscribe((sportTab: SportTab) => {
      this.isMarketsEdited = false;
      this.sportTab = this.normalizeTab(sportTab);
      this.actionButtons.extendCollection(this.sportTab);
      this.snackBar.open(message? message: `Sport Tab is saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.showMarketSwitcherTable();
    });
  }

  public revertChanges(): void {
    this.loadInitialData();
  }

  public isValidForm(sportTab: SportTab): boolean {
    const filters = sportTab.filters || {};
    return !!(sportTab.displayName && sportTab.displayName.length > 0) && (sportTab.interstitialBanners?.bannerEnabled ?
      (((sportTab.interstitialBanners?.mobileBannerId) || (sportTab.interstitialBanners?.desktopBannerId))  && 
        (sportTab.interstitialBanners?.bannerPosition)) : true) &&
      !Object.values(filters).some((f: SportTabFilter<any>) => f && f.enabled && !(f.values && f.values.length));
  }

  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute
      .params
      .pipe(
        map((params: Params) => {
          this.sportParams = params;
          const sportTab = this.getSportTabById(params['sportTabId']);
          const sportCategory = this.getSportCategoryById(params['id']);
          return forkJoin([sportTab, sportCategory]);
        }),
        switchAll())
      .subscribe(([sportTab, sport]) => {
        this.buildBreadCrumbsData(sportTab, sport);
        this.sportTab = this.normalizeTab(sportTab);
        this.addInitialBannerData(sport);
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.showMarketSwitcherTable();
      });
  }
  private addInitialBannerData(sport) {
    if (sport.tier === Tier.UNTIED) {
      this.isUntiedSport = true;
    }
    if (this.sportTab.interstitialBanners === null)
    {
      this.sportTab.interstitialBanners = {
        desktopBannerId: "",
        mobileBannerId: "",
        bannerPosition: "",
        bannerEnabled: false,
        ctaButtonLabel: "",
        redirectionUrl: ""
      }
    }
  }

  private getSportTabById(id: string): Observable<SportTab> {
    return this.apiClientService
      .sportTabService()
      .getById(id)
      .map((response: HttpResponse<SportTab>) => response.body);
  }

  private getSportCategoryById(id: string): Observable<SportCategory> {
    return this.apiClientService
      .sportCategory()
      .findOne(id)
      .map((data: HttpResponse<SportCategory>) => data.body);
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

  private buildBreadCrumbsData(tab: SportTab, sport: SportCategory) {
    this.breadcrumbsData = [{
      label: `Sport Categories`,
      url: `/sports-pages/sport-categories`
    }, {
      label: sport.imageTitle,
      url: `/sports-pages/sport-categories/${sport.id}`
    }, {
      label: tab.displayName,
      url: `/sports-pages/sport-categories/${sport.id}/sport-tab/${tab.id}`
    }];
  }

  private normalizeTab(sportTab: SportTab): SportTab {
    Object.keys(this.filtersConfig).forEach((filterName: string) => {
      const config = this.filtersConfig[filterName];

      if (config && config.tabs && config.tabs.indexOf(sportTab.name) >= 0) {
        if (!sportTab.filters) { sportTab.filters = {}; }
        if (!sportTab.filters[filterName]) { sportTab.filters[filterName] = {}; }
        if (!sportTab.filters[filterName].values) {
          sportTab.filters[filterName].values = [];
          sportTab.filters[filterName].enabled = false;
        }
      }
    });

    return sportTab;
  }

  /**
   * handle deleting row
   * Display Remove market confirmation popup
   * @param rowData 
   */
   removeRow(rowData: Markets): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Market',
      message: 'Are You Sure You Want to Remove Market?',
      yesCallback: () => {
       this.sendRemoveRequest(rowData);
      }
    });
  }

  /**
   * Send SAVE API request
   * Removes selected market from marketsNames array
   * @param rowData 
   */
   sendRemoveRequest(rowData: Markets): void {
    if(this.sportTab.marketsNames.length === 1) {
      this.snackBar.open(`Cannot delete default market!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    } else {
      this.sportTab.marketsNames = this.sportTab.marketsNames.filter(item => item.templateMarketName !== rowData.templateMarketName);
      this.isMarketsEdited = true;
      this.saveChanges('Market Switcher Labels is removed!');
    }
   }

  /**
   * Condition to check if to display market switcher table
   * retuns {boolean}
   */
  showMarketSwitcherTable(): void {
    this.showMarketSwitcher = false;
    setTimeout(() => {
      const tabs = ['matches', 'competitions', 'golf_matches'];
      this.showMarketSwitcher = tabs.indexOf(this.sportTab.name.toLocaleLowerCase()) !== -1;
    }, 1);
  }

  /**
   * To enable/disable- Add market Button
   */
  addMarket(): void {
    this.isAddTable = true;
  }

  /**
   * Remove Market for market switcher table
   * @param data
   */
  removeNewMarket(data): void {
    this.isAddTable = data;
  }

  /**
   * handle Add new market
   * push new market sportTab
   * @param data
   */

  addNewmarket(data): void {
    if(!this.sportTab.marketsNames){
      this.sportTab.marketsNames = [];
    }
    this.sportTab.marketsNames.push({
      'templateMarketName': data.templateMarketName,
      'title': data.title,
      'aggregated': data.aggregated
    });
    this.isAddTable = false;
    this.isMarketsEdited = true;
    this.saveChanges('Market Switcher Labels is saved!');
  }

  /**
   * handle Reordering of markets
   * @param data
   */
  reorderMarkets(data): void {
    this.sportTab.marketsNames = data;
    this.isMarketsEdited = true;
    this.saveChanges('Market Switcher Labels is saved!');
  }

}
