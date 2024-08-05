import { Component, Input, Output, EventEmitter, OnInit, ViewEncapsulation } from '@angular/core';
import * as _ from 'underscore';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { IOddsBoostConfig, IVerticalMenu } from '@app/core/services/cms/models';
import { IMenuActionResult } from '@app/core/services/cms/models/menu/menu-action.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ODDS_BOOST_URL } from '@oddsBoost/constants/odds-boost.constant';
@Component({
  selector: 'vertical-menu',
  templateUrl: 'vertical-menu.component.html',
  styleUrls: ['vertical-menu.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class VerticalMenuComponent implements OnInit {
  @Input() menuItems: IVerticalMenu[];
  @Input() header: string;
  @Input() showHeader: boolean = false;
  @Input() showRetailHeader: boolean;
  @Input() showDescription: boolean = false;
  @Input() disableDefaultNavigation: boolean = false;
  @Input() gtmDimension?: string;
  @Output() readonly itemClickFn: EventEmitter<IVerticalMenu> = new EventEmitter<IVerticalMenu>();
  @Output() readonly itemClickFnGrid: EventEmitter<IVerticalMenu> = new EventEmitter<IVerticalMenu>();

  private oddsBoostEnabled: boolean;

  constructor(
    private navigationService: NavigationService,
    private cmsService: CmsService
  ) { }

  ngOnInit(): void {
    this.cmsService.getOddsBoost().subscribe((config: IOddsBoostConfig) => {
      this.oddsBoostEnabled = config && config.enabled;
    });
  }

  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Menu item click handler
   *
   * @param  {IVerticalMenu} menuItem
   * @returns void
   */
  /**
   * Menu item click handler
   *
   * @param  {IVerticalMenu} menuItem
   * @returns void
   */
  menuItemClick(menuItem: IVerticalMenu): void {
    if (menuItem.action && _.isFunction(menuItem.action)) {
      menuItem.action().subscribe((actionResult: IMenuActionResult) => {
        if (actionResult && !actionResult.cancelled) {
          this.doMenuRouting({ ...menuItem, targetUri: actionResult.redirectUri || menuItem.targetUri });
        }
      });
    } else {
      this.doMenuRouting(menuItem);
    }
  }

  showOddsBoostCount(targetUri: string): boolean {
    return this.oddsBoostEnabled && targetUri.indexOf(ODDS_BOOST_URL) > -1;
  }

  private doMenuRouting(menuItem: IVerticalMenu): void {
    if (this.disableDefaultNavigation) {
      this.itemClickFnGrid.emit(menuItem);
    } else if (menuItem.type !== 'button') {
      this.navigationService.openUrl(menuItem.targetUri, menuItem.inApp,false,menuItem,this.header);
    }
  }
}
