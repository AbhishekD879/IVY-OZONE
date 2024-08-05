import * as _ from 'underscore';
import {
  AfterViewInit,
  Directive,
  ElementRef,
  EventEmitter,
  Input,
  NgZone,
  OnChanges,
  OnDestroy, OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';

import { Subject, fromEvent } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { DeviceService } from '@core/services/device/device.service';
import { CarouselService } from './carousel.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { Carousel } from '@shared/directives/ng-carousel/carousel.class';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Directive({
  // eslint-disable-next-line
  selector: '[ngCarousel]',
})
export class NgCarouselDirective implements OnInit, OnDestroy, OnChanges, AfterViewInit {
  @Input() ngCarouselWatch: string;
  @Input() ngCarouselName: string;
  @Input() ngCarouselFluid: boolean;
  @Input() ngCarouselLoop: boolean;
  @Input() ngCarouselRandom: boolean;
  @Input() ngCarouselAmount: number;
  @Input() ngCarouselTimer: number;
  @Input() ngCarouselMoveThresholdPercentage: number;
  @Input() ngCarouselActiveClass?: string;
  @Input() ngCenterMode?: boolean;
  @Input() slidesToScroll?: number;
  @Input() ngCarouselDisableRightSwipe?: boolean;
  @Input() ngStopSlideOnHover?: boolean;
  @Input() ngAdditionalCopyAdd?: boolean;
  @Input() ngDisableCarouselDragOnCenterMode?:boolean;
  @Output() readonly isCarouselInit: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly activeSlideIndex: EventEmitter<number> = new EventEmitter();

  interval: number | boolean;
  looping: boolean;
  random: boolean;
  fluid: boolean;
  centerMode: boolean;
  stopSlidesOnHover: boolean = false;
  toggleSliding: boolean = false;
  additionalCopyAdd: boolean = false;
  activeClass: string;

  slides: HTMLElement[];
  activeIndex: number = 0;
  currentCarousel: Carousel;
  firstSlideCopy: HTMLElement;
  secondSlideCopy: HTMLElement;
  lastSlideCopy: HTMLElement;
  beforeLastSlideCopy: HTMLElement;
  slideContainer: HTMLElement;
  name: string;
  amount: number;
  timeoutPromise;
  width: number;
  deltaXFactor: number = 0;

  public animationListeners: Function[] = [];
  protected readonly MOVE_TRESHOLD_PERCENTAGE: number = 25;
  public mouseListeners: Function[] = [];
  private destroyed = new Subject<null>();
  private transitionProperty: string = 'transform';
  private isCirclePassed: boolean = false;
  private isAdditionalCopies: boolean = false;
  private scrollWidth: number; // in percent

  constructor(
    public domToolsService: DomToolsService,
    public carouselService: CarouselService,
    public elementRef: ElementRef,
    public windowRef: WindowRefService,
    public deviceService: DeviceService,
    public rendererService: RendererService,
    private ngZone: NgZone,
  ) {
    this.slideContainerTransitionAnimation = this.slideContainerTransitionAnimation.bind(this);
  }

  ngOnInit(): void {
    if (!this.ngCarouselMoveThresholdPercentage) {
      this.ngCarouselMoveThresholdPercentage = this.MOVE_TRESHOLD_PERCENTAGE;
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.ngCarouselWatch) {
      this.windowRef.nativeWindow.setTimeout(() => {
        this.refreshInteractionWithDom();
      });
    }
  }

