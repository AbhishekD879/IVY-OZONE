import * as _ from 'underscore';
import { AfterViewInit, Directive } from '@angular/core';

import { NgCarouselDirective } from '@shared/directives/ng-carousel/carousel.directive';

/**
 * Carousel for slides with dynamic widths.
 * Created for mobile quick links with dynamic links text.
 * Not tested on desktop as it will net be used there now.
 * TODO verify if usage on desktop needed.
 */
@Directive({
  // eslint-disable-next-line
  selector: '[ngCarouselExtended]',
})
export class NgCarouselExtendedDirective extends NgCarouselDirective implements AfterViewInit {
  startPosition: any;
  protected readonly MOVE_TRESHOLD_PERCENTAGE: number = 5;

  ngAfterViewInit(): void {
    // Options
    this.name = this.ngCarouselName;
    this.interval = this.ngCarouselTimer;
    this.looping = this.ngCarouselLoop;
    this.fluid = this.ngCarouselFluid;
    this.amount = typeof(this.ngCarouselAmount) !== 'undefined' ? this.ngCarouselAmount : 1;

    this.refreshInteractionWithDom();
  }

  carouselDrag(newDeltaX: number): void {
    this.deltaXFactor = newDeltaX / this.width;
    this.deltaXFactor = this.deltaXFactor > 1 ? 1 : this.deltaXFactor < -1 ? -1 : this.deltaXFactor;

    this.rendererService.renderer.addClass(this.slideContainer, 'carousel-is-sliding');
    this.touchScroll(this.startPosition + newDeltaX);
  }

  /**
   * @param {Function} transitionEndCallback
   * @return {() => void}
   */
  slideContainerTransitionAnimation(transitionEndCallback: Function): () => void {
    return () => {
      if (typeof transitionEndCallback === 'function') {
        transitionEndCallback();
      }

      if (this.animationListeners.length > 0) {
        _.each(this.animationListeners, listener => listener());
        this.animationListeners = [];
      }

      this.animate(this.currentCarousel.currentSlide + 1);
    };
  }

  carouselRelease(): void {
    if (Math.abs(this.deltaXFactor) > this.ngCarouselMoveThresholdPercentage / 100) {
      if (this.deltaXFactor > 0) {
        this.currentCarousel.previous(); // user dragged right, go to previous slide
      } else {
        this.currentCarousel.next(); // user dragged left, go to next slide
      }
      this.deltaXFactor = 0;
    } else if (this.deltaXFactor > 0 || this.deltaXFactor < 0) {
      this.animate(this.currentCarousel.currentSlide + 1, () => {
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
      this.touchHorizScroll();
    } else {
      // eslint-disable-next-line
      console.log('ng-carousel error: No slidecontainer found');
    }
    this.isCarouselInit.emit(true);
  }

  onSlideChangeCallback(slideIndex: number, wrapping: string): void {
    let newSlideIndex = slideIndex + 1; // because the first slide doesn't count

    if (wrapping === 'left') {
      newSlideIndex = 0; // first slide
    } else if (wrapping === 'right') {
      newSlideIndex = this.slides.length + 1; // last slide
    }

    this.animate(newSlideIndex, () => {
      if (wrapping === 'left') {
        this.animate(this.slides.length);
      } else if (wrapping === 'right') {
        this.animate(1);
      }
    });

    this.setNextSlideTimeout();
    this.refreshVirtualSlides();
  }

  touchHorizScroll(): void {
    let scrollStartPos = 0;
    let scrollStartPosY = 0;
    const events = {
      start: this.isTouchDevice() || this.deviceService.isTablet ? 'touchstart' : 'mousedown',
      end:  this.isTouchDevice() ? 'touchend' : 'mouseup',
      move: this.isTouchDevice ? 'touchmove' : 'mousemove',
      isDown: false
    };

    // On release
    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, events.start, () => this.carouselPress())
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, events.end, () => this.carouselRelease())
    );

