import {GlobalLoaderService} from './../../shared/globalLoader/loader.service';
import {Component, OnInit} from '@angular/core';
import {ApiClientService} from '../../client/private/services/http/index';
import {PromotionsAPIService} from '../service/promotions.api.service';
import {Promotion} from '../../client/private/models/promotion.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {AppConstants} from '../../app.constants';
import {DataTableColumn} from '../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../client/private/models/activeInactiveExpired.model';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {Order} from '../../client/private/models/order.model';

@Component({
  selector: 'promotions-page',
  templateUrl: './promotions.page.component.html',
  styleUrls: ['./promotions.page.component.scss']
})
export class PromotionsPageComponent implements OnInit {
  promotionsData: Array<Promotion>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: 'promotion/'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Popup title',
      property: 'popupTitle'
    },
    {
      name: 'Promo Key',
      property: 'promoKey'
    },
    {
      name: 'Validity start',
      property: 'validityPeriodStart',
      type: 'date',
      width: 2
    },
    {
      name: 'Validity end',
      property: 'validityPeriodEnd',
      type: 'date',
      width: 2
    },
    {
      name: 'Opt. In Req.',
      property: 'requestId'
    },
    {
      name: 'Category',
      property: 'categoryId'
    },
    {
      name: 'Vip L.',
      property: 'vipLevelsInput'
    },
    {
      name: 'Show',
      property: 'showToCustomer'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(
    public snackBar: MatSnackBar,
    public router: Router,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private promotionsAPIService: PromotionsAPIService,
    private globalLoaderService: GlobalLoaderService,
  ) {}

  get promotionsAmount(): ActiveInactiveExpired {
    const activePromos = this.promotionsData && this.promotionsData.filter(promotion => promotion.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.promotionsData.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  /**
   * handle deleting promotion
   * @param {Promotion} promotion
   */
  removePromotion(promotion: Promotion) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Promotion',
      message: 'Are You Sure You Want to Remove Promotion?',
      yesCallback: () => {
        this.sendRemoveRequest(promotion);
      }
    });
  }

  /**
   * Removes many promotions
   * @param promotionIds string[]
   */
  removeHandlerMulty(promotionIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Promotions (${promotionIds.length})`,
      message: 'Are You Sure You Want to Remove Promotions?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(promotionIds.map(id => this.apiClientService.promotionsService().deletePromotion(id)))
          .subscribe(() => {
            promotionIds.forEach((id) => {
              const index = _.findIndex(this.promotionsData, { id: id });
              this.promotionsData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Promotion} promotion
   */
  sendRemoveRequest(promotion: Promotion) {
    this.promotionsAPIService.deletePromotion(promotion.id)
      .subscribe((data: any) => {
        this.promotionsData.splice(this.promotionsData.indexOf(promotion), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Promotion is Removed.'
        });
      });
  }


  reorderHandler(newOrder: Order) {

    this.promotionsAPIService.postNewPromotionsOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New Promotion Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  ngOnInit() {
    forkJoin([
      this.promotionsAPIService.getPromotionsData(),
      this.promotionsAPIService.getSportCategories()]
    )
    .map((data: any) => {
      const categories = data[1].body;
      return data[0].body.map((d => {
        d.categoryId = d.categoryId.map((id: string) => {
          const category = _.find(categories, (c) => c.id === id);
          return category ? category.imageTitle : '';
        });
        return d;
      }));
    })
    .subscribe((data: Promotion[]) => {
      this.promotionsData = data;
    });
  }
}
