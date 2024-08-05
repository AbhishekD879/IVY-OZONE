import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { ToteRoutingModule } from '@toteModule/tote-routing.module';
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
import { ToteTabsResultsComponent } from '@app/tote/components/toteTabsResults/tote-tabs-results.component';
import { PostSpotlightComponent } from '@app/tote/components/postSpotlight/post-spotlight.component';
import { ToteSportComponent } from '@app/tote/components/toteSport/tote-sport.component';
import { ToteRequestErrorComponent } from '@app/tote/components/tote-request-error/tote-request-error.component';
import { BetItemComponent } from '@app/tote/components/betItem/bet-item.component';
import { BetErrorHandlingService } from '@app/tote/services/betErrorHandling/bet-error-handling.service';
import { ToteBetReceiptService } from '@app/tote/services/toteBetReceipt/tote-bet-receipt.service';
import { ToteBetSlipService } from '@app/tote/services/toteBetSlip/tote-bet-slip.service';
import { ToteEventPageComponent } from '@app/tote/components/toteEventPage/tote-event-page.component';
// Overridden app components
import { DesktopTotePageComponent } from '@ladbrokesDesktop/tote/components/totePage/tote-page.component';
import { DesktopToteInfoComponent } from '@ladbrokesDesktop/tote/components/toteInfo/tote-info.component';
import { DesktopToteSliderComponent } from '@ladbrokesDesktop/tote/components/toteSlider/tote-slider.component';
import { DesktopModule } from '@ladbrokesDesktop/desktop/desktop.module';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
    // Overridden app components
    DesktopTotePageComponent,
    DesktopToteInfoComponent,

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
    ToteTabsResultsComponent,
    PostSpotlightComponent,
    ToteSportComponent,
    ToteRequestErrorComponent,
    ToteEventPageComponent,
    BetItemComponent,
    DesktopToteSliderComponent
  ],
  exports: [
    // Overridden app components
    DesktopTotePageComponent,
    DesktopToteInfoComponent,

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
    ToteTabsResultsComponent,
    PostSpotlightComponent,
    ToteSportComponent,
    ToteRequestErrorComponent,
    ToteEventPageComponent,
    BetItemComponent
  ],
  imports: [
    DesktopModule,
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
  static entry = DesktopToteSliderComponent;
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-tote.css', true, true).subscribe();
  }
}
