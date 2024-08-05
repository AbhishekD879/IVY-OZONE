import { Component, Input } from '@angular/core';
import { IVirtualSportsMenuItem } from '@app/vsbr/models/menu-item.model';
import { NavigationService } from '@core/services/navigation/navigation.service';

@Component({
  selector: 'virtual-carousel-menu',
  templateUrl: 'virtual-carousel-menu.component.html',
  styleUrls: ['./virtual-carousel-menu.component.scss']
})
export class VirtualCarouselMenuComponent {
  @Input() activeMenuItemUri: string;

  menuItem: IVirtualSportsMenuItem;
  elementsInMenu: Array<IVirtualSportsMenuItem>;
  @Input() set menuElements(menuElements: Array<IVirtualSportsMenuItem>) {
    this.elementsInMenu = menuElements;
  }

  constructor(
    private navigationService: NavigationService
  ) {}

  goToVirtual(item: IVirtualSportsMenuItem, isSubItem?: boolean): void {
    const url = isSubItem ? item.targetUri : item.childMenuItems[0].targetUri;
    this.navigationService.openUrl(url, item.inApp, true);
  }

  trackByMenu(index: number, item: IVirtualSportsMenuItem): string {
    return `${index}${item.name}`;
  }
}
