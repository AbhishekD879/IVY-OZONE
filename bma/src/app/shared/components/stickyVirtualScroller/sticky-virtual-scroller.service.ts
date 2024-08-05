import { Injectable, NgZone } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { IScrollInfo, IScrollDimensions } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.model';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { Subject } from 'rxjs';
import { DeviceService } from '@app/core/services/device/device.service';
import { CarouselMenuStateService } from '@app/core/services/carouselMenuState/carousel-menu-state.service';
import { sampleTime, debounceTime } from 'rxjs/operators';
import { runOutsideZone } from '@core/operators/runOutsideZone.operator';

@Injectable({ providedIn: 'root' })
export class StickyVirtualScrollerService {
  wasSticked: boolean;

  initialScrollDimensions: IScrollDimensions;
  isSuspended: boolean;

  suspendScroll$: Subject<boolean>;
  updateScrollDimensions$: Subject<void>;
  updateScrollVisibility$: Subject<void>;

  private serviceScrollInfo: IScrollInfo;
  private lastScrollInfo: IScrollInfo;
  private firstStickyElement: Element;

  private orientationChange: Function;
  private resize: Function;
  private scrollHandler: Function;
  private stickCarousel: Function;
  private isCarouselStick: boolean;
  private isSticky: boolean;
  private readonly channelName: string = 'stickyVirtualScroll';
  private keepStickyHeader: boolean = true;
  get scrollInfo(): IScrollInfo {
    return this.serviceScrollInfo;
  }

  set scrollInfo(value:IScrollInfo){}

  constructor(private windowRef: WindowRefService,
    private renderService: RendererService,
    private pubSubService: PubSubService,
    private domToolsService: DomToolsService,
    private zone: NgZone,
    private deviceService: DeviceService,
    private carouselMenuStateService: CarouselMenuStateService) {
    this.suspendScroll$ = new Subject();
    this.updateScrollDimensions$ = new Subject();
    this.updateScrollVisibility$ = new Subject();

    this.init();
  }

  destroyEvents(): void {
    if (this.orientationChange) {
      this.orientationChange();
    }

    if (this.resize) {
      this.resize();
    }

    this.scrollHandler && this.scrollHandler();
    this.pubSubService.unsubscribe(this.channelName);
    this.carouselMenuStateService.carouselStick$.next({ stick: false, forceVisibility: false });
    this.keepStickyHeader = false;
  }

  setScrollInfo(incomingScrollInfo: IScrollInfo) {
    this.keepScrollPositions(incomingScrollInfo);

    // using for collapsing prev scrollable section when next is stick (not using at the moment)
    if (!this.lastScrollInfo
      || this.lastScrollInfo && this.serviceScrollInfo && this.lastScrollInfo.uuid !== this.serviceScrollInfo.uuid) {
      this.lastScrollInfo = incomingScrollInfo.isFirstStickyElement ? null : this.serviceScrollInfo;
    }

    this.serviceScrollInfo = incomingScrollInfo;
  }

  keepScrollPositions(scrollInfo: IScrollInfo): void {
    if (!scrollInfo || this.isSuspended) {
      return;
    }

    // another scrollable area (ex. current: Football, new: Tennis)
    const isNewStickyArea = this.serviceScrollInfo && this.serviceScrollInfo.uuid !== scrollInfo.uuid;

    // handle incoming scroll info
    if (isNewStickyArea) {
      const firstScrollablePosition = this.domToolsService.getElementTopPosition(scrollInfo.firstScrollableElement);

      const isFirstTopAboveSticky = firstScrollablePosition <= scrollInfo.dimensions.scrollableMaxPosition;
      // trigger async scroll in order to set correct positions
      if (isFirstTopAboveSticky && !this.isSticky || !isFirstTopAboveSticky && this.isSticky) {
        this.scrollBy(-1);
        this.scrollBy(1);
      }

      // unstick current sticky header
      this.stick(false, false, this.serviceScrollInfo);
    }

    if (!this.firstStickyElement && scrollInfo.isFirstStickyElement) {
      this.firstStickyElement = scrollInfo.stickyElement;
    }
  }

  handleStickyPosition(scrollInfo: IScrollInfo): void {
    if (this.isSuspended || !scrollInfo) {
      return;
    }

    this.handleExternalStickyPositions(scrollInfo);
    this.handleStickHeaderPosition(scrollInfo);
  }

