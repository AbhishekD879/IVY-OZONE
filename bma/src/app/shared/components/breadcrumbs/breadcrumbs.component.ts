import { Component, Input, Output, EventEmitter } from '@angular/core';
import { IGroupedSportEvent } from '@core/models/sport-event.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@Component({
  selector: 'breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss']
})
export class BreadcrumbsComponent {
  @Input() sportName: string;
  @Input() items: { name: string, targetUri: string }[];
  @Output() readonly navigationMenu: EventEmitter<void> = new EventEmitter();
  @Input() isExpanded: boolean;
  @Input() menuItems: IGroupedSportEvent[];
  @Input() defaultTab: string = '';

  constructor(private routingState: RoutingState) { }

  trackByBreadcrumb(breadCrumb): string {
    return breadCrumb.name;
  }

  lastItemClick(): void {
    if (this.menuItems && this.menuItems.length) {
      this.navigationMenu.emit();
    } else {
      return;
    }
  }
  /**
   * Validates the uri allows further routing
   * @returns void
   */
  navigateUri($event: MouseEvent, routeUrl: string): void {
    this.routingState.navigateUri($event, routeUrl, this.sportName, this.defaultTab);
  }
}
