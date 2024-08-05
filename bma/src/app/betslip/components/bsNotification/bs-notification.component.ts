import { ChangeDetectionStrategy, ChangeDetectorRef, Component, ElementRef, HostListener, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Router } from '@angular/router';

import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
@Component({
  selector: 'bs-notification',
  templateUrl: 'bs-notification.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BsNotificationComponent implements OnInit, OnChanges, OnDestroy {

  @Input() bsType: string;
  @Input() bsPosition?: string;
  @Input() bsIsClosable?: boolean;
  @Input() bsMessage: string;
  @Input() bsNoScroll?: boolean;

  cssClass: string;
  message: SafeHtml;

  private notifyTimeout: number;
  private element: HTMLElement;
  private document: HTMLDocument;

  constructor(
    private deviceService: DeviceService,
    private windowRefService: WindowRefService,
    private domTools: DomToolsService,
    private domSanitizer: DomSanitizer,
    private router: Router,
    elementRef: ElementRef,
    private changeDetection:ChangeDetectorRef
  ) {
    this.element = elementRef.nativeElement;
    this.document = windowRefService.document;
  }

  ngOnInit(): void {
    this.element.focus();
    this.cssClass = `${this.bsPosition} ${this.bsType}`;
  }

  ngOnDestroy(): void {
    this.windowRefService.nativeWindow.clearTimeout(this.notifyTimeout);
  }

  ngOnChanges(changes: SimpleChanges): void {
    const isMessageChanged = changes.bsMessage;

    if (isMessageChanged) {
      const bsMessage: string = changes.bsMessage.currentValue;
      this.message = bsMessage ? this.domSanitizer.bypassSecurityTrustHtml(bsMessage) : '';
      this.cssClass = `${this.bsPosition} ${this.bsType}`;

      if (!this.bsNoScroll && (bsMessage !== undefined || bsMessage !== null) && this.bsType !== 'default') {
        this.scrollToNotification();
      }
    }
  }

  @HostListener('click', ['$event'])
  checkRedirect(event: MouseEvent): void {
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;

    if (redirectUrl) {
      this.router.navigateByUrl(redirectUrl);
    }
  }

  scrollTop(position: number): void {
    this.document.querySelector('.bs-selections-wrapper.scrollable-content').scrollTop = position;
  }

  hideNotification(): void {
    if (this.bsIsClosable) {
      this.notifyTimeout = this.windowRefService.nativeWindow.setTimeout(() => {
        this.bsMessage = undefined;
        this.message = undefined;
        this.element.style.display = 'none';
        this.changeDetection.detectChanges();
      }, 100);
    }
  }

  scrollToNotification(): void {
    if (!this.document.querySelector('input:focus')) {
      this.windowRefService.nativeWindow.setTimeout(() => {
        const errorDiv = this.document.querySelector('.bs-notification.danger, .bs-notification.success');
        const isVisible = this.document.querySelector('.is-visible') || this.deviceService.isMobile || this.deviceService.isDesktop;
        const scrollDiv = this.document.querySelector('.bs-selections-wrapper');

        const sidebarMenuHeaderElm = this.document.querySelector('.sidebar-menu-header');
        const sidebarHeaderHeight = sidebarMenuHeaderElm && sidebarMenuHeaderElm.clientHeight;

        const singleStakeHeightElm = this.document.querySelector('.single-stake');
        const singleStakeHeight = singleStakeHeightElm && singleStakeHeightElm.clientHeight;

        const topErrorSpace = sidebarHeaderHeight + singleStakeHeight;

        if (isVisible && errorDiv) {
          const panelPosition = this.domTools.getOffset(errorDiv).top - errorDiv.clientHeight - topErrorSpace;
          const panelOffset = this.domTools.getOffset(errorDiv).top + errorDiv.clientHeight + topErrorSpace;

          let scrollPos;
          if (this.windowRefService.nativeWindow.innerHeight <= panelOffset) {
            scrollPos = panelPosition;
          } else {
            scrollPos = this.domTools.getOffset(errorDiv).top - this.domTools.getOffset(scrollDiv).top
              - topErrorSpace + scrollDiv.scrollTop;
          }

          this.scrollTop(scrollPos);
        }
        this.changeDetection.detectChanges();
      });
    }
  }
}
