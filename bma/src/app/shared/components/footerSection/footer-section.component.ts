import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'footer-section',
  templateUrl: 'footer-section.component.html',
  styleUrls: ['footer-section.component.scss'],
})

export class FooterSectionComponent implements OnInit, OnDestroy {
  // Indicator to show/hide footer.
  showFooter: boolean = true;
  // Indicator to show/hide footer menu
  showFooterMenu: boolean = true;
  hideNotification: boolean = false;
  footerMenuVisible: boolean = true;

  // Timer configuration object.
  clock: { interval: number, time: string, visible: boolean } = {
    interval: 1000,
    time: '',
    visible: false
  };
  interval: number;
  isMobile: boolean;
  private document: HTMLDocument;
  private tagName: string = 'footerSection';

  constructor(
    protected filtersService: FiltersService,
    protected windowRefService: WindowRefService,
    protected commandService: CommandService,
    protected pubSubService: PubSubService,
    protected deviceService: DeviceService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    this.document = windowRefService.document;
  }

  ngOnInit(): void {
    this.isMobile = this.deviceService.isMobile;

    this.commandService.register(this.commandService.API.TOGGLE_FOOTER_MENU, (state: boolean) => {
      this.toogleFooterMenu(state);
      return Promise.resolve();
    });

    this.commandService.register(this.commandService.API.SHOW_HIDE_FOOTER_MENU, (state: boolean) => {
      this.showHideFooterMenu(state);
      return Promise.resolve();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.QUICK_SWITCHER_ACTIVE,
      (state: boolean) => {
        this.hideNotification = state;
      });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.TOGGLE_MOBILE_HEADER_FOOTER,
      (state: boolean) => this.toggleFooterVisibility(state));
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LOGIN_COUNTER_UPDATE,
      (time: number) => this.updateSessionCounter(time));

    this.pubSubService.subscribe(
        this.tagName, [this.pubSubService.API.SESSION_LOGOUT, this.pubSubService.API.SESSION_LOGIN], () => this.handleSessionEnd()
    );
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.tagName);
  }

  /**
   * Handles event to show/hide footer emitted from signup page.
   * @param {boolean} state Visibility indicator.
   * @private
   */
  private toggleFooterVisibility(state: boolean): void {
    this.showFooter = state;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Show/hide footer menu on different pages
   * @param state
   */
  private toogleFooterMenu(state: boolean): void {
    this.showFooterMenu = state;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Show/hide footer menu on different pages
   * @param state
   */
  private showHideFooterMenu(state: boolean): void {
    this.footerMenuVisible = state;
    this.pubSubService.publish(this.pubSubService.API.TOTEPOOL_SHOWN, !state);
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Handles session end by hiding session timer.
   * @private
   */
  private handleSessionEnd(): void {
    this.clock.visible = false;
    this.windowRefService.nativeWindow.clearInterval(this.interval);
  }

  /**
   * Updates session counter in format hh:mm:ss.
   * @param {number} timeSession Session time value in milliseconds.
   * @private
   */
  private updateSessionCounter(timeSession: number): void {
    const element = this.document.querySelector('#session-timer');
    if (element) {
      const time = this.formatSessionTimeValue(timeSession);
      element.textContent = time;
    }
  }

  /**
   * Format session timer in format d hh:mm:ss.
   * @param {number} time Session time value in milliseconds.
   * @private
   * @return {string} e.g. 2d 23:22:51
   */
  private formatSessionTimeValue(time: number): string {
    const seconds = time % 60;
    const minutes = Math.floor(time / 60) % 60;
    const hours = Math.floor(time / 3600) % 24;
    const days = Math.floor(time / (3600 * 24));

    const hoursStr = hours ? `${this.doubleDigitFormat(hours)}:` : '';
    const daysStr = days ? `${days}${this.daysCount(days)}` : '';

    return `${daysStr}${hoursStr}${this.doubleDigitFormat(minutes)}:${this.doubleDigitFormat(seconds)}`;
  }

  private doubleDigitFormat(n: number): string {
    return (n < 10 ? '0' : '') + n;
  }

  private daysCount(count: number): string {
    return count > 1 ? ' days ' : ' day ';
  }
}
