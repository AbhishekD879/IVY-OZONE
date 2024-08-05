import { Directive, OnDestroy, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';

// eslint-disable-next-line
@Directive({selector: '[scroll-fix]'})
export class ScrollFixDirective implements OnInit, OnDestroy {
  // eslint-disable-next-line max-len
  public readonly overlayClasses = `.football-content-overlay, .quickbet-opened, .fiveasideentry-content-overlay, .fiveasideentry-rules-overlay, .fiveaside-cards-overlay, .fiveaside-lobby-overlay`;
  // eslint-disable-next-line max-len
  public readonly scrollClasses = `.scrollable-content, #football-tutorial-overlay, #fiveaside-entry-overlay, #fiveaside-terms-rules, #fiveaside-welcome-overlay, #fiveaside-lobby-tutorial`;

  touchYPos: number = null;
  options: { [key: string]: string } = {
    // Class for opened slide-out
    overlayOpenedClass: this.overlayClasses,
    // Class for scrollabel content
    scrollableClass: this.scrollClasses
  };

  constructor(private windowRef: WindowRefService,
              private device: DeviceService) {
    this.touchHandler = this.touchHandler.bind(this);
  }

  ngOnInit() {
    if (this.device.isIos) {
      this.windowRef.nativeWindow.addEventListener('touchstart', this.touchHandler);
      this.windowRef.nativeWindow.addEventListener('touchmove', this.touchHandler);
    }
  }

  ngOnDestroy() {
    this.windowRef.nativeWindow.removeEventListener('touchstart', this.touchHandler);
    this.windowRef.nativeWindow.removeEventListener('touchmove', this.touchHandler);
  }

  private getYpos(event: TouchEvent): number {
    return event && event.touches && event.touches[0] && event.touches[0].pageY;
  }

  private touchHandler(event: TouchEvent): void {
    // It's nothing to do if overlay isn't opened
    if (!this.isOverlayOpened()) {
      return;
    }

    const touchY = this.getYpos(event);

    if (event.type === 'touchstart') {
      this.touchYPos = touchY;
    }

    if (event.type === 'touchmove') {
      const container = this.getScrollableContainer();
      if (container) {
        const isPreventScrollClassPresent = _.indexOf(container.classList, 'prevented-container') !== -1;
        const isTouchedTop = touchY - this.touchYPos >= 0 && container.scrollTop <= 0;
        const isScrolledToBottom = container.scrollTop >= container.scrollHeight - container.offsetHeight;
        // Check where we are scrolling
        if (!isPreventScrollClassPresent && !isTouchedTop && !isScrolledToBottom) {
          return;
        }
      }

      event.preventDefault();
    }
  }

  private isOverlayOpened(): boolean {
    return !!this.windowRef.document.querySelector(this.options.overlayOpenedClass);
  }

  private getScrollableContainer(): HTMLElement {
    return this.windowRef.document.querySelector(this.options.scrollableClass);
  }
}
