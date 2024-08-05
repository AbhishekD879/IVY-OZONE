import { Component, EventEmitter, Inject, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { IBetReceiptBuilder } from './../../models/bet-receipt-builder.model';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'bet-receipt',
  templateUrl: './bet-receipt.component.html'
})
export class BetReceiptComponent implements OnInit, OnDestroy {
  @Input() betsReceiptData: IBetReceiptBuilder;
  @Input() poolCurrencySymbol: string;
  // @Input() lottobetslipData;
  @Output() readonly betReceiptContinue: EventEmitter<void> = new EventEmitter();
  @Output() readonly scrollToBetReceipt: EventEmitter<void> = new EventEmitter();

  expanded: boolean;

  constructor(
    @Inject(DOCUMENT) private document: any,
    private rendererService: RendererService,
  ) {}

  /**
   * Event Listener callbacks
   */
  eventClickSub: any = () => {};

  ngOnInit(): void {
    this.expanded = false;

    this.closeReceiptOnOutsideClick = this.closeReceiptOnOutsideClick.bind(this);
    this.removeEventListeners = this.removeEventListeners.bind(this);

    this.eventClickSub = this.rendererService.renderer.listen(this.document, 'click', this.closeReceiptOnOutsideClick.bind(this));
    if (this.scrollToBetReceipt) {
      this.scrollToBetReceipt.emit();
    }
  }

  ngOnDestroy(): void {
    this.removeEventListeners();
  }

  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Call on continue callback
   */
  continue(): void {
    if (this.betReceiptContinue) {
      this.betReceiptContinue.emit();
    }
  }

  /**
   * @param {object} event
   * @private
   */
  private closeReceiptOnOutsideClick(event: Event): void {
    event.stopPropagation();
    this.continue();
  }

  /**
   * @private
   */
  private removeEventListeners(): void {
    this.eventClickSub();
  }
}
