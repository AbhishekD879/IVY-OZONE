import * as _ from 'lodash';

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { NavigationPointsApiService } from '../navigation-points.api.service';

import { NavigationPoint, DataTableColumn } from '../../../client/private/models';
import { AppConstants, CSPSegmentConstants, CSPSegmentLSConstants } from '@app/app.constants';
import { Order } from '@root/app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';
import { ISegmentMsg } from '@root/app/client/private/models/segment.model';

@Component({
  templateUrl: './navigation-points-list.component.html',
  styleUrls: ['./navigation-points-list.component.scss']
})
export class NavigationPointsListComponent implements OnInit {

  public navigationPoints: Array<NavigationPoint>;
  public searchField: string = '';
  public selectedSegment: string = CSPSegmentConstants.UNIVERSAL_TITLE;
  public segmentChanged: boolean = true;

  public dataTableColumns: Array<DataTableColumn> = [{
    'name': 'Title',
    'property': 'title',
    'link': {
      hrefProperty: 'id'
    },
    'type': 'link'
  }, {
    'name': 'Segment(s)',
    'property': 'inclusionList',
    'type': 'array'
  }, {
    'name': 'Segment(s) Exclusion',
    'property': 'exclusionList',
     'type': 'array'
  }, {
    'name': 'Description',
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
  }];
  public searchableProperties: Array<string> = [ 'title' ];
  public orderMessage: string;

  constructor(
    private navigationPointsApiService: NavigationPointsApiService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    private snackBar: MatSnackBar,
    private segmentStoreService: SegmentStoreService
  ) { }

  ngOnInit() {
    this.segmentStoreService.validateSegmentValue();

    this.segmentStoreService.getSegmentMessage().subscribe((segmentMsg: ISegmentMsg) => {
      if (segmentMsg.segmentModule === CSPSegmentLSConstants.SUPER_BUTTON) {
        this.selectedSegment = segmentMsg.segmentValue;
      }
    });
    
    this.navigationPointsApiService.getNavigationPointsBySegment(this.selectedSegment)
      .subscribe((data: HttpResponse<NavigationPoint[]>) => {
        this.navigationPoints = data.body;
        this.orderMessage = this.navigationPoints.length ? this.navigationPoints[0].message : '';
      });
  }

  public createNavigationPoint(): void {
    this.globalLoaderService.showLoader();
    this.router.navigate(['/quick-links/navigation-points/add'])
  }

  public removeHandler(navigationPoint: NavigationPoint): void {
    this.dialogService.showConfirmDialog({
      title: `Remove ${navigationPoint.title}`,
      message: `Are You Sure You Want to Remove ${navigationPoint.title}?`,
      yesCallback: () => {
        this.navigationPointsApiService.deleteNavigationPoint(navigationPoint.id)
          .subscribe(() => {
            _.remove(this.navigationPoints, { id: navigationPoint.id });
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Super Button is Removed'
            });
          });
      }
    });
  }

  /**
   * get super button list based on segment selection
   * @param segment value
   */
  public segmentHandler(segment: string): void {
    this.globalLoaderService.showLoader();
    this.segmentChanged = false;
    this.segmentStoreService.updateSegmentMessage(
      { segmentModule: CSPSegmentLSConstants.SUPER_BUTTON, segmentValue: segment });

    this.navigationPointsApiService.getNavigationPointsBySegment(segment).subscribe(
      (data: HttpResponse<NavigationPoint[]>) => {
        this.navigationPoints = data.body;
        this.orderMessage = this.navigationPoints.length ? this.navigationPoints[0].message : '';
        this.selectedSegment = segment;
        this.segmentChanged = true;
        this.globalLoaderService.hideLoader();
      },
      (error) => {
        this.globalLoaderService.hideLoader();
      }
    );
  }

  /**
   * sort the super button list
   * @param newOrder value
   */
  reorderHandler(newOrder: Order): void {
    this.navigationPointsApiService.reorderNavigationPoints(newOrder).subscribe(() => {
      this.snackBar.open('New Super Buttons Order Saved!!', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }
}
