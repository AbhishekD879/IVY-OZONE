import { Component, OnInit } from '@angular/core';
import { AppConstants } from '@app/app.constants';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { CouponMarketMappingCreateComponent } from '../coupon-market-mapping-create/coupon-market-mapping-create.component';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { CouponMarketMapping } from '@app/client/private/models/couponMarketMapping.model';
import * as _ from 'lodash';
import { CouponMarketMappingEditComponent } from '../coupon-market-mapping-edit/coupon-market-mapping-edit.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-coupon-market-mapping-list',
  templateUrl: './coupon-market-mapping-list.component.html',
  styleUrls: ['./coupon-market-mapping-list.component.scss']
})
export class CouponMarketMappingListComponent implements OnInit {
  public searchField: string = '';
  // public couponMarketMappings: any[];
  marketMappingData : any[];
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Coupon ID',
      property: 'couponId',
      link: {
        hrefProperty: 'id'
      },
      type: 'mappingLink'
    },
    {
      name: 'Market Template Name',
      property: 'marketName'
    }
  ];

  public searchableProperties: Array<string> = [
    'couponId'
  ];
  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private globalLoaderService: GlobalLoaderService,
    // private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.couponMarketMapping()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: CouponMarketMapping[]) => {
        this.marketMappingData = data;
        this.globalLoaderService.hideLoader();
      }, error => {
         console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createCouponMarketMapping(): void {
    this.dialogService.showCustomDialog(CouponMarketMappingCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Coupon Market Selector',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (marketMapping: any) => {
        this.apiClientService.couponMarketMapping()
          .add(marketMapping)
          .map(response => {
            return response.body;
          })
          .subscribe((data: any) => {
            this.marketMappingData.push(data);
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

  removeHandler(couponMarketMapping: CouponMarketMapping): void {
    this.dialogService.showConfirmDialog({
      title: 'Coupon Market Mapping',
      message: 'Are You Sure You Want to Remove coupon market mapping?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.couponMarketMapping()
          .delete(couponMarketMapping.id)
          .subscribe(() => {
            _.remove(this.marketMappingData, {id: couponMarketMapping.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  public editCouponId(coupon: CouponMarketMapping) {
    const dialog = this.dialog.open(CouponMarketMappingEditComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        coupon: _.cloneDeep(coupon)
      }
    });
    dialog.afterClosed()

    .subscribe((newCoupon: CouponMarketMapping) => {
      if (newCoupon) {
        const coupons  = _.cloneDeep(this.marketMappingData);
        _.extend(_.find(coupons, m => m.couponId === coupon.couponId), newCoupon);
            this.dialogService.showNotificationDialog({
              title: 'Save Completed',
              message: 'Coupon is Saved'
            });

      }
    });
  }



}
