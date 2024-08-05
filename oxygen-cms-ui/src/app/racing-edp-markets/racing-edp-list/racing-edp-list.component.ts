import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { DialogService } from '../../shared/dialog/dialog.service';
import { ApiClientService } from '../../client/private/services/http';
import { RacingEdpMarket } from '../../client/private/models/racing.edpmarket.model';
import { CreateRacingEdpMarketComponent } from '../create-racing-edp-market/create-racing-edp-market.component';
import { AppConstants } from '../../app.constants';
import { DataTableColumn } from '../../client/private/models';
import {
  RACING_EDP_TABLE_COLUMNS,
  FILTER_PROPERTIES, RACING_TYPE,
  SAVE_CONFIRMATION_DIALOG, RACING_EDP_ROUTES,
  RACING_EDP_ERRORS, REMOVE_CONFIRMATION_DIALOG,
  REMOVE_NOTIFICATION_DIALOG,
  SNACKBAR
} from '../constants/racing-edp.constants';
import { Order } from '../../client/private/models/order.model';

@Component({
  selector: 'app-racing-edp-list',
  templateUrl: './racing-edp-list.component.html'
})
export class RacingEdpListComponent implements OnInit {

  isLoading: boolean = false;
  racingEDPMarkets: RacingEdpMarket[] = [];
  searchField: string = '';
  dataTableColumns: DataTableColumn[] = RACING_EDP_TABLE_COLUMNS;
  filterProperties: string[] = FILTER_PROPERTIES;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    public snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.apiClientService.racingEdp()
        .findAllByBrand()
        .map((response: HttpResponse<RacingEdpMarket[]>) => {
          return response.body;
        })
        .subscribe((edpList: RacingEdpMarket[]) => {
          this.racingEDPMarkets = edpList;
          this.racingEDPMarkets.forEach((market) => {
            const racingGroups = [];
            if (market.isHR) {
              racingGroups.push(RACING_TYPE.horseRacing);
            }
            if (market.isGH) {
              racingGroups.push(RACING_TYPE.greyHound);
            }
            market.racing = racingGroups.length ? racingGroups.join(', ') : '';
          });
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  /**
   * Create Racing EDP Market
   */
  createRacingEdpMarket(): void {
    this.dialogService.showCustomDialog(CreateRacingEdpMarketComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_CONFIRMATION_DIALOG.title,
      yesOption: SAVE_CONFIRMATION_DIALOG.yesOption,
      noOption: SAVE_CONFIRMATION_DIALOG.noOption,
      yesCallback: (edpMarket: RacingEdpMarket) => {
        this.apiClientService.racingEdp()
            .add(edpMarket)
            .map((res: HttpResponse<RacingEdpMarket>) => res.body)
            .subscribe((market: RacingEdpMarket) => {
          this.racingEDPMarkets.unshift(market);
          this.router.navigate([`${RACING_EDP_ROUTES.base}/${market.id}`]);
        }, () => {
          console.error(RACING_EDP_ERRORS.createError);
        });
      }
    });
  }

  /**
   * Remove Racing EDP market
   * @param {RacingEdpMarket} racingEDPMarket
   */
  removeRacingEdpMarket(racingEDPMarket: RacingEdpMarket): void {
    this.dialogService.showConfirmDialog({
      title: REMOVE_CONFIRMATION_DIALOG.title,
      message: `${REMOVE_CONFIRMATION_DIALOG.message} ${racingEDPMarket.name}?`,
      yesCallback: () => {
        this.racingEDPMarkets = this.racingEDPMarkets.filter((market: RacingEdpMarket) => {
          return market.id !== racingEDPMarket.id;
        });
        this.apiClientService.racingEdp().remove(racingEDPMarket.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: REMOVE_NOTIFICATION_DIALOG.title,
            message: REMOVE_NOTIFICATION_DIALOG.message
          });
        });
      }
    });
  }

  /**
   * Reordering racing edp markets
   * @param {order} newOrder
   */
  reorderHandler(newOrder: Order): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
      .racingEdp()
      .postNewOrder(newOrder)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.snackBar.open(SNACKBAR.message, SNACKBAR.action, {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
   * To show or hide spinner
   * @param {boolean} toShow
   */
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

}
