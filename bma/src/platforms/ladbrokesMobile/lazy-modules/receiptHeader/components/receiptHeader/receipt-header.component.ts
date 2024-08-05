import { Component } from '@angular/core';
import {
   ReceiptHeaderComponent as BaseReceiptHeaderComponent
} from '@lazy-modules/receiptHeader/components/receiptHeader/receipt-header.component';

@Component({
  selector: 'receipt-header',
  templateUrl: '../../../../../../app/lazy-modules/receiptHeader/components/receiptHeader/receipt-header.component.html',
  styleUrls: [
    '../../../../../../app/lazy-modules/receiptHeader/components/receiptHeader/receipt-header.component.scss',
    'receipt-header.component.scss'
  ]
})
export class ReceiptHeaderComponent extends BaseReceiptHeaderComponent {}
