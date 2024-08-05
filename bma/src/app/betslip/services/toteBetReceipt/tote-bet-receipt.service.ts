import { of as observableOf,  Observable } from 'rxjs';

import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { IPoolBetDetail, IResponseTransPoolGetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Injectable({ providedIn: BetslipApiModule })
export class ToteBetReceiptService {
  id: string = '';

  constructor(private bppService: BppService) {}

  /**
   * Gets bets receipts.
   * @return {defer.promise} - promise object
   */
  getToteBetReceipt(): Observable<IPoolBetDetail[]> {
    return !this.id ? observableOf([])
      : this.bppService.send('getPoolBetDetail', { poolBetId: this.id }).pipe(
        map((receiptData: IResponseTransPoolGetDetail): IPoolBetDetail[] => receiptData.response.poolBetDetail.poolBet));
  }
}
