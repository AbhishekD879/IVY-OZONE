import { ILottoResult } from './../../models/lotto-result.model';
import { Injectable } from '@angular/core';

@Injectable()
export class LottoReceiptService {
  receiptData: ILottoResult = {};

  getReceipt(): ILottoResult {
    const data = this.receiptData;
    this.receiptData = {};
    return data;
  }

  setReceipt(data: ILottoResult): void {
    this.receiptData = data;
  }
}
