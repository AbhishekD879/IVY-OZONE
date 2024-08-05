import * as _ from 'lodash';

import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Params } from '@angular/router';

import { SportsModule } from '@app/client/private/models/homepage.model';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DataTableColumn } from '@app/client/private/models';
import { ISegmentModel, ISegmentMsg } from '@app/client/private/models/segment.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { HomeInplayModule } from '@app/client/private/models/inplaySportModule.model';
import { ErrorService } from '@app/client/private/services/error.service';
import { SportsModulesService } from '../../sports-modules.service';
import { InplaySportCreateComponent } from '../inplay-sport-create/inplay-sport-create.component';

@Component({
  selector: 'app-inplay-module',
  templateUrl: './inplay-module.component.html',
  styleUrls: ['./inplay-module.component.scss']
})
export class InplayModuleComponent implements OnInit {
  module: SportsModule;
  moduleClone: SportsModule;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;
  segmentsList: ISegmentModel;
  inplaySportsList: HomeInplayModule[] = [];
  brand: string = this.brandService.brand;
  public showSegmentDropdown: boolean = true;
  public segmentChanged: boolean = false;
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public searchField: string;
  public dataTableColumns: DataTableColumn[] = [];
  public searchableProperties: Array<string> = [
    'sportName'
  ];
  public orderMessage: string;

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService,
    private brandService: BrandService,
    private globalLoaderService: GlobalLoaderService,
    private segmentStoreService: SegmentStoreService,
    private errorService: ErrorService,
  ) {
    this.isValidModule = this.isValidModule.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  loadInitialData(params): void {
    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
        this.module = moduleData[0];
        this.moduleClone = _.cloneDeep(this.module);

        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });

        if(this.isHomePageModule()) {
          this.segmentStoreService.validateSegmentValue();
          this.getSegmentValue();
          this.sportsModulesService.getInplaySportsBySegment(this.selectedSegment, this.brand).subscribe((result) => {
            this.inplaySportsList = result;
          });
          this.setDataTableColumns();
          this.segmentChanged = true;
        }
      });
  }

  isHomePageModule(): boolean {
    return this.module.sportId === 0;
  }

  public createSportConfigRow(): void {
    this.dialogService.showCustomDialog(InplaySportCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Sport Configuration',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (createSportData: HomeInplayModule) => {
        this.globalLoaderService.showLoader();
        this.showSegmentDropdown = false;
        this.selectedSegment = createSportData.inclusionList.length !== 0 ? createSportData.inclusionList[0] : CSPSegmentConstants.UNIVERSAL_TITLE;
        this.segmentHandler(this.selectedSegment);
        this.globalLoaderService.hideLoader();
        this.snackBar.open(`Sports configuration created!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }
    });
  }

  public isValidModule(): boolean {
    const correctSportsCount = this.module.inplayConfig.homeInplaySports.filter((sport) => {
      return sport.eventCount > 0 || sport.eventCount === 0;
    }).length;
    const sportCount = this.module.inplayConfig.homeInplaySports.length;
    return this.module.inplayConfig.maxEventCount > 0 &&
              (!this.isHomePageModule() || correctSportsCount === sportCount);
  }

  public isEqualCollection(): boolean {
    return _.isEqual(this.module, this.moduleClone) || this.module.inplayConfig.maxEventCount < 0
    || this.module.inplayConfig.maxEventCount === null;
  }

  public reorderHandler(order: any): void {
    this.sportsModulesService
      .inplaySportsReorder(order)
      .subscribe(() => {
        this.snackBar.open(`Inplay Sports order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  public removeHandler(selectedSport: HomeInplayModule): void {
    this.dialogService.showConfirmDialog({
      title: 'Inplay Sport Module',
      message: 'Are You Sure You Want to Remove Inplay Sport Module?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.sportsModulesService.deleteSportById(selectedSport.id).subscribe(() => {
          _.remove(this.inplaySportsList, { id: selectedSport.id });
          this.globalLoaderService.hideLoader();
        }, error => {
          this.errorService.emitError(error.message);
          this.globalLoaderService.hideLoader();
        });
      }
    });
  }

  /**
   * get sports list based on segment selection
   * @param segment value
   */
  public segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.INPLAY_SPORTS_MODULE, segmentValue: segment });
    this.globalLoaderService.showLoader();
    this.sportsModulesService.getInplaySportsBySegment(this.selectedSegment, this.brand).subscribe((result) => {
      this.inplaySportsList = result;
      this.showSegmentDropdown = true;
      this.orderMessage = this.inplaySportsList.length ? this.inplaySportsList[0].message : '';
      this.globalLoaderService.hideLoader();
      this.segmentChanged = true;
    }, error => {
      this.globalLoaderService.hideLoader();
      this.segmentChanged = true;
    });
  }

  actionsHandler(event) {
    switch (event) {
      case 'save':
        if(this.isHomePageModule()){
          this.dialogService.showConfirmDialog({
            title: 'Saving of: Inplay Module',
            message: 'Are You sure You want to save this: Inplay Module?',
            yesCallback: () => {
              this.updateModule();
            }
          });
        } else {
          this.updateModule();
        }
        break;
      case 'revert':
        this.loadInitialData(this.routeParams);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private updateModule(): void {
    this.sportsModulesService.updateModule(this.module)
      .subscribe((module: SportsModule) => {
        this.module = module;
        if(!this.isHomePageModule()){
          this.actionButtons.extendCollection(this.module);
        } else {
          this.loadInitialData(this.routeParams);
        }
        this.snackBar.open(`Sports module saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  private getSegmentValue(): void {
    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.INPLAY_SPORTS_MODULE) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
  }

  private setDataTableColumns(): void {
    this.dataTableColumns = [
      {
        name: 'Sport',
        property: 'sportName',
        link: {
          hrefProperty: 'id',
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
        name: 'Event Count',
        property: 'eventCount'
      },
      {
        name: 'Tier',
        property: 'tier'
      }
    ];
  }
}
