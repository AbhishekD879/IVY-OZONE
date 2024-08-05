import { Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import * as _ from 'lodash';

import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActiveSurfaceBets, Reference, SurfaceBet } from '@app/client/private/models/surfaceBet.model';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { forkJoin } from 'rxjs/observable/forkJoin';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
@Component({
  selector: 'sports-surface-bets',
  templateUrl: './surface-bets-list.component.html',
  styleUrls: ['./surface-bets-list.component.scss']
})

export class SportsSurfaceBetsListComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  @Input() sportId: number = 0;
  @Input() module: SportsModule;
  @Output() onModuleFlagChange: EventEmitter<void> = new EventEmitter<void>();

  public expiredSearchField: string;
  public activeSearchField: string;

  public surfaceBets: SurfaceBet[];
  public activeBets: SurfaceBet[];
  public expiredBets: SurfaceBet[];
  public filteredBySport: boolean = true;
  public breadcrumbsData: Breadcrumb[];
  public sportCategory: SportCategory;
  public sportCategories: SportCategory[];

  public hubId: string;
  public hubData: IEventHub;
  public eventHubs: IEventHub[];
  public segments: any;
  public segmentChanged: boolean = false;
  public cspSegmentConstants = CSPSegmentConstants;
  public selectedSegment: string = this.cspSegmentConstants.UNIVERSAL_TITLE;
  public dataTableColumns: DataTableColumn[] = [];
  public isHomePage: boolean;
  public homePageDataTableColumns: DataTableColumn[];
  public eventHubDataTableColumns: DataTableColumn[];
  public getTypeId: number;
  public getPageType: string;
  public orderMessage: string;
  public surfaceBetsFlag: boolean = true;
  public surfaceBetsData: ActiveSurfaceBets[];
  public moduleData: SportsModule;
  public filterModuleData: SportsModule;
  public cloneModuleData: SportsModule;
  public cloneSurfaceBetsData: ActiveSurfaceBets[];
  public filterSbData: any;
  public validateSbData: boolean;
  public validateModuleData: boolean;
  disableActionHandler: boolean = true;

  //Active Surface bets property mappings for checkboxes
  public activeSbMappings = {
    "Highlights Tab": "highlightsTabOn",
    "EDP": "edpOn",
    "Display in Desktop": "displayOnDesktop",
    "Enabled": "disabled"
  };

  constructor(
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private brandService: BrandService,
    private snackBar: MatSnackBar,
    private segmentStoreService: SegmentStoreService,
    private sportsModulesService: SportsModulesService
  ) {
     this.isHomePage = this.segmentStoreService.validateHomeModule();
  }

  public searchableProperties: Array<string> = [
    'title'
  ];

  public ngOnInit(): void {
    this.loadInitialData();
  }

  /**
  * to load initial data
  * @returns - {void}
  */
  loadInitialData(): void {
    this.setDataTableColumns();
    // Below logic checks if the segment exist or not. 
    this.segmentStoreService.validateSegmentValue();
    
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.SURFACE_BET_TAB) {
        this.selectedSegment = segmentMsg.segmentValue;
        this.filteredBySport = true;
      }
    });
    
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];

      forkJoin([
        this.sportsSurfaceBetsService.getSportCategories(),
        this.apiClientService.eventHub().getAllEventHubs()
      ]).subscribe((result: [SportCategory[], IEventHub[]]) => {
        this.sportCategories = result[0];
        this.eventHubs = result[1];

        if (this.hubId) {
          this.hubData = _.find(this.eventHubs, (hub: IEventHub) => hub.id === this.hubId);
        }

        if (this.sportId) {
          this.sportCategory = _.find(this.sportCategories, (sportCategory: SportCategory) => sportCategory.id === this.sportId.toString());
        }

        this.onFilterChange(this.selectedSegment);
      });
    });
  }

   /**
  * to set action items save and revert
  * @param {string} event -;
  * @returns - {void}
  */
   public actionsHandler(event: string): void {
    switch (event) {
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

  /**
  * revert changes
  *  @returns - {void}
  */
  public revert(): void {
    this.onModuleFlagChange.emit();
    this.loadInitialData();
  }

  /**
  * Save changes
  *  @returns - {void}
  */
  public save(): void {
    this.disableActionHandler = true;
    this.validateModuleData = _.isEqual(this.cloneModuleData, this.filterModuleData);
    this.validateSbData = _.isEqual(this.cloneSurfaceBetsData, this.filterSbData);
    if(!this.validateModuleData) {
      this.sendRequestModule();
    }
    else if(!this.validateSbData) {
      this.sendRequestSurfaceBet();
    }
  }

  /**
  * to save module data and active surface bets data
  *  @returns - {void}
  */
  sendRequestModule(): void {
    this.sportsModulesService.updateModule(this.filterModuleData)
      .subscribe((module: SportsModule) => {
        this.filterModuleData = module;
        if(this.filterModuleData && !this.validateSbData) {
          this.sendRequestSurfaceBet();
          this.snackBar.open(`Sports module and surface bets saved!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
        else {
          this.snackBar.open(`Sports module saved!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
        this.actionButtons.extendCollection(this.surfaceBetsData);
        this.loadInitialData();
      });
  }

  /**
  * to save active surface bets data
  *  @returns - {void}
  */
  sendRequestSurfaceBet(): void {
    this.surfaceBetsData.pop();
    this.apiClientService.sportsSurfaceBets().updateActiveBets(this.surfaceBetsData)
      .subscribe(() => {
        this.actionButtons.extendCollection(this.surfaceBetsData);
        if(this.validateModuleData){
          this.snackBar.open(`Surface bets are saved!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
      });
      this.loadInitialData();
  }
  
  /**
  * to toggle multiple checkboxes based on user preference
  *  @returns - {void}
  */
  saveSurfaceBetsFlagChange(data) {
    this.disableActionHandler = false;
    let { rowIndex, name, flag } = data;
    let propertyName = this.activeSbMappings[name];
    if (propertyName !== undefined) {
      this.surfaceBetsData[rowIndex][propertyName] = (propertyName === "disabled") ? !flag : flag;
      this.activeBets[rowIndex][propertyName] = (propertyName === "disabled") ? !flag : flag;
      if (propertyName === "displayOnDesktop" && flag) {
        this.surfaceBetsData[rowIndex].highlightsTabOn = true;
        this.activeBets[rowIndex].highlightsTabOn = true;
      }
    }
  }

  public removeHandler(bet: SurfaceBet): void {
    this.dialogService.showConfirmDialog({
      title: AppConstants.SURFACE_BET,
      message: AppConstants.REMOVE_SURFACE_BET,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportsSurfaceBets()
          .delete(bet.id)
          .subscribe(() => {
            _.remove(this.surfaceBets, { id: bet.id });
            _.remove(this.activeBets, { id: bet.id });
            _.remove(this.expiredBets, { id: bet.id });
            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  public onFilterChange(segment): void {
    this.getTypeId = (this.hubData && this.hubData.indexNumber) || this.sportId;
    this.getPageType = this.hubData ? 'eventhub' : 'sport';
    this.segmentChanged = false;
    if (this.filteredBySport) {
      this.getSurfaceBetsBySport(this.getPageType, this.getTypeId, segment);
    } else {
      this.getAllSurfaceBets();
    }
  }

  private getSurfaceBetsBySport(pageType: string, typeId: number, segment: string): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().findAllByBrandAndSport(this.brandService.brand, pageType, typeId, segment)
      .map((response: HttpResponse<SurfaceBet[]>) => {
        // filter only active for current sport id
        const bets = _.filter(response.body, bet => {
          return _.some(bet.references, { refId: typeId.toString(), relatedTo: pageType, enabled: true });
        });

        // set field sportsString - list of related sports
        return this.mapBetSports(bets);
      })
      .subscribe((bets: SurfaceBet[]) => {
        this.getRequestCallback(bets);
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private getAllSurfaceBets(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportsSurfaceBets().findAllByBrand(this.brandService.brand)
      .map((response: HttpResponse<SurfaceBet[]>) => {
        return this.mapBetSports(response.body);
      })
      .subscribe((bets: SurfaceBet[]) => {
        this.getRequestCallback(bets);
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private getRequestCallback(bets: SurfaceBet[]): void {
    this.surfaceBets = bets;
    this.orderMessage = this.surfaceBets.length ? this.surfaceBets[0].message : '';
    this.filterBetsByDate(bets);
    this.segmentChanged = true;
    this.globalLoaderService.hideLoader();
  }

  private mapBetSports(bets: SurfaceBet[]): SurfaceBet[] {
    bets = _.map(bets, (bet: SurfaceBet) => {
      // set new field sportString to display on table
      bet.sportsString = _.chain(bet.references)
        .filter((ref: Reference) => {
          return (ref.relatedTo === 'sport' &&
            ref.refId !== '0' && ref.enabled &&
            _.some(this.sportCategories, { categoryId: Number(ref.refId) })) ||
            (ref.relatedTo === 'eventhub' &&
              _.some(this.eventHubs, { indexNumber: Number(ref.refId) }));
        })
        .map((ref: Reference) => {
          const sportMatch = ref.relatedTo === 'sport' && _.find(this.sportCategories, { categoryId: parseInt(ref.refId, 10) });
          const eventHubMatch = ref.relatedTo === 'eventhub' && _.find(this.eventHubs, { indexNumber: Number(ref.refId) });
          return (sportMatch && sportMatch.imageTitle) || (eventHubMatch && eventHubMatch.title);
        })
        .value().join(', ');
      return bet;
    });
    return bets;
  }

  private filterBetsByDate(allBets: SurfaceBet[]): void {
    const currentDate = (new Date()).getTime();
    this.activeBets = _.filter(allBets, bet => {
      return (new Date(bet.displayTo)).getTime() >= currentDate;
    });
    this.sortActiveBets(this.activeBets);
    let expectedData = this.activeBets;
    this.moduleData = this.module;
    this.filterSbData = expectedData.map(obj => _.pick(obj, ['id', 'disabled', 'displayOnDesktop', 'edpOn', 'highlightsTabOn']));
    this.surfaceBetsData = this.filterSbData.concat(this.moduleData);
    this.filterModuleData = this.surfaceBetsData[this.surfaceBetsData.length - 1];
    this.cloneModuleData = _.cloneDeep(this.filterModuleData);
    this.cloneSurfaceBetsData = _.cloneDeep(this.filterSbData);
    this.expiredBets = _.filter(allBets, bet => {
      return (new Date(bet.displayTo)).getTime() < currentDate;
    });
    this.actionButtons?.extendCollection(this.surfaceBetsData);
  }

  private sortActiveBets(activeBets: SurfaceBet[]) {
    const pageType = this.hubData ? 'eventhub' : 'sport';
    activeBets.forEach((activeBet)=>{
      activeBet.references = [activeBet?.references.find(ref=> +ref.refId === this.sportId && pageType === ref.relatedTo)];
    })
    activeBets.sort((bet1,bet2)=> bet1?.references[0]?.sortOrder - bet2?.references[0]?.sortOrder);
  }

  private setDataTableColumns(): void {
    this.homePageDataTableColumns = [
      {
        name: 'Title',
        property: 'title',
        link: {
          hrefProperty: 'id',
          path: 'bet/edit'
        },
        type: 'link'
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
        name: 'Content',
        property: 'content'
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        name: 'Highlights Tab',
        property: 'highlightsTabOn',
        type: 'boolean'
      },
      {
        name: 'EDP',
        property: 'edpOn',
        type: 'boolean'
      },
      {
        name: 'Display in Desktop',
        property: 'displayOnDesktop',
        type: 'boolean'
      },
      {
        name: 'Sports',
        property: 'sportsString'
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
          path: 'bet/edit'
        },
        type: 'link'
      },
      {
        name: 'Content',
        property: 'content'
      },
      {
        name: 'Enabled',
        property: 'disabled',
        type: 'boolean',
        isReversed: true
      },
      {
        name: 'Highlights Tab',
        property: 'highlightsTabOn',
        type: 'boolean'
      },
      {
        name: 'EDP',
        property: 'edpOn',
        type: 'boolean'
      },
      {
        name: 'Display in Desktop',
        property: 'displayOnDesktop',
        type: 'boolean'
      },
      {
        name: 'Sports',
        property: 'sportsString'
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

  // updates the list order to backend once the order id's array is emitted here.
  reorderHandler(list) {
    this.apiClientService
    .sportsSurfaceBets()
    .reorder(list)
    .subscribe(() => {
      this.snackBar.open(`Surface Bet order saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
      this.filterSbData = this.activeBets.map(obj => _.pick(obj, ['id', 'disabled', 'displayOnDesktop', 'edpOn', 'highlightsTabOn']));
      this.surfaceBetsData = this.filterSbData.concat(this.moduleData);
      if(this.disableActionHandler) {
        this.actionButtons.extendCollection(this.surfaceBetsData);
      }
    });
  }

   // Gets the navigation points based on Segment selected.
   segmentHandler(segment: string): void {
     this.segmentChanged = false;
     this.globalLoaderService.showLoader();
     this.segmentStoreService.updateSegmentMessage(
       { segmentModule: CSPSegmentLSConstants.SURFACE_BET_TAB, segmentValue: segment });
     this.onFilterChange(segment);
     this.selectedSegment = segment;
   }
     /**
   * Removes many Expired Surface Bets
   * @param betIds string[]
   */
  removeHandlerMulty(Ids: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Expired Surface Bets (${Ids.length})`,
      message: `Are you sure you want to remove (${Ids.length}) surface bet(S)?`,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportsSurfaceBets()
          .delete(Ids.toString())
          .subscribe(() => {
            Ids.forEach(id =>{
              _.remove(this.expiredBets, { id: id });
            })
            this.globalLoaderService.hideLoader();
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }
}
