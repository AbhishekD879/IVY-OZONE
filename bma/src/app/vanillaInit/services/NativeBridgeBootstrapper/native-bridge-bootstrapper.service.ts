import { Injectable } from '@angular/core';
import { Router, NavigationEnd, Event } from '@angular/router';
import { filter, first } from 'rxjs/operators';
import { NativeBridgeAdapter } from '../NativeBridgeAdapter/nativebridge.adapter';
import { PortalNativeEventNotifier } from '../PortalNativeEventNotifier/portal-nativeEvent-notifier';
import { NativeAppService } from '@frontend/vanilla/core';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';

@Injectable()
export class NativeBridgeBootstrapperService {

  constructor(
    private bridge: NativeBridgeService,
    private nativeBridgeAdapter: NativeBridgeAdapter,
    private portalNativeEventNotifier: PortalNativeEventNotifier,
    private vanillaNativeAppService: NativeAppService,
    private router: Router
  ) { }

  init(): void {
    this.portalNativeEventNotifier.attachNativeMessageNotifier();
    this.nativeBridgeAdapter.attachNativeMessageReceiver();

    if (this.vanillaNativeAppService.isNativeWrapper) {
      this.router.events.pipe(
          filter(((e: Event) => e instanceof NavigationEnd)),
          first()
      ).subscribe((e: Event) => {
          this.vanillaNativeAppService.sendToNative({ eventName: 'AFTER_INITIAL_NAVIGATION' });

          // TODO: check with with BMA-47851
          this.bridge.onCookieBannerClosed();
      });
    }
  }

}
