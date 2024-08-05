import { Component, OnInit } from '@angular/core';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import * as _ from 'lodash';
import { FilterModel } from '../model/bet-pack-banner.model';
import { MatDialog } from '@angular/material/dialog';
import { FilterCreateComponent } from './create-filter/filter-create.component';
import { AppConstants } from '@root/app/app.constants';
import { ApiClientService } from '@app/client/private/services/http';
import { Order } from '@root/app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';

@Component({
  selector: 'filter',
  templateUrl: './filter.component.html'
})
export class FilterComponent implements OnInit {
  filters: Array<FilterModel>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Filter(s)',
      property: 'filterName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Active/De-active',
      property: 'filterActive',
      type: 'boolean'
    }
  ];

  constructor(private dialogService: DialogService,
    private dialog: MatDialog,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private globalLoaderService: GlobalLoaderService) { }

  ngOnInit(): void {
    this.loadFilters();
  }
  /**
  * Load List of Filters
  *  @returns - {void}
  */
  loadFilters(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.betpackService().getFilters().map((response: HttpResponse<FilterModel[]>) => response.body)
      .subscribe((res: FilterModel[]) => {
        this.filters = res;
      });
    this.globalLoaderService.hideLoader();
  }

  /**
  * Remove Filter Check
  * @param {FilterModel} filter - ;
  *  @returns - {void}
  */
  removeFilter(filter: FilterModel): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Filter',
      message: 'Are You Sure You Want to Remove Filter?',
      yesCallback: () => {
        this.sendRemoveRequest(filter);
      }
    });
  }

  /**
  * Remove Filter Call
  * @param {FilterModel} data - ;
  *  @returns - {void}
  */
  sendRemoveRequest(data: FilterModel): void {
    this.apiClientService.betpackService().deleteFilter(data.filterName)
      .subscribe((val: any) => {
        if (!val.body.filterAssociated) {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Filter is Removed.'
          });
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Remove Not Done',
            message: 'Filter is associated with ' + JSON.stringify(val.body.betpackNames)
          });
        }
        this.loadFilters();
      }, error => console.log(error)
      );
  }

  /**
  * Navigate to Filter Create
  * @returns - {void}
  */
  createFilter(): void {
    const dialogRef = this.dialog.open(FilterCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(data => {
      if (data) {
        this.apiClientService.betpackService().postFilter(data)
          .map((response: HttpResponse<FilterModel>) => response.body)
          .subscribe((res: FilterModel) => {
            this.loadFilters();
            this.dialogService.showNotificationDialog({
              title: 'Save Completed',
              message: 'Filter is Created and Stored.'
            });
          });
      }
    });
  }
  /**
  * Ordering Filter
  * @returns - {void}
  */
  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .betpackService()
      .reorderFilter(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Filter order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
  * Get Active and Inactive filter count
  * @returns - {active: number, inactive: number}
 */
  get filterLength(): ActiveInactiveExpired {
    const activeFilter = this.filters && this.filters.filter(filter => filter.filterActive === true);
    const activeFilterLength = activeFilter && activeFilter.length;
    const inactiveFilterLength = this.filters.length - activeFilterLength;
    return {
      active: activeFilterLength,
      inactive: inactiveFilterLength
    };
  }
}