  handleExternalStickyPositions(scrollInfo: IScrollInfo): void {
    this.zone.runOutsideAngular(() => {
      if (this.firstStickyElement) {
        const firstStickyPosition = this.domToolsService.getElementTopPosition(this.firstStickyElement);
        if (!this.isCarouselStick && firstStickyPosition < scrollInfo.dimensions.stickyMaxPosition) {
          requestAnimationFrame(() => {
            this.stickCarousel(true);
          });
        } else if (this.isCarouselStick && firstStickyPosition > scrollInfo.dimensions.stickyMaxPosition) {
          requestAnimationFrame(() => {
            this.stickCarousel(false);
          });
        }
      }
    });
  }

  handleStickHeaderPosition(scrollInfo: IScrollInfo = this.scrollInfo): void {
    // stick(unstick) section header, when reach (reachout) top calculated position
    const firstScrollablePosition: number = this.domToolsService.getElementTopPosition(scrollInfo.firstScrollableElement);
    const lastScrollablePosition: number = this.domToolsService.getElementTopPosition(scrollInfo.lastScrollableElement);
    const isFirstTopAboveSticky: boolean = firstScrollablePosition !== 0
      && firstScrollablePosition <= scrollInfo.dimensions.scrollableMaxPosition;
    const isLastBottomBelowSticky: boolean = lastScrollablePosition !== 0 &&
      lastScrollablePosition + scrollInfo.lastScrollableHeight
      > scrollInfo.dimensions.stickyMaxPosition + scrollInfo.dimensions.scrollableMaxPosition;

    const isFirstBelowSticky: boolean = firstScrollablePosition > scrollInfo.dimensions.scrollableMaxPosition;
    const isLastBottomAboveSticky: boolean = lastScrollablePosition + scrollInfo.lastScrollableHeight
      < scrollInfo.dimensions.stickyMaxPosition + scrollInfo.dimensions.scrollableMaxPosition;

    if (!this.isSticky && isFirstTopAboveSticky && isLastBottomBelowSticky) {
      this.stick(true, false, scrollInfo);
      this.stickCarousel(true);

      if (this.lastScrollInfo) {
        this.lastScrollInfo.toogleStickyVisiblity.emit(true);
      }
    } else if (this.isSticky && (isFirstBelowSticky || isLastBottomAboveSticky)) {
      this.stick(false, false, scrollInfo);
    }
  }

  stick(stick: boolean, keepScroll: boolean, scrollInfo: IScrollInfo = this.serviceScrollInfo): void {
    if (!scrollInfo) {
      return;
    }

    this.zone.runOutsideAngular(() => {
      requestAnimationFrame(() => {
        this.domToolsService.toggleClass(scrollInfo.stickyElement, 'sticky-virtual-scroll', stick);
        this.domToolsService.toggleClass(scrollInfo.stickyElementPlaceholder, 'sticky-virtual-scroll-placeholder', stick);
        if (stick) {
          this.updateStickyHeaderWidth(scrollInfo);
          this.updateStickyHeaderTop(scrollInfo);
          this.domToolsService.css(scrollInfo.stickyElement, 'box-shadow', '0px 2px 10px 0px rgba(0, 0, 0, 0.2)');
        } else {
          (scrollInfo.stickyElement as HTMLElement).style.removeProperty('top');
          (scrollInfo.stickyElement as HTMLElement).style.removeProperty('width');
          (scrollInfo.stickyElement as HTMLElement).style.removeProperty('box-shadow');
        }
        this.isSticky = stick;
        scrollInfo.isSticked = stick;

        if (keepScroll && this.keepStickyHeader) {
          this.keepStickyHeaderPosition(scrollInfo);
        }
      });
    });
  }

  updateScrollVisibility(): void {
    this.updateScrollVisibility$.next();
  }

  setElementHeight(selector: string): number {
    const el = this.windowRef.nativeWindow.document.querySelector(selector);
    return el ? this.domToolsService.getOuterHeight(el) : 0;
  }

  elementsIScrollDimensions(cookieSel: string, topSel: string): IScrollDimensions {
    const cookieElementHeight = this.setElementHeight(cookieSel);
    const topBarHeight = this.setElementHeight(topSel);
    const headerHeight = this.domToolsService.HeaderEl ? this.domToolsService.getOuterHeight(this.domToolsService.HeaderEl) : 0;
    const footerMenuHeight = this.domToolsService.FooterEl ? this.domToolsService.getOuterHeight(this.domToolsService.FooterEl) : 0;

    const documentHeight = this.domToolsService.getHeight(this.windowRef.nativeWindow as Window);
    const stickyMaxPosition = headerHeight + topBarHeight + cookieElementHeight;

    return {
      documentHeight,
      topBarHeight,
      headerHeight,
      footerMenuHeight,
      stickyMaxPosition
    } as IScrollDimensions;
  }

