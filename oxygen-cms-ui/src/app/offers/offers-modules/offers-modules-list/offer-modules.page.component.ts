import {ApiClientService} from './../../../client/private/services/http/index';
import {GlobalLoaderService} from './../../../shared/globalLoader/loader.service';
import {Component, OnInit} from '@angular/core';
import {OfferModuleAPIService} from '../../service/offer-module.api.service';
import {OfferModule} from '../../../client/private/models/offermodule.model';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {OfferModuleCreateComponent} from '../offers-module-create/offer-module.create.component';
import {AppConstants} from '../../../app.constants';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'offer-modules-page',
  templateUrl: './offer-modules.page.component.html',
  styleUrls: ['./offer-modules.page.component.scss']
})
export class OfferModulesPageComponent implements OnInit {
  offerModulesData: Array<OfferModule>;
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
      name: 'Show module on ',
      property: 'showModuleOn'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];
  constructor(
    public snackBar: MatSnackBar,
    private offerModuleAPIService: OfferModuleAPIService,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService
  ) {}

  /**
   * Reorder offer modules
   */
  reorderHandler(newOrder: Order) {

    this.offerModuleAPIService.postNewOfferModulesOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New Offer Modules Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

    /**
   * handle deleting offer module
   * @param {Offer} offer
   */
  removeOfferModule(offerModule: OfferModule) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Offer Module',
      message: 'Are You Sure You Want to Remove Offer Module?',
      yesCallback: () => {
        this.sendRemoveRequest(offerModule);
      }
    });
  }

  removeHandlerMulty(offerModulesIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Offer Module (${offerModulesIds.length})`,
      message: 'Are You Sure You Want to Remove Offer Modules?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(offerModulesIds.map(id => this.apiClientService.offerModulesService().deleteOfferModule(id)))
          .subscribe(() => {
            offerModulesIds.forEach((id) => {
              const index = _.findIndex(this.offerModulesData, { id: id });
              this.offerModulesData.splice(index, 1);
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
  sendRemoveRequest(offerModule: OfferModule) {
    this.offerModuleAPIService.deleteOfferModule(offerModule.id)
      .subscribe((data: any) => {
        this.offerModulesData.splice(this.offerModulesData.indexOf(offerModule), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Offer Module is Removed.'
        });
      });
  }

  get offerModulesAmount(): ActiveInactiveExpired {
    const activePages = this.offerModulesData && this.offerModulesData.filter(offerModule => offerModule.disabled === false);
    const activePagesAmount = activePages && activePages.length;
    const inactivePagesAmount = this.offerModulesData.length - activePagesAmount;

    return {
      active: activePagesAmount,
      inactive: inactivePagesAmount
    };
  }

  /**
   * Reload offers data
   */
  reloadOffers() {
    this.offerModuleAPIService.getOfferModulesData()
      .subscribe((data: any) => {
        this.offerModulesData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  /**
   * Opens create offer module modal window and provides action to create offer module
   */
  createOfferModule() {
    const dialogRef = this.dialog.open(OfferModuleCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newOfferModule => {
      if (newOfferModule) {
        this.offerModuleAPIService.postNewOfferModule(newOfferModule)
          .subscribe(isOk => {
            if (isOk) {
              this.offerModulesData.push(newOfferModule);
              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Offer Module is Created and Stored.'
              });
              this.reloadOffers();
            }
          });
      }
    });
  }

  ngOnInit() {
    this.reloadOffers();
  }
}
