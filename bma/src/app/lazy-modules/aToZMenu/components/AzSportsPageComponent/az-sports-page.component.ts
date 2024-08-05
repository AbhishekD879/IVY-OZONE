
import { map } from 'rxjs/operators';
import * as _ from 'underscore';
import { Component, OnInit } from '@angular/core';

import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { ISportCategory } from '@core/services/cms/models/sport-category.model';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IVerticalMenu } from '@core/services/cms/models';
import { AZ_SPORTS_PAGE } from './az-sports-page.constant';
import { RETAIL_MENU_CONFIG } from '@platform/retail/constants/retail.config';
import { FANZONE_CATEGORY_ID } from '@app/fanzone/constants/fanzoneconstants';
import { FiltersService } from '@core/services/filters/filters.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

interface IAZData {
  azItems: IVerticalMenu[];
  topItems: IVerticalMenu[];
}

@Component({
  selector: 'az-sports-page',
  templateUrl: './az-sports-page.component.html',
  styleUrls: ['./az-sports-page.component.scss']
})
export class AzSportsPageComponent implements OnInit {
  readonly CONST = AZ_SPORTS_PAGE;

  azItems: IVerticalMenu[];
  topItems: IVerticalMenu[];
  showRetailMenu: boolean = false;

  constructor(
    protected moduleExtensionsStorageService: ModuleExtensionsStorageService,
    protected cmsService: CmsService,
    protected casinoLinkService: CasinoLinkService,
    protected filtersService: FiltersService,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    this.processMenu = this.processMenu.bind(this);
  }

  ngOnInit(): void {
    this.showRetailMenu = RETAIL_MENU_CONFIG.includes('AZ');
    this.cmsService.getMenuItems().pipe(
      map(this.processMenu))
      .subscribe((data: IAZData) => {
        this.topItems = data.topItems.length ? data.topItems : null;
        this.azItems = data.azItems.length ? data.azItems : null;
      });
  }

  processMenu(menuList: ISportCategory[]): IAZData {
    const extensionMenuItems = this.moduleExtensionsStorageService.getList()
      .filter(ext => ext.extendsModule === 'sb' && ext.menuConfig)
      .map(ext => ext.menuConfig as ISportCategory[]);

    if (extensionMenuItems.length) {
      menuList = _.uniq(menuList.concat(extensionMenuItems[0]), 'imageTitle');
    }

    this.casinoLinkService.decorateCasinoLink(menuList);

    let menuItems = menuList.map((item: ISportCategory) => {
      const menuItem: Partial<ISportCategory & IVerticalMenu> = item;
      menuItem.title = item.imageTitle;
      menuItem.svgId = item.svgId || 'icon-generic';
      if(menuItem.targetUri.includes('racingsuperseries')){
        this.filtersService.filterLinkforRSS(menuItem.targetUri).subscribe(data =>{
          menuItem.targetUri = data;
        })
       }
      return menuItem as IVerticalMenu;
    });
    const index = menuItems.findIndex(menuItem => menuItem.categoryId === FANZONE_CATEGORY_ID);
    if(index !== -1) {
      menuItems[index].disabled = false;
      menuItems[index].fzDisabled = false;
    }
    
    menuItems = _.where(menuItems, { disabled: false, hasEvents: true });

    menuItems =  menuItems.filter((item) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(item.title);
    });

    const topItems = _.where(menuItems, { isTopSport: true });
    topItems.sort((a, b) => { return a.sortOrder - b.sortOrder });
    let azItems = _.where(menuItems, { showInAZ: true });
    azItems = _.sortBy(azItems, 'title');

    return {
      topItems,
      azItems
    };
  }
}