    this.mouseListeners.push(
      this.rendererService.renderer.listen(this.elementRef.nativeElement, 'mouseover', () => {
        if (this.timeoutPromise) {
          this.windowRef.nativeWindow.clearTimeout(this.timeoutPromise);
        }
        this.setNextSlideTimeout();
      })
    );

    this.slideContainer.addEventListener(events.start, (event: TouchEvent | MouseEvent) => {
      if (!this.isTouchDevice()) {
        events.isDown = true;
      }

      this.startPosition = this.getContainerTRansformPosition();

      scrollStartPos = this.slideContainer.scrollLeft - this.getPageX(event);
      scrollStartPosY = this.slideContainer.scrollTop - this.getPageY(event);
    }, false);

    this.slideContainer.addEventListener(events.move, (event: TouchEvent | MouseEvent) => {
      if (!this.isTouchDevice() && !events.isDown) {
        return;
      }

      if (this.isVerticalSwipe(scrollStartPos, this.getPageX(event), scrollStartPosY, this.getPageY(event))) {
        this.carouselDrag(scrollStartPos + this.getPageX(event));
        event.preventDefault();
      }
    }, false);

    if (!this.isTouchDevice()) {
      this.slideContainer.addEventListener('mouseup', () => {
        events.isDown = false;
      });

      this.slideContainer.addEventListener('mouseout', (event: MouseEvent) => {
        if (!events.isDown) {
          return;
        }
        events.isDown = false;
        const moveToSlide = this.currentCarousel.currentSlide + (this.getPageX(event) > 0 ? 1 : -1);
        this.animate(moveToSlide);
      });
    }
  }

  private animate(slideIndex: number, transitionEndCallback?: Function): void {
    let rule: string;
    const toSlidePosition = this.getSlidePosition(slideIndex);

    this.rendererService.renderer.removeClass(this.slideContainer, 'carousel-is-sliding');
    this.rendererService.renderer.addClass(this.slideContainer, 'carousel-animate');

    if (this.deviceService.isDesktop) {
      rule = `translate3d(-${toSlidePosition - this.windowRef.nativeWindow.innerWidth}px, 0)`;
    } else {
      rule = `translate(-${toSlidePosition - this.windowRef.nativeWindow.innerWidth}px, 0)`;
    }

    this.domToolsService.css(this.slideContainer, {
      '-webkit-transform': rule,
      '-moz-transform': rule,
      '-ms-transform': rule,
      '-o-transform': rule,
      'transform': rule
    });

    const slideContainerEvents = ['transitionend', 'oTransitionEnd', 'webkitTransitionEnd'];

    _.each(slideContainerEvents, (event: string) => {
      this.animationListeners.push(
        this.rendererService.renderer.listen(this.slideContainer, event, this.slideContainerTransitionAnimation(transitionEndCallback))
      );
    });
  }

  private touchScroll(position: number): void {
    let rule: string;

    this.rendererService.renderer.removeClass(this.slideContainer, 'carousel-animate');

    if (this.deviceService.isDesktop) {
      rule = `translate3d(${Math.ceil(position)}px, 0, 0)`;
    } else {
      rule = `translate(${Math.ceil(position)}px, 0)`;
    }

    this.domToolsService.css(this.slideContainer, {
      '-webkit-transform': rule,
      '-moz-transform': rule,
      '-ms-transform': rule,
      '-o-transform': rule,
      'transform': rule
    });
  }

  /**
   * get slide offset number
   * @param index
   */
  private getSlidePosition(index: number): number {
    const elements = this.slideContainer.querySelectorAll('slide');
    const slide: any = elements[index];
    const padding = index === 1 ? 0 : 15;

    return slide.offsetLeft + this.windowRef.nativeWindow.innerWidth - padding;
  }

  private getContainerTRansformPosition(): number {
    const transformMatch = window.getComputedStyle(this.slideContainer).transform.match(/(\d+)/g);
    const transformXValue = transformMatch && transformMatch[4] || 0;
    return -transformXValue;
  }
}
