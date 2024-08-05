import { Directive, Input, ElementRef, OnInit, OnChanges, SimpleChanges, EventEmitter, Output } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';
import { PriceOddsButtonService } from '@shared/components/priceOddsButton/price-odds-button.service';
import { IOutcomePrice } from '@core/models/outcome-price.model';

@Directive({
  // eslint-disable-next-line
  selector: '[priceOddsDisabled]'
})
export class PriceOddsDisabledDirective implements OnInit, OnChanges {
  @Input() priceOddsDisabled: [IOutcome, string, string, string, string, string, IOutcomePrice, boolean];
  @Output() readonly oddsPriceDisabled: EventEmitter<boolean> = new EventEmitter();

  outcome: IOutcome;
  outcomeStatusCode: string;
  marketStatusCode: string;
  eventStatusCode: string;
  eventDisplayed: string;
  priceTypeCodes: string;
  prices: IOutcomePrice;
  isRacing?: boolean;

  constructor(private elementRef: ElementRef, private priceOddsButtonService: PriceOddsButtonService) {}

  ngOnInit(): void {
    this.setStatus();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.priceOddsDisabled && !changes.priceOddsDisabled.firstChange) {
      this.setStatus();
    }
  }

  private setStatus(): void {
    this.outcome = this.priceOddsDisabled[0];
    this.outcomeStatusCode = this.priceOddsDisabled[1];
    this.marketStatusCode = this.priceOddsDisabled[2];
    this.eventStatusCode = this.priceOddsDisabled[3];
    this.eventDisplayed = this.priceOddsDisabled[4];
    this.priceTypeCodes = this.priceOddsDisabled[5];
    this.prices = this.priceOddsDisabled[6];
    this.isRacing = this.priceOddsDisabled[7];
    if (this.isOddsDisabled) {
      this.elementRef.nativeElement.setAttribute('disabled', this.isOddsDisabled);
      if (this.outcome.racingFormOutcome || this.outcome.nonRunner === false || this.isRacing === true) {
        this.oddsPriceDisabled.emit(false);
      } else {
        this.elementRef.nativeElement.parentElement.classList.add('disabled');
        this.oddsPriceDisabled.emit(true);
      }
    } else {
      this.elementRef.nativeElement.removeAttribute('disabled');
      this.elementRef.nativeElement.parentElement.classList.remove('disabled');
      this.oddsPriceDisabled.emit(false);
    }
  }

  /**
   * Checking event/marker/outcome is suspended or not.
   *
   * @private
   * @return {Boolean}
   */
  private get isOddsDisabled(): boolean {
    const prices = this.outcome.prices && this.outcome.prices[0];
    const isRacing = this.priceOddsButtonService.isRacingOutcome(this.outcome, this.priceTypeCodes);
    return this.eventStatusCode === 'S' ||
      this.marketStatusCode === 'S' ||
      this.outcomeStatusCode === 'S' ||
      this.eventDisplayed === 'N' ||
      this.outcome.nonRunner ||
      (!prices && !isRacing);
  }
  private set isOddsDisabled(value:boolean){}
}
