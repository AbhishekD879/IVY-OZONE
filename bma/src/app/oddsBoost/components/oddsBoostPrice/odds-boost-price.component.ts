import { AfterViewInit, Component, ElementRef, Input, OnDestroy, OnInit, QueryList, ViewChildren } from '@angular/core';

import { OddsBoostPriceService } from '@oddsBoost/services/odds-boost-price.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { UserService } from '@core/services/user/user.service';
import { IPrice, IPriceRangeItem } from './odds-boost-price.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'odds-boost-price',
  templateUrl: './odds-boost-price.component.html',
  styleUrls: ['./odds-boost-price.component.scss']
})
export class OddsBoostPriceComponent implements OnInit, AfterViewInit, OnDestroy {

  private static id: number = 0;

  // Odds format:
  //   frac  - fractional
  //   dec   - decimal
  //   auto  - use format from user settings (userService.oddsFormat)
  @Input() format: 'frac' | 'dec' | 'auto' = 'auto';

  // Old/new price
  @Input() oldPrice: IPrice;
  @Input() newPrice: IPrice;

  // Delay before showing animation
  @Input() animationDelay: number = 200;

  @ViewChildren('numbersList') numbersLists: QueryList<ElementRef<HTMLElement>>;

  animate: boolean = false;
  priceRange: IPriceRangeItem[] = [];

  private readonly animationDuration: number = 1000;
  private resizeTimer: number;
  private cmpId: string = `OddsBoostPriceComponent-${++OddsBoostPriceComponent.id}`;

  constructor(
    private oddsBoostPriceService: OddsBoostPriceService,
    private windowRefService: WindowRefService,
    private userService: UserService,
    private pubSubService: PubSubService
  ) {
    this.adjustPricesWidth = this.adjustPricesWidth.bind(this);
  }

  ngOnInit(): void {
    this.applyAnimation();

    this.pubSubService.subscribe(this.cmpId, this.pubSubService.API['show-slide-out-betslip-true'], () => this.betslipShown());
  }

  ngAfterViewInit(): void {
    this.resizeTimer = this.windowRefService.nativeWindow.setTimeout(this.adjustPricesWidth, this.animationDuration);
  }

  ngOnDestroy(): void {
    this.windowRefService.nativeWindow.clearTimeout(this.resizeTimer);
    this.pubSubService.unsubscribe(this.cmpId);
  }

  trackByIndex(item: number, index: number): any {
    return index;
  }

  private applyAnimation(): void {
    this.priceRange = this.getFormat() === 'frac' ?
      this.getFractionalPriceRange() :
      this.getDecimalPriceRange();

    this.windowRefService.nativeWindow.setTimeout(() => {
      this.animate = true;
    }, this.animationDelay);
  }

  private getFractionalPriceRange(): IPriceRangeItem[] {
    return this.oddsBoostPriceService.getFractionalPriceRange(this.oldPrice, this.newPrice);
  }

  private getDecimalPriceRange(): IPriceRangeItem[] {
    return this.oddsBoostPriceService.getDecimalPriceRange(this.oldPrice, this.newPrice);
  }

  private getFormat(): 'frac' | 'dec' {
    return this.format === 'auto' ? this.userService.oddsFormat : this.format;
  }

  private adjustPricesWidth(): void {
    this.numbersLists.forEach((numbersList: ElementRef) => {
      const ul = numbersList.nativeElement.firstElementChild;
      const activePrice = ul && (ul.classList.contains('scroll-up') ? ul.firstElementChild : ul.lastElementChild);

      if (activePrice) {
        // Reset width property to correctly fit into needed space
        activePrice.style.display = 'inline-block';
        numbersList.nativeElement.style.width = `${activePrice.offsetWidth}px`;
      }
    });
  }

  private betslipShown(): void {
    // Fix for BMA-43358
    if (this.numbersLists.some(el => !el.nativeElement.offsetWidth)) {
      this.adjustPricesWidth();
    }
  }
}
