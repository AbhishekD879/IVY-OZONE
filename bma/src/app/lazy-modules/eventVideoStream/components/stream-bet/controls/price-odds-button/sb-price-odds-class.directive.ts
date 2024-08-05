import { Directive, ElementRef, Input, OnChanges, OnInit, SimpleChanges, OnDestroy } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IOutcome } from '@core/models/outcome.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  // eslint-disable-next-line
  selector: '[sbPriceOddsClass]'
})
export class SBPriceOddsClassDirective implements OnChanges, OnInit, OnDestroy {
  @Input() sbPriceOddsClass: [IOutcome, string, string, boolean];

  outcome: IOutcome;
  cssClass: string = '';
  priceClass: string = '';

  private uniqueId: string;
  private activeClass = 'active';

  constructor(
    private elementRef: ElementRef,
    private pubsubService: PubSubService,
    private coreToolsService: CoreToolsService,
    private rendererService: RendererService
  ) {
  }

  ngOnInit(): void {
      this.setClasses(); 
      this.uniqueId = `sb-bet-${this.outcome.id}-${this.coreToolsService.uuid()}`; 
      this.pubsubService.subscribe(this.uniqueId,
        this.pubsubService.API.REMOVE_FROM_SB_QUICKBET, () => {
            this.rendererService.renderer.removeClass(this.elementRef.nativeElement, this.activeClass);
        });  
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.uniqueId);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.sbPriceOddsClass && !changes.sbPriceOddsClass.firstChange) {
      this.setClasses();
    }
  }

  private setClasses(): void {
    this.outcome = this.sbPriceOddsClass[0];
    this.cssClass = this.sbPriceOddsClass[1];
    this.priceClass = this.sbPriceOddsClass[2];
    this.elementRef.nativeElement.setAttribute('class', this.getOddsClasses);
  }

  /**
   * Return active button class and classes of up/down price changes.
   * @private
   * @return {Array}
   */
  private get getOddsClasses(): string {
    const classes = ['snb-btn-bet'];

    if (this.sbPriceOddsClass[3]) {
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
}
