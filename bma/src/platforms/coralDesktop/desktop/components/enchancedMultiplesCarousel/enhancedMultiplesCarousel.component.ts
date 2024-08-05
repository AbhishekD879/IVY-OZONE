import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { EnhancedMultiplesCarouselService } from './enhancedMultiplesCarousel.service';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { Subscription } from 'rxjs';

@Component({
  selector: 'enhanced-multiples-carousel',
  templateUrl: 'enhancedMultiplesCarousel.component.html',
  styleUrls: ['enhancedMultiplesCarousel.component.scss'],
  providers: [
    EnhancedMultiplesCarouselService
  ]
})
export class EnhancedMultiplesCarouselComponent implements OnInit, OnDestroy {
  @Input() public sportName: string;
  @Input() public isHomePage?: boolean;

  carouselName: string = 'enhanced-multiples-carousel';
  isSingleSlide: boolean;
  slidesOnPage: number = 1;
  isHovered: boolean = false;
  events: ISportEvent[] = [];

  private initDataSubscription: Subscription;

  constructor(private carouselService: CarouselService,
              private enhancedMultiplesCarouselService: EnhancedMultiplesCarouselService) {}

  ngOnInit() {
    /**
     * Get all enhanced multiples for sport
     */
    this.initDataSubscription = this.enhancedMultiplesCarouselService.getEnhancedMultiplesEvents(this.sportName)
      .subscribe((events: ISportEvent[]) => {
        this.enhancedMultiplesCarouselService.setEventDate(events);
        this.events = this.enhancedMultiplesCarouselService.buildEnhancedMultiplesData(events, this.sportName);
        this.isSingleSlide = this.events.length <= 1;
      }, (error => {
        console.warn(error);
      }));
  }

  ngOnDestroy(): void {
    this.initDataSubscription && this.initDataSubscription.unsubscribe();
  }

  /**
   * Go to next slide
   */
  prevSlide(): void {
    this.carouselService.get(this.carouselName).previous();
  }

  /**
   * Go to previous slide
   */
  nextSlide(): void {
    this.carouselService.get(this.carouselName).next();
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

  /**
   * Checking if current slide is last
   * @returns {boolean}
   */
  isLastSlide(): boolean {
    const carousel: Carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide === (carousel.slidesCount - this.slidesOnPage);
  }

  /**
   * Checking if current slide is first
   * @returns {boolean}
   */
  isFirstSlide(): boolean {
    const carousel: Carousel = this.carouselService.get(this.carouselName);
    return carousel.currentSlide !== 0;
  }

  /**
   * TrackBy function
   * @param {number} index
   * @param {ISportEvent} outcome
   * @returns {string}
   */
  trackById(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }
}
