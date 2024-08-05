import { Directive, Input, ElementRef, OnInit, OnChanges, SimpleChanges, EventEmitter, Output } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';
import { PriceOddsButtonService } from '@shared/components/priceOddsButton/price-odds-button.service';
import { IOutcomePrice } from '@core/models/outcome-price.model';

@Directive({
  // eslint-disable-next-line
  selector: '[sbpriceOddsDisabled]'
})
export class SBPriceOddsDisabledDirective implements OnInit, OnChanges {
  @Input() sbpriceOddsDisabled: [IOutcome, string, string, string, string, string, IOutcomePrice, boolean];
  @Output() readonly sboddsPriceDisabled: EventEmitter<boolean> = new EventEmitter();

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
    if (changes.sbpriceOddsDisabled && !changes.sbpriceOddsDisabled.firstChange) {
      this.setStatus();
    }
  }

  private setStatus(): void {
    this.outcome = this.sbpriceOddsDisabled[0];
    this.outcomeStatusCode = this.sbpriceOddsDisabled[1];
    this.marketStatusCode = this.sbpriceOddsDisabled[2];
    this.eventStatusCode = this.sbpriceOddsDisabled[3];
    this.eventDisplayed = this.sbpriceOddsDisabled[4];
    this.priceTypeCodes = this.sbpriceOddsDisabled[5];
    this.prices = this.sbpriceOddsDisabled[6];
    this.isRacing = this.sbpriceOddsDisabled[7];
    if (this.isOddsDisabled) {
      this.elementRef.nativeElement.setAttribute('disabled', this.isOddsDisabled);     
      this.elementRef.nativeElement.parentElement.classList.add('disabled');
      this.sboddsPriceDisabled.emit(true);      
    } else if (this.isOddsDisabledAndNonRunner) {
      this.elementRef.nativeElement.setAttribute('disabled', this.isOddsDisabled);
      if (this.outcome.racingFormOutcome || this.outcome.nonRunner === false || this.isRacing === true) {
        this.sboddsPriceDisabled.emit(false);
      } else {
        this.elementRef.nativeElement.parentElement.classList.add('disabled');
        this.sboddsPriceDisabled.emit(true);
      }
    } else {
      this.elementRef.nativeElement.removeAttribute('disabled');
      this.elementRef.nativeElement.parentElement.classList.remove('disabled');
      this.sboddsPriceDisabled.emit(false);
    }
  }

  /**
   * Checking event/marker/outcome is suspended or not.
   *
   * @private
   * @return {Boolean}
   */
  private get isOddsDisabled(): boolean {   
    return this.eventStatusCode === 'S' ||
      this.marketStatusCode === 'S' ||
      this.outcomeStatusCode === 'S' 
  }
  private set isOddsDisabled(value:boolean){}

  /**
   * Checking event/marker/outcome is suspended or not.
   *
   * @private
   * @return {Boolean}
   */
  private get isOddsDisabledAndNonRunner(): boolean {
    const prices = this.outcome.prices && this.outcome.prices[0];
    const isRacing = this.priceOddsButtonService.isRacingOutcome(this.outcome, this.priceTypeCodes);
    return this.isOddsDisabled ||
      this.eventDisplayed === 'N' ||
      this.outcome.nonRunner ||
      (!prices && !isRacing);
  }
  private set isOddsDisabledAndNonRunner(value:boolean){}
}
