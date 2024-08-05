import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { concatMap } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import * as _ from 'lodash';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';

import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { tabsTypes, tabsTypesLads } from '@app/module-ribbon/constant/tabs-types.constant';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { ModuleRibbonService } from '@app/module-ribbon/module-ribbon.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { ISegmentModel } from '@app/client/private/models/segment.model';
import { CSPSegmentLSConstants } from '@app/app.constants';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'app-edit-module-ribbon-tab',
  templateUrl: './edit-module-ribbon-tab.component.html',
  styleUrls: ['./edit-module-ribbon-tab.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditModuleRibbonTabComponent implements OnInit {
  public eventHubsList: IEventHub[] = [];
  public eventHubsNames: string[] = [];
  public selectedHubName: string;

  public isLoading: boolean = false;
  public moduleRibbonTab: ModuleRibbonTab;

  public breadcrumbsData: Breadcrumb[];

  public directiveNames: string[];
  public isRevert = false;
  segmentsList: ISegmentModel = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };
  isSegmentValid: boolean = false;
  @ViewChild('actionButtons') actionButtons;
  brand: string;

  constructor(
    private moduleRibbonService: ModuleRibbonService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private segmentStoreService: SegmentStoreService,
    private brandService: BrandService
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit() {
    this.brand = this.brandService.brand;
    this.getDirectiveNames();
    this.loadInitData();
  }

  public isValidForm(moduleRibbonTab: ModuleRibbonTab): boolean {
    return moduleRibbonTab.title && moduleRibbonTab.title.length > 0;
  }

  public saveChanges(): void {
    this.apiClientService.moduleRibbonTab()
      .udpate(this.moduleRibbonTab)
      .map((response: HttpResponse<ModuleRibbonTab>) => {
        return response.body;
      })
      .subscribe((data: ModuleRibbonTab) => {
        const self = this;
        this.moduleRibbonTab = data;
        this.actionButtons.extendCollection(this.moduleRibbonTab);
        this.segmentStoreService.setSegmentValue(this.moduleRibbonTab ,CSPSegmentLSConstants.MODULE_RIBBON_TAB);
        this.dialogService.showNotificationDialog({
          title: `Module Ribbon Tab Saving`,
          message: `Module Ribbon Tab is Saved.`,
          closeCallback() {
            self.router.navigate([`/module-ribbon-tabs`]);
          }
        });
      });
  }

  public revertChanges(): void {
    this.loadInitData();
    this.isRevert = true;
  }

  public removeModuleRibbonTab(): void {
    this.apiClientService.moduleRibbonTab().remove(this.moduleRibbonTab.id).subscribe(() => {
      this.router.navigate(['/module-ribbon-tabs']);
    });
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.moduleRibbonTab().getById(params['id']).map((moduleRibbonTab: HttpResponse<ModuleRibbonTab>) => {
        return moduleRibbonTab.body;
      }).subscribe((moduleRibbonTab: ModuleRibbonTab) => {
        moduleRibbonTab['bybVisble']= null ? false : moduleRibbonTab['bybVisble'];
        this.moduleRibbonTab = moduleRibbonTab;
        this.segmentsList = {
          exclusionList: this.moduleRibbonTab.exclusionList,
          inclusionList: this.moduleRibbonTab.inclusionList,
          universalSegment: this.moduleRibbonTab.universalSegment
        };
        this.breadcrumbsData = [{
          label: `Module Ribbon Tabs`,
          url: `/module-ribbon-tabs`
        }, {
          label: this.moduleRibbonTab.title,
          url: `/module-ribbon-tabs/edit/${this.moduleRibbonTab.id}`
        }];
        this.globalLoaderService.hideLoader();
        this.isLoading = false;

        if (this.isEventHubTab()) {
          this.loadEventHubs().subscribe();
        } else {
          // remove eventhub from directives list to not have posibility to change tab type to EventHub
          this.directiveNames.splice(1, 1);
        }
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

  public onChangeDirectiveName(value: string): void {
    this.moduleRibbonTab.directiveName = value;

    if (this.isEventHubTab() && this.eventHubsList.length === 0) {
      this.loadEventHubs().subscribe();
    }
  }

  getDirectiveNames() {
    if (this.brand == 'ladbrokes') {
      this.directiveNames = tabsTypesLads;
    }
    else
      this.directiveNames = tabsTypes;
  }


  public onChangeShowTabOn(value: string): void {
    this.moduleRibbonTab.showTabOn = value;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeModuleRibbonTab();
        break;
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

  isEventHubTab(): boolean {
    return this.moduleRibbonTab.directiveName === 'EventHub';
  }

  setChosenHub(tabUrl: string): void {
    const hubIndexMatch = tabUrl.match(/\d+$/);
    const hubIndex = hubIndexMatch && parseInt(hubIndexMatch[0], 10);
    const selectedHub = _.find(this.eventHubsList, (hub: IEventHub) => hub.indexNumber === hubIndex);

    this.selectedHubName = selectedHub && selectedHub.title;
  }

  /**
   * Get tabs without current opened tab to check mapped EventHubs
   */
  loadTabs(): Observable<ModuleRibbonTab[]> {
    return this.apiClientService.moduleRibbonTab()
      .getByBrand()
      .map((moduleRibbonResponse: HttpResponse<ModuleRibbonTab[]>) => {
        _.remove(moduleRibbonResponse.body, {
          id: this.moduleRibbonTab.id
        });

        return moduleRibbonResponse.body;
      });
  }

  loadEventHubs(): Observable<void> {
    return this.loadTabs()
      .pipe(concatMap((tabs: ModuleRibbonTab[]) => {
        return this.moduleRibbonService.getPossibleEventHubsToMap(tabs)
          .map((eventHubsList: IEventHub[]) => {
            this.eventHubsList = eventHubsList;

            this.eventHubsNames = _.map(eventHubsList, 'title');

            if (this.moduleRibbonTab.internalId.indexOf('tab-eventhub') >= 0) {
              this.setChosenHub(this.moduleRibbonTab.url);
            }
          });
      }));
  }

  /**
   * Set Tab data according to Chosen EventHub
   * @param eventHubName
   */
  onChangeSelectedHub(eventHubName: string): void {
    const eventHub = _.find(this.eventHubsList, {title: eventHubName});

    this.moduleRibbonTab.internalId = `tab-eventhub-${eventHub.indexNumber}`;
    this.moduleRibbonTab.url = `/home/eventhub/${eventHub.indexNumber}`;
    this.moduleRibbonTab.hubIndex = eventHub.indexNumber;
  }

  /**
   * Handle data comes from dataTime component, set tab property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleVisibilityDateUpdate(data: DateRange): void {
    this.moduleRibbonTab.displayFrom = data.startDate;
    this.moduleRibbonTab.displayTo = data.endDate;
  }

  /*
  *Disables save button based upon the return type
   */
  public validationHandler(): boolean {
    return this.isSegmentValid;
  }

  /**
   * updates issegmentvalid true/false on child form changes
  */
   isSegmentFormValid(isValid: boolean): void {
    this.isSegmentValid = isValid;
  }

  /*
   * Handles logic for child emitted data. 
  */
  modifiedSegmentsHandler(segmentConfigData: ISegmentModel): void {
    this.isRevert = false;
    this.moduleRibbonTab = { ...this.moduleRibbonTab, ...segmentConfigData };
  }
}
