import { Component, ElementRef, Input, ViewEncapsulation } from '@angular/core';

@Component({
   selector: 'action-arrows',
   templateUrl: 'action-arrows.component.html',
  styleUrls: ['./action-arrows.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class ActionArrowsComponent {
  @Input() scrollStep: number = 50;

  isShowLeftArrow: boolean = false;
  isShowRightArrow: boolean = false;
  private scrollable = null;

  constructor(private elementRef: ElementRef) {
  }

  /**
   * On mouseover action
   */
  mouseOver(): void {
    this.scrollable = this.elementRef.nativeElement.querySelector('.scroll-container');
    this.isShowLeftArrow = this.isScrollLeftAvailable();
    this.isShowRightArrow = this.isScrollRightAvailable();
  }

  /**
   * On mouseleave action
   */
  mouseLeave(): void {
    this.scrollable = null;
    this.isShowLeftArrow = false;
    this.isShowRightArrow = false;
  }

  /**
   * Scroll scrollable left
   * @param event
   */
  scrollLeft($event): void {
    if ($event) {
      $event.stopPropagation();
    }
    this.scrollable.scrollLeft = this.scrollable.scrollLeft - this.scrollStep;
  }

  /**
   * Scroll scrollable right
   * @param event
   */
  scrollRight($event): void {
    if ($event) {
      $event.stopPropagation();
    }
    this.scrollable.scrollLeft = this.scrollable.scrollLeft + this.scrollStep;
  }


  /**
   * Get width of scroll inner element
   * @returns {number}
   * @private
   */
  private getInnerWidth(): number {
    if (this.scrollable) {
      return this.scrollable.children[0].scrollWidth;
    }
    return 0;
  }

  /**
   * Check if scroll available
   * @returns {*|boolean
   * @private
   */
  private isScrollAvailable(): boolean {
    return this.scrollable && this.scrollable.clientWidth < this.getInnerWidth();
  }

  /**
   *  Check if left scroll arrow available
   *  @returns {*|boolean}
   */
   private isScrollLeftAvailable(): boolean {
    return this.isScrollAvailable() && this.scrollable.scrollLeft > 0;
  }

  /**
   * Check if right scroll arrow available
   * @returns {*|boolean}
   */
  private isScrollRightAvailable(): boolean {
    return this.isScrollAvailable() &&
      this.scrollable.scrollLeft < this.getInnerWidth() - this.scrollable.clientWidth;
  }
}
