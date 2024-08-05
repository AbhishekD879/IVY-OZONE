import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { TotePageComponent } from './components/totePage/tote-page.component';
import { ToteRoutingModule } from './tote-routing.module';
import { WnPoolStakesComponent } from './components/wnPoolStakes/wn-pool-stakes.component';
import { PlPoolStakesComponent } from './components/plPoolStakes/pl-pool-stakes.component';
import { ShPoolStakesComponent } from './components/shPoolStakes/sh-pool-stakes.component';
import { ExPoolPlacesComponent } from './components/exPoolPlaces/ex-pool-places.component';
import { TrPoolPlacesComponent } from './components/trPoolPlaces/tr-pool-places.component';
import { BetReceiptComponent } from './components/betReceipt/bet-receipt.component';
import { PoolStakeComponent } from './components/poolStake/pool-stake.component';
import { PoolSizeComponent } from './components/poolSize/pool-size.component';
import { ToteEventsByMeetingComponent } from './components/toteEventsByMeeting/tote-events-by-meeting.component';
import { ToteEventsByTimeComponent } from './components/toteEventsByTime/tote-events-by-time.component';
import { ToteInfoComponent } from './components/toteInfo/tote-info.component';
import { ToteTabsResultsComponent } from './components/toteTabsResults/tote-tabs-results.component';
import { PostSpotlightComponent } from './components/postSpotlight/post-spotlight.component';
import { ToteSportComponent } from './components/toteSport/tote-sport.component';
import { ToteRequestErrorComponent } from './components/tote-request-error/tote-request-error.component';
import { BetItemComponent } from './components/betItem/bet-item.component';
import { BetErrorHandlingService } from './services/betErrorHandling/bet-error-handling.service';
import { ToteBetReceiptService } from './services/toteBetReceipt/tote-bet-receipt.service';
import { ToteBetSlipService } from './services/toteBetSlip/tote-bet-slip.service';
import { ToteEventPageComponent } from './components/toteEventPage/tote-event-page.component';
import { ToteSliderComponent } from '@app/tote/components/toteSlider/tote-slider.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
    WnPoolStakesComponent,
    PlPoolStakesComponent,
    ShPoolStakesComponent,
    BetReceiptComponent,
    PoolStakeComponent,
    PoolSizeComponent,
    ToteEventsByMeetingComponent,
    ToteEventsByTimeComponent,
    ExPoolPlacesComponent,
    TrPoolPlacesComponent,
    ToteInfoComponent,
    ToteTabsResultsComponent,
    PostSpotlightComponent,
    ToteSportComponent,
    ToteRequestErrorComponent,
    ToteEventPageComponent,
    BetItemComponent,
    TotePageComponent,
    ToteSliderComponent
  ],
  exports: [
    WnPoolStakesComponent,
    PlPoolStakesComponent,
    ShPoolStakesComponent,
    BetReceiptComponent,
    PoolStakeComponent,
    PoolSizeComponent,
    ExPoolPlacesComponent,
    TrPoolPlacesComponent,
    ToteEventsByMeetingComponent,
    ToteEventsByTimeComponent,
    ToteInfoComponent,
    ToteTabsResultsComponent,
    PostSpotlightComponent,
    ToteSportComponent,
    ToteRequestErrorComponent,
    ToteEventPageComponent,
    BetItemComponent,
    TotePageComponent
  ],
  imports: [
    SharedModule,
    ToteRoutingModule
  ],
  providers: [
    BetErrorHandlingService,
    ToteBetReceiptService,
    ToteBetSlipService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class ToteModule {
  static entry = ToteSliderComponent;
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-tote.css', true, true).subscribe();
  }
}
