import { Component, Input, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { AbstractNotificationComponent } from '@shared/components/oxygenNotification/abstract-notification';
import { DeviceService } from '@core/services/device/device.service';
import { IFreebetsPopupDetails } from '@app/core/services/cms/models/system-config';

@Component({
  selector: 'free-bets-notification',
  templateUrl: 'free-bets-notification.component.html',
  styleUrls: ['free-bets-notification.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FreeBetsNotificationComponent extends AbstractNotificationComponent implements OnInit {

  @Input() isBetslip: boolean;
  @Input() hasFreeBets: boolean;
  @Input() hasBetTokens: boolean;
  @Input() hasFanzones: boolean;
  @Input() isNoSelections: boolean;
  @Input() freebetsConfig: IFreebetsPopupDetails;
  isDesktop: boolean;
  isMobile: boolean;
  message: string;
  freebetSvgId:string;
  bannerMsgText:string;

  constructor(
    private device: DeviceService,
    protected changeDetectorRef: ChangeDetectorRef
  ) {
    super();
    const deviceViewType = this.device.getDeviceViewType();
    this.isDesktop = deviceViewType.desktop || deviceViewType.tablet;
    this.isMobile = deviceViewType.mobile;
  }

  ngOnInit(): void {
    this.changeDetectorRef.detectChanges();
  }

  closeNotification(): void {
    this.close();
  }

  /**
   * 
   * @returns {string}
   */
  bannerMsg(): string {
    switch (true) {
      case this.hasBetTokens && this.hasFreeBets:
        return this.freebetsConfig.freebetAndTokensAvailableText + ' ';
      case  (this.hasFreeBets) || (this.hasFanzones && this.hasFreeBets):
        return this.freebetsConfig.freeBetsAvailableText + ' ';
      case this.hasBetTokens:
        return this.freebetsConfig.betTokensAvailableText + ' ';
      case this.hasFanzones:
        return this.freebetsConfig.fanZonesAvailableText + ' ';
      default:
        return '';
    }
  }

  getSvgImgName(): string {
    return (!this.hasFreeBets && this.hasFanzones) ? 'fanzone-bet-label' : 'free-bet-label';
  }
}
