import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Location } from '@angular/common';
import { StorageService } from '@core/services/storage/storage.service';
import { Router } from '@angular/router';
import { RetailService } from '@app/retail/services/retail/retail.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';

@Component({
  selector: 'retail-overlay',
  templateUrl: 'retail-overlay.component.html',
  styleUrls: ['retail-overlay.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RetailOverlayComponent implements OnInit {
  isVisible: boolean = false;

  constructor(protected location: Location,
    protected storage: StorageService,
    protected retailService: RetailService,
    protected nativeBridgeService: NativeBridgeService,
    protected router: Router,
    protected changeDetectorRef: ChangeDetectorRef) { }

  ngOnInit(): void {
    const isHomeURL = this.location.path() === '' || this.location.path().indexOf('home') > -1;
    let showCount: number = this.storage.get('retailOverlayRemain');

    if (isHomeURL) {
      if (!showCount && showCount !== 0 && showCount === null) {
        this.retailService.checkRetail().subscribe((isRetail: boolean) => {
          if (isRetail) {
            showCount = 3;
            this.showOverlay();
          } else {
            showCount = 0;
          }
          this.storage.set('retailOverlayRemain', showCount);
          this.storage.setCookie('CONNECT_TRACKER', 'true', '.coral.co.uk', 183);
        });
      } else if (showCount > 0) {
        this.showOverlay();
        showCount--;
        this.storage.set('retailOverlayRemain', showCount);
      } else {
        this.isVisible = false;
      }
    }
  }

  /**
   * Show connect overlay
   *
   * @memberof RetailOverlayComponent
   */
  showOverlay(): void {
    this.isVisible = true;
    this.changeDetectorRef.markForCheck();
    this.nativeBridgeService.onOpenPopup('retail_overlay');
  }

  /**
   * Hide connect overlay
   *
   * @param {boolean} resetCount
   * @memberof RetailOverlayComponent
   */
  hideOverlay(resetCount: boolean = false): void {
    this.nativeBridgeService.onClosePopup('retail_overlay', {});
    this.isVisible = false;
    if (resetCount) {
      this.storage.set('retailOverlayRemain', 0);
    }
  }

  /**
   * navigate to connect page
   *
   * @memberof RetailOverlayComponent
   */
  navigateToRetail(): void {
    this.hideOverlay(false);
    this.router.navigate(['/retail']);
  }
}

