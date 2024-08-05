import {
  AfterContentInit, Component, ElementRef, EventEmitter, Input, OnDestroy, OnInit, Output, ViewChild
} from '@angular/core';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import {
  IScrollChanges, IScrollDimensions, IScrollInfo, IScrollVisibility
} from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.model';
import { StickyVirtualScrollerService } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.service';
import { Subscription } from 'rxjs';
import * as _ from 'underscore';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'sticky-virtual-scroller',
  templateUrl: './sticky-virtual-scroller.component.html',
  styleUrls: ['sticky-virtual-scroller.component.scss']
})
export class StickyVirtualScrollerComponent implements OnInit, OnDestroy, AfterContentInit {
  @Input() items: any[];
  @Input() scrollUniqueId: string;
  @Input() scrollableElementLevel: number;
  @Input() scrollableHeaderSelector: string;
  @Input() stickyHeaderTag: string;
  @Input() stickyHeaderLevel: number;
  @Input() stickyContainerTag: string;
  @Input() stickyContainerLevel: number;
  @Input() scrollDebounceTime: number = 1000;

  @Output() readonly preFetchNext: EventEmitter<boolean> = new EventEmitter();
  @Output() readonly scrollHandler: EventEmitter<IScrollChanges> = new EventEmitter();
  @Output() readonly toggleVisibility: EventEmitter<IScrollVisibility> = new EventEmitter();
  @Output() readonly toogleStickyVisiblity: EventEmitter<boolean> = new EventEmitter();

  scrollActive: boolean;
  scrollableEvents: any[];
  itemHeight: number = 93;

  @ViewChild('scrollableContaier', {static: true})
  private scrollableContaierElementRef: ElementRef;
  private stickyElement: Element;
  private firstScrollableElement: Element;
  private scrollableElement: Element;
  private lastScrollableElement: Element;
  private stickyElementPlaceholder: Element = null;
  private scrollEnabled: boolean;
  private isFirstStickyElement: boolean;
  private visible: boolean = false;
  private touchStartPosition: number;

  private scrollDimensions: IScrollDimensions;
  private scrollInfo: IScrollInfo;

  private touchStart: Function;
  private touchEnd: Function;
  private windowScroll: Function;

  private toggleVisibilityDebounced: Function;

  private updateScrollDimensionsSubscription: Subscription;
  private updateScrollVisibilitySubscription: Subscription;

  private isIOsEnabled: boolean;
  private isAndroidEnabled: boolean;
  private lastScrollableTopPosition: number;
  private readonly itemSelector: string = '.sticky-virtual-scroll-item';

  constructor(
    private stickyScrollService: StickyVirtualScrollerService,
    private domToolsService: DomToolsService,
    private windowRef: WindowRefService,
    private rendererService: RendererService,
    private element: ElementRef,
    private cmsService: CmsService,
    private deviceService: DeviceService) {
    this.toggleVisibilityDebounced = _.debounce((visible: boolean, reloadData: boolean) => {
      this.toggleVisibility.emit({ visible, reloadData });
    }, this.scrollDebounceTime);
  }

  ngOnInit(): void {
    this.updateScrollDimensionsSubscription = this.stickyScrollService.updateScrollDimensions$.subscribe(() => {
      this.calculateScrollDimensions();
      if (!this.stickyScrollService.scrollInfo) {
        this.setScrollInfo();
        this.stickyScrollService.handleStickHeaderPosition();
      }
    });

    this.updateScrollVisibilitySubscription = this.stickyScrollService.updateScrollVisibility$.subscribe(() => {
      this.windowRef.nativeWindow.setTimeout(() => {
        this.scrollVisibilityHandler();
      }, 200);
    });

    this.cmsService.getSystemConfig().subscribe(systemConfig => {
      if (systemConfig && systemConfig.VirtualScrollConfig && systemConfig.VirtualScrollConfig.enabled) {
        this.isIOsEnabled = this.deviceService.isIos && systemConfig.VirtualScrollConfig.iOSInnerScrollEnabled;
        this.isAndroidEnabled = this.deviceService.isAndroid && systemConfig.VirtualScrollConfig.androidInnerScrollEnabled;
      }
    });
  }

