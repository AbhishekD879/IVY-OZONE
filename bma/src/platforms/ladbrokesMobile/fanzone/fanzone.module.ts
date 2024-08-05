import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@ladbrokesMobile/shared/shared.module';
import { FanzoneApiModule } from '@ladbrokesMobile/fanzone/fanzone-api.module';
import { FanzoneRoutingModule } from '@ladbrokesMobile/fanzone/fanzone-routing.module';
import { FanzoneHomeComponent } from '@ladbrokesMobile/fanzone/components/fanzoneHome/fanzone-home.component';
import { FeaturedModule } from '@ladbrokesMobile/featured/featured.module';
import { FanzoneClubComponent } from '@ladbrokesMobile/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneStatsComponent } from '@ladbrokesMobile/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FanzoneNowNextComponent } from '@ladbrokesMobile/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneEventMarketsComponent } from '@ladbrokesMobile/fanzone/components/fanzoneEventMarkets/fanzone-event-markets.component';
import { FanzoneOutrightsComponent } from '@ladbrokesMobile/fanzone/components/fanzoneOutrights/fanzone-outrights.component';
import { FanzoneSelectYourTeamComponent } from '@ladbrokesMobile/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzoneSharedModule } from '@app/lazy-modules/fanzone/fanzone-shared.module';
import { FanzonePreferenceCentreComponent } from '@ladbrokesMobile/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component';
import { FanzoneMobileLeagueTableModalComponent } from '@ladbrokesMobile/fanzone/components/fanzoneLeagueTableModal/fanzone-league-table-modal.component';
import { FanzoneVacationComponent } from '@ladbrokesMobile/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneGamesComponent } from '@ladbrokesMobile/fanzone/components/fanzoneGames/fanzone-games.component';

@NgModule({
  declarations: [
    FanzoneHomeComponent,
    FanzoneStatsComponent,
    FanzoneClubComponent,
    FanzoneNowNextComponent,
    FanzoneEventMarketsComponent,
    FanzoneOutrightsComponent,
    FanzoneSelectYourTeamComponent,
    FanzonePreferenceCentreComponent,
    FanzoneMobileLeagueTableModalComponent,
    FanzoneVacationComponent,
    FanzoneGamesComponent
  ],
  exports: [FanzonePreferenceCentreComponent],
  imports: [
    CommonModule,
    SharedModule,
    FanzoneRoutingModule,
    FanzoneApiModule,
    FeaturedModule,
    FanzoneSharedModule
  ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FanzoneModule {
  static entry = { FanzoneHomeComponent };
}
