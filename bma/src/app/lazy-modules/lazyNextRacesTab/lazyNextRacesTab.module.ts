import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { ExtraPlaceHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/extraPlaceHome/extra-place-home.component';
import { LazyNextRacesTabRoutingModule } from '@lazy-modules/lazyNextRacesTab/lazyNextRacesTab-routing.module';
import { NextRacesHomeTabComponent } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHomeTab/next-races-home-tab.component';
import { NextRacesHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.component';
import { SharedModule } from '@sharedModule/shared.module';
import { RaceCardHomeComponent } from '@lazy-modules/lazyNextRacesTab/components/raceCardHome/race-card-home.component';

@NgModule({
  imports: [
    SharedModule,
    LazyNextRacesTabRoutingModule
  ],
  declarations: [
    RaceCardHomeComponent,
    ExtraPlaceHomeComponent,
    NextRacesHomeTabComponent,
    NextRacesHomeComponent
  ],
  providers: [],
  exports: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class LazyNextRacesTabModule {}
