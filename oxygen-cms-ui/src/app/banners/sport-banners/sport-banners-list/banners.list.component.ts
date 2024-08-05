import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {BannerCreateComponent} from '../sport-banner-create/banner.create.component';
import {Banner} from '../../../client/private/models/banner.model';
import {BannersApiService} from '../service/banners.api.service';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {AppConstants} from '../../../app.constants';
import {SportCategory} from '../../../client/private/models/sportcategory.model';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {HttpResponse} from '@angular/common/http';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'sport-banners-list',
  templateUrl: './banners.list.component.html',
  styleUrls: ['./banners.list.component.scss'],
  providers: [
  ]
})
export class SportBannersListComponent implements OnInit {
  bannersData: Banner[] = [];
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'imageTitle',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Alt ext',
      property: 'alt'
    },
    {
      name: 'In App',
      property: 'inApp',
      type: 'boolean'
    },
    {
      name: 'Target URI',
      property: 'targetUri',
    },
    {
      name: 'Validity start',
      property: 'validityPeriodStart',
      type: 'date'
    },
    {
      name: 'Validity end',
      property: 'validityPeriodEnd',
      type: 'date'
    },
    {
      name: 'Category',
      property: 'categoryName',
    },
    {
      name: 'Vip Levels',
      property: 'vipLevels',
    },
    {
      name: 'Show to',
      property: 'showToCustomer',
    }
  ];

  searchableProperties: Array<string> = [
    'imageTitle'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private bannersApiService: BannersApiService,
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
  ) {}

  /**
   * Create new SSO page.
   */
  createBanner() {
    const dialogRef = this.dialog.open(BannerCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        bannersData: this.bannersData
      }
    });

    dialogRef.afterClosed().subscribe(newBanner => {
      if (newBanner) {
        this.bannersApiService.postNewBanner(newBanner)
          .subscribe(data => {
            if (data) {
              newBanner.id = data.body.id;
              this.bannersData.push(newBanner);
              this.router.navigate([`/banners/sport-banners/${newBanner.id}`]);
            }
          });
      }
    });
  }

  /**
   * Het amount of Active/Inactive elements.
   * @return {{active:number, inactive:number}}
   */
  get bannersAmount(): ActiveInactiveExpired {
    const activePromos = this.bannersData && this.bannersData.filter(banner => banner.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.bannersData.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  /**
   * handle deleting banner
   * @param {Banner} banner
   */
  removeHandler(banner: Banner) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Banner',
      message: 'Are You Sure You Want to Remove Banner?',
      yesCallback: () => {
        this.sendRemoveRequest(banner);
      }
    });
  }

  /**
   * handle deleting banner
   * @param {Banner} banner
   */
  removeHandlerMulty(bannersIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Banners (${bannersIds.length})`,
      message: 'Are You Sure You Want to Remove Banner selected banners?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(bannersIds.map(id => this.bannersApiService.deleteBanner(id)))
          .subscribe(() => {
            bannersIds.forEach((id) => {
              const index = _.findIndex(this.bannersData, { id: id });
              this.bannersData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Banner} banner
   */
  sendRemoveRequest(banner: Banner) {
    this.bannersApiService.deleteBanner(banner.id)
      .subscribe((data: any) => {
        this.bannersData.splice(this.bannersData.indexOf(banner), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Banner is Removed.'
        });
      });
  }


  /**
   * Handle reorder of data items.
   */
  reorderHandler(newOrder: Order) {
    this.bannersApiService.postNewBannersOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('NEW BANNERS ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }

  ngOnInit() {
    // load sport categories to map promotion
    this.bannersApiService
      .getSportCategories()
      .map((data: HttpResponse<SportCategory[]>) => data.body)
      .subscribe((data: SportCategory[]) => {
        const sportCategories: SportCategory[] = data;

        this.bannersApiService.getBannersData()
          .map((bannersDataResponse: HttpResponse<Banner[]>) => {
            // set categoryName for banners as we don't have it inside, only id.
            bannersDataResponse.body.forEach((banner: Banner) => {
              const category = _.find(sportCategories, (sportCategory: SportCategory) => {
                return sportCategory.id === banner.categoryId;
              });

              banner.categoryName = category ? category.alt : '';
            });
            return bannersDataResponse.body;
          })
          .subscribe((bannersData: Banner[]) => {
            this.bannersData = bannersData;
          }, error => {
            this.getDataError = error.message;
          });
      });
  }
}
