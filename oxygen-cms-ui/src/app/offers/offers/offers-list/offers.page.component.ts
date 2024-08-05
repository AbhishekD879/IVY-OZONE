import {ApiClientService} from './../../../client/private/services/http/index';
import {GlobalLoaderService} from './../../../shared/globalLoader/loader.service';
import {Component, OnInit} from '@angular/core';
import {OffersAPIService} from '../../service/offers.api.service';
import {Offer} from '../../../client/private/models/offer.model';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {OfferCreateComponent} from '../offer-create/offer.create.component';
import {AppConstants} from '../../../app.constants';
import {HttpResponse} from '@angular/common/http';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import * as _ from 'lodash';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {Router} from '@angular/router';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'offers-page',
  templateUrl: './offers.page.component.html',
  styleUrls: ['./offers.page.component.scss']
})
export class OffersPageComponent implements OnInit {
  offersData: Array<Offer>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Module',
      property: 'moduleName'
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
    },
    {
      name: 'Show offer on',
      property: 'showOfferOn'
    },
    {
      name: 'Show offer to',
      property: 'showOfferTo'
    },
    {
      name: 'Include vip levels',
      property: 'vipLevelsInput'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    public router: Router,
    public snackBar: MatSnackBar,
    private offersAPIService: OffersAPIService,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {}

  get offersAmount(): ActiveInactiveExpired {
    const activePages = this.offersData && this.offersData.filter(offer => offer.disabled === false);
    const activePagesAmount = activePages && activePages.length;
    const inactivePagesAmount = this.offersData.length - activePagesAmount;

    return {
      active: activePagesAmount,
      inactive: inactivePagesAmount
    };
  }

  /**
   * Reorder offers
   */
  reorderHandler(newOrder: Order) {

    this.offersAPIService.postNewOffersOrder(newOrder)
      .subscribe((data: HttpResponse<Offer[]>) => {
        this.snackBar.open('New Offers Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

    /**
   * handle deleting offer
   * @param {Offer} offer
   */
  removeOffer(offer: Offer) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Offer',
      message: 'Are You Sure You Want to Remove Offer?',
      yesCallback: () => {
        this.sendRemoveRequest(offer);
      }
    });
  }

  removeHandlerMulty(offerIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Offers (${offerIds.length})`,
      message: 'Are You Sure You Want to Remove Offers?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(offerIds.map(id => this.apiClientService.offersService().deleteOffer(id)))
          .subscribe(() => {
            offerIds.forEach((id) => {
              const index = _.findIndex(this.offersData, { id: id });
              this.offersData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
        }
      });
  }

  /**
   * Send DELETE API request
   * @param {Offer} offer
   */
  sendRemoveRequest(offer: Offer) {
    this.offersAPIService.deleteOffer(offer.id)
      .subscribe((data: HttpResponse<void>) => {
        this.offersData.splice(this.offersData.indexOf(offer), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Offer is Removed'
        });
      });
  }

  /**
   * Reload offers data
   */
  reloadOffers() {
    this.offersAPIService.getOffersData()
      .map((data: HttpResponse<Offer[]>) => data.body)
      .subscribe((data: Offer[]) => {
        this.offersData = data;
      }, error => {
        this.getDataError = error.message;
      });
  }

  /**
   * Opens create offer modal window and provides action to create offer
   */
  createOffer() {
    const dialogRef = this.dialog.open(OfferCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newOffer => {
      const self = this;

      if (newOffer) {
        this.offersAPIService.postNewOffer(newOffer)
          .map((data: HttpResponse<Offer>) => data.body)
          .subscribe((newCreatedOffer: Offer) => {
            if (newCreatedOffer) {
              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Offer is Created and Stored.',
                closeCallback() {
                  self.router.navigate([`/offers/offers/${newCreatedOffer.id}`]);
                }
              });
            }
          });
      }
    });
  }

  ngOnInit() {
    this.reloadOffers();
  }
}
