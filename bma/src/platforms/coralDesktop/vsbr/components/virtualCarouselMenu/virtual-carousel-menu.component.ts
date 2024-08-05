import { Component, Input, ElementRef } from '@angular/core';

import { Router } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DomToolsService } from '@core/services/domTools/dom.tools.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';
import { TabsPanelComponent } from '@coralDesktop/shared/components/tabsPanel/tabs-panel.component';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';

@Component({
  selector: 'virtual-carousel-menu',
  templateUrl: './virtual-carousel-menu.component.html',
  styleUrls: ['../../../../../app/vsbr/components/virtualCarouselMenu/virtual-carousel-menu.component.scss']
})
export class DesktopVirtualCarouselMenuComponent extends TabsPanelComponent {
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
    public gtmTrackingService: GtmTrackingService,
    public casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    public navigationService: NavigationService,
    public domToolsService: DomToolsService,
  ) {
    super(elementRef, locale, router, gtmTrackingService, casinoMyBetsIntegratedService, navigationService, domToolsService) /* istanbul ignore next */;
  }

  goToVirtual(item: IVirtualSportsMenuItem, isSubItem?: boolean): void {
    const url = isSubItem ? item.targetUri : item.childMenuItems[0].targetUri;

    this.navigationService.openUrl(url, item.inApp, true);
  }

  trackByMenu(index: number, item: IVirtualSportsMenuItem): string {
    return `${index}${item.name}`;
  }
}
