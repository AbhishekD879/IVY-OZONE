import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { TotePageComponent } from '@app/tote/components/totePage/tote-page.component';
import { ToteRoutingModule } from '@app/tote/tote-routing.module';
import { WnPoolStakesComponent } from '@app/tote/components/wnPoolStakes/wn-pool-stakes.component';
import { PlPoolStakesComponent } from '@app/tote/components/plPoolStakes/pl-pool-stakes.component';
import { ShPoolStakesComponent } from '@app/tote/components/shPoolStakes/sh-pool-stakes.component';
import { ExPoolPlacesComponent } from '@app/tote/components/exPoolPlaces/ex-pool-places.component';
import { TrPoolPlacesComponent } from '@app/tote/components/trPoolPlaces/tr-pool-places.component';
import { BetReceiptComponent } from '@app/tote/components/betReceipt/bet-receipt.component';
import { PoolStakeComponent } from '@app/tote/components/poolStake/pool-stake.component';
import { PoolSizeComponent } from '@app/tote/components/poolSize/pool-size.component';
import { ToteEventsByMeetingComponent } from '@app/tote/components/toteEventsByMeeting/tote-events-by-meeting.component';
import { ToteEventsByTimeComponent } from '@app/tote/components/toteEventsByTime/tote-events-by-time.component';
import { ToteInfoComponent } from '@app/tote/components/toteInfo/tote-info.component';
import { ToteTabsResultsComponent } from '@app/tote/components/toteTabsResults/tote-tabs-results.component';
import { PostSpotlightComponent } from '@app/tote/components/postSpotlight/post-spotlight.component';
import { ToteSportComponent } from '@app/tote/components/toteSport/tote-sport.component';
import { ToteRequestErrorComponent } from '@app/tote/components/tote-request-error/tote-request-error.component';
import { BetItemComponent } from '@app/tote/components/betItem/bet-item.component';
import { BetErrorHandlingService } from '@app/tote/services/betErrorHandling/bet-error-handling.service';
import { ToteService } from '@app/tote/services/mainTote/main-tote.service';
import { ToteBetReceiptService } from '@app/tote/services/toteBetReceipt/tote-bet-receipt.service';
import { ToteBetSlipService } from '@app/tote/services/toteBetSlip/tote-bet-slip.service';
import { ToteEventPageComponent } from '@app/tote/components/toteEventPage/tote-event-page.component';
import { LadbrokesToteSliderComponent } from '@ladbrokesMobile/tote/components/toteSlider/tote-slider.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

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
    LadbrokesToteSliderComponent
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
    LadbrokesToteSliderComponent
  ],
  imports: [
    SharedModule,
    ToteRoutingModule
  ],
  providers: [
    BetErrorHandlingService,
    ToteService,
    ToteBetReceiptService,
    ToteBetSlipService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class ToteModule {
  static entry = LadbrokesToteSliderComponent;
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-tote.css', true, true).subscribe();
  }
}
