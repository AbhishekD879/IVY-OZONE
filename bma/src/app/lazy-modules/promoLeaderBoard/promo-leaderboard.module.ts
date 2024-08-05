import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { LeaderboardDetailsComponent } from '@lazy-modules/promoLeaderBoard/components/leaderboard-details/leaderboard-details.component';
import { LeaderboardDetailsCoralDesktopComponent } from '@lazy-modules/promoLeaderBoard/components/leaderboard-details-coral-desktop/leaderboard-details-coral-desktop.component';
import { LeaderboardService } from './service/leaderboard.service';
import { LeaderboardDetailsLadbrokesMobileComponent } from './components/leaderboard-details-ladbrokes-mobile/leaderboard-details-ladbrokes-mobile.component';
import { LeaderboardDetailsLadbrokesDesktopComponent } from './components/leaderboard-details-ladbrokes-desktop/leaderboard-details-ladbrokes-desktop.component';

@NgModule({
  declarations: [
    LeaderboardDetailsComponent,
    LeaderboardDetailsCoralDesktopComponent,
    LeaderboardDetailsLadbrokesDesktopComponent,
    LeaderboardDetailsLadbrokesMobileComponent
  ],
  imports: [
    CommonModule,
  ],exports:[
    LeaderboardDetailsComponent,
    LeaderboardDetailsCoralDesktopComponent,
    LeaderboardDetailsLadbrokesDesktopComponent,
    LeaderboardDetailsLadbrokesMobileComponent
  ],
  providers:[LeaderboardService],
  schemas: [NO_ERRORS_SCHEMA]
})


export class PromoLeaderboardModule {
  static entry = {
    LeaderboardDetailsComponent,
    LeaderboardDetailsCoralDesktopComponent,
    LeaderboardDetailsLadbrokesDesktopComponent,
    LeaderboardDetailsLadbrokesMobileComponent
  };
}
