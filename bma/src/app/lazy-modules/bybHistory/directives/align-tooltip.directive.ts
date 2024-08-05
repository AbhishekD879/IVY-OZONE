import {
  Directive,
  Input,
  ElementRef,
  HostListener,
  AfterViewInit
} from '@angular/core';

import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';

@Directive({
  // eslint-disable-next-line
  selector: '[align-tooltip]'
})
export class AlignTooltipDirective implements AfterViewInit {
  @Input() infoIconXPosition: number;
  @Input() isUsedFromWidget: boolean;

  constructor( private element: ElementRef,
               private domToolsService: DomToolsService,
               private windowRefService: WindowRefService,
               private pubSubService: PubSubService,
               private deviceService: DeviceService) {}

  ngAfterViewInit(): void {
    this.alignTooltipPosition();
  }

  /**
   * Align tooltip position
   */
  alignTooltipPosition() {
    const windowWidth = this.domToolsService.getWidth(this.windowRefService.document.body);
    const tooltipWidth = this.domToolsService.getWidth(this.element.nativeElement);
    const tooltipCenterXPosition = tooltipWidth/2;
    const { paddingRight } = this.windowRefService.nativeWindow.getComputedStyle(this.element.nativeElement);

    if (this.deviceService.isDesktop || this.deviceService.isTablet) {
      this.handleDesktopTooltipPositions(windowWidth, tooltipWidth, tooltipCenterXPosition, paddingRight);
    } else {
      this.handleMobileTooltipPosition(windowWidth, tooltipWidth, tooltipCenterXPosition, paddingRight);
    }
  }

  /**
   * Align widget tooltip position if needed on desktop
   * @param windowWidth
   * @param tooltipWidth
   * @param tooltipCenterXPosition
   * @param paddingRight
   */
  handleDesktopTooltipPositions(windowWidth: number, tooltipWidth: number, tooltipCenterXPosition: number, paddingRight: string) {
    const widgetContainer = this.windowRefService.document.getElementById('home-betslip-tabs');
    const mainContentContainer = this.windowRefService.document.getElementById('content');
    const pageWrapperContainer =
      this.windowRefService.document.getElementById(this.deviceService.isTablet ? 'page-content' : 'page-wrapper');
    const pageWrapperWidth = this.domToolsService.getWidth(pageWrapperContainer);
    const mainContentContainerWidth = this.domToolsService.getWidth(mainContentContainer);
    const widgetWidth = this.domToolsService.getWidth(widgetContainer);
    const lateralElementsWidth = (windowWidth - pageWrapperWidth) / 2;
    const widgetZeroPosition = windowWidth - lateralElementsWidth - widgetWidth;
    const mainContentContainerZeroPosition = windowWidth - lateralElementsWidth - widgetWidth - mainContentContainerWidth;
    const elementZeroPosition = this.isUsedFromWidget ? widgetZeroPosition : mainContentContainerZeroPosition;

    // If outside of main content container or widget from the left
    if (this.infoIconXPosition - elementZeroPosition < tooltipCenterXPosition) {
      this.domToolsService.css(this.element.nativeElement, { left: `-${this.infoIconXPosition - elementZeroPosition - 6}px`});
    } else if (tooltipCenterXPosition + this.infoIconXPosition + parseFloat(paddingRight) > pageWrapperWidth + lateralElementsWidth) {
      // If outside of main content container or widget from the right
      const moveLeft = tooltipCenterXPosition + this.infoIconXPosition - windowWidth;
      this.domToolsService.css(this.element.nativeElement, { left: `-${moveLeft + tooltipCenterXPosition + lateralElementsWidth + 12}px`});
    }
  }

  /**
   * Align tooltip position if needed on mobile|desktop on main app container
   * @param windowWidth
   * @param tooltipWidth
   * @param tooltipCenterXPosition
   * @param paddingRight
   */
  handleMobileTooltipPosition(windowWidth: number, tooltipWidth: number, tooltipCenterXPosition: number, paddingRight: string) {
    // If outside of window from the left
    if (this.infoIconXPosition - tooltipCenterXPosition < 0) {
      this.domToolsService.css(this.element.nativeElement, { left: `-${this.infoIconXPosition - 10}px`});
    } else if (tooltipCenterXPosition + this.infoIconXPosition + parseFloat(paddingRight) > windowWidth) {
      // If outside of window from the right
      const moveLeft = tooltipCenterXPosition + this.infoIconXPosition - windowWidth;
      this.domToolsService.css(this.element.nativeElement, { left: `-${moveLeft + tooltipCenterXPosition + 10}px`});
    }
  }

  @HostListener('document:click', ['$event'])
  clickOutside(event: Event): void {
    event.preventDefault();
    this.pubSubService.publishSync(this.pubSubService.API.CLOSE_TOOLTIPS);
  }
}
