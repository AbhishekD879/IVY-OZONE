import { Directive, ElementRef, Input, OnDestroy, OnInit } from '@angular/core';
import { RendererService } from '@shared/services/renderer/renderer.service';

/**
 * The overscroll-fix directive makes scrolling action occur only within the target element without propagating outside,
 * when its or some of its descendants' content is overscrolled or non-scrollable area is scrolled.
 * i.e. such actions will not affect the whole page scroll. Supports touch and wheel vertical scrolling.
 * Other page parts still remain scrollable if they are targeted directly.
 * By default, overscrolling is prevented only on elements with 'position: fixed' CSS rule applied,
 * though this condition may be ignored if directive is provided as 'overscroll-fix="always"'
 *
 * When scrolling event occurs on the element marked by overscroll-fix directive,
 * the 'scrollability' of it and all its children up from the event target is checked.
 * If neither of them is scrollable or has reached its scroll limits,
 * then the event is prevented and scrolling stops without affecting rest of the page.
 */
@Directive({
  // eslint-disable-next-line
  selector: '[overscrollFix]'
})
export class OverscrollFixDirective implements OnInit, OnDestroy {
  @Input() overscrollFix;

  private initialTouchY: number;
  private element: HTMLElement;

  private touchStartListener: Function;
  private touchMoveListener: Function;
  private wheelMoveListener: Function;

  constructor(private rendererService: RendererService,
              private elementRef: ElementRef) {
    this.touchStartHandler = this.touchStartHandler.bind(this);
    this.touchMoveHandler = this.touchMoveHandler.bind(this);
    this.wheelHandler = this.wheelHandler.bind(this);
  }

  ngOnInit(): void {
    this.element = this.elementRef.nativeElement;
    this.touchStartListener = this.rendererService.renderer.listen(this.element, 'touchstart', this.touchStartHandler);
    this.touchMoveListener = this.rendererService.renderer.listen(this.element, 'touchmove', this.touchMoveHandler);
    this.wheelMoveListener = this.rendererService.renderer.listen(this.element, 'wheel', this.wheelHandler);
  }

  ngOnDestroy(): void {
    this.touchStartListener();
    this.touchMoveListener();
    this.wheelMoveListener();
  }

  private shouldBePrevented(): boolean {
    return this.overscrollFix === 'always' || this.element.style.position === 'fixed';
  }

  private getTouchY(event: TouchEvent): number  {
    return (event && event.touches && event.touches[0] && event.touches[0].clientY) || 0;
  }

  private hasScrollableContent(target: HTMLElement): boolean {
    return target.scrollHeight > target.clientHeight ||
              (target !== this.element && this.hasScrollableContent(target.parentElement));
  }

  private isScrollableDown(target: HTMLElement): boolean {
    return target.scrollTop < target.scrollHeight - target.clientHeight ||
            (target !== this.element && this.isScrollableDown(target.parentElement));
  }

  private isScrollableUp(target: HTMLElement): boolean {
    return target.scrollTop > 0 || (target !== this.element && this.isScrollableUp(target.parentElement));
  }

  private touchStartHandler(event: TouchEvent): void {
    this.initialTouchY = this.getTouchY(event);
  }

  private touchMoveHandler(event: TouchEvent): void {
    const currentTouchY = this.getTouchY(event);
    const isSingleTouch = event && event.touches && event.touches.length === 1;
    const isSwipingUp = currentTouchY < this.initialTouchY;
    const isSwipingDown = currentTouchY > this.initialTouchY;
    const targetElement = event.target as HTMLElement;

    /* Note: swipe direction is opposite to scroll direction */
    if (this.shouldBePrevented() && isSingleTouch && (!this.hasScrollableContent(targetElement) ||
      (isSwipingUp && !this.isScrollableDown(targetElement)) || (isSwipingDown && !this.isScrollableUp(targetElement)))) {
      event.preventDefault();
    }

    this.initialTouchY = currentTouchY;
  }

  private wheelHandler(event: WheelEvent): void {
    const isScrollingUp = event.deltaY < 0;
    const isScrollingDown = event.deltaY > 0;
    const targetElement = event.target as HTMLElement;

    if (this.shouldBePrevented() && (!this.hasScrollableContent(targetElement) ||
      (isScrollingUp && !this.isScrollableUp(targetElement)) || (isScrollingDown && !this.isScrollableDown(targetElement)))) {
      event.preventDefault();
    }
  }
}
