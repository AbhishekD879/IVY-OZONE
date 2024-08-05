import { Injectable, NgZone, Renderer2, RendererFactory2 } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Injectable({
  providedIn: 'root'
})
export class BodyScrollLockService {
  private renderer: Renderer2;

  private initialClientY: number = -1;
  private isBodyScrollLocked: boolean = false;
  private elTouchStartSub: () => void;
  private elTouchMoveSub: () => void;
  private windowTouchMoveSub: () => void;

  constructor(
    private windowRef: WindowRefService,
    private rendererFactory: RendererFactory2,
    private ngZone: NgZone
  ) {
    this.renderer = this.rendererFactory.createRenderer(null, null);
  }

  /**
   * Disable body scroll (needed only for iOS)
   * @param {HTMLElement} element - element allowed to scroll
   */
  disableBodyScroll(element: HTMLElement): void {
    if (element) {
      // Remove listeners
      if (this.isBodyScrollLocked) {
        this.elTouchStartSub();
        this.elTouchMoveSub();
      }

      this.elTouchStartSub = this.renderer.listen(element, 'touchstart', (event) => {
        this.initialClientY = event.targetTouches[0].clientY;
      });

      this.elTouchMoveSub = this.renderer.listen(element, 'touchmove', (event) => {
        this.ngZone.runOutsideAngular(() => {
          this.handleScroll(event, element);
        });
      });

      if (!this.isBodyScrollLocked) {
        this.windowTouchMoveSub = this.renderer.listen(this.windowRef.document, 'touchmove', this.preventDefault);
        this.isBodyScrollLocked = true;
      }
    }
  }

  /**
   * Enable body scroll if was disabled - unbind all added blockers
   */
  enableBodyScroll(): void {
    if (this.isBodyScrollLocked) {
      this.elTouchStartSub();
      this.elTouchMoveSub();
      this.windowTouchMoveSub();

      this.isBodyScrollLocked = false;
      this.initialClientY = -1;
    }
  }

  /**
   * Prevent touch events
   * @param {TouchEvent} event
   * @returns {boolean}
   */
  private preventDefault(event: TouchEvent): boolean {
    if (event.preventDefault) {
      event.preventDefault();
    }

    return false;
  }

  /**
   * Element totally scrolled to bottom
   * @param {HTMLElement} element
   * @returns {boolean}
   */
  private isElementTotallyScrolled(element: HTMLElement): boolean {
    return element.scrollHeight - element.scrollTop <= element.clientHeight;
  }

  /**
   * Handle touch scroll
   * @param {TouchEvent} event
   * @param {HTMLElement} element
   * @returns {boolean}
   */
  private handleScroll(event: TouchEvent, element: HTMLElement): boolean {
    const clientY = event.targetTouches[0].clientY - this.initialClientY;

    // top position
    if (element.scrollTop === 0 && clientY > 0) {
      return this.preventDefault(event);
    }

    // bottom position
    if (this.isElementTotallyScrolled(element) && clientY < 0) {
      return this.preventDefault(event);
    }

    event.stopPropagation();
    return true;
  }
}
