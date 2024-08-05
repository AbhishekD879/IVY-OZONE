import { Component, ViewChild } from '@angular/core';

import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { DeviceService } from '@core/services/device/device.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FormControl } from '@angular/forms';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { EzNavVanillaService } from '@app/core/services/ezNavVanilla/eznav-vanilla.service';

@Component({
  selector: 'odds-boost-info-dialog',
  templateUrl: './odds-boost-info-dialog.component.html',
  styleUrls: ['./odds-boost-info-dialog.component.scss']
})
export class OddsBoostInfoDialogComponent extends AbstractDialogComponent {
  @ViewChild('oddsBoostDialog', { static: true }) dialog;

  tokens: IFreebetToken[];
  avaiLableBoostsText: string;
  showToggle: boolean;
  isMyBetsInCasino: boolean = false;
  dontShowPopupAgain: FormControl;

  constructor(
    device: DeviceService,
    private localeService: LocaleService,
    windowRef: WindowRefService,
    private storageService: StorageService,
    private userService: UserService,
    private ezNavVanillaService: EzNavVanillaService
  ) {
    super(device, windowRef);
    this.showToggle = false;
    this.dontShowPopupAgain = new FormControl(false);
    
    this.isMyBetsInCasino = this.ezNavVanillaService.isMyBetsInCasino;
  }

  open(): void {
    !this.isMyBetsInCasino && super.open();
    this.tokens = this.params.oddsBoostTokens;
    this.showToggle = this.params.oddsBoostConfig.allowUserToToggleVisibility;
    this.setText();
  }

  closeDialog(): void {
    const storageKey = 'keepOddsBoostPopupHidden';
    const data = this.storageService.get(storageKey) || {};
    const userKey = `setDate-${this.userService.username}`;
    if (this.dontShowPopupAgain.value) {
      data[userKey] = new Date(Date.now());
      this.storageService.set(storageKey, data);
    } else {
      delete data[userKey];
      this.storageService.set(storageKey, data);
    }
    super.closeDialog();
  }

  private setText(): void {
    const boostPlural = this.tokens && this.tokens.length === 1 ? this.localeService.getString('oddsboost.tokensInfoDialog.boost') :
      this.localeService.getString('oddsboost.tokensInfoDialog.boosts');

    this.avaiLableBoostsText = this.localeService.getString('oddsboost.tokensInfoDialog.available2', [boostPlural]);
  }
}
