import { Injectable } from '@angular/core';
import { StorageService } from '@app/core/services/storage/storage.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { Observable, Observer } from 'rxjs';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class RetailService {
  constructor(private storageService: StorageService,
              private nativeBridgeService: NativeBridgeService,
              private pubSubService: PubSubService,
              private deviceService: DeviceService,
              private router: Router) {}
  /**
   * Check if connect app was used previously.
   *
   * @returns {boolean}
   */
  checkRetail(): Observable<boolean> {
    const connectTracker: string = this.storageService.getCookie('CONNECT_TRACKER');
    const connectNotChecked: boolean = !!connectTracker ? connectTracker === 'false' : true;

    return Observable.create((observer: Observer<boolean>) => {
      if (connectNotChecked && this.deviceService.isWrapper) {
        this.pubSubService.subscribe('checkRetailNative', this.pubSubService.API.CHECK_RETAIL_NATIVE,
          (isRetail: boolean) => {
            observer.next(isRetail);
            observer.complete();
            this.pubSubService.unsubscribe('checkRetailNative');
          });

        this.nativeBridgeService.checkConnect();
      } else {
        observer.next(false);
        observer.complete();
      }
    });
  }

  /**
   * Check if grid app was used previously.
   * @returns {boolean}
   */
  checkGridRetail(): Observable<boolean> {
    const connectTracker: string = this.storageService.getCookie('grid');
    const connectNotChecked: boolean = !!connectTracker ? connectTracker === 'false' : true;
    return Observable.create((observer: Observer<boolean>) => {
      if (connectNotChecked && this.deviceService.isWrapper) {
        this.pubSubService.subscribe('checkRetailNative', this.pubSubService.API.CHECK_RETAIL_NATIVE,
          (isRetail: boolean) => {
            observer.next(isRetail);
            observer.complete();
            this.pubSubService.unsubscribe('checkRetailNative');
          });
        this.nativeBridgeService.checkGrid();
      } else {
        observer.next(false);
        observer.complete();
      }
    });
  }

  subscribe(): void {
    this.pubSubService.subscribe('retailThirdPartyRedirection', this.pubSubService.API.REDIRECT_TO_URL, (url: string) => {
      this.router.navigateByUrl(url);
    });
  }
}
