import { Component } from '@angular/core';

import { DeviceService } from '@core/services/device/device.service';
import { OddsBoostInfoDialogComponent } from '@shared/components/oddsBoostInfoDialog/odds-boost-info-dialog.component';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { UserService } from '@app/core/services/user/user.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';

@Component({
  selector: 'odds-boost-info-dialog',
  templateUrl: './odds-boost-info-dialog.component.html',
  styleUrls: ['./odds-boost-info-dialog.component.scss']
})
export class DesktopOddsBoostInfoDialogComponent extends OddsBoostInfoDialogComponent {

  constructor(
    device: DeviceService,
    localeService: LocaleService,
    windowRef: WindowRefService,
    storageService: StorageService,
    userService: UserService,
    ezNavVanillaService: EzNavVanillaService
  ) {
    super(
      device,
      localeService,
      windowRef,
      storageService,
      userService,
      ezNavVanillaService
    );
  }

}
