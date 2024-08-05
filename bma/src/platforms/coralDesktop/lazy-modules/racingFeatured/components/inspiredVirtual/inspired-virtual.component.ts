import { Component, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { InspiredVirtualComponent } from '@app/lazy-modules/racingFeatured/components/inspiredVirtual/inspired-virtual.component';
import { InspiredVirtualService } from '@app/lazy-modules/racingFeatured/components/inspiredVirtual/inspired-virtual.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { TempStorageService } from '@core/services/storage/temp-storage.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'inspired-virtual-module',
  templateUrl: 'inspired-virtual.component.html',
  styleUrls: ['inspired-virtual.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class DesktopInspiredVirtualComponent extends InspiredVirtualComponent {

  constructor(inspiredVirtualService: InspiredVirtualService,
              router: Router,
              protected storage: TempStorageService,
              private privateCarousel: CarouselService,
              private pubSubService: PubSubService,
              protected virtualSharedService: VirtualSharedService,
              protected vEPService : VirtualEntryPointsService) {
    super(inspiredVirtualService, router, storage, virtualSharedService,vEPService);
  }

  /**
   * send GTM tracking, Collapse
   */
  sendCollapseGTM(): void {
    this.storage.set(this.SECTION_FLAG, !this.isExpanded);
    if (this.isFirstTimeCollapsed) {
      return;
    }
    this.sendGTM('collapse');
    this.isFirstTimeCollapsed = true;
  }

  /**
   * send GTM tracking, view All
   */
  viewAllGTM(): void {
    this.sendGTM('view all');
  }

  /**
   * Go to Live Virtual sport event
   */
  goToLiveEvent(event: ISportEvent): void {
    const url =  event ? this.virtualSharedService.formVirtualEventUrl(event) : 'virtual-sports/sports';
    if (this.isVirtualHomePage) {
      this.inspiredVirtualService.virtualsGTMEventTracker(url, event);
    } else {
      this.sendGTM('bet now');
    }
    this.router.navigateByUrl(url);
  }

  /**
   * Go to next slide
   */
  prevSlide(): void {
    this.privateCarousel.get(this.carouselName).previous();
    this.sendGTM('navigate left');
  }

  /**
   * Go to previous slide
   */
  nextSlide(): void {
    this.privateCarousel.get(this.carouselName).next();
    this.sendGTM('navigate right');
  }

  /**
   * Check if next slide action is available. Needs to show/hide next action arrow.
   * @returns {boolean}
   */
  isNextActionAvailable(): boolean {
    const carousel: Carousel = this.privateCarousel.get(this.carouselName);
    return carousel && carousel.currentSlide !== (carousel.slidesCount - 1);
  }

  /**
   * Check if previous action is available. Needs to show/hide previous action arrow.
   * @returns {boolean}
   */
  isPrevActionAvailable(): boolean {
    const carousel: Carousel = this.privateCarousel.get(this.carouselName);
    return carousel && carousel.currentSlide !== 0;
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   */
  private sendGTM(eventLabel: string): void {
    const gtmCommonObject = this.inspiredVirtualService.getGtmCommonObject(this.sportName);

    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, [
      'trackEvent', _.extendOwn({ eventLabel }, gtmCommonObject)
    ]);
  }
}
