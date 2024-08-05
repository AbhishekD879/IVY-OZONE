import { Component, ElementRef } from '@angular/core';

import { Router } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { DesktopVirtualCarouselMenuComponent } from '@coralDesktop/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';

@Component({
  selector: 'virtual-carousel-sub-menu',
  templateUrl: './virtual-carousel-sub-menu.component.html',
  styleUrls: ['../../../../../app/vsbr/components/virtualCarouselSubMenu/virtual-carousel-sub-menu.component.scss']
})
export class DesktopVirtualCarouselSubMenuComponent extends DesktopVirtualCarouselMenuComponent {

  constructor(
    public elementRef: ElementRef,
    public locale: LocaleService,
    public router: Router,
    public gtmTrackingService: GtmTrackingService,
    public casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    public navigationService: NavigationService,
    public domToolsService: DomToolsService,
  ) {
    super(elementRef, locale, router, gtmTrackingService, casinoMyBetsIntegratedService, navigationService, domToolsService);
  }
}
