import { Component, Input, Output, OnInit, OnDestroy, ElementRef,
  ChangeDetectorRef, ChangeDetectionStrategy, EventEmitter } from '@angular/core';
import { CarouselService } from '@shared/directives/ng-carousel/carousel.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { JOURNEY_SLIDER_MODE } from '@yourcall/constants/five-a-side.constant';
import { IJourneyItems } from '@core/services/cms/models/five-a-side-journey.model';
import { StorageService } from '@core/services/storage/storage.service';

@Component({
  selector: 'five-a-side-journey',
  templateUrl: './five-a-side-journey.component.html',
  styleUrls: ['./five-a-side-journey.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class FiveASideJourneyComponent implements OnInit, OnDestroy {
  @Input() slides: IJourneyItems[];
  @Input() availableFiveASideFreeBets: boolean;
  @Output() readonly sliderClosed: EventEmitter<any> = new EventEmitter();

  carouselName: string = 'five-a-side-journey-carousel';
  carouselMode: string;
  isCarouselInit: boolean;
  showJourney: boolean = false;

  constructor(
    private el: ElementRef,
    private carouselService: CarouselService,
    private rendererService: RendererService,
    private changeDetectorRef: ChangeDetectorRef,
    private storageService: StorageService,
  ) { }

  ngOnInit(): void {
    this.carouselMode = JOURNEY_SLIDER_MODE.next;
  }

  trackBySlide(i: number, element): string {
    return `${i}_${element.title}`;
  }

  trackByDot(i: number, element): string {
    return `${i}_${element.title}`;
  }

  /**
   * Set status on carousel initialization
   * @param {boolean} status
   */
  onCarouselInitChangeStatus(status: boolean): void {
    this.isCarouselInit = status;
  }

  /**
   * Update current slide index on slide change
   * (by swipe or clicking bullet)
   * @param {number} index
   */
  navigateToSlide(index: number): void {
    if (this.slideIndex !== index) {
      this.currentCarousel.toIndex(index);
    }
  }

  /**
   * Update current slide index on slide change
   * (by click on 'Next')
   * Close panel if current slide is last
   */
  navigateToNextSlide(): void {
    if (this.carouselMode !== JOURNEY_SLIDER_MODE.done) {
      this.currentCarousel.toIndex(this.slideIndex + 1);
    } else {
      this.onClose();
    }
  }

  /**
   * Set carousel mode on slide change, updates view
   */
  setCarouselMode(): void {
    this.carouselMode = this.slideIndex === this.slides.length - 1 ?
      JOURNEY_SLIDER_MODE.done : JOURNEY_SLIDER_MODE.next;
      this.changeDetectorRef.detectChanges();
  }

  ngOnDestroy(): void {
    this.carouselService.remove(this.carouselName);
  }

  /**
   * Send event to parent component on panel close
   */
  onClose(): void {
    this.rendererService.renderer.setStyle(this.el.nativeElement, 'display', 'none');
    this.sliderClosed.emit();
    this.closeJourney();
  }

  /**
   * Get current slide index if carousel is initialized
   * @private
   */
  get slideIndex(): number {
    return this.currentCarousel ? this.currentCarousel.currentSlide : null;
  }
  set slideIndex(value:number){}

  private closeJourney(): void {
    this.storageService.set(`five-a-side-journey-seen`, true);
    this.showJourney = false;
  }

  /**
   * Get current carousel name if carousel is initialized
   * @private
   */
  private get currentCarousel(): Carousel {
    return this.isCarouselInit ? this.carouselService.get(this.carouselName) : null;
  }
  private set currentCarousel(value:Carousel){}
}
