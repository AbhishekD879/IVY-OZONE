import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@ladbrokesDesktop/shared/shared.module';
import { FanzoneDesktopApiModule } from '@ladbrokesDesktop/fanzone/fanzone-api.module';
import { FanzoneDesktopRoutingModule } from '@ladbrokesDesktop/fanzone/fanzone-routing.module';
import { FanzoneHomeDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneHome/fanzone-home.component';
import { FeaturedModule } from '@ladbrokesDesktop/featured/featured.module';
import { FanzoneStatsComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FanzoneClubComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneNowNextComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneDesktopOutrightsComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneOutrights/fanzone-outrights.component';
import { FanzoneDesktopEventMarketsComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneEventMarkets/fanzone-event-markets.component';
import { FanzoneSelectYourTeamDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzoneSharedModule } from '@app/lazy-modules/fanzone/fanzone-shared.module';
import { FanzoneDesktopLeagueTableModalComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneLeagueTableModal/fanzone-league-table-modal.component';
import { FanzoneVacationDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneGamesComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneGames/fanzone-games.component';
@NgModule({
  declarations: [
    FanzoneHomeDesktopComponent,
    FanzoneStatsComponent,
    FanzoneClubComponent,
    FanzoneNowNextComponent,
    FanzoneDesktopOutrightsComponent,
    FanzoneDesktopEventMarketsComponent,
    FanzoneSelectYourTeamDesktopComponent,
    FanzoneDesktopLeagueTableModalComponent,
    FanzoneVacationDesktopComponent,
    FanzoneGamesComponent
  ],
  exports: [],
  imports: [
    CommonModule,
    SharedModule,
    FanzoneDesktopRoutingModule,
    FanzoneDesktopApiModule,
    FeaturedModule,
    FanzoneSharedModule
  ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FanzoneModule { }
