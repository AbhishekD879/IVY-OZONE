import * as _ from 'lodash';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DataTableColumn, ExtraNavigationPoint } from '../../../client/private/models';
import { AppConstants } from '@app/app.constants';
import { Order } from '@root/app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ExtraNavigationPointsApiService } from '@app/quick-links/extra-navigation-points/extra-navigation-points-api.service';
import { ExtraNavigationPointsCreateComponent } from '@app/quick-links/extra-navigation-points/extra-navigation-points-create/extra-navigation-points-create.component';

@Component({
  templateUrl: './extra-navigation-points-list.component.html'
})

export class ExtraNavigationPointsListComponent implements OnInit {


  public extraNavigationPoints: Array<ExtraNavigationPoint>;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [{
    'name': 'Title',
    'property': 'title',
    'link': {
      hrefProperty: 'id'
    },
    'type': 'link'
  }, {
    'name': 'Short Description',
    'property': 'description'
  }, {
    'name': 'Destination URL',
    'property': 'targetUri'
  }, {
    'name': 'Validity Period Start',
    'property': 'validityPeriodStart',
    'type': 'date'
  }, {
    'name': 'Validity Period End',
    'property': 'validityPeriodEnd',
    'type': 'date'
  }, {
    'name': 'Enabled',
    'property': 'enabled',
    'type': 'boolean'
  },
  {
    'name': 'Feature Tag',
    'property': 'featureTag'
  }];
  public searchableProperties: Array<string> = ['title'];

  constructor(
    private ExtranavigationPointsApiService: ExtraNavigationPointsApiService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.ExtranavigationPointsApiService.getNavigationPointsList()
      .subscribe((data: HttpResponse<ExtraNavigationPoint[]>) => {
        this.extraNavigationPoints = data.body;
      });
  }

  public createNavigationPoint(): void {
    this.globalLoaderService.showLoader();

    this.dialogService.showCustomDialog(ExtraNavigationPointsCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Special Super Button',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (extraNavigationPoint: ExtraNavigationPoint) => {
        this.ExtranavigationPointsApiService.createNavigationPoint(extraNavigationPoint)
          .map((response: HttpResponse<ExtraNavigationPoint>) => {
            return response.body;
          })
          .subscribe((data: ExtraNavigationPoint) => {
            this.extraNavigationPoints.push(data);
            this.router.navigate([`/quick-links/extra-navigation-points/${data.id}`]);
          });
      }
    });
  }

  public removeHandler(extranavigationPoint: ExtraNavigationPoint): void {
    this.dialogService.showConfirmDialog({
      title: `Remove ${extranavigationPoint.title}`,
      message: `Are You Sure You Want to Remove ${extranavigationPoint.title}?`,
      yesCallback: () => {
        this.ExtranavigationPointsApiService.deleteNavigationPoint(extranavigationPoint.id)
          .subscribe(() => {
            _.remove(this.extraNavigationPoints, { id: extranavigationPoint.id });
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Special Super Button is Removed'
            });
          });
      }
    });
  }
  /*
     * sort the special super button list
     * @param newOrder value
     */
  reorderHandler(newOrder: Order): void {
    this.ExtranavigationPointsApiService.reorderNavigationPoints(newOrder).subscribe(() => {
      this.snackBar.open('New Super Buttons Order Saved!!', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  } 
}

