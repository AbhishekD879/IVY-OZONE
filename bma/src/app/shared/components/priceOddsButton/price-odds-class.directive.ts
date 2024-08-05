import { Directive, ElementRef, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IOutcome } from '@core/models/outcome.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IQuickbetSelectionModel } from '@core/models/quickbet-selection.model';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  // eslint-disable-next-line
  selector: '[priceOddsClass]'
})
export class PriceOddsClassDirective implements OnChanges, OnInit, OnDestroy {
  @Input() priceOddsClass: [IOutcome, string, string];

  outcome: IOutcome;
  cssClass: string = '';
  priceClass: string = '';

  private uniqueId: string;
  private activeClass = 'active';
  private isStreamBetUpdate: boolean = false;

  constructor(
    private betSlipSelectionsData: BetslipSelectionsDataService,
    private elementRef: ElementRef,
    private pubsubService: PubSubService,
    private coreToolsService: CoreToolsService,
    private rendererService: RendererService
  ) {
  }

  ngOnInit(): void {
    this.setClasses();
    this.uniqueId = `bet-${this.outcome.id}-${this.coreToolsService.uuid()}`;
    this.pubsubService.subscribe(this.uniqueId,
      this.pubsubService.API.BETSLIP_SELECTIONS_UPDATE, () => this.setClasses());

    this.pubsubService.subscribe(this.uniqueId,
      this.pubsubService.API.ADD_TO_QUICKBET, (selectionData: IQuickbetSelectionModel) => {
        if (this.checkOutcomeId(selectionData) && !selectionData.isStreamBet) {
          this.rendererService.renderer.addClass(this.elementRef.nativeElement, this.activeClass);
        }
      });

    this.pubsubService.subscribe(this.uniqueId,
      this.pubsubService.API.REMOVE_FROM_QUICKBET, (data: any) => {
        if (!(data.isAddToBetslip as boolean) && this.checkOutcomeId(data as IQuickbetSelectionModel) && !data.isStreamBet) {
          this.rendererService.renderer.removeClass(this.elementRef.nativeElement, this.activeClass);
        }
      });

      this.pubsubService.subscribe(this.uniqueId, this.pubsubService.API.ADD_TO_QUICKBET_BMA_STREAM_BET,
        (selectionData: IQuickbetSelectionModel) => {
          this.isStreamBetUpdate = selectionData.isStreamBet;
        });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.uniqueId);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.priceOddsClass && !changes.priceOddsClass.firstChange && !this.isStreamBetUpdate) {
      this.setClasses();
    }
  }

  private setClasses(): void {
    this.outcome = this.priceOddsClass[0];
    this.cssClass = this.priceOddsClass[1];
    this.priceClass = this.priceOddsClass[2];
    this.elementRef.nativeElement.setAttribute('class', this.getOddsClasses);
    this.isStreamBetUpdate = false;
  }

  /**
   * Return active button class and classes of up/down price changes.
   * @private
   * @return {Array}
   */
  private get getOddsClasses(): string {
    const classes = ['btn-bet'];

    if (this.isActive) {
      classes.push(this.activeClass);
    }

    if (this.priceClass) {
      classes.push(this.priceClass);
    }

    if (this.cssClass) {
      classes.push(this.cssClass);
    }

    return classes.toString().replace(/,/g, ' ');
  }
  private set getOddsClasses(value:string){}

  /**
   * Return true/false in case user adding bet to the betslip
   * @private
   *
   * @return {boolean}
   */
  private get isActive(): boolean {
    return this.outcome && !!this.betSlipSelectionsData.getSelectionsByOutcomeId(this.outcome.id).length;
  }
  private set isActive(value:boolean){}

  /**
   * Check directive outcome and channel outcome
   * @private
   * @params {IQuickbetSelectionModel}
   * @return {boolean}
   */
  private checkOutcomeId(selectionData: IQuickbetSelectionModel): boolean {
    const outcomeId = selectionData &&
      (selectionData.outcomeId || selectionData.outcomes && selectionData.outcomes.length && selectionData.outcomes[0].id);
    return !!outcomeId && outcomeId === this.outcome.id;
  }
}
