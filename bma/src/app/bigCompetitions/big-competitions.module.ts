import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { ParticipantsService } from './services/participants/participants.service';
import { BigCompetitionsService } from './services/bigCompetitions/big-competitions.service';
import { BigCompetitionsProvider } from './services/bigCompetitionsProvider/big-competitions-provider.service';
import { BigCompetitionsLiveUpdatesService } from './services/bigCompetitionsLiveUpdates/big-competitions-live-updates.service';
import { InplaySubscriptionService } from './services/inplaySubscription/inplay-subscription-service';
import { BigCompetitionsSpecialsService } from './services/bigCompetitionsSpecials/big-competitions-specials-service';
import { CompetitionKnockoutsService } from './services/competitionKnockouts/competition-knockouts.service';
import { ListViewComponent } from '@app/bigCompetitions/components/listView/list-view.component';
import { CompetitionSpecialsComponent } from './components/competitionSpecials/competition-specials.component';
import { CompetitionSpecialsOverviewComponent } from './components/competitionSpecialsOverview/competition-specials-overview.component';
import { CompetitionSpecialsViewComponent } from './components/competitionSpecialsView/competition-specials-view.component';
import { CardViewWidgetComponent } from './components/cardViewWidget/card-view-widget.component';
import { CardViewBodyComponent } from './components/cardViewWidget/cardViewBody/card-view-body.component';
import { CardViewFooterComponent } from './components/cardViewWidget/cardViewFooter/card-view-footer.component';
import { PrematchCardDetailsComponent } from './components/cardViewWidget/prematchCardDetails/prematch-card-details.component';
import { InplayCardDetailsComponent } from './components/cardViewWidget/inplayCardDetails/inplay-card-details.component';
import { LiveEventsCarouselComponent } from '@app/bigCompetitions/components/liveEventsCarousel/live-events-carousel.component';
import { KnockoutsCardComponent } from '@app/bigCompetitions/components/competitionKnockouts/knockoutsCard/knockouts-card.component';
import {
  KnockoutsRoundWinnerComponent
} from '@app/bigCompetitions/components/competitionKnockouts/knockoutsRoundWinner/knockouts-round-winner.component';
import {
  CompetitionKnockoutsComponent
} from '@app/bigCompetitions/components/competitionKnockouts/competition-knockouts.component';
import { CompetitionGroupsWidgetComponent } from './components/competitionGroupsWidget/competition-groups-widget.component';
import { CompetitionGroupIndividualComponent } from './components/competitionGroupIndividual/competition-groups-individual.component';
import { CompetitionGroupAllComponent } from './components/competitionGroupAll/competition-groups-all.component';
import { CompetitionGroupCardComponent } from './components/competitionGroupCard/competition-group-card.component';
import { CompetitionOutrightsComponent } from './components/competitionOutrights/competition-outrights.component';
import { CompetitionPromotionsComponent } from './components/competitionPromotions/competition-promotions.component';
import { CompetitionResultsComponent } from './components/competitionResults/competition-results.component';
import { CardViewComponent } from './components/outrightCard/outright-card.component';
import { GridViewWidgetComponent } from './components/outrightGrid/outright-grid.component';
import { ListViewWidgetComponent } from './components/outrightList/outright-list.component';
import { ViewTypeContainerComponent } from './components/viewTypeContainer/view-type-container.component';
import { CompetitionNextEventsComponent } from '@app/bigCompetitions/components/competitionNextEvents/competition-next-events.component';
import { BigCompetitionComponent } from './components/bigCompetition/big-competition.component';
import { BigCompetitionTabsComponent } from './components/bigCompetitionTabs/big-competition-tabs.component';
import { CompetitionModuleComponent } from './components/competitionModule/competition-module.component';
import { CompetitionModuleDirective } from './directives/competition-module.directive';
import { BigCompetitionsRoutingModule } from '@app/bigCompetitions/big-competitions-routing.module';
import { CompetitionCardResultComponent } from './components/oddsCardResult/competition-odds-card-result.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
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
    BigCompetitionComponent,
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
  this.asls.loadCssFile('assets-big-competition.css', true, true).subscribe();
}
}
