import { Component, OnInit } from '@angular/core';
import { BSCONST, BS_LABELS, dataTableColumns } from '../service/betslip.constants';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ApiClientService} from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IbetSlipAccaTable, IbetslipsAcca, IoddsBoost } from '../service/betslip.model';
import { Observable, forkJoin } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

 @Component({
  selector: 'betslip-main',
  templateUrl: './betslip-main.component.html'
})
export class BetslipMainComponent implements OnInit {
   betslipInitTable : IbetSlipAccaTable[];
   showtabel:boolean;
   BSLABELS = BS_LABELS;
   betslipLabels = BSCONST;
   cmsdataTableColumns = dataTableColumns;
   betSlipAccaResp:IbetslipsAcca;
   isLoading:boolean;
   betSlipOddsBoost: IoddsBoost;

  
  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
  ) { }

  ngOnInit(): void {
    this.loadInitialData();
  }
  /**
   * creating a static table with active or disable status
   */
  private createBetslipTable() {
    this.betslipInitTable = [];
        this.betslipInitTable.push({
          href: this.betslipLabels.BS_ACCA_INSURANCE,
          enable: this.betSlipAccaResp && this.betSlipAccaResp.enabled,
          tabName: this.betslipLabels.ACCA_INS_MSG,
        }
        ,{
          href: this.betslipLabels.BS_ODDS_BOOST,
          enable: this.betSlipOddsBoost && this.betSlipOddsBoost.oddsBoostMsgEnabled,
          tabName: this.betslipLabels.ODDS_BOOST_MSG,
        }
      );
    this.showtabel = true;
  }
  public reorderHandler (event?){};

  private getAccaInsurance(): Observable<any> {
    return this.apiClientService
    .betslipService().getBetSlip().map((response: HttpResponse<any>) => response.body);
  }

  private getOddsBoost(): Observable<any> {
    return this.apiClientService
    .betslipService().getOddsBoost().map((response: HttpResponse<any>) => response.body);
  }

  /**
   * load the intial data to render the dom
   */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();
    forkJoin([this.getAccaInsurance(),this.getOddsBoost()]).subscribe((data: [IbetslipsAcca,IoddsBoost]) => {
        this.betSlipAccaResp = data && data[0];
        this.betSlipOddsBoost = data.length > 1 && data[1];
      this.createBetslipTable()
        this.globalLoaderService.hideLoader();
        this.isLoading = false;  
      },
      error => {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
      });
  }
}
