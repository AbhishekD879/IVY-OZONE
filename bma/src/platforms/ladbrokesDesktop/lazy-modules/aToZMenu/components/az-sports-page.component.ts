import { map } from 'rxjs/operators';
import { Component, OnInit, OnDestroy,Input } from '@angular/core';

import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { AzSportsPageComponent } from '@app/lazy-modules/aToZMenu/components/AzSportsPageComponent/az-sports-page.component';
import { IVerticalMenu } from '@app/core/services/cms/models';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneDetails } from '@app/fanzone/models/fanzone.model';
import { FANZONE_CATEGORY_ID } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { UserService } from '@app/core/services/user/user.service';

interface IAZData {
  azItems: IVerticalMenu[];
  topItems: IVerticalMenu[];
}

@Component({
  selector: 'az-sports-page',
  templateUrl: './az-sports-page.component.html',
  styleUrls: ['./az-sports-page.component.scss']
})
export class LadbrokesAzSportsPageComponent extends AzSportsPageComponent implements OnInit, OnDestroy {
 //Property added to fix strict mode issue fix
  @Input() disableDefaultNavigation: boolean;
  constructor(
    protected moduleExtensionsStorageService: ModuleExtensionsStorageService,
    protected cmsService: CmsService,
    protected casinoLinkService: CasinoLinkService,
    private germanSupportService: GermanSupportService,
    private pubSubService: PubSubService,
    public fanzoneStorageService: FanzoneStorageService,
    protected user : UserService,
    protected filtersService: FiltersService,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    super(moduleExtensionsStorageService, cmsService, casinoLinkService, filtersService, bonusSuppressionService);
  }
  ngOnInit(): void {
    this.loadAzData();
    this.pubSubService.subscribe('LadbrokesAzSportsPageComponent',
      [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT, this.pubSubService.API.FANZONE_DATA], () => {
        this.loadAzData();
      }
    );
  }

  loadAzData(): void {
    this.cmsService.getMenuItems().pipe(
      map(this.processMenu))
      .subscribe((data: IAZData) => {
        const updatedMenu = this.updateFanzoneMenu(data.topItems,data.azItems);
        data.azItems = updatedMenu.azItemsData;
        data.topItems = updatedMenu.topItemsData;

        this.topItems = data.topItems.length ? this.filterRestrictedSports(data.topItems) : null;
        this.azItems = data.azItems.length ? this.filterRestrictedSports(data.azItems) : null;
      });
  }

  filterRestrictedSports(items: IVerticalMenu[]): IVerticalMenu[] {
    return this.germanSupportService.toggleItemsList(items, 'filterRestrictedSports');
  }

  public updateFanzoneMenu(topItems, azItems) {
    let fanzone: FanzoneDetails;
    let topItemsData = JSON.parse(JSON.stringify(topItems));
    let azItemsData = JSON.parse(JSON.stringify(azItems));
    const topIndex = topItems.findIndex(link => link.categoryId === FANZONE_CATEGORY_ID);
    const azIndex = azItems.findIndex(link => link.categoryId === FANZONE_CATEGORY_ID);
    const fanzoneStorage = this.fanzoneStorageService.get('fanzone');
    if (topIndex !== -1) {
      fanzone = topItemsData[topIndex].selectedFanzone;       
      if (fanzoneStorage && fanzoneStorage.teamId && fanzone && fanzone.active && fanzone.fanzoneConfiguration.atozMenu) {
        topItemsData[topIndex].disabled = false;
      } else {
        topItemsData[topIndex].disabled = true;
        topItemsData[topIndex].fzDisabled = true;
      }
    }
    if (azIndex !== -1) {
      fanzone = azItemsData[azIndex].selectedFanzone;       
      if (fanzoneStorage && fanzoneStorage.teamId && fanzone && fanzone.active && fanzone.fanzoneConfiguration.atozMenu) {
        azItemsData[azIndex].disabled = false;
      } else {
        azItemsData[azIndex].disabled = true;
        azItemsData[azIndex].fzDisabled = true;
      }
    }
    topItemsData = topItemsData.filter(topItem => topItem.disabled === false && topItem.hasEvents);
    azItemsData = azItemsData.filter(azItem => azItem.disabled === false && azItem.hasEvents);

    return {
      topItemsData,
      azItemsData
    };
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('LadbrokesAzSportsPageComponent');
   }
}
