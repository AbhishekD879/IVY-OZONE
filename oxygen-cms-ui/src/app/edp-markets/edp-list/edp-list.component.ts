import {Component, OnInit} from '@angular/core';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../shared/dialog/dialog.service';
import {ApiClientService} from '../../client/private/services/http';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {EdpMarket} from '../../client/private/models/edpmarket.model';
import {CreateEdpMarketComponent} from '../create-edp-market/create-edp-market.component';
import {Router} from '@angular/router';
import {AppConstants} from '../../app.constants';
import {Order} from '../../client/private/models/order.model';

@Component({
  selector: 'app-edp-list',
  templateUrl: './edp-list.component.html',
  styleUrls: ['./edp-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class EdpListComponent implements OnInit {

  public isLoading: boolean = false;
  public searchField: string = '';
  public edpMarkets: EdpMarket[] = [];

  filterProperties: string[] = [
    'name'
  ];

  dataTableColumns: any[] = [
    {
      name: 'Title',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Last Item',
      property: 'lastItem',
      type: 'boolean'
    }];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
    public snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.showHideSpinner();
    this.apiClientService.edp()
        .findAllByBrand()
        .map((edmResponse: HttpResponse<EdpMarket[]>) => {
          return edmResponse.body;
        })
        .subscribe((edpList: EdpMarket[]) => {
          this.edpMarkets = edpList;
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  public createEdpMarket(): void {
    this.dialogService.showCustomDialog(CreateEdpMarketComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New EDP Market Block',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (edpMarket: EdpMarket) => {
        this.apiClientService.edp()
            .add(edpMarket)
            .map((res: HttpResponse<EdpMarket>) => res.body)
            .subscribe((market: EdpMarket) => {
          this.edpMarkets.unshift(market);
          this.router.navigate([`/edp-markets/${market.id}`]);
        }, () => {
          console.error('Can not create EDP market');
        });
      }
    });
  }

  public removeEdpMarket(edpMarket: EdpMarket): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove EDP Market',
      message: `Are You Sure You Want to Remove Edp Market: ${edpMarket.name}?`,
      yesCallback: () => {
        this.edpMarkets = this.edpMarkets.filter((l) => {
          return l.id !== edpMarket.id;
        });
        this.apiClientService.edp().remove(edpMarket.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'EDP Market is Removed.'
          });
        });
      }
    });
  }

  public reorderHandler(newOrder: Order): void {
    this.globalLoaderService.showLoader();
    this.apiClientService
        .edp()
        .postNewOrder(newOrder)
        .subscribe(() => {
          this.globalLoaderService.hideLoader();
          this.snackBar.open('New Edp Markets Order Saved!!', 'OK!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

}
