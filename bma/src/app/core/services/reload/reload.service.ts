import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { DeviceService } from '../device/device.service';
import { InfoDialogService } from '@coreModule/services/infoDialogService/info-dialog.service';
import { WindowRefService } from '../windowRef/window-ref.service';
import { NETWORK_CONSTANTS } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
import { StorageService } from '@core/services/storage/storage.service';

@Injectable()
export class ReloadService {

  private connectionLostTimeout;
  private connectionLost: boolean = false;

  private readonly TIME_TO_WAIT: number = 10000;
  private readonly CHECK_CONNECTION_INTERVAL = 30000;

  constructor(
    private device: DeviceService,
    private windowRef: WindowRefService,
    private pubsub: PubSubService,
    private infoDialogService: InfoDialogService,
    private storageService: StorageService
    ) {
    this.init();
  }

  reload(): void {
    if (this.connectionLost || !this.windowRef.nativeWindow.navigator.onLine) {
      console.warn('reload components failed, no internet connection');
      return;
    }

    setTimeout(() => {
      // eslint-disable-next-line no-console
      console.info(`reload components ${+(+new Date())}`);
      this.pubsub.publish(this.pubsub.API.RELOAD_COMPONENTS);
    }, 1000);
  }

  private init(): void {
    const isOldSamsung: boolean = this.isOldSamsung();

    if (this.windowRef.nativeWindow.addEventListener && !isOldSamsung) {
      this.windowRef.nativeWindow.addEventListener('offline', () => {
        this.connectionLostLogic();
        this.pubsub.publish(NETWORK_CONSTANTS.NW_I_STATUS_RELOAD, 'offline');
      });

      this.windowRef.nativeWindow.addEventListener('online', () => {
        this.connectionLost = false;
        this.infoDialogService.closeConnectionLostPopup();
        this.reload();
        this.pubsub.publish(NETWORK_CONSTANTS.NW_I_STATUS_RELOAD, 'online');
      });
    }

    this.windowRef.nativeWindow.setInterval(() => {
      this.connectionLostLogic();
    }, this.CHECK_CONNECTION_INTERVAL);
  }

  private connectionLostLogic(): void {
    if (this.connectionLostTimeout) {
      clearTimeout(this.connectionLostTimeout);
    }

    this.connectionLostTimeout = setTimeout(() => {
      if (!this.device.isOnline() && this.windowRef.nativeWindow.location.href.indexOf('/under-maintenance') !== 0) {
        this.connectionLost = true;
        this.openConnectionLostPopupForDesktop();
      }
    }, this.TIME_TO_WAIT);
  }

  private openConnectionLostPopupForDesktop(): void {
    const networkIndicatorEnabled = this.storageService.get(NETWORK_CONSTANTS.NETWORK_STORAGE_KEY);
    if (!networkIndicatorEnabled || this.device.isDesktop) {
      this.infoDialogService.openConnectionLostPopup();
    }
  }

  private isOldSamsung(): boolean {
    return this.device.isNativeAndroid && this.device.osVersion < '6.0.0' &&
      _.intersection(this.device.deviceType.split(' '), ['Samsung', 'S4', 'S5']).length > 1;
  }
}
