import { Component, ChangeDetectorRef, ChangeDetectionStrategy } from '@angular/core';
import { IFirstMultipleInfo } from '@betslip/models/first-multiple-info';

import {
  AccaNotificationComponent as BaseAccaNotificationComponent
} from '../../../../../app/shared/components/accaNotification/acca-notification.component';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { FiltersService } from '@core/services/filters/filters.service';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: 'acca-notification',
  templateUrl: 'acca-notification.component.html',
  styleUrls: ['acca-notification.component.scss']
})

export class AccaNotificationComponent extends BaseAccaNotificationComponent {
  accaPaysOfferText: string;
  readonly accaBaseStake = 10; // the offered stake for acca bar calculations

  constructor(
    nativeBridgeService: NativeBridgeService,
    user: UserService,
    fracToDec: FracToDecService,
    domTools: DomToolsService,
    pubsub: PubSubService,
    deviceService: DeviceService,
    GTM: GtmService,
    windowRef: WindowRefService,
    localeService: LocaleService,
    cmsService: CmsService,
    changeDetectorRef: ChangeDetectorRef,
    filterService: FiltersService
  ) {
    super(
      nativeBridgeService,
      user,
      fracToDec,
      domTools,
      pubsub,
      deviceService,
      GTM,
      windowRef,
      localeService,
      cmsService,
      changeDetectorRef,
      filterService
    );
  }

  updateAccaData(ACCAData: IFirstMultipleInfo): void {
    super.updateAccaData(ACCAData);

    const { potentialPayout, translatedType, stake } = ACCAData;

    if (potentialPayout) {
      const accaStake = stake || this.accaBaseStake;
      const multiplier = stake ? 1 : this.accaBaseStake;
      const currencySymbol = this.user.currencySymbol;
      const payout = multiplier * potentialPayout;
      const stakePaysText = this.localeService.getString('bs.accaNotificationPays');

      this.accaPaysOfferText = `${ currencySymbol }${ accaStake } ${ stakePaysText } ${ currencySymbol }${ payout.toFixed(2) }`;

      if (translatedType.startsWith('AC')) {
        this.betType = `Acca (${translatedType.replace(/\D/g, '')})`;
      }
      this.changeDetectorRef.markForCheck();
    }
  }
}
