import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { AbstractDialogComponent } from '@app/shared/components/oxygenDialogs/abstract-dialog';

import { DeviceService } from '@app/core/services/device/device.service';
import { StorageService } from '@app/core/services/storage/storage.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

import { IFanzonePreferences } from '@app/fanzone/models/fanzone-preferences.model';
import { gtmTackingKeys } from '@app/fanzone/constants/fanzonePreferenceConstants';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneSharedService } from '../../services/fanzone-shared.service';
import { SHOW_YOUR_COLORS } from '@app/fanzone/constants/fanzoneconstants';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'fanzone-preference-dialog',
  templateUrl: './fanzone-preference-dialog.component.html',
  styleUrls: ['./fanzone-preference-dialog.component.scss']
})
export class FanzonePreferenceDialogComponent extends AbstractDialogComponent{

  @ViewChild('fanzonePreferenceDialog', { static: true }) dialog;
  params: IFanzonePreferences;
  constructor(
    protected device: DeviceService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected router: Router,
    protected storageService: StorageService,
    protected windowRef: WindowRefService,
    protected pubsub: PubSubService,
    protected routingState: RoutingState
  ) { 
    super(device, windowRef);
  }

  /**
   * Method on open of preference dialog
   * returns {void}
   */
  open(): void {
    this.params = { ...this.params };
    if (this.params) {
      super.open();
    }
  }

  /**
   * Method on click of confirm user preference
   * returns {void}
   */
  savePreferences() {
    const bridge = this.windowRef.nativeWindow.NativeBridge;
    this.fanzoneSharedService.pushCachedEvents(this.params.optInCTA, '', gtmTackingKeys.show_your_colors);
    bridge.showNotificationSettings();
    super.closeDialog();
  }
 

  /**
   * Method on click of exit preference dialog
   * returns {void}
   */
  exitDialog() {
    this.pubsub.publish(this.pubsub.API.FANZONE_NO_THANKS);
    this.fanzoneSharedService.pushCachedEvents(this.params.noThanksCTA, '', gtmTackingKeys.show_your_colors);
    const route = this.routingState && this.routingState.getPreviousUrl().includes(SHOW_YOUR_COLORS.SHOW_YOUR_COLORS);
    route && this.router.navigate([`${SHOW_YOUR_COLORS.FOOTBALL_LANDING_PAGE_PATH}`]);
    super.closeDialog();
  }
}
