// This module is required only to allow coralDesktop to build with AOT
// HERE you should place all components which extented from LadbrokesMobile
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { OddsCardSportComponent } from '@ladbrokesMobile/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';
import {
  OddsCardEnhancedMultiplesComponent
} from '@ladbrokesMobile/shared/components/oddsCard/oddsCardEnhancedMultiples/odds-card-enhanced-multiples.component';
import { HorseracingTabsComponent } from '@ladbrokesMobile/racing/components/racingTabsModule/horseracingTabs/horseracing-tabs.component';
import { RacingMainComponent } from '@ladbrokesMobile/racing/components/racingMain/racing-main.component';
import { LadbrokesAccordionComponent } from '@ladbrokesMobile/shared/components/accordion/accordion.component';

import { LadbrokesFeaturedModuleComponent } from '@ladbrokesMobile/featured/components/featured-module/featured-module.component';
import {
  LadbrokesRacingEventComponent
} from '@ladbrokesMobile/racing/components/racingEventComponent/racing-event.component';
import { VirtualSportsPageComponent } from '@ladbrokesMobile/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import {
  LadbrokesMobileRacingSpecialsTabComponent
} from '@ladbrokesMobile/racing/components/racingSpecialsTab/racing-specials-tab.component';
import { LadbrokesToteSliderComponent } from '@ladbrokesMobile/tote/components/toteSlider/tote-slider.component';
import { LadbrokesRaceCardsControlsComponent } from '@ladbrokesMobile/racing/components/race-cards-controls/race-cards-controls.component';
import {
  LadbrokesGreyhoundsTabsComponent
} from '@ladbrokesMobile/racing/components/racingTabsModule/greyhoundsTabs/greyhounds-tabs.component';
import { LadbrokesMobileBetFinderComponent } from '@ladbrokesMobile/bf/components/betFinder/bet-finder.component';
import { RacingPanelComponent } from '@ladbrokesMobile/shared/components/racingPanel/racing-panel.component';
import { SharedPipesModule } from '@shared/pipes/shared-pipes.module';
import { LadbrokesLoadingScreenComponent } from '@ladbrokesMobile/shared/components/loadingScreen/loading-screen.component';
import { InplayPageComponent } from '@ladbrokesMobile/inPlay/components/inplayPage/inplay-page.component';
import { MobileBigCompetitionComponent } from '@ladbrokesMobile/bigCompetitions/components/big-competition.component';
import { VirtualHomePageComponent } from '@app/vsbr/components/virtualHomePage/virtual-home-page.component';
import { VirtualOtherSports } from '@app/vsbr/components/virtualOtherSports/virtual-other-sports.component';

/**
 * Overridden Ladbrokes Mobile Components
 */
@NgModule({
  declarations: [
    LadbrokesFeaturedModuleComponent,
    HorseracingTabsComponent,
    RacingMainComponent,
    LadbrokesAccordionComponent,
    OddsCardSportComponent,
    LadbrokesRacingEventComponent,
    VirtualSportsPageComponent,
    LadbrokesMobileRacingSpecialsTabComponent,
    LadbrokesToteSliderComponent,
    LadbrokesRaceCardsControlsComponent,
    LadbrokesGreyhoundsTabsComponent,
    LadbrokesMobileBetFinderComponent,
    InplayPageComponent,
    RacingPanelComponent,
    LadbrokesLoadingScreenComponent,
    MobileBigCompetitionComponent,
    OddsCardEnhancedMultiplesComponent,
    VirtualHomePageComponent,
    VirtualOtherSports
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    SharedPipesModule
  ],
  exports: [],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FakeLadbrokesMobileModule {
}
