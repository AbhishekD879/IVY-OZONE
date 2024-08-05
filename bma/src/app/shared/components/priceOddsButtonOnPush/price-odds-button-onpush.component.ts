import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  HostBinding,
  Input,
  OnChanges,
  SimpleChanges
} from '@angular/core';

@Component({
  selector: 'button[price-odds-button]',
  templateUrl: 'price-odds-button-onpush.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PriceOddsButtonOnPushComponent implements OnChanges {
  @Input() priceNum: number;
  @Input() priceDen: number;
  @Input() priceDec: number;
  @Input() priceType: string;
  @Input() categoryId?: string;

  @Input() handicapVal?: string;

  @Input() active: boolean;
  @Input() displayed: string;
  @Input() eventStatusCode: string;
  @Input() marketStatusCode: string;
  @Input() outcomeStatusCode: string;

  @Input() head?: string;

  @Input() isRacing?: boolean;
  @Input() nonRunner?: boolean;

  @HostBinding('attr.disabled') disabled: string | null;
  isFootball: boolean;

  // Time after which class given to price-odds-button after live Update should be removed
  private readonly hideLiveUpdateClassTime: number = 2000;

  constructor(
    private elementRef: ElementRef
  ) { }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.handicapVal) {
      this.handicapVal = this.handicapVal.replace(/,/g, '');
    }
    if (this.categoryId) {
      this.isFootball = this.categoryId === '16';
    }
    if (changes.priceDec && !changes.priceDec.firstChange) {
      const priceChangeClass = changes.priceDec.previousValue > changes.priceDec.currentValue ? 'bet-down' : 'bet-up';

      requestAnimationFrame(() => {
        this.elementRef.nativeElement.classList.add(priceChangeClass);
      });

      setTimeout(() => {
        requestAnimationFrame(() => {
          this.elementRef.nativeElement.classList.remove(priceChangeClass);
        });
      }, this.hideLiveUpdateClassTime);
    }

    this.disabled = this.isDisabled();
  }

  /**
   * Disabled outcome status
   * Implemented as PriceOddsDisabledDirective.isOddsDisabled
   * TODO: PriceOddsButtonService outdated after applying this implementation
   */
  private isDisabled(): string | null {
    return this.eventStatusCode === 'S' || this.marketStatusCode === 'S' || this.outcomeStatusCode === 'S' || this.displayed === 'N' ||
      this.nonRunner || (!this.priceType && !this.isRacing) ? 'disabled' : null;
  }
}
