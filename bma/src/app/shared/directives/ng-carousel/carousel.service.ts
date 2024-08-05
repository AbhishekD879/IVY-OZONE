import { Injectable } from '@angular/core';

import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { Carousel } from './carousel.class';

@Injectable()
export class CarouselService {

  instances: {
    [key: string]: Carousel
  } = {};

  constructor(
    private domTools: DomToolsService
  ) {}

  /**
   * Create carousel instance
   * @param {number} slidesCount
   * @param {string} name
   * @param {{looping: boolean}} options
   * @param {HTMLElement} element
   * @return {Carousel}
   */
  add(slidesCount: number,
      name: string,
      options: { looping?: boolean; },
      element: HTMLElement
  ): Carousel {

    if (!name) {
      console.error('Error: no carousel name specified');
    }

    // Check slidesCount
    slidesCount = slidesCount || 0;

    // Create carousel instance
    const instance = new Carousel(slidesCount, options, element, this.domTools);

    // Save new carousel instance
    this.instances[name] = instance;

    return instance;
  }

  get(name: string): Carousel {
    const instance = this.instances[name] || false;

    // if (!instance) {
    //   console.error(`Carousel with name ${name} do not exist`);
    // }

    return instance ? instance : null;
  }

  remove(name: string): void {
    delete this.instances[name];
  }
}
