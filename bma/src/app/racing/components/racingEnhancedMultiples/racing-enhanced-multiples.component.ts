import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { RacingEnhancedMultiplesService } from './racing-enhanced-multiples.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';

@Component({
  selector: 'racing-enhanced-multiples',
  templateUrl: 'racing-enhanced-multiples.component.html'
})

export class RacingEnhancedMultiplesComponent implements OnInit, OnDestroy {
  @Input() isRacingFeatured? :boolean;
  carouselName: string = 'enhanced-multiples-carousel';
  slidesOnPage: number = 1;
  events: ISportEvent[] = [];
  isSingleSlide: boolean;
  isFirstTimeCollapsed: boolean = false;
  isHovered: boolean = false;
  bannerBeforeAccorditionHeader: string= '';
  targetTab: ISportConfigTab | null = null;

  public sportName: string = 'horseracing';
  private loadDataSubscription: Subscription;

  constructor(
    private racingEnhancedMultiplesService: RacingEnhancedMultiplesService,
    private gtmService: GtmService,
    private carouselService: CarouselService,
    protected vEPService : VirtualEntryPointsService
  ) { }

  ngOnInit(): void {
    /*
     * Get all enhanced multiples for sport
     */
    this.loadDataSubscription = this.racingEnhancedMultiplesService.getEnhancedMultiplesEvents(this.sportName)
      .subscribe(events => {
        this.events = this.racingEnhancedMultiplesService.sortOutcomesByDate(events);
        this.racingEnhancedMultiplesService.setEventDate(this.events);

        this.isSingleSlide = this.events.length <= 1;
      });

      this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
        this.bannerBeforeAccorditionHeader = header;
      });
    
      this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
        this.targetTab = tab;
      });
      
  }

  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

  ngOnDestroy(): void {
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }
  }

  /**
   * Send GA on first collapse
   */
  sendCollapseGTM(): void {
    if (!this.isFirstTimeCollapsed) {
      this.gtmService.push('trackEvent', {
        eventCategory: 'horse racing',
        eventAction: 'enhanced multiples',
        eventLabel: 'collapse'
      });
      this.isFirstTimeCollapsed = true;
    }
  }

  /**
   * Go to previous slide
   */
  prevSlide(): void {
    this.carouselService.get(this.carouselName).previous();
  }

  /**
   * Go to next slide
   */
  nextSlide(): void {
    this.carouselService.get(this.carouselName).next();
  }

  /**
   * Checking if current slide is first (TODO it doesn't look exactly like that!)
   * @returns {boolean}
   */
  isFirstSlide(): boolean {
    const carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide !== 0;
  }

  /**
   * Checking if current slide is last
   * @returns {boolean}
   */
  isLastSlide(): boolean {
    const carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide === (carousel.slidesCount - this.slidesOnPage);
  }

  /**
   * Check if previous action is available. Needs to show/hide previous action arrow.
   * @returns {boolean}
   */
  isPrevActionAvailable(): boolean {
    return this.isFirstSlide();
  }

  /**
   * Check if next slide action is available. Needs to show/hide next action arrow.
   * @returns {boolean}
   */
  isNextActionAvailable(): boolean {
    return !this.isLastSlide();
  }

  trackById(index: number, event: ISportEvent): string {
    return `${event.id}`;
  }
}
