import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ModuleRibbonTab } from '@app/client/private/models/moduleribbontab.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { tabsTypes, tabsTypesLads } from '@app/module-ribbon/constant/tabs-types.constant';
import {IEventHub} from '@app/sports-pages/event-hub/models/event-hub.model';
import * as _ from 'lodash';
import { ModuleRibbonService } from '@app/module-ribbon/module-ribbon.service';
import { DateRange } from '@app/client/private/models/dateRange.model';

@Component({
  selector: 'app-create-module-ribbon-tab',
  templateUrl: './create-module-ribbon-tab.component.html',
  styleUrls: ['./create-module-ribbon-tab.component.scss']
})
export class CreateModuleRibbonTabComponent implements OnInit {
  public eventHubsList: IEventHub[] = [];
  public eventHubsNames: string[] = [];
  public directiveNames: string[];

  public moduleRibbonTab: ModuleRibbonTab;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private moduleRibbonService: ModuleRibbonService
  ) { }

  ngOnInit() {
    const brand = this.brandService.brand;

    this.moduleRibbonTab = {
      id: '',
      brand: brand,
      updatedAt: '',
      updatedBy: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      internalId: '',
      directiveName: 'Featured',
      key: '',
      lang: '',
      sortOrder: null,
      targetUri: '',
      title: '',
      title_brand: '',
      visible: false,
      showTabOn: 'both',
      devices: {},
      url: '',
      bybVisible: false,
      exclusionList: [],
      inclusionList: [],
      applyUniversalSegments: false
    };
    
    this.getDirectiveNames();
    this.loadEventHubs();
  }

  public getNewModuleRibbonTab(): ModuleRibbonTab {
    return this.moduleRibbonTab;
  }

  public isValidModuleRibbonTab(): boolean {
    return !!(
      this.moduleRibbonTab.brand &&
      this.moduleRibbonTab.directiveName &&
      this.moduleRibbonTab.title &&
      this.moduleRibbonTab.internalId &&
      this.moduleRibbonTab.url &&
      this.moduleRibbonTab.showTabOn
    );
  }

  public closeDialog() {
    this.dialogRef.close();
  }

  public onChangeDirectiveName(value: string): void {
    this.moduleRibbonTab.directiveName = value;
  }

  isEventHubTab() {
    return this.moduleRibbonTab.directiveName === 'EventHub';
  }

  getDirectiveNames() {
    if (this.moduleRibbonTab.brand == 'ladbrokes') {
      this.directiveNames = tabsTypesLads;
    }
    else
      this.directiveNames = tabsTypes;
  }

  loadEventHubs(): void {
    this.moduleRibbonService.getPossibleEventHubsToMap(this.data.data.currentTabs)
      .subscribe((eventHubsList: IEventHub[]) => {
        this.eventHubsList = eventHubsList;

        this.eventHubsNames = _.map(eventHubsList, 'title');
      });
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
}
