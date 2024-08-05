import {  OnInit, Input, OnDestroy, AfterViewInit, ChangeDetectorRef, Component, ElementRef, NgZone, ViewChild } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SHOP_LOCATOR_PARAMS, GRID_GA_TRACKING } from '@app/retail/constants/retail.constant';

@Component({
  selector: 'shop-locator',
  templateUrl: 'shop-locator.component.html'
})
export class ShopLocatorComponent implements OnInit, OnDestroy, AfterViewInit {
  trackStatus: boolean = false;
  readonly title: string = 'Shop Locator';
  readonly shopLocatorUrl: SafeResourceUrl;
  @Input() trackingLocation: string;
  @ViewChild('shopLocator', {static: false}) private shopLocatorView: ElementRef;
  private timeInterval: number;
  private readonly intervalTime: number = 1000;

  constructor(
    private rendererService: RendererService,
    private domSanitizer: DomSanitizer,
    private zone: NgZone,
    private changeDetector: ChangeDetectorRef,
    private windowRef: WindowRefService,
    private domTools: DomToolsService,
    private gtmService: GtmService
  ) {
    this.shopLocatorUrl = this.domSanitizer.bypassSecurityTrustResourceUrl(
      environment.SHOP_LOCATOR_ENDPOINT
    );
    setTimeout(() => {
      this.zone.run(() => {
        this.changeDetector.detectChanges();
      });
    });
  }

  ngOnInit(): void {
    if (this.gtmService.shopLocatorTrack && this.windowRef.nativeWindow.localStorage.getItem('locationPermission') !== '0') {
      this.timeInterval = this.windowRef.nativeWindow.setInterval(() => {
        this.windowRef.nativeWindow.navigator.geolocation.getCurrentPosition(position => {
          this.trackShopLocatorPermissions(SHOP_LOCATOR_PARAMS.ALLOW);
        }, error => {
          this.trackShopLocatorPermissions(SHOP_LOCATOR_PARAMS.DENY);
        });
      }, this.intervalTime);
    }
  }

  /**
   * Setting value based on the user permission for location
   * @param permission {string}
   * @return {void}
   */
  trackShopLocatorPermissions(permission: string): void {
    if(!this.trackStatus) {
      this.trackStatus = true;
      this.windowRef.nativeWindow.localStorage.setItem(SHOP_LOCATOR_PARAMS.SHOP_LOCATION_LOCATION, '0');
      GRID_GA_TRACKING.eventLabel = permission;
      GRID_GA_TRACKING.eventAction = SHOP_LOCATOR_PARAMS.SHOP_LOCATION_POPUP;
      this.gtmService.push('trackEvent', GRID_GA_TRACKING);
    }
  }

  ngOnDestroy(): void {
    this.windowRef.nativeWindow.clearInterval(this.timeInterval);
  }

  ngAfterViewInit(): void {
    this.windowRef.nativeWindow.setTimeout(() => this.setShopLocatorHeight(), 500);
  }

  private setShopLocatorHeight(): void {
    this.rendererService.renderer.setStyle(
      this.shopLocatorView.nativeElement,
      'min-height',
      `${this.calcFreeHeight()}px`
    );
  }

  private calcFreeHeight(): number {
    const windowHeight: number = this.windowRef.nativeWindow.innerHeight,
      headerViewHeight: number = this.domTools.HeaderEl.offsetHeight,
      footerMenuHeight: number = this.domTools.FooterEl ? this.domTools.FooterEl.offsetHeight : 0,
      contentTop: number = this.shopLocatorView.nativeElement.offsetTop;

    return windowHeight - footerMenuHeight - headerViewHeight - contentTop;
  }
}