  ngAfterViewInit(): void {
    // Options
    this.name = this.ngCarouselName;
    this.interval = this.ngCarouselTimer;
    this.random = this.ngCarouselRandom;
    this.looping = this.ngCarouselLoop;
    this.fluid = this.ngCarouselFluid;
    this.activeClass = this.ngCarouselActiveClass;
    this.centerMode = this.ngCenterMode;
    this.stopSlidesOnHover = this.ngStopSlideOnHover;
    this.additionalCopyAdd = this.ngAdditionalCopyAdd;
    this.amount = typeof(this.ngCarouselAmount) !== 'undefined' ? this.ngCarouselAmount : 1;

    // On release
    const pressEvent = this.isTouchDevice() ? 'touchstart' : 'mousedown';
    const releaseEvent = this.isTouchDevice() ? 'touchend' : 'mouseup';
    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, pressEvent, () => this.carouselPress())
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, releaseEvent, () => this.carouselRelease())
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, 'mouseover', () => {
        if (this.timeoutPromise) {
          this.windowRef.nativeWindow.clearTimeout(this.timeoutPromise);
        }
        if(this.stopSlidesOnHover) {
          this.toggleSliding = true;
        }
      })
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, 'mouseover', () => this.setNextSlideTimeout()
       )
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, 'mouseleave', () => {
        this.toggleSliding = false;
        this.setNextSlideTimeout();
      })
    );

    this.refreshInteractionWithDom();
  }

  ngOnDestroy(): void {
    if (this.mouseListeners.length > 0) {
      _.each(this.mouseListeners, (listener: Function) => listener());
      this.mouseListeners = [];
    }

    if (this.slideContainer && this.currentCarousel) {
      if (this.animationListeners.length > 0) {
        _.each(this.animationListeners, (listener: Function) => listener());
        this.animationListeners = [];
      }

      this.currentCarousel.onSlideChangeCallbacks = [];
    }

    this.carouselService.remove(this.name);
    this.isCarouselInit.emit(false);

    this.destroyed.next(null);
    this.destroyed.complete();
  }

  setNextSlideTimeout(): void {
    if (!this.interval || this.toggleSliding || this.currentCarousel && this.currentCarousel.slidesCount < 2) {
      return;
    }

    if (this.timeoutPromise) {
      this.windowRef.nativeWindow.clearTimeout(this.timeoutPromise);
    }

    if (this.currentCarousel) {
      this.timeoutPromise = this.windowRef.nativeWindow.setTimeout(() => {
        this.currentCarousel.next();
      }, this.interval);
    }
  }

  move(slideIndex: number, animate: boolean, transitionEndCallback?: Function): void {
    requestAnimationFrame(() => {
      if (animate) {
        this.rendererService.renderer.addClass(this.slideContainer, 'carousel-animate');
        this.rendererService.renderer.removeClass(this.slideContainer, 'carousel-is-sliding');

        if (transitionEndCallback) {
          const slideContainerEvents = ['transitionend', 'webkitTransitionEnd'];

          slideContainerEvents.forEach((event: string) => {
            this.animationListeners.push(
              this.rendererService.renderer.listen(
                this.slideContainer,
                event,
                this.slideContainerTransitionAnimation(transitionEndCallback))
            );
          });
        }
      }
      if (Number.isInteger(slideIndex)) {
        let i = slideIndex - 1;
        let slideCopy: HTMLElement;
        if (!this.isCirclePassed && (i === this.slides.length || i < 0)) {
          this.isCirclePassed = true;
          this.rendererService.renderer.removeClass(this.slideContainer, 'circle-not-passed');
        }
        if (i === this.slides.length) {
          i = 0;
          slideCopy = this.firstSlideCopy;
        } else if (i < 0) {
          slideCopy = this.lastSlideCopy;
          i = this.slides.length - 1;
        }
        this.toggleActiveClass(i, slideCopy);
        this.activeIndex = i;
      }

      // slide index with additional slide copy (secondSlideCopy)
      const ind = this.secondSlideCopy ? slideIndex + 1 : slideIndex;
      const rule = `translate3d(-${(this.scrollWidth * ind) / this.amount}%, 0, 0)`;

      this.domToolsService.css(this.slideContainer, {
        '-ms-transform': rule,
        '-webkit-transform': rule,
        'transform': rule
      });

      this.activeSlideIndex.emit(slideIndex);
    });
  }

  toggleActiveClass(i: number, slideCopy?: HTMLElement): void {
    if (!this.activeClass) {
      return;
    }

    if (slideCopy) {
      this.rendererService.renderer.addClass(slideCopy, this.activeClass);
    }
    this.rendererService.renderer.removeClass(this.slides[this.activeIndex], this.activeClass);
    this.rendererService.renderer.addClass(this.slides[i], this.activeClass);
  }

  /**
   * @param {Function} transitionEndCallback
   * @return {() => void}
   */
  slideContainerTransitionAnimation(transitionEndCallback: Function): (event?: any) => void {
    return (event) => {
      if (event && event.propertyName !== this.transitionProperty) {
        return;
      }

      if (typeof transitionEndCallback === 'function') {
        transitionEndCallback();
      }

      if (this.animationListeners.length > 0) {
        _.each(this.animationListeners, listener => listener());
        this.animationListeners = [];
      }
    };
  }

  carouselDrag(newDeltaX: number): void {
    this.deltaXFactor = newDeltaX / this.width;
    this.deltaXFactor = this.deltaXFactor > 1 ? 1 : this.deltaXFactor < -1 ? -1 : this.deltaXFactor;

    if (this.ngCarouselDisableRightSwipe && this.deltaXFactor < 0) {
      return;
    }

    this.rendererService.renderer.addClass(this.slideContainer, 'carousel-is-sliding');
    this.move(this.currentCarousel.currentSlide + 1 - this.deltaXFactor, false);
  }

  carouselPress(): void {
    this.width = this.slideContainer.offsetWidth;
  }

  carouselRelease(): void {
    if (Math.abs(this.deltaXFactor) > this.ngCarouselMoveThresholdPercentage / 100) {
      if (this.deltaXFactor > 0) {
        this.currentCarousel.previous(); // user dragged right, go to previous slide
      } else if (!this.ngCarouselDisableRightSwipe) {
        this.currentCarousel.next(); // user dragged left, go to next slide
      }
      this.deltaXFactor = 0;
    } else if (this.deltaXFactor > 0 || this.deltaXFactor < 0) {
      this.move(this.currentCarousel.currentSlide + 1, true, () => {
        this.deltaXFactor = 0;
      });
    }
  }

  refreshInteractionWithDom(): void {
    // Add initial classes
    this.rendererService.renderer.addClass(this.elementRef.nativeElement,
      'ng-carousel');
    this.rendererService.renderer.addClass(this.elementRef.nativeElement,
      this.isTouchDevice() ? 'carousel-touch' : 'carousel-no-touch');

    // Find slide wrapper
    this.slideContainer = this.elementRef.nativeElement.querySelector('slidecontainer');
    if (this.centerMode) {
      this.rendererService.renderer.addClass(this.slideContainer, 'center-mode');
    }
    this.rendererService.renderer.addClass(this.slideContainer, 'circle-not-passed');

    // Remove old carousel
    let savedSlideIndex;
    let savedCallbacks;
    if (this.name && this.carouselService.get(this.name)) {
      savedSlideIndex = this.carouselService.get(this.name).currentSlide;
      savedCallbacks = this.carouselService.get(this.name).onSlideChangeCallbacks;
      this.carouselService.remove(this.name);
    }
    // Find slides
    this.removeOldVirtualSlides();
    this.slides = this.elementRef.nativeElement.querySelectorAll('slide');
    if (this.scrollWidth === undefined) {
      this.scrollWidth = this.slidesToScroll
        ? this.slides[0].offsetWidth / (this.slideContainer.offsetWidth / 100) * this.slidesToScroll
        : 100;

      this.isAdditionalCopies = this.slides.length >= 2 && (this.centerMode || this.scrollWidth < 100);
    }

    if (this.activeClass) {
      this.rendererService.renderer.addClass(this.slides[0], this.activeClass);
    }

    // Add slides before and after the current slides
    if (this.slides.length > 0) {
      this.currentCarousel = this.carouselService.add(this.slides.length, this.name, {
        looping: this.looping
      }, this.elementRef.nativeElement);
      this.currentCarousel.amount = this.amount;
      this.currentCarousel.fluid = this.fluid;
      this.currentCarousel.quantity = this.fluid ? this.currentCarousel.getSlidesQuantity(this.elementRef.nativeElement) : 0;

      _.forEach(savedCallbacks, (savedCallback: Function) => {
        this.currentCarousel.onSlideChange(savedCallback);
        this.currentCarousel.unbindOnSlideChangeCallback(0);
      });

      this.currentCarousel.move = this.move;

      this.refreshVirtualSlides();

      if (this.currentCarousel && typeof this.currentCarousel !== 'string') {
        this.currentCarousel.onSlideChange((slideIndex: number, wrapping: string) => {
          this.onSlideChangeCallback(slideIndex, wrapping);
        });
      }

      // If new slide was out of range, move to the new assigned one
      if (savedSlideIndex && this.currentCarousel.currentSlide !== savedSlideIndex) {
        this.onSlideChangeCallback(this.currentCarousel.currentSlide, 'false');
        this.currentCarousel.toIndex(savedSlideIndex);
      }

      // Option: random
      if (this.random) {
        const randomSlide = Math.floor(Math.random() * this.currentCarousel.slidesCount);
        this.currentCarousel.toIndex(randomSlide);
      }

      // Option: interval
      if (this.interval && this.currentCarousel.slidesCount >= 2) {
        this.setNextSlideTimeout();
      }
    } else {
      // eslint-disable-next-line
      console.log('ng-carousel error: No slides found');
    }

    // Initialize left right logic
    if (this.slideContainer) {
      this.touchHorizScroll(this.slideContainer);
    } else {
      // eslint-disable-next-line
      console.log('ng-carousel error: No slidecontainer found');
    }
    this.isCarouselInit.emit(true);
  }

  public refreshVirtualSlides(): void {
    this.removeOldVirtualSlides();
    this.slides = this.elementRef.nativeElement.querySelectorAll('slide');

    if (this.looping) {
      this.cloneSlides();
    } else {
      this.makeClonedSlidesEmpty();
    }

    this.rendererService.renderer.addClass(this.firstSlideCopy, 'carousel-slide-copy');
    this.rendererService.renderer.addClass(this.lastSlideCopy, 'carousel-slide-copy');

    this.slideContainer.appendChild(this.firstSlideCopy);

    if (this.isAdditionalCopies && !this.additionalCopyAdd) {
      this.rendererService.renderer.addClass(this.secondSlideCopy, 'carousel-slide-copy');
      this.rendererService.renderer.addClass(this.beforeLastSlideCopy, 'carousel-slide-copy');
      this.slideContainer.appendChild(this.secondSlideCopy);
      this.slides[0].parentNode.insertBefore(this.beforeLastSlideCopy, this.slides[0]);
    } else {
      this.rendererService.renderer.addClass(this.slideContainer, 'carousel-ignore-first-slide');
    }

    this.slides[0].parentNode.insertBefore(this.lastSlideCopy, this.slides[0]);
  }

  public removeOldVirtualSlides(): void {
    const oldSlides = this.elementRef.nativeElement.querySelectorAll('.carousel-slide-copy');
    if (oldSlides.length > 0) {
      _.each(oldSlides, (slide: HTMLElement) => slide.parentNode.removeChild(slide));
    }
  }

  public isTouchDevice(): boolean {
    return ('ontouchstart' in this.windowRef.nativeWindow) ||
      (this.windowRef.nativeWindow.MaxTouchPoints > 0) || (this.windowRef.nativeWindow.msMaxTouchPoints > 0);
  }

  public getPageX(event: TouchEvent | MouseEvent): number {
    return this.isTouchDevice() ? (event as TouchEvent).touches[0].pageX : (event as MouseEvent).pageX;
  }

  public getPageY(event: TouchEvent | MouseEvent): number {
    return this.isTouchDevice() ? (event as TouchEvent).touches[0].pageY : (event as MouseEvent).pageY;
  }

  public isVerticalSwipe(scrollStartPos: number,
                         endPosition: number,
                         scrollStartPosY: number,
                         endPositionY: number
  ): boolean {
    const offset = 20;
    return (Math.abs(Math.abs(endPosition) - Math.abs(scrollStartPos)) > offset) &&
      (Math.abs(Math.abs(endPositionY) - Math.abs(scrollStartPosY)) < offset);
    // 50 is not magic number that value which define
    // if swipe is higher from 100px that do up donw scroll
  }

  public touchHorizScroll(element: HTMLElement): void {
    let scrollStartPos = 0;
    let scrollStartPosY = 0;
    const handlers = {
      start: this.isTouchDevice() || this.deviceService.isTablet ? 'touchstart' : 'mousedown',
      move: this.isTouchDevice() ? 'touchmove' : 'mousemove',
      isDown: false
    };

    if (!this.isTouchDevice()) {
      fromEvent(element, 'mouseup')
        .pipe(
          takeUntil(this.destroyed),
        )
        .subscribe(() => {
          handlers.isDown = false;
        });

      fromEvent(element, 'mouseout')
        .pipe(
          takeUntil(this.destroyed),
        )
        .subscribe((event: MouseEvent) => {
          if (!handlers.isDown) {
            return;
          }
          handlers.isDown = false;
          const moveToSlide = this.currentCarousel.currentSlide + (this.getPageX(event) > 0 ? 1 : -1);
          this.move(moveToSlide, true);
        });
    }

    fromEvent(element, handlers.start)
      .pipe(
        takeUntil(this.destroyed),
      )
      .subscribe((event: TouchEvent | MouseEvent) => {
        this.ngZone.runOutsideAngular(() => {
          if (!this.isTouchDevice()) {
            handlers.isDown = true;
          }
          scrollStartPos = element.scrollLeft - this.getPageX(event);
          scrollStartPosY = element.scrollTop - this.getPageY(event);
        });
      });

    fromEvent(element, handlers.move)
      .pipe(
        takeUntil(this.destroyed),
      )
      .subscribe((event: TouchEvent | MouseEvent) => {
        if (!this.isTouchDevice() && !handlers.isDown) {
          return;
        }

        this.ngZone.runOutsideAngular(() => {
          if (this.isVerticalSwipe(scrollStartPos, this.getPageX(event), scrollStartPosY, this.getPageY(event)) && !this.ngDisableCarouselDragOnCenterMode) {
            this.carouselDrag(scrollStartPos + this.getPageX(event));
            if (event.cancelable) {
              event.preventDefault();
            }
          }
        });

      });
  }

  public onSlideChangeCallback(slideIndex: number, wrapping: string): void {
    let newSlideIndex = slideIndex + 1; // because the first slide doesn't count

    if (wrapping === 'left') {
      newSlideIndex = 0; // first slide
    } else if (wrapping === 'right') {
      newSlideIndex = this.slides.length + 1; // last slide
    }

    this.move(newSlideIndex, true, () => this.wrapTo(wrapping));

    this.setNextSlideTimeout();
    !this.centerMode && this.refreshVirtualSlides();
  }

  private wrapTo(wrapping: string): void {
    const slideIndex = wrapping === 'left' && this.slides.length
      || wrapping === 'right' && 1
      || null;

    if (!wrapping || slideIndex === null) {
      return;
    }
    this.rendererService.renderer.removeClass(this.slideContainer, 'carousel-animate');
    this.move(slideIndex, false);

    this.centerMode && this.refreshVirtualSlides();
  }

  private cloneSlides(): void {
    const firstSlide: HTMLElement = this.slides[0];
    const firstSlideEventId = firstSlide.dataset.eventId || '';
    const firstSlideHtml = firstSlide.innerHTML || '';

    const lastSlide: HTMLElement = this.slides[this.slides.length - 1];
    const lastSlideEventId = lastSlide.dataset.eventId || '';
    const lastSlideHtml = lastSlide.innerHTML || '';

    if (this.isAdditionalCopies) {
      const secondSlide: HTMLElement = this.slides[1];
      const secondSlideEventId = secondSlide.dataset.eventId || '';
      const secondSlideHtml = secondSlide.innerHTML || '';

      const beforeLastSlide: HTMLElement = this.slides[this.slides.length - 2];
      const beforeLastSlideEventId = beforeLastSlide.dataset.eventId || '';
      const beforeLastSlideHtml = beforeLastSlide.innerHTML || '';
      this.secondSlideCopy = this.createSlideForEvent(secondSlideEventId, secondSlideHtml);
      this.beforeLastSlideCopy = this.createSlideForEvent(beforeLastSlideEventId, beforeLastSlideHtml);
    }
    this.firstSlideCopy = this.createSlideForEvent(firstSlideEventId, firstSlideHtml);
    this.lastSlideCopy = this.createSlideForEvent(lastSlideEventId, lastSlideHtml);

  }

  private makeClonedSlidesEmpty(): void {
    const slidesCopy: string[] = ['firstSlideCopy', 'lastSlideCopy'];
    if (this.isAdditionalCopies) {
      slidesCopy.push('secondSlideCopy', 'beforeLastSlideCopy');
    }
    slidesCopy.forEach((slideName:string) => this[slideName] = this.createEmptySlide());
  }

  private createSlideForEvent(eventId: string, innerHtml: string): HTMLElement {
    const slide = this.windowRef.document.createElement('slide');
    slide.className = 'slide';
    slide.dataset.crlat = 'raceCard.event';
    slide.dataset.eventid = eventId;

    slide.innerHTML = innerHtml;

    return slide;
  }

  private createEmptySlide(): HTMLElement {
    const slide = this.windowRef.document.createElement('slide');
    slide.className = 'empty';

    return slide;
  }
}
