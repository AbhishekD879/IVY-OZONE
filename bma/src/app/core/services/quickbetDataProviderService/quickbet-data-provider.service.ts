import { Subject } from 'rxjs';
import { Injectable } from '@angular/core';

import { IRemoteBetslipBet } from '../remoteBetslip/remote-betslip.constant';
import { IQuickbetReceiptDetailsModel, IYCBetReceiptModel } from '@app/quickbet/models/quickbet-receipt.model';

@Injectable()
export class QuickbetDataProviderService {

  private placeBetObservable: Subject<IRemoteBetslipBet>;
  private quickbetReceiptObservable: Subject<IQuickbetReceiptDetailsModel[] | IYCBetReceiptModel>;

  constructor() {
    this.placeBetObservable = new Subject<IRemoteBetslipBet>();
    this.quickbetReceiptObservable = new Subject<IQuickbetReceiptDetailsModel[] | IYCBetReceiptModel>();
  }

  get quickbetPlaceBetListener(): Subject<IRemoteBetslipBet> {
    return this.placeBetObservable;
  }
  set quickbetPlaceBetListener(value:Subject<IRemoteBetslipBet>){}
  get quickbetReceiptListener(): Subject<IQuickbetReceiptDetailsModel[] | IYCBetReceiptModel> {
    return this.quickbetReceiptObservable;
  }
  set quickbetReceiptListener(value:Subject<IQuickbetReceiptDetailsModel[] | IYCBetReceiptModel>){}
}