  calculateInitialScrollDimensions(reset: boolean = false): void {
    if (reset || !this.initialScrollDimensions) {
      this.initialScrollDimensions = this.elementsIScrollDimensions('#agreements', '.top-bar');
    }
  }

  scrollBy(relY: number): void {
    this.windowRef.nativeWindow.scrollBy(0, relY);
  }

  redrawScrollableElements(): void {
    this.calculateInitialScrollDimensions(true);
    this.updateScrollDimensions$.next();
    if (this.serviceScrollInfo) {
      this.serviceScrollInfo.dimensions = this.serviceScrollInfo.calculateScrollDimensions();
      this.updateStickyHeaderWidth(this.serviceScrollInfo);
    }
  }

  private init(): void {
    this.attachEventListeners();

    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.FIXED_CONTENT_REDRAW, () => {
      this.handleCookieBannerPosition();
    });

    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.WS_EVENT_DELETE, () => {
      this.updateScrollVisibility();
    });

    this.pubSubService.subscribe(this.channelName, ['INPLAY_COMPETITION_ADDED'],
      () => {
        this.windowRef.nativeWindow.setTimeout(() => {
          this.updateScrollVisibility();
        }, 200);
      });

    this.pubSubService.subscribe(this.channelName, ['INPLAY_COMPETITION_UPDATED'],
      () => {
        this.windowRef.nativeWindow.setTimeout(() => {
          this.updateScrollVisibility();
        }, 200);
      });

    this.pubSubService.subscribe(this.channelName, [this.pubSubService.API.INPLAY_COMPETITION_REMOVED],
      () => {
        this.windowRef.nativeWindow.setTimeout(() => {
          this.updateScrollVisibility();
        }, 200);
      });
  }

  private attachEventListeners(): void {
    const scrollEndEmulation$ = new Subject<void>();

    scrollEndEmulation$.pipe(
      sampleTime(50),
      runOutsideZone(this.zone)
    ).subscribe(() => {
      this.handleStickyPosition(this.serviceScrollInfo);
    });

    // scroll-end emulation for position calculations after scroll/animation finished.
    scrollEndEmulation$.pipe(
      debounceTime(300),
      runOutsideZone(this.zone)
    ).subscribe(() => {
      this.handleStickyPosition(this.serviceScrollInfo);
    });

    this.scrollHandler = this.renderService.renderer.listen(this.windowRef.nativeWindow, 'scroll', (event: Event) => {
      scrollEndEmulation$.next();
    });

    this.stickCarousel = (stick: boolean) => {
      this.carouselMenuStateService.carouselStick$.next({ stick: stick, forceVisibility: true });
      this.isCarouselStick = stick;
    };

    if (this.deviceService.isMobileOrigin) {
      this.orientationChange = this.windowRef.nativeWindow.addEventListener('orientationchange', () => {
        this.redrawScrollableElements();
      });
      this.resize = this.windowRef.nativeWindow.addEventListener('resize', () => this.redrawScrollableElements());
    }
  }

  private handleCookieBannerPosition(): void {
    this.calculateInitialScrollDimensions(true);
    this.updateScrollDimensions$.next();
    if (this.serviceScrollInfo) {
      this.serviceScrollInfo.dimensions = this.serviceScrollInfo.calculateScrollDimensions();
      if (this.isSticky) {
        this.updateStickyHeaderTop(this.serviceScrollInfo);
      }
    }
  }

  private keepStickyHeaderPosition(scrollInfo: IScrollInfo): void {
    if (this.wasSticked) {
      const headerInitialPosition = this.domToolsService.getOffset(scrollInfo.stickyElement).top
        - this.initialScrollDimensions.headerHeight - this.initialScrollDimensions.topBarHeight;

      this.isSuspended = true;
      this.serviceScrollInfo = null;
      this.windowRef.nativeWindow.scroll(0, headerInitialPosition);
      this.isSuspended = false;

      this.carouselMenuStateService.carouselStick$.next({ stick: true, forceVisibility: false });
      this.wasSticked = false;
    }
  }

  private updateStickyHeaderWidth(scrollInfo: IScrollInfo): void {
    const width = this.domToolsService.getWidth(scrollInfo.scrollableElement);
    this.domToolsService.css(scrollInfo.stickyElement, 'width', width);
  }

  private updateStickyHeaderTop(scrollInfo: IScrollInfo): void {
    this.domToolsService.css(scrollInfo.stickyElement, 'top', scrollInfo.dimensions.stickyMaxPosition);
  }
}
