import { Component, ElementRef, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';

import { TabsPanelComponent as AppTabsPanelComponent } from '@shared/components/tabsPanel/tabs-panel.component';
import { LocaleService } from '@core/services/locale/locale.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';

@Component({
  selector: 'tabs-panel',
  templateUrl: './tabs-panel.component.html',
  styleUrls: ['./tabs-panel.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class TabsPanelComponent extends AppTabsPanelComponent {
  isShowLeftArrow: boolean = false;
  isShowRightArrow: boolean = false;

  private scrollable = null;
  private scrollStep = 50;

  constructor(
    public elementRef: ElementRef,
    public locale: LocaleService,
    public router: Router,
    public gtmTrackingService: GtmTrackingService,
    public casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    public navigationService: NavigationService,
    public domToolsService: DomToolsService,
  ) {
    super(elementRef, locale, router, gtmTrackingService, casinoMyBetsIntegratedService, navigationService);
  }

  /**
   * On mouseover action
   */
  mouseOver(): void {
    this.scrollable = this.elementRef.nativeElement.querySelector('.scroll-container');
    this.isShowLeftArrow = this.isScrollLeftAvailable();
    this.isShowRightArrow = this.isScrollRightAvailable();
  }

  /**
   * On mouseleave action
   */
  mouseLeave(): void {
    this.scrollable = null;
    this.isShowLeftArrow = false;
    this.isShowRightArrow = false;
  }

  /**
   * Scroll scrollable left
   * @param event
   */
  scrollLeft(event: CustomEvent): void {
    if (event) {
      event.stopPropagation();
    }

    this.scrollable.scrollLeft = this.domToolsService.getScrollLeft(this.scrollable) - this.scrollStep;
  }

  /**
   * Scroll scrollable right
   * @param event
   */
  scrollRight(event: CustomEvent): void {
    if (event) {
      event.stopPropagation();
    }
    this.scrollable.scrollLeft = this.domToolsService.getScrollLeft(this.scrollable) + this.scrollStep;
  }

  /**
   * Get width of scroll inner element
   * @returns {number}
   * @private
   */
  private getInnerWidth(): number {
    if (this.scrollable) {
      return this.scrollable.querySelector('.scroll-inner').scrollWidth;
    }
    return 0;
  }

  /**
   * Check if scroll available
   * @returns {*|boolean}
   * @private
   */
  private isScrollAvailable(): boolean {
    return this.scrollable && this.domToolsService.getWidth(this.scrollable) < this.getInnerWidth();
  }

  /**
   * Check if left scroll arrow available
   * @returns {*|boolean}
   */
  private isScrollLeftAvailable(): boolean {
    return this.isScrollAvailable() && this.domToolsService.getScrollLeft(this.scrollable) > 0;
  }

  /**
   * Check if right scroll arrow available
   * @returns {*|boolean}
   */
  private isScrollRightAvailable(): boolean {
    return this.isScrollAvailable() &&
      this.domToolsService.getScrollLeft(this.scrollable) < this.getInnerWidth() - this.domToolsService.getWidth(this.scrollable);
  }
}
