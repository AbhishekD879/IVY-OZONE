import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Order } from '@root/app/client/private/models/order.model';
import { TableColumn } from '@root/app/client/private/models/table.column.model';
import { ApiClientService } from '@root/app/client/private/services/http';
import { ILotto, ILottos, ILottoUpdate } from '../lotto.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '../../app.constants';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { LOTTOS_UPDATE, LOTTO_ROUTES, LOTTO_VALUES } from '../lotto.constants';
@Component({
  selector: 'app-lotto-list',
  templateUrl: './lotto-list.component.html'
})
export class LottoListComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  public mainLotto: ILotto;
  public updateLotto: ILottoUpdate;
  public isLoading: boolean = false;
  public lotto: ILottos;
  brand: string = this.brandService.brand;
  public error: string;
  
  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Lottery Title',
      property: 'label',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Lotto Game ID',
      property: 'ssMappingId'
    },
    {
      name: 'SVG ID',
      property: 'svgId',
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean',
      isReversed: false
    }
  ];
  
  constructor(
    private router: Router,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private brandService: BrandService,
    ) { }
  
  ngOnInit() {
    this.loadInitialData();
    this.mainLotto = LOTTO_VALUES;
  }
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.lottosService()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: ILotto) => {
        this.mainLotto = data;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
  }
  public isValidModel(Lottery: ILotto): boolean {
    if(Lottery.lottoConfig.length > 0) {
      return Lottery && Lottery.globalBannerText && Lottery.globalBannerLink && Lottery.globalBannerText?.length <= 100 && Lottery.dayCount <= 30;
    }
  }
  reorderHandler(order: Order): void {
    this.apiClientService.lottosService()
    .reorder(order)
    .subscribe(() => {
      this.snackBar.open(`Segments order saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    })
  }
  public removeLotto(lottery: ILottos): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Segment',
      message: `Are You Sure You Want to Remove ${lottery.label} Segment`,
      yesCallback: () => {
        this.apiClientService
          .lottosService()
          .remove(lottery.id)
          .subscribe(() => {
            _.remove(this.mainLotto.lottoConfig, {id: lottery.id});
          });
      }
    });
  }
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        break;
    }
  }
  
  private revert(): void {
    this.ngOnInit();
  }
  private save(): void {
      this.sendRequest('putAllByBrand');
  }
public sendRequest(requestType: string, isInitialLoad:boolean = false): void {
    this.updateLotto = LOTTOS_UPDATE;
    this.updateLotto.ids = [];
    this.mainLotto.lottoConfig.forEach((data: any) => {
    this.updateLotto?.ids.push(data.id);
  });
  this.updateLotto.globalBannerLink = this.mainLotto.globalBannerLink;
  this.updateLotto.globalBannerText = this.mainLotto.globalBannerText;
  this.updateLotto.dayCount = this.mainLotto.dayCount;
  this.globalLoaderService.showLoader();
  this.apiClientService.lottosService()[requestType](this.updateLotto)
    .map((response) => response.body)
    .subscribe((data: ILottoUpdate) => {
      this.updateLotto = data;
      this.actionButtons.extendCollection(this.updateLotto);
      if(!isInitialLoad){
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        })
        this.globalLoaderService.hideLoader();
      }}, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });   
        this.globalLoaderService.hideLoader();
    })
}
  public createLotto(): void {
    this.router.navigate([`${LOTTO_ROUTES.base}/add`]);
  }
}
