import {
  Component,
  ElementRef,
  Input, OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
  ViewChild
} from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';

@Component({
  selector: 'sport-carousel',
  templateUrl: './sport-carousel.component.html',
  styleUrls: [
    './sport-carousel.component.scss',
    '../../../../../app/lazy-modules/carouselMenu/components/carousel-menu.component.scss'
  ]
})
export class SportCarouselComponent implements OnInit, OnDestroy, OnChanges {
  eventName: string;
  categoryName: string;
  isShowLeftArrow: boolean = false;
  isShowRightArrow: boolean = false;

  @Input() menuElements: ISportEvent[];
  @Input() activeMenuItemUri: string;
  @ViewChild('inplayLiveStreamCarousel', {static: false}) private inplayLiveStreamCarousel: ElementRef;
  @ViewChild('inplayLiveStreamCarouselInner', {static: false}) private inplayLiveStreamCarouselInner: ElementRef;

  private scrollable: HTMLElement = null;
  private scrollStep: number = 50;

  constructor(
    private pubSubService: PubSubService,
    private domToolsService: DomToolsService
  ) {

  }

  ngOnInit() {
    this.categoryName = this.menuElements && this.menuElements[0] && this.menuElements[0].categoryName;
    this.pubSubService.subscribe('CarouselMenu', this.pubSubService.API.EVENT_COUNT, eventName => (this.eventName = eventName));
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe('CarouselMenu');
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.menuElements && changes.menuElements.previousValue) {
      const isCurrentSportRemoved = !_.findWhere(changes.menuElements.currentValue, { categoryName: this.categoryName });
      if (changes.menuElements.previousValue.length &&
        (changes.menuElements.currentValue.length !== changes.menuElements.previousValue.length) && isCurrentSportRemoved) {
        this.setActive(this.menuElements[0]);
      }
    }
  }

  trackBycategoryName(index: number, menuElement: ISportEvent): string {
    return menuElement.categoryName;
  }

  /**
   * Show Event Counter
   * @param event
   * @returns {*}
   */
  eventCount(event: IRibbonItem): number {
    // using default name if event 'EVENT_COUNT' is triggered before subscription
    const eventName = this.eventName || 'livenow';
    if (eventName === 'livenow' && event.liveEventCount) {
      return event.liveEventCount;
    } else if (eventName === 'livestream' && event.liveStreamEventCount) {
      return event.liveStreamEventCount;
    }
    return null;
  }

  /**
   * set active menu item
   */
  setActive(item: ISportEvent): void {
    this.pubSubService.publish(this.pubSubService.API.SPORT_CHANGED, item);
    this.categoryName = item.categoryName;
  }

  /**
   * On mouseover action
   */
  mouseOver(): void {
    this.scrollable = this.inplayLiveStreamCarousel.nativeElement;
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
    this.scrollable.scrollLeft = (this.domToolsService.getScrollLeft(this.scrollable) - this.scrollStep);
  }

  /**
   * Scroll scrollable right
   * @param event
   */
  scrollRight(event: CustomEvent): void {
    if (event) {
      event.stopPropagation();
    }
    this.scrollable.scrollLeft = (this.domToolsService.getScrollLeft(this.scrollable) + this.scrollStep);
  }

  /**
   * Get width of scroll inner element
   * @returns {number}
   * @private
   */
  private getInnerWidth(): number {
    if (this.scrollable) {
      return this.inplayLiveStreamCarouselInner.nativeElement.scrollWidth;
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
