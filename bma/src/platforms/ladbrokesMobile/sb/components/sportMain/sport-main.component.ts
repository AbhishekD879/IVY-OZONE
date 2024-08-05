import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

import { SportMainComponent as CoralSportMainComponent } from '@sb/components/sportMain/sport-main.component';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { TimeService } from '@core/services/time/time.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
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
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'sport-main-component',
  templateUrl: './sport-main.component.html'
})
export class SportMainComponent extends CoralSportMainComponent implements OnInit {
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
    protected freeRideHelperService: FreeRideHelperService,
    protected navigationService: NavigationService,
    protected windowRefService: WindowRefService,
    protected dialogService: DialogService,
    protected gtmService:GtmService,
    private bonusSuppressionService: BonusSuppressionService) {
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

  ngOnInit(): void {
    super.ngOnInit();

    /* eslint-disable-next-line:pubsub-connect */
    this.pubSubService.subscribe(this.channelName, [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGIN], () => {
      this.sportTabs = this.filterTabs(this.sportTabs);
    });
  }

  protected filterTabs(sportTabs: ISportConfigTab[]): ISportConfigTab[] {
    sportTabs = super.filterTabs(sportTabs);

    sportTabs.forEach((tab: ISportConfigTab, index: number) => {
      if (this.sportName === 'football' && this.germanSupportService.isGermanUser() && tab.id === 'tab-jackpot') {
        tab.hidden = true;
      }
    });

    return sportTabs;
  }
}
