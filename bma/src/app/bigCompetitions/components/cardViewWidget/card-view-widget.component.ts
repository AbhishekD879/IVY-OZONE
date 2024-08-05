import { Component, Input, OnInit, OnChanges, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'card-view-widget',
  templateUrl: './card-view-widget.component.html',
  providers: [ CarouselService ]
})
export class CardViewWidgetComponent implements OnInit, OnChanges {
  @Input() events: IBigCompetitionSportEvent[];
  @Input() maxDisplay: number;
  @Input() viewType?: string = 'prematch';
  @Input() gtmModuleTitle?: string;

  chunkEvents: IBigCompetitionSportEvent[];
  loadChunkStep: number;
  carouselName: string;
  showLoader: boolean;
  isInPlay: boolean;
  isPrevSlideAvailable: boolean;
  isNextSlideUnAvailable: boolean;
  showPaginationSlide: boolean;
  singleEvent: boolean;

  constructor(
    private carouselService: CarouselService,
    private changeDetectorRef: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadChunkStep = +this.maxDisplay;
    this.isInPlay = this.viewType === 'inplay';
    this.carouselName = `card-widget-carousel-${this.viewType}`;
    this.showLoader = true;
    if (Array.isArray(this.events)) {
      this.chunkEvents = this.getChunk(0, this.loadChunkStep);
    }
    this.showPaginationSlide = this.isPaginationRequired();

    // Timeout needed to detect finish of child's rendering
    setTimeout(() => {
      this.showLoader = false;
      this.changeDetectorRef.markForCheck();
    });
  }

  ngOnChanges(changes) {
    if (changes.events && changes.events.currentValue && !changes.events.firstChange) {
      this.chunkEvents = this.getChunk(0, this.loadChunkStep);
      this.showPaginationSlide = this.isPaginationRequired();
      this.singleEvent = this.isSingleEvent();
    }
  }

  /**
   * Add next events to list of events
   * @param start {Number}
   * @param end {Number}
   * @returns {Array}
   */
  getChunk(start: number, end: number): IBigCompetitionSportEvent[] {
    if (end) {
      const arr = [];
      for (let i = start > 0 ? start : 0; i < end; i++) {
        if (this.events[i]) {
          arr.push(this.events[i]);
        }
      }
      return arr;
    }

    return this.events;
  }

  trackByEventId(index: number, chunkEvents: IBigCompetitionSportEvent): number {
    return chunkEvents.id;
  }

  /**
   * Load next events(regarding to maxDisplay configuration)
   */
  loadChunk(): void {
    this.chunkEvents = this.getChunk(0, this.chunkEvents.length + this.loadChunkStep);
    this.showPaginationSlide = this.isPaginationRequired();
    this.changeDetectorRef.markForCheck();
  }


  /**
   * Call previous() and available
   * @returns {void}
   */
  prevSlide(): void {
    this.carousel.previous();
    this.slidesAvailable();
  }


  /**
   * Call next() and checking available to show
   * @returns {void}
   */
  nextSlide(): void {
    this.carousel.next();
    this.slidesAvailable();
  }

  /**
   * Checking if slides are available to show
   * @returns {void}
   */
  slidesAvailable(): void {
    const carousel = this.carousel;
    if (this.shouldUpdateSlidesAvailability(carousel)) {
      this.isPrevSlideAvailable = carousel.currentSlide > 0;
      this.isNextSlideUnAvailable = carousel.currentSlide === (carousel.slidesCount - 1);
      this.changeDetectorRef.detectChanges();
    }
  }

  /**
   * Init carousel
   * @returns {Carousel}
   */
  private get carousel(): Carousel {
    return this.carouselService.get(this.carouselName);
  }
  private set carousel(value:Carousel){}
  /**
   * check if pagination is needed
   */
  private isPaginationRequired(): boolean {
    return !this.isInPlay && this.events.length > this.chunkEvents.length;
  }


  /**
   * Check if only one event is present
   * @returns {boolean}
   */
  private isSingleEvent(): boolean {
    return this.events && this.events.length === 1;
  }

  /**
   * check if slides availability should be updated
   * @param carousel
   */
  private shouldUpdateSlidesAvailability(carousel: Carousel): boolean {
    return (this.isPrevSlideAvailable !== carousel.currentSlide > 0) ||
      (this.isNextSlideUnAvailable !== (carousel.currentSlide === (carousel.slidesCount - 1)));
  }
}
