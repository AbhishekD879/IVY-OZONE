import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

import { SportMainComponent as CoralSportMainComponent } from '@app/sb/components/sportMain/sport-main.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { TimeService } from '@core/services/time/time.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { DeviceService } from '@core/services/device/device.service';
import { GermanSupportService } from '@core/services/germanSupport/german-support.service';
import { ISportConfigTab } from '@app/core/services/cms/models';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { SlpSpinnerStateService } from '@core/services/slpSpinnerState/slpSpinnerState.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'sport-main-component',
  styleUrls: ['sport-main.component.scss'],
  templateUrl: 'sport-main.component.html'
})

export class SportMainComponent extends CoralSportMainComponent implements OnInit { // TODO extend ladbrokesMobile instead!
  constructor(
    protected cmsService: CmsService,
    protected timeService: TimeService,
    protected sportsConfigService: SportsConfigService,
    protected routingState: RoutingState,
    protected pubSubService: PubSubService,
    protected location: Location,
    protected Storage: StorageService,
    public User: UserService,
    protected router: Router,
    protected route: ActivatedRoute,
    protected device: DeviceService,
    protected germanSupportService: GermanSupportService,
    protected sportTabsService: SportTabsService,
    protected coreToolsService: CoreToolsService,
    protected slpSpinnerStateService: SlpSpinnerStateService,
    protected navigationService: NavigationService,
    protected freeRideHelperService: FreeRideHelperService,
    protected windowRefService: WindowRefService,
    protected dialogService: DialogService,
    protected gtmService:GtmService,
    protected bonusSuppressionService: BonusSuppressionService) {
    super(
      cmsService,
      timeService,
      sportsConfigService,
      routingState,
      pubSubService,
      location,
      Storage,
      User,
      router,
      route,
      device,
      sportTabsService,
      coreToolsService,
      slpSpinnerStateService,
      navigationService,
      windowRefService,
      dialogService,
      gtmService);
  }

  get sportDetailPage(): string {
    return this.isSportDetailPage ? 'eventDetailsPage' : '';
  }
  set sportDetailPage(value:string){}

  ngOnInit(): void {
    super.ngOnInit();

    // eslint-disable-next-line
    this.pubSubService.subscribe(this.channelName, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
      this.sportTabs = this.filterTabs(this.sportTabs);
    });
  }

  protected shouldNavigatedToTab() {
    return this.isHomeUrl();
  }

  protected setDefaultTab(sportTabs: ISportConfigTab[]): void{
    const matchesTab: ISportConfigTab = sportTabs.find((tab: ISportConfigTab) => tab.name === 'matches' && !tab.hidden);
    if (matchesTab) {
      this.defaultTab = matchesTab.name;
    } else {
      const firstTab = sportTabs.find((tab: ISportConfigTab) => !tab.hidden);
      this.defaultTab = firstTab && firstTab.name;
    }
  }

  protected filterTabs(sportTabs: ISportConfigTab[]): ISportConfigTab[] {
    // if(this.sportId!=='18'){
    sportTabs.forEach((tab: ISportConfigTab, index: number) => {
      if (this.sportName === 'football' && this.germanSupportService.isGermanUser() && tab.id === 'tab-jackpot') {
        tab.hidden = true;
      }

      if ((tab.id === 'tab-matches' || tab.id === 'tab-live') && this.sportId !== '18') {
        tab.hidden = false;
      }

      if(tab.id === 'tab-matches') {
        tab.url = `/sport/${this.sportPath}/matches/today`
      }
      // this.defaultTab = 'matches';
      // const firstTab = sportTabs.find((tab: ISportConfigTab) => !tab.hidden);
      // this.defaultTab = firstTab && firstTab.name;
    });
    this.setDefaultTab(sportTabs);

  if(this.sportId!=='18'){
    if (!sportTabs.find(sportTab => sportTab.id === 'tab-live')) {
      sportTabs.unshift({
        id: 'tab-live',
        name: 'live',
        label: 'sb.tabsNameInPlay',
        url: `/sport/${this.sportPath}/live`,
        hidden: false,
        sortOrder: 1
      });
    }
  }

    return sportTabs;
  }
}