  ngOnDestroy(): void {
    this.windowScroll && this.windowScroll();
    this.touchStart && this.touchStart();
    this.touchEnd && this.touchEnd();

    this.updateScrollDimensionsSubscription.unsubscribe();
    this.updateScrollVisibilitySubscription.unsubscribe();
    this.visible = false;
    if (this.scrollInfo && this.scrollInfo.isSticked) {
      this.stickyScrollService.wasSticked = true;
    }
  }

  ngAfterContentInit(): void {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.stickyScrollService.calculateInitialScrollDimensions();
      this.calculateScrollDimensions();
      this.scrollVisibilityHandler(false, true);
      if (this.scrollDimensions) {
        this.scrollEnabled = this.items && this.items.length * this.itemHeight >= this.scrollDimensions.viewPortHeight;
        if (!this.scrollEnabled) {
          this.preFetchNext.emit(true);
        }
      }
      this.attachEventListeneres();
    }, 200);
  }

  scrollVisibilityHandler(reloadData: boolean = true, forcePrefetch: boolean = false): void {
    if (this.stickyScrollService.isSuspended || !this.scrollDimensions) {
      return;
    }

    const scrollableTopEdge: number = this.domToolsService.getElementTopPosition(this.scrollableElement);
    const scrollableBottomEdge: number = this.domToolsService.getElementBottomPosition(this.scrollableElement);

    const viewPortTopEdge: number = this.scrollDimensions.scrollableMaxPosition;
    const viewPortBottomEdge: number = this.scrollDimensions.documentHeight - this.scrollDimensions.footerMenuHeight;

    const isOutsideViewPort: boolean = scrollableTopEdge >= viewPortBottomEdge || scrollableBottomEdge <= viewPortTopEdge;
    const isInsideViewPort: boolean = scrollableBottomEdge > viewPortTopEdge && scrollableBottomEdge <= viewPortBottomEdge
      || scrollableTopEdge >= viewPortTopEdge && scrollableTopEdge < viewPortBottomEdge;

    if (this.visible && isOutsideViewPort) {
      this.visible = false;
      this.toggleVisibilityDebounced(this.visible, reloadData);
    } else if (!this.visible && isInsideViewPort) {
      this.visible = true;
      this.toggleVisibilityDebounced(this.visible, reloadData);

      if (this.scrollEnabled && (this.lastScrollableTopPosition > scrollableTopEdge || forcePrefetch)) {
        this.preFetchNext.emit(true);
      }
    }

    this.lastScrollableTopPosition = scrollableTopEdge;
  }

  touchEndHandler(event: TouchEvent): void {
    if (this.stickyScrollService.isSuspended) {
      return;
    }

    const touchEndPosition: number = event.changedTouches[0].clientY;

    if (this.scrollEnabled && this.scrollableElement) {
      const scrollablePosition: number = this.domToolsService.getElementTopPosition(this.scrollableElement);

      const isBelowSticky: boolean = scrollablePosition > this.scrollDimensions.scrollableMaxPosition;
      const isAboveSticky: boolean = scrollablePosition < this.scrollDimensions.scrollableMaxPosition;
      const isScrollingUp: boolean = this.touchStartPosition > touchEndPosition + 5;
      const isScrollingDown: boolean = this.touchStartPosition < touchEndPosition - 5;

      if (isBelowSticky && isScrollingUp) {
        if (this.isIOsEnabled || this.isAndroidEnabled) {
          this.windowRef.nativeWindow.scrollBy(0, scrollablePosition - this.scrollDimensions.scrollableMaxPosition);
        }
      } else if (isAboveSticky && isScrollingDown) {
        if (this.isIOsEnabled || this.isAndroidEnabled) {
          this.windowRef.nativeWindow.scrollBy(0, -(this.scrollDimensions.scrollableMaxPosition - scrollablePosition));
        }
      }
    }
  }

  private attachEventListeneres(): void {
    if (this.scrollableElement) {
      this.windowScroll = this.rendererService.renderer.listen(this.windowRef.nativeWindow, 'scroll', (event: Event) => {
        this.scrollVisibilityHandler();
      });

      this.touchStart = this.rendererService.renderer.listen(this.scrollableElement, 'touchstart', (event: TouchEvent) => {
        this.touchStartPosition = event.touches[0].clientY;
        this.setScrollInfo();
      });

      this.touchEnd = this.rendererService.renderer.listen(this.scrollableElement, 'touchend', (event: TouchEvent) => {
        this.touchEndHandler(event);
      });
    }
  }

  private setScrollInfo(): void {
    this.lastScrollableElement = this.scrollableElement.parentElement.querySelector(`${this.scrollableElement.tagName}:last-of-type`);
    const lastScrollableHeight = this.domToolsService.getOuterHeight(this.lastScrollableElement as HTMLElement);
    this.scrollInfo = {
      ...this.scrollInfo,
      uuid: this.scrollUniqueId,
      dimensions: this.scrollDimensions,
      stickyElement: this.stickyElement,
      stickyElementPlaceholder: this.stickyElementPlaceholder,
      isFirstStickyElement: this.isFirstStickyElement,
      firstScrollableElement: this.firstScrollableElement,
      lastScrollableElement: this.lastScrollableElement,
      lastScrollableHeight: lastScrollableHeight === 0 ? 1 : lastScrollableHeight,
      scrollableElement: this.scrollableElement,
      isVirtualScroll: this.scrollEnabled,
      scrollDebounceTime: this.scrollDebounceTime,

      calculateScrollDimensions: this.calculateScrollDimensions.bind(this),
      preFetchNext: this.preFetchNext,
      toogleStickyVisiblity: this.toogleStickyVisiblity
    };

    this.stickyScrollService.setScrollInfo(this.scrollInfo);
  }

  private calculateScrollDimensions(): IScrollDimensions {
    const initialScrollDimensions: IScrollDimensions = this.stickyScrollService.initialScrollDimensions;

    const scrollableHeaderElement = this.element.nativeElement.parentNode.querySelector(this.scrollableHeaderSelector);
    this.scrollableElement = this.domToolsService.getParentByLevel(this.element.nativeElement, this.scrollableElementLevel);
    this.stickyElement = this.domToolsService.getParentByLevel(this.element.nativeElement, this.stickyHeaderLevel, this.stickyHeaderTag);
    if (this.stickyElement) {
      this.stickyElementPlaceholder = this.stickyElement && this.stickyElement.nextElementSibling;

      const stickyElementParent = this.domToolsService.getParentByLevel(this.element.nativeElement, this.stickyContainerLevel);
      this.isFirstStickyElement = stickyElementParent && stickyElementParent.previousSibling.nodeName !== this.stickyContainerTag;

      const scrollableHeaderHeight: number = scrollableHeaderElement ? this.domToolsService.getOuterHeight(scrollableHeaderElement) : 0;
      let scrollableHeight: number = 0;

      if (this.scrollableElement) {
        scrollableHeight = this.domToolsService.getOuterHeight(this.scrollableElement as HTMLElement);

        if (this.scrollableElement.parentElement) {
          this.firstScrollableElement = this.scrollableElement.parentElement.querySelector(
            `${this.scrollableElement.tagName}:first-of-type`
          );
          this.lastScrollableElement = this.scrollableElement.parentElement.querySelector(
            `${this.scrollableElement.tagName}:last-of-type`
          );
        }
      }

      const stickyElementHeight: number = this.domToolsService.getOuterHeight(this.stickyElement as HTMLElement);

      const scrollableMaxPosition: number = stickyElementHeight + initialScrollDimensions.stickyMaxPosition;
      const viewPortHeight: number = initialScrollDimensions.documentHeight
        - initialScrollDimensions.footerMenuHeight
        - scrollableMaxPosition
        - scrollableHeaderHeight;

      this.scrollDimensions = {
        ...initialScrollDimensions,
        stickyElementHeight: stickyElementHeight,
        scrollableHeaderHeight: scrollableHeaderHeight,
        scrollableHeight: scrollableHeight,
        scrollableMaxPosition: scrollableMaxPosition,
        viewPortHeight: viewPortHeight
      };

      if ((this.isAndroidEnabled || this.isIOsEnabled) && scrollableHeight > viewPortHeight) {
        this.scrollDimensions.scrollableHeight = viewPortHeight + scrollableHeaderHeight;
      }

      this.itemHeight = this.domToolsService.getOuterHeight(this.element.nativeElement.querySelector(this.itemSelector));
      this.scrollEnabled = this.items && this.items.length * this.itemHeight >= viewPortHeight;

      if (this.isIOsEnabled || this.isAndroidEnabled) {
        requestAnimationFrame(() => {
          this.domToolsService.css(this.scrollableContaierElementRef.nativeElement, 'max-height', this.scrollDimensions.viewPortHeight);
        });
      }
    }
    return this.scrollDimensions;
  }
}
