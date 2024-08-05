import { Directive, Output, ChangeDetectorRef, Input, EventEmitter, OnInit, OnChanges, SimpleChanges, OnDestroy } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { IOutcome } from '@core/models/outcome.model';
import { PriceOddsButtonService } from '@shared/components/priceOddsButton/price-odds-button.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';

@Directive({
  // eslint-disable-next-line
  selector: '[priceOddsValue]'
})
export class PriceOddsValueDirective implements OnInit, OnChanges, OnDestroy {
  @Input() priceOddsValue: [IOutcome, number, number, string];
  @Input() oddsPrice: string;
  @Output() readonly oddsPriceChange: EventEmitter<any> = new EventEmitter();

  outcome: IOutcome;
  priceDen: number;
  priceNum: number;
  priceTypeCodes: string;
  private uniqueId: string;

  constructor(
    private fracToDecService: FracToDecService,
    private changeDetectorRef: ChangeDetectorRef,
    private priceOddsButtonService: PriceOddsButtonService,
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService
  ) {}

  ngOnInit(): void {
    this.setPrices();
    this.uniqueId = `bet-${this.outcome.id}-${this.coreToolsService.uuid()}`;
    this.pubSubService.subscribe(this.uniqueId, this.pubSubService.API.SET_ODDS_FORMAT, () => this.setPrices());
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.uniqueId);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.priceOddsValue && !changes.priceOddsValue.firstChange) {
      this.setPrices();
    }
  }

  private setPrices(): void {
    this.outcome = this.priceOddsValue[0];
    this.priceDen = this.priceOddsValue[1];
    this.priceNum = this.priceOddsValue[2];
    this.priceTypeCodes = this.priceOddsValue[3];
    this.oddsPriceChange.emit(this.oddsPriceValue);
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Set Odds Price
   *
   * @private
   * @returns {string}
   */
  private get oddsPriceValue(): string {
    const prices = this.outcome.prices && this.outcome.prices[0];
    switch (true) {
      case this.priceOddsButtonService.isRacingOutcome(this.outcome, this.priceTypeCodes):
        return 'SP';
      case (!prices):
        return 'SUSP';
      default:
        return this.outputPrice;
    }
  }
  private set oddsPriceValue(value:string){}

  /**
   * Return price in correct format (frac/dec).
   * @private
   * @return {string}
   */
  private get outputPrice(): string {
    return <string>this.fracToDecService.getFormattedValue(this.priceNum, this.priceDen);
  }
  private set outputPrice(value:string){}
}
