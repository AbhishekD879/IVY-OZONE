import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Params, Router } from '@angular/router';
import * as _ from 'lodash';
import { concatMap } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import { forkJoin } from 'rxjs/observable/forkJoin';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { HomeModule, HomeModuleExtented } from '@app/client/private/models/homemodule.model';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ISegmentMsg } from '@app/client/private/models/segment.model';
import { Location } from '@angular/common';

@Component({
  selector: 'app-featured-modules-list',
  templateUrl: './featured-modules-list.component.html',
  styleUrls: ['./featured-modules-list.component.scss']
})
export class FeaturedModulesListComponent implements OnInit {
  public hubId: string;
  public isLoading: boolean = false;
  public modules: HomeModuleExtented[] = [];
  public searchFieldActive: string = '';
  public searchFieldDisabled: string = '';
  public searchFieldExpired: string = '';
  public searchFieldUpcoing: string = '';
  public message: string;

  public searchableProperties: string[] = [
    'title'
  ];

  public dataTableColumns: DataTableColumn[];
  public homePageDataTableColumns: DataTableColumn[];
  public eventHubDataTableColumns: DataTableColumn[];
  public activeModules: HomeModuleExtented[] = [];

  private eventHubData: IEventHub;
  public segmentChanged: boolean = false;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public isHomePage: boolean;
  public orderMessage: string;
  public multyRemoveFlag:boolean=true;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private snackBar: MatSnackBar,
    private segmentStoreService: SegmentStoreService,
    private location: Location
  ) {
    this.isHomePage = this.location.path().includes('featured-modules');
  }

  ngOnInit(): void {
    this.showHideSpinner();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];
      this.setDataTableColumns();
      this.segmentStoreService.validateSegmentValue();
      this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
        if (segmentMsg.segmentModule === CSPSegmentLSConstants.FEATURED_TAB_MODULE) {
         this.selectedSegment = segmentMsg.segmentValue;
        }
      });
      this.loadModulesList(this.selectedSegment);
    });
  }

  private setDataTableColumns() {
    this.homePageDataTableColumns = [
      {
        name: 'Name',
        property: 'title',
        link: {
          hrefProperty: 'id',
          path: this.hubId ? 'featured-modules/edit' : '/featured-modules/edit'
        },
        type: 'link',
        width: 2
      },
      {
        name: 'Segment(s)',
        property: 'inclusionList',
        type: 'array'
      },
      {
        name: 'Segment(s) Exclusion',
        property: 'exclusionList',
        type: 'array'
      },
      {
        name: 'Enabled',
        property: 'enabled',
        type: 'boolean',
        width: 1
      },
      {
        name: 'Display From',
        property: 'displayFrom',
        type: 'date',
        width: 2
      },
      {
        name: 'Display To',
        property: 'displayTo',
        type: 'date',
        width: 2
      },
      {
        name: 'Channels',
        property: 'channels',
        width: 2
      },
      {
        name: 'Personalized',
        property: 'personalised',
        type: 'boolean',
        width: 1
      }
    ];

    this.eventHubDataTableColumns = [
      {
        name: 'Name',
        property: 'title',
        link: {
          hrefProperty: 'id',
          path: this.hubId ? 'featured-modules/edit' : '/featured-modules/edit'
        },
        type: 'link',
        width: 2
      },
      {
        name: 'Enabled',
        property: 'enabled',
        type: 'boolean',
        width: 1
      },
      {
        name: 'Display From',
        property: 'displayFrom',
        type: 'date',
        width: 2
      },
      {
        name: 'Display To',
        property: 'displayTo',
        type: 'date',
        width: 2
      },
      {
        name: 'Disp. Order',
        property: 'displayOrder',
        width: 1
      },
      {
        name: 'Channels',
        property: 'channels',
        width: 2
      },
      {
        name: 'Personalized',
        property: 'personalised',
        type: 'boolean',
        width: 1
      }
    ];

    this.dataTableColumns = this.isHomePage? this.homePageDataTableColumns : this.eventHubDataTableColumns;
  }

  private loadEventHubAndModules(hubId): Observable<HomeModule[]> {
    return this.apiClientService.eventHub().getEventHubById(hubId)
      .pipe(concatMap((hubData: IEventHub) => {
        this.eventHubData = hubData;

        return this.apiClientService.featuredTabModules().findAllByEventHubIndex(this.eventHubData.indexNumber)
          .map((modulesDataSesponce: HttpResponse<HomeModule[]>) => {
            return modulesDataSesponce.body;
          });
      }));
  }

  public createFeaturedTabModule(): void {
    if (this.hubId) {
      this.router.navigate([`featured-modules/add`], {
        relativeTo: this.activatedRoute
      });
    } else {
      this.router.navigate([`/featured-modules/add`]);
    }
  }

  public get modulesAmount(): ActiveInactiveExpired {
    return {
      active: this.activeModules.length,
      inactive: this.disabledModules.length,
      expired: this.expiredModules.length
    };
  }

  public removeModule(featuredModule: HomeModuleExtented): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Feature Tab Module',
      message: 'Are You Sure You Want to Remove Feature Tab Module?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.featuredTabModules().remove(featuredModule.id).subscribe(() => {
          this.globalLoaderService.hideLoader();
          this.modules = this.modules.filter(m => m.id !== featuredModule.id);
          this.activeModules = this.modules.filter((module) => module.enabled && !module.expired && !module.upcoming);
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Feature Tab Module is Removed.'
          });
        });
      }
    });
  }

  removeHandlerMulty(featuredTabIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Feature Tab Modules (${featuredTabIds.length})`,
      message: 'Are You Sure You Want to Remove Feature Tab Modules?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(featuredTabIds.map(id => this.apiClientService.featuredTabModules().remove(id)))
          .subscribe(() => {
            featuredTabIds.forEach((id) => {
              const index = _.findIndex(this.modules, { id: id });
              this.modules.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  // updates the list order to backend once the order id's array is emitted here.
  reorderHandler(order) {
    this.apiClientService
    .featuredTabModules()
    .reorder(order)
    .subscribe(() => {
        this.snackBar.open(`Featured Tab order saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  /**
   * get footerMenu list based on segment selection
   * @param segment value
   */
  segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.selectedSegment = segment;
    this.multyRemoveFlag = segment === CSPSegmentConstants.UNIVERSAL_TITLE;
    this.globalLoaderService.showLoader();
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.FEATURED_TAB_MODULE, segmentValue: segment });
    this.loadModulesList(segment);
    this.globalLoaderService.hideLoader();
  }

  public get disabledModules(): HomeModuleExtented[] {
    return this.modules.filter((module) => !module.enabled && !module.expired && !module.upcoming);
  }

  public get expiredModules(): HomeModuleExtented[] {
    return this.modules.filter((module) => module.expired);
  }

  public get upcomingModules(): HomeModuleExtented[] {
    return this.modules.filter((module) => module.upcoming);
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  private loadModulesList(segment: string): void {
    if (this.hubId) {
      this.loadEventHubAndModules(this.hubId)
        .subscribe((modulesList: HomeModuleExtented[]) => {
          modulesList.forEach((module: HomeModuleExtented) => {
            module.enabled = module.visibility.enabled;
            module.upcoming = new Date(module.visibility.displayFrom) > new Date();
            module.expired = new Date(module.visibility.displayTo) < new Date();
            module.displayFrom = module.visibility.displayFrom;
            module.displayTo = module.visibility.displayTo;
            module.channels = module.publishToChannels.join(', ');
            return module;
          });
          this.modules = modulesList;
          this.activeModules = this.modules.filter((module) => module.enabled && !module.expired && !module.upcoming);
          this.showHideSpinner(false);
        });
   } else {
     forkJoin([
       this.apiClientService.featuredTabModules().findAllByBrandAndSegment(true, segment),
       this.apiClientService.featuredTabModules().findAllByBrandAndSegment(false, segment)
       // @ts-ignore
     ]).map((data: HttpResponse<HomeModuleExtented[]>[]) => {
       return data[0].body.concat(data[1].body).map((module: HomeModuleExtented) => {
         module.enabled = module.visibility.enabled;
         module.upcoming = new Date(module.visibility.displayFrom) > new Date();
         module.expired = new Date(module.visibility.displayTo) < new Date();
         module.displayFrom = module.visibility.displayFrom;
         module.displayTo = module.visibility.displayTo;
         module.channels = module.publishToChannels.join(', ');
         return module; 
       }).filter((module: HomeModuleExtented) => {
         return module.pageId === undefined || module.pageId === '0';
       });
     }).subscribe((modules: HomeModuleExtented[]) => {
       this.modules = modules;
       this.orderMessage = this.modules.length ? this.modules[0].message : '';
       this.activeModules = this.modules.filter((module) => module.enabled && !module.expired && !module.upcoming);
       this.segmentChanged = true;
       this.showHideSpinner(false);
     }, () => {
       this.showHideSpinner(false);
     });
   }
  }
}
