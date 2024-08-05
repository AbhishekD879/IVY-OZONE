import * as _ from 'lodash';

import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';

import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportCategoriesCreateComponent } from '../sport-categories-create/sport-categories-create.component';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { Router } from '@angular/router';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@app/client/private/models/order.model';
import { Tier } from '@app/client/private/models/tier.enum';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { HttpResponse } from '@angular/common/http';
import { SportCategoryService } from '@app/client/private/services/http/menu/sportCategory.service';

@Component({
  templateUrl: './sport-categories-list.component.html',
  styleUrls: ['./sport-categories-list.component.scss']
})
export class SportCategoriesListComponent implements OnInit {

  public sportCategories: SportCategory[] = [];
  public updatedSportCategories: SportCategory[] = [];
  public error: string;
  public searchField: string = '';
  public orderMessage: string;
  @ViewChild('actionButtons') actionButtons;
  public dataTableColumns: Array<DataTableColumn> = [];
  public sportsCategoryDataTableColumns: DataTableColumn[];
  public showInSportsRibbonDataTableColumns: DataTableColumn[];
  public searchableProperties: Array<string> = [
    'imageTitle'
  ];

  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public segmentChanged: boolean = false;
  public nonSegmented: boolean = true;
  public sportsCategoryFlag: boolean = true;
  private readonly sportCategoryService: SportCategoryService;

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router,
    private segmentStoreService: SegmentStoreService
  ) {
    this.sportCategoryService = apiClientService.sportCategory();
  }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.onFilterChange(this.selectedSegment);
  }

  getAllSportsCaterogy() {
    this.nonSegmented = false;
    this.apiClientService.sportCategory()
      .findAllByBrand()
      .map((response) => {
        return response.body;
      })
      .subscribe((data: SportCategory[]) => {
        data.forEach(function (category) {
          category.tier = Tier.title(Tier[category.tier]);
        });
        this.sportCategories = data;
        this.nonSegmented = true;
        this.orderMessage = '';
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createSportCategory(): void {
    this.dialogService.showCustomDialog(SportCategoriesCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Sport Category',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (sportCategory: SportCategory) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportCategory()
          .save(sportCategory)
          .map(response => {
            return response.body;
          })
          .subscribe((data: SportCategory) => {
            this.sportCategories.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/sports-pages/sport-categories/${data.id}`], { queryParams: { expanded: true } });
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(sportCategory: SportCategory): void {
    this.dialogService.showConfirmDialog({
      title: 'Sport Category',
      message: 'Are You Sure You Want to Remove Sport Category?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.sportCategory()
          .delete(sportCategory.id)
          .subscribe(() => {
            _.remove(this.sportCategories, { id: sportCategory.id });
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .sportCategory()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Sport category order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }


  // Gets the navigation points based on Segment selected.
  segmentHandler(segment: string): void {
    this.segmentChanged = false;
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.SPORTS_QUICK_LINK, segmentValue: segment });
    this.selectedSegment = segment;
    this.onFilterChange(segment);
  }

  // called when choosing sportscategory/ show in sports ribbon radio button
  public onFilterChange(selectedSegment: string): void {
   this.setDataTableColumns();
    if (this.sportsCategoryFlag) {
      this.selectedSegment = CSPSegmentConstants.UNIVERSAL_TITLE;
      this.getAllSportsCaterogy();
    } else {
      this.segmentChanged = false;
      this.getCategorisedSports(selectedSegment);
    }
  }

  //get segment based sports data 
  private getCategorisedSports(segment: string): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.sportCategoryService().getSportCategory(segment)
      .map((response) => {
        this.sportCategories = response.body;
        return response.body;
      })
      .subscribe((sports: SportCategory[]) => {
        this.getRequestCallback(sports);
      }, error => {
        this.globalLoaderService.hideLoader();
      });
  }

  private getRequestCallback(sports: SportCategory[]): void {
    this.updatedSportCategories = _.cloneDeep(sports);
    this.updatedSportCategories .forEach(function (category) {
      category.tier = Tier.title(Tier[category.tier]);
    });
    this.orderMessage = this.sportCategories.length ? this.sportCategories[0].message : '';
    this.segmentChanged = true;
    this.globalLoaderService.hideLoader();
  }

  // save show in sports ribbon checkbox enabling/disabling option in the sports category table
  saveSportsRibbonFlagChange(data) {
    const index = data.rowIndex;
    const updatedSportsCategoryData =  this.sportCategories[index];
    updatedSportsCategoryData.showInHome = data.sportsRibbonFlag;
    this.globalLoaderService.showLoader();
    this.sportCategoryService
      .update(updatedSportsCategoryData)
      .map((data: HttpResponse<SportCategory>) => {
        return data.body;
      })
      .subscribe((data: SportCategory) => {
        this.sportCategories[index] = data;
        this.sportCategories[index].isRealSport = (() => {
          return this.sportCategories[index].tier === Tier.TIER_1 || this.sportCategories[index].tier === Tier.TIER_2;
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });

  }


  

  private setDataTableColumns(): void {
    this.sportsCategoryDataTableColumns = [
      {
        'name': 'Name',
        'property': 'imageTitle',
        'link': {
          hrefProperty: 'id'
        },
        'type': 'link'
      },
      {
        'name': 'Tier',
        'property': 'tier'
      }
    ];

    this.showInSportsRibbonDataTableColumns = [
      {
        'name': 'Name',
        'property': 'imageTitle'
      },
      {
        'name': 'Tier',
        'property': 'tier'
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
        'name': 'Show in Sports Ribbon',
        'property': 'showInHome',
        'type': 'boolean'
      }
    ];

    this.dataTableColumns = this.sportsCategoryFlag ? this.sportsCategoryDataTableColumns : this.showInSportsRibbonDataTableColumns;
  }
}
