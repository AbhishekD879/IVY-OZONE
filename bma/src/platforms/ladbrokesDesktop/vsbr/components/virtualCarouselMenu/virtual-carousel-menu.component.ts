import { Component, Input, ElementRef } from '@angular/core';

import { DesktopTabsPanelComponent } from '@ladbrokesDesktop/shared/components/tabsPanel/tabs-panel.component';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';
import { Router } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';

@Component({
  selector: 'virtual-carousel-menu',
  templateUrl: './virtual-carousel-menu.component.html',
  styleUrls: ['./virtual-carousel-menu.component.scss']
})
export class VirtualCarouselMenuComponent extends DesktopTabsPanelComponent {
  @Input() activeMenuItemUri: string;

  menuItem: IVirtualSportsMenuItem;
  elementsInMenu: Array<IVirtualSportsMenuItem>;
  @Input() set menuElements(menuElements: Array<IVirtualSportsMenuItem>) {
    this.elementsInMenu = menuElements;
  }

  constructor(
    public elementRef: ElementRef,
    public locale: LocaleService,
    public router: Router,
    public navigationService: NavigationService,
    public domToolsService: DomToolsService,
    public casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    public gtmTrackingService: GtmTrackingService,
  ) {
    super(elementRef, locale, router, navigationService, casinoMyBetsIntegratedService, domToolsService, gtmTrackingService) /* istanbul ignore next */;
  }

  goToVirtual(item: IVirtualSportsMenuItem, isSubItem?: boolean): void {
    const url = isSubItem ? item.targetUri : item.childMenuItems[0].targetUri;

    this.navigationService.openUrl(url, item.inApp, true);
  }

  trackByMenu(index: number, item: IVirtualSportsMenuItem): string {
    return `${index}${item.name}`;
  }
}
