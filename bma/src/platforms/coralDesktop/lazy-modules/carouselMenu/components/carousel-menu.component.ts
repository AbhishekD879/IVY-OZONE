import {
  Component,
  ViewChild,
  ElementRef,
  ChangeDetectionStrategy, Input
} from '@angular/core';
import { CarouselMenuComponent as AppCarouselMenuComponent } from '@app/lazy-modules/carouselMenu/components/carousel-menu.component';
@Component({
  selector: 'carousel-menu',
  styleUrls: ['../../../../../app/lazy-modules/carouselMenu/components/carousel-menu.component.scss'],
  templateUrl: './carousel-menu.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CarouselMenuComponent extends AppCarouselMenuComponent {

  @ViewChild('menuContainer', {static: false}) menuContainer: ElementRef;

  isShowLeftArrow: boolean = false;
  isShowRightArrow: boolean = false;
  @Input() carouselClass?: string;
  @Input() carouselId? : string;
  private readonly SCROLL_STEP: number = 50;

  /**
   * On mouseover action
   */
  mouseOver(): void {
    this.isShowLeftArrow = this.isScrollLeftAvailable();
    this.isShowRightArrow = this.isScrollRightAvailable();
  }

  /**
   * On mouseleave action
   */
  mouseLeave(): void {
    this.isShowLeftArrow = false;
    this.isShowRightArrow = false;
  }

  /**
   * Scroll menuContainer left
   * @param event
   */
  scrollLeft(event: MouseEvent): void {
    if (event) {
      event.stopPropagation();
    }
    this.menuContainer.nativeElement.scrollLeft = this.domTools.getScrollLeft(this.menuContainer.nativeElement) - this.SCROLL_STEP;
  }

  /**
   * Scroll menuContainer right
   * @param event
   */
  scrollRight(event: MouseEvent): void {
    if (event) {
      event.stopPropagation();
    }

    this.menuContainer.nativeElement.scrollLeft = this.domTools.getScrollLeft(this.menuContainer.nativeElement) + this.SCROLL_STEP;
  }


  /**
   * Get width of scroll inner element
   * @returns {number}
   * @private
   */
  private getInnerWidth(): number {
    if (this.menuContainer) {
      return this.menuContainer.nativeElement.firstChild.scrollWidth;
    }
    return 0;
  }

  /**
   * Check if scroll available
   * @returns {*|boolean}
   * @private
   */
  private isScrollAvailable(): boolean {
    return this.menuContainer && this.domTools.getWidth(this.menuContainer.nativeElement) < this.getInnerWidth();
  }

  /**
   * Check if left scroll arrow available
   * @returns {*|boolean}
   */
  private isScrollLeftAvailable(): boolean {
    return this.isScrollAvailable() && this.domTools.getScrollLeft(this.menuContainer.nativeElement) > 0;
  }

  /**
   * Check if right scroll arrow available
   * @returns {*|boolean}
   */
  private isScrollRightAvailable(): boolean {
    return this.isScrollAvailable() &&
      this.domTools.getScrollLeft(this.menuContainer.nativeElement) <
      this.getInnerWidth() - this.domTools.getWidth(this.menuContainer.nativeElement);
  }

}
