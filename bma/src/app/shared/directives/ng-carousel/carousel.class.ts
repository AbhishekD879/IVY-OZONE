import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import * as _ from 'underscore';

export class Carousel {
  currentSlide: number;
  onSlideChangeCallbacks: Function[];
  quantity: number;
  fluid: boolean;
  amount: number;
  move: Function;

  constructor(
    public slidesCount: number,
    private options: { looping?: boolean },
    private element: HTMLElement,
    private domTools: DomToolsService
  ) {

    this.options = options || {};
    if (typeof options.looping === 'undefined') {
      this.options.looping = true;
    }

    this.slidesCount = slidesCount;
    this.currentSlide = 0;
    this.onSlideChangeCallbacks = [];
  }

  getSlidesQuantity(carousel: HTMLElement): number {
    const carouselPadding = 10; // Show next slides if it almost fully visible
    return Math.floor((this.domTools.getWidth(carousel.parentElement) + carouselPadding) /
      this.domTools.getWidth(carousel.querySelector('slide')) ) - 1;
  }

  next(): number {
    this.quantity = this.fluid ? this.getSlidesQuantity(this.element) : 0;
    let nextSlide = this.currentSlide + this.quantity + 1;
    let wrapping;

    if (nextSlide > this.slidesCount - this.amount) {
        if (this.options.looping) {
            nextSlide = 0;
            wrapping = 'right';
        } else {
            nextSlide = this.slidesCount - this.amount;
        }

    }

    this.toIndex(nextSlide, wrapping);
    return nextSlide;
  }

  previous(): number {
    this.quantity = this.fluid ? this.getSlidesQuantity(this.element) : 0;
    let previousSlide = this.currentSlide - this.quantity - 1;
    let wrapping;

    if (previousSlide < 0) {
        if (this.options.looping) {
            previousSlide = this.slidesCount - 1;
            wrapping = 'left';
        } else {
            previousSlide = 0;
        }

    }

    this.toIndex(previousSlide, wrapping);
    return previousSlide;
  }

  onSlideChange(callback: Function): number {
    this.onSlideChangeCallbacks.push(callback);
    return this.onSlideChangeCallbacks.indexOf(callback);
  }

  unbindOnSlideChangeCallback(index: number): void {
    if (typeof(this.onSlideChangeCallbacks[index]) === 'undefined') {
      return;
    }
    this.onSlideChangeCallbacks.splice(index, 1);
  }

  toIndex(index, wrapping?): void {
    wrapping = wrapping || false;
    this.currentSlide = index % this.slidesCount;

    // Own on slide change callbacks
    _.forEach(this.onSlideChangeCallbacks, (callback: Function) => {
        if (typeof(callback) === 'function') {
          callback(this.currentSlide, wrapping);
        }
    });
  }

}
