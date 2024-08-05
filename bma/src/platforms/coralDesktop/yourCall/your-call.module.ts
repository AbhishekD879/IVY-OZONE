import { FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { DesktopModule } from '@desktopModule/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';
import { YourCallTabDialogComponent } from '@yourcall/components/yourCallTabDialog/your-call-tab-dialog.component';
import { YourCallMarketComponent } from '@yourcall/components/yourCallMarket/your-call-market.component';
import { YourCallMarketGroupComponent } from '@yourcall/components/yourCallMarketGroup/your-call-market-group.component';

import { YourCallMarketPlayerBetsComponent } from '@yourcall/components/yourCallMarketPlayerBets/your-call-market-player-bets.component';
import { YourCallCorrectScoreComponent } from '@yourcall/components/yourCallCorrectScore/your-call-correct-score.component';
import { YourCallMarketSwitcherComponent } from '@yourcall/components/yourCallMarketSwitcher/your-call-market-switcher.component';
import { BybHomeService } from '@yourcall/components/bybHome/byb-home.service';
import { BybHelperService } from '@yourcall/services/BYB/byb-helper.service';
import { BybApiService } from '@yourcall/services/BYB/byb-api.service';
import { YourcallValidationService } from '@yourcall/services/yourcallValidation/yourcall-validation-service';
import { YourcallStoredBetsService } from '@yourcall/services/yourCallStoredBets/yourcall-stored-bets.service';
import { YourcallBetslipService } from '@yourcall/services/yourcallBetslip/yourcall-betslip.service';
import { YourCallNotificationService } from '@yourcall/services/yourCallNotification/yourcall-notification.service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { YourcallService } from '@yourcall/services/yourcallService/yourcall.service';
import { YourcallDashboardService } from '@yourcall/services/yourcallDashboard/yourcall-dashboard.service';
import { YourCallStaticBlockComponent } from '@yourcall/components/yourCallStaticBlock/your-call-static-block.component';
import {
  YourCallMarketsProviderService
} from '@yourcall/services/yourCallMarketsProvider/yourcall-markets-provider.service';
import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { YourcallBetslipComponent } from '@yourcall/components/yourCallBetslip/yourcall-betslip.component';
import { YourcallBybLeagueService } from '@yourcall/components/bybLeague/yourcall-byb-league.service';
import { YourcallDashboardComponent } from '@yourcall/components/yourcallDashboard/yourcall-dashboard.component';
import { YourCallIconComponent } from '@yourcall/components/yourCallIcon/your-call-icon.component';
import { YourcallRunService } from '@yourcall/services/yourcallRunService/yourcall-run.service';
import { FiveASideTabContentComponent } from '@yourcall/components/fiveASideTabContent/five-a-side-tab-content.component';
import { FiveASidePitchComponent } from '@yourcall/components/fiveASidePitch/five-a-side-pitch.component';
import { FiveASideJourneyComponent } from '@yourcall/components/fiveASideJourney/five-a-side-journey.component';
import { FiveASidePlayerListComponent } from '@yourcall/components/fiveASidePlayerList/five-a-side-player-list.component';
import { PlayerCardComponent } from '@yourcall/components/playerCard/player-card.component';
import { FiveASidePlayerPageComponent } from '@yourcall/components/fiveASidePlayerPage/five-a-side-player-page.component';
import { FiveASideService } from '@yourcall/services/fiveASide/five-a-side.service';
import { BtnOddsComponent } from '@yourcall/components/btn-odds/btn-odds.component';
import { FiveASidePlayerStatComponent } from '@yourcall/components/fiveASidePlayerStat/five-a-side-player-stat.component';
import { StatsDropDownComponent } from '@yourcall/components/statsDropDown/stats-drop-down.component';

// Overridden
import { DesktopBybHomeComponent } from '@coralDesktop/yourCall/components/bybHome/byb-home.component';
import { DesktopYourcallBybLeagueComponent } from '@coralDesktop/yourCall/components/bybLeague/yourcall-byb-league.component';
import { DesktopYourCallTabContentComponent } from '@coralDesktop/yourCall/components/yourCallTabContent/your-call-tab-content.component';
import { FiveASideEventNameHeaderComponent } from '@yourcall/components/fiveASideEventNameHeader/five-a-side-event-name-header.component';
import { YourCallMarketButtonsComponent } from '@app/yourCall/components/yourCallMarketButtons/your-call-market-buttons.component';
import { YourCallPlayerBetsComponent } from '@app/yourCall/components/YourcallPlayerBets/your-call-player-bets.component';
import { YourCallGoalscorerComponent } from '@app/yourCall/components/yourCallGoalscorer/your-call-goalscorer.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    DesktopModule
  ],
  declarations: [
    YourCallStaticBlockComponent,
    YourcallBetslipComponent,
    YourCallMarketComponent,
    YourCallMarketGroupComponent,
    YourCallMarketSwitcherComponent,
    YourCallMarketPlayerBetsComponent,
    YourCallCorrectScoreComponent,
    YourcallDashboardComponent,
    YourCallTabDialogComponent,
    YourCallIconComponent,
    FiveASideTabContentComponent,
    FiveASidePitchComponent,
    FiveASideJourneyComponent,
    FiveASidePlayerListComponent,
    PlayerCardComponent,
    FiveASidePlayerPageComponent,
    BtnOddsComponent,
    FiveASidePlayerStatComponent,
    FiveASideEventNameHeaderComponent,
    StatsDropDownComponent,
    YourCallMarketButtonsComponent,
    YourCallPlayerBetsComponent,

    // Overridden
    DesktopYourCallTabContentComponent,
    DesktopYourcallBybLeagueComponent,
    DesktopBybHomeComponent,
    YourCallGoalscorerComponent
  ],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class YourCallModule {
  static forRoot() {
    return {
      ngModule: YourCallModule,
      providers: [
        YourcallRunService,
        BybHelperService,
        BybHomeService,
        BybApiService,
        YourcallValidationService,
        YourcallStoredBetsService,
        YourcallBetslipService,
        YourCallNotificationService,
        YourcallProviderService,
        YourcallService,
        YourcallDashboardService,
        YourCallMarketsProviderService,
        YourcallMarketsService,
        YourcallBybLeagueService,
        FiveASideService
      ],
    };
  }

  static entry = {
    DesktopYourCallTabContentComponent,
    YourCallStaticBlockComponent,
    DesktopBybHomeComponent,
    YourCallIconComponent,
    FiveASideTabContentComponent,
    YourCallMarketComponent,
    YourCallMarketButtonsComponent,
    YourCallPlayerBetsComponent,
    YourCallGoalscorerComponent
  };
  constructor(private asls: AsyncScriptLoaderService,yourcallRunService: YourcallRunService) {
    yourcallRunService.run();
    this.asls.loadCssFile('assets-your-call.css', true, true).subscribe();
  }
}
