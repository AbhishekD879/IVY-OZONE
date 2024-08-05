import { Component, ElementRef, HostListener, Inject, Input, OnChanges, OnDestroy, OnInit, SimpleChanges, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DOCUMENT } from '@angular/common';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { DeviceService } from '@core/services/device/device.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'ng-info-panel',
  templateUrl: 'ng-info-panel.component.html',
  styleUrls:['ng-info-panel.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class NgInfoPanelComponent implements OnInit, OnDestroy, OnChanges {
  @Input() message: string;
  @Input() type: string;
  @Input() align?: string;
  @Input() noScroll?: boolean;
  @Input() noHide?: boolean;
  @Input() noHideMessage?: boolean;
  @Input() withArrowTop?: boolean;
  @Input() withArrowBottom?: boolean;
  @Input() noBgColor?: boolean;
  @Input() quickDepositPanel?: boolean;

  /**
   * visibility Flag
   */
  isPanelShown: boolean = false;
  infoMsg: SafeHtml;
  isScrolledToPanel: boolean;
  touchMoved: boolean;

  constructor(
    @Inject(DOCUMENT) private document: any,
    private windowRef: WindowRefService,
    private elementRef: ElementRef,
    private domToolsService: DomToolsService,
    private rendererService: RendererService,
    private domSanitizer: DomSanitizer,
    private router: Router,
    private deviceService: DeviceService
  ) {
    this.watchClick = this.watchClick.bind(this);
    this.hideInfoPanel = this.hideInfoPanel.bind(this);
  }

  @HostListener('click', ['$event'])
  checkRedirect(event: MouseEvent): void {
    const redirectUrl: string = (<HTMLElement>event.target).dataset.routerlink;

    if (redirectUrl) {
      this.router.navigateByUrl(redirectUrl);
    }
  }

  ngOnInit(): void {
    // default triangle alignment
    this.align = this.align || ' left';
    // initialize immediately if dynamic creation
    !!this.message && this.initInfoPanel();
  }

  ngOnDestroy(): void {
    this.removeWatchingEventListeners();
  }

  ngOnChanges(changesObj: SimpleChanges): void {
    if (changesObj.message && !changesObj.message.firstChange && changesObj.message.currentValue) {
      this.initInfoPanel();
    }
  }

  initInfoPanel(): void {
    if (this.message === undefined || this.message === null) {
      this.hideInfoPanel();
    } else {
      this.showInfoPanel();
    }
  }

  /**
   * Show panel element
   *
   * @param message - message text for dynamic showing
   * @param {string} type
   */
  showInfoPanel(message?: string, type?: string): void {
    if (type) {
      this.type = type;
    }

    if (message) {
      this.message = message;
    }

    this.infoMsg = ''; // Clear previously message
    this.infoMsg = this.getMessageElem(this.message);
    this.isPanelShown = !!this.message;
    this.makeAutoScroll();
    this.addWatchingEventListeners();
  }

  /**
   * Hide panel element
   */
  hideInfoPanel(): void {
    this.message = '';
    this.isPanelShown = false;
    this.isScrolledToPanel = false;
    this.removeWatchingEventListeners();
  }

  /**
   * Event Listener callbacks
   */
  eventClickSub: any = () => {};
  eventTouchSub: any = () => {};
  eventChangeSelectSub: any = () => {};
  eventToStopBubblingSub: any = () => {};

  /**
   *
   * @returns {boolean}
   */
  get hasArrow(): boolean {
    return !!(this.withArrowTop || this.withArrowBottom || this.noBgColor);
  }
  set hasArrow(value:boolean){}

  /**
   * Css class for infoPanel with arrow
   * @returns {string}
   */
  get ngInfoPanelWithArrowClass(): string {
    let cssClass: string = this.messageTypeClass;

    cssClass += this.withArrowTop ? ' arrow-panel top' : '';
    cssClass += this.withArrowBottom ? ' arrow-panel bottom' : '';
    cssClass += this.noBgColor ? ' no-bg-color' : '';
    return cssClass;
  }
  set ngInfoPanelWithArrowClass(value:string){}

  /**
   * Css class for infoPanel without arrow
   * @returns {string}
   */
  get ngInfoPanelClass(): string {
    let cssClass: string = this.messageTypeClass;
    cssClass += this.align;
    if (this.quickDepositPanel) {
      cssClass += ' quick-deposit-info';
    }
    return cssClass;
  }
  set ngInfoPanelClass(value:string){}

  /**
   * Html element class for different types of messages
   * @returns {string}
   */
  get messageTypeClass(): string {
    return this.message ? `${this.type}-panel ` : '';
  }
  set messageTypeClass(value:string){}

  /**
   * Scroll to panel position
   */
  private makeAutoScroll(): void {
    const panelPosition: number = this.elementRef.nativeElement.getBoundingClientRect().top;
    const fixedHeadersHeight: number = 85;
    const scrollTop: number = this.windowRef.nativeWindow.scrollY;
    const isPanelInViewport: boolean = panelPosition > scrollTop + fixedHeadersHeight;

    if (!this.noScroll && !isPanelInViewport && !this.isScrolledToPanel) {
      this.windowRef.nativeWindow.document.querySelectorAll('html, body, .w-content-scroll').forEach(element => {
        element.scrollTop += panelPosition - fixedHeadersHeight;
      });
      this.isScrolledToPanel = true;
    }
  }

  /**
   * Hide panel on any document click
   */
  private watchClick(event: MouseEvent): void {
    if (!this.isPanelShown || this.noHideMessage) {
      return;
    }

    const eventElement: HTMLElement = <HTMLElement>event.target;
    const actionElements: string[] = ['A', 'BUTTON', 'INPUT', 'SELECT', 'LABEL', 'TEXTAREA'];
    const timeout: number = (!this.deviceService.isDesktop && actionElements.includes(eventElement.tagName.toUpperCase())) ? 50 : 0;
    const redirectUrl: string = (eventElement).dataset.routerlink;

    if (!redirectUrl && !this.windowRef.document.querySelectorAll('.modal-dialog').length && this.message !== '') {
      // hide if it was a click, and not scroll (case for mobile)
      if (!this.touchMoved ) {
        setTimeout(() => {
          this.hideInfoPanel();
        }, timeout);
      }
    }
  }

  /**
   * Preventing bubling.
   * @param {object} e - event object
   */
  private stopBubbling(e): void {
    e.stopPropagation();
  }

  /**
   * set default (false) value on touchStart
   */
  private onTouchStart(): void {
    this.touchMoved = false;
  }
  /**
   * If it was scroll (there was moving event)
   * - setting moving flag to true
   */
  private onTouchMove(): void {
    this.touchMoved = true;
  }

  /**
   * Message could be HTMLElement and string, If message is an string, wrap string to span.
   * @param {HTMLElement|String} message - message elem or message text
   * @returns {SafeHtml} - message element
   */
  private getMessageElem(message) {
    return this.domSanitizer.bypassSecurityTrustHtml(message.replace(/href="(?!https:)/g, 'data-routerlink="'));
  }

  private eventTouchStartSub: any = () => {};
  private eventTouchMoveSub: any = () => {};

  /**
   * While message is visible we watch for user interaction
   */
  private addWatchingEventListeners(): void {
    this.removeWatchingEventListeners();
    // panel shouldn't react on touches and to be hidden if this attribute specified
    if (!this.noHide) {
      if (this.deviceService.isDesktop) {
        this.eventClickSub = this.rendererService.renderer.listen(this.document, 'click', this.watchClick.bind(this));
      } else {
        this.eventTouchSub = this.rendererService.renderer.listen(this.document, 'touchend', this.watchClick.bind(this));
        this.eventTouchStartSub = this.rendererService.renderer.listen(this.document, 'touchstart', this.onTouchStart.bind(this));
        this.eventTouchMoveSub = this.rendererService.renderer.listen(this.document, 'touchmove', this.onTouchMove.bind(this));
      }
    }
    this.elementRef.nativeElement.querySelectorAll('select').forEach(element => {
      this.eventChangeSelectSub = this.rendererService.renderer.listen(element, 'change', $event => {
        if (!this.domToolsService.hasClass($event.target, 'default-select')) {
          this.hideInfoPanel();
        }
      });
    });
    setTimeout(() => {
      this.elementRef.nativeElement.querySelectorAll('button[type=submit], select, .info-panel a, input.from-input')
        .forEach(element => {
          this.eventToStopBubblingSub = this.rendererService.renderer.listen(element, 'touchend',  this.stopBubbling.bind(this));
        });
    }, 0);
  }

  /**
   * Remove listeres After message is hidden or scope destroyed
   */
  private removeWatchingEventListeners(): void {
    if (!this.noHide) {
      this.eventClickSub();
      this.eventTouchSub();
      this.eventTouchStartSub();
      this.eventTouchMoveSub();
    }
    this.elementRef.nativeElement.querySelectorAll('select').forEach(element => {
      this.eventChangeSelectSub();
    });
    this.elementRef.nativeElement.querySelectorAll('button[type=submit], select, .info-panel a, input.from-input').forEach(element => {
      this.eventToStopBubblingSub();
    });
  }
}
