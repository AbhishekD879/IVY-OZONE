import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { ParticipantsService } from '@app/bigCompetitions/services/participants/participants.service';
import { BigCompetitionsService } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.service';
import { BigCompetitionsProvider } from '@app/bigCompetitions/services/bigCompetitionsProvider/big-competitions-provider.service';
import {
  BigCompetitionsLiveUpdatesService
} from '@app/bigCompetitions/services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { InplaySubscriptionService } from '@app/bigCompetitions/services/inplaySubscription/inplay-subscription-service';
import { BigCompetitionsSpecialsService } from '@app/bigCompetitions/services/bigCompetitionsSpecials/big-competitions-specials-service';
import { CompetitionKnockoutsService } from '@app/bigCompetitions/services/competitionKnockouts/competition-knockouts.service';
import { ListViewComponent } from '@app/bigCompetitions/components/listView/list-view.component';
import { CompetitionSpecialsComponent } from '@app/bigCompetitions/components/competitionSpecials/competition-specials.component';
import {
  CompetitionSpecialsOverviewComponent
} from '@app/bigCompetitions/components/competitionSpecialsOverview/competition-specials-overview.component';
import {
  CompetitionSpecialsViewComponent
} from '@app/bigCompetitions/components/competitionSpecialsView/competition-specials-view.component';
import { CardViewWidgetComponent } from '@app/bigCompetitions/components/cardViewWidget/card-view-widget.component';
import { CardViewBodyComponent } from '@app/bigCompetitions/components/cardViewWidget/cardViewBody/card-view-body.component';
import { CardViewFooterComponent } from '@app/bigCompetitions/components/cardViewWidget/cardViewFooter/card-view-footer.component';
import {
  PrematchCardDetailsComponent
} from '@app/bigCompetitions/components/cardViewWidget/prematchCardDetails/prematch-card-details.component';
import { InplayCardDetailsComponent } from '@app/bigCompetitions/components/cardViewWidget/inplayCardDetails/inplay-card-details.component';
import { LiveEventsCarouselComponent } from '@app/bigCompetitions/components/liveEventsCarousel/live-events-carousel.component';
import { KnockoutsCardComponent } from '@app/bigCompetitions/components/competitionKnockouts/knockoutsCard/knockouts-card.component';
import {
  KnockoutsRoundWinnerComponent
} from '@app/bigCompetitions/components/competitionKnockouts/knockoutsRoundWinner/knockouts-round-winner.component';
import {
  CompetitionKnockoutsComponent
} from '@app/bigCompetitions/components/competitionKnockouts/competition-knockouts.component';
import {
  CompetitionGroupsWidgetComponent
} from '@app/bigCompetitions/components/competitionGroupsWidget/competition-groups-widget.component';
import {
  CompetitionGroupIndividualComponent
} from '@app/bigCompetitions/components/competitionGroupIndividual/competition-groups-individual.component';
import { CompetitionGroupAllComponent } from '@app/bigCompetitions/components/competitionGroupAll/competition-groups-all.component';
import { CompetitionGroupCardComponent } from '@app/bigCompetitions/components/competitionGroupCard/competition-group-card.component';
import { CompetitionOutrightsComponent } from '@app/bigCompetitions/components/competitionOutrights/competition-outrights.component';
import { CompetitionPromotionsComponent } from '@app/bigCompetitions/components/competitionPromotions/competition-promotions.component';
import { CompetitionResultsComponent } from '@app/bigCompetitions/components/competitionResults/competition-results.component';
import { CardViewComponent } from '@app/bigCompetitions/components/outrightCard/outright-card.component';
import { GridViewWidgetComponent } from '@app/bigCompetitions/components/outrightGrid/outright-grid.component';
import { ListViewWidgetComponent } from '@app/bigCompetitions/components/outrightList/outright-list.component';
import { ViewTypeContainerComponent } from '@app/bigCompetitions/components/viewTypeContainer/view-type-container.component';
import { CompetitionNextEventsComponent } from '@app/bigCompetitions/components/competitionNextEvents/competition-next-events.component';
import { BigCompetitionTabsComponent } from '@app/bigCompetitions/components/bigCompetitionTabs/big-competition-tabs.component';
import { CompetitionModuleComponent } from '@app/bigCompetitions/components/competitionModule/competition-module.component';
import { CompetitionModuleDirective } from '@app/bigCompetitions/directives/competition-module.directive';

// Overridden app components
import { MobileBigCompetitionComponent } from '@ladbrokesMobile/bigCompetitions/components/big-competition.component';
import { BigCompetitionsRoutingModule } from '@ladbrokesMobile/bigCompetitions/big-competitions-routing.module';
import { CompetitionCardResultComponent } from '@app/bigCompetitions/components/oddsCardResult/competition-odds-card-result.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
    // Overridden app components
    MobileBigCompetitionComponent,

    KnockoutsCardComponent,
    KnockoutsRoundWinnerComponent,
    CompetitionKnockoutsComponent,
    CardViewWidgetComponent,
    CardViewFooterComponent,
    PrematchCardDetailsComponent,
    InplayCardDetailsComponent,
    CardViewBodyComponent,
    LiveEventsCarouselComponent,
    ListViewComponent,
    CompetitionSpecialsComponent,
    CompetitionSpecialsOverviewComponent,
    CompetitionSpecialsViewComponent,
    CompetitionGroupsWidgetComponent,
    CompetitionGroupIndividualComponent,
    CompetitionGroupAllComponent,
    CompetitionGroupCardComponent,
    CompetitionOutrightsComponent,
    CompetitionPromotionsComponent,
    CompetitionResultsComponent,
    CardViewComponent,
    GridViewWidgetComponent,
    ListViewWidgetComponent,
    ViewTypeContainerComponent,
    BigCompetitionTabsComponent,
    CompetitionNextEventsComponent,
    CompetitionModuleComponent,
    CompetitionModuleDirective,
    CompetitionCardResultComponent
  ],
  imports: [
    SharedModule,
    BigCompetitionsRoutingModule
  ],
  exports: [
  ],
  schemas: [
    NO_ERRORS_SCHEMA
  ],
  providers: [
    ParticipantsService,
    BigCompetitionsService,
    BigCompetitionsProvider,
    BigCompetitionsLiveUpdatesService,
    InplaySubscriptionService,
    BigCompetitionsSpecialsService,
    CompetitionKnockoutsService
  ],
})
export class BigCompetitionsModule {
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-big-competition.css',true, true).subscribe();
  }
}
