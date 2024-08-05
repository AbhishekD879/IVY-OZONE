import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';


import { EventVideoStreamComponent } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream.component';
import { IGameMediaComponent } from '@lazy-modules/eventVideoStream/components/iGameMedia/i-game-media.component';
import {
  VideoStreamProvidersComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamProviders/video-stream-providers.component';
import {
  StreamBetProviderComponent
} from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers/stream-bet-provider.component';
import {
  StreamBetIOSProviderComponent
} from '@lazy-modules/eventVideoStream/components/stream-bet/video-providers-ios/stream-bet-ios-provider.component';
import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import { CSBPlayerComponent } from '@lazy-modules/eventVideoStream/components/csb-player/csb-player.component';
import { SbRacingMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/racing-market-item/sb-racing-market-item.component';
import { StreamBetTemplatesComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates-provider/stream-bet-templates.component';
import { StreamBetOverlayProviderComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/overlay-provider/stream-bet-overlay-provider.component'
import { StreamBetOverlayProviderRacingComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/overlay-provider-racing/stream-bet-overlay-provider-racing.component';
import { SbCounterComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/counter/sb-counter.component';
import { SbCorrectScoreMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/correct-score-market-item/sb-correct-score-market-item.component';
import { StreamBetTemplateDropDownComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/drop-down/sb-template-drop-down.component';
import { SbSingleDropDownSingleOddComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/single-drop-down-single-odd/sb-single-drop-down-single-odd.component';
import { SbMultipleOddsMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/multiple-odds-market-item/sb-multiple-odds-market-item.component';
import { SbPriceOddsButtonComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-button.component';
import { SBPriceOddsClassDirective } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-class.directive';
import { SBPriceOddsDisabledDirective } from '@lazy-modules/eventVideoStream/components/stream-bet/controls/price-odds-button/sb-price-odds-disabled.directive';
import { SbOverUnderMarketItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/over-under-market-item/sb-over-under-market-item.component';
import { SbSingleDropDoubleOddItemComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/single-drop-double-odd-item/sb-single-drop-double-odd-item.component';
import { SbGroupedMarketTemplatesComponent } from '@lazy-modules/eventVideoStream/components/stream-bet/templates/grouped-market-templates/sb-grouped-market-templates.component';
import { StreamBetService } from '@lazy-modules/eventVideoStream/services/streamBet/stream-bet.service';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    EventVideoStreamComponent,
    IGameMediaComponent,
    VideoStreamProvidersComponent,
    CSBPlayerComponent,
    VideoStreamErrorDialogComponent,
    StreamBetProviderComponent,
    StreamBetIOSProviderComponent,
    StreamBetOverlayProviderComponent,
    StreamBetOverlayProviderRacingComponent,
    StreamBetTemplatesComponent,
    SbCounterComponent,
    SbCorrectScoreMarketItemComponent,
    SbOverUnderMarketItemComponent,
    SbSingleDropDoubleOddItemComponent,
    StreamBetTemplateDropDownComponent,
    SbSingleDropDownSingleOddComponent,
    SbMultipleOddsMarketItemComponent,
    SbRacingMarketItemComponent,
    SbPriceOddsButtonComponent,
    SBPriceOddsClassDirective,
    SBPriceOddsDisabledDirective,
    SbGroupedMarketTemplatesComponent
  ],
  providers: [StreamBetService],
  exports: [
    EventVideoStreamComponent,
    IGameMediaComponent,
    VideoStreamProvidersComponent,
    CSBPlayerComponent,
    VideoStreamErrorDialogComponent,
    StreamBetProviderComponent,
    StreamBetIOSProviderComponent,
    StreamBetOverlayProviderComponent,
    StreamBetOverlayProviderRacingComponent,
    StreamBetTemplatesComponent,
    SbCounterComponent,
    SbCorrectScoreMarketItemComponent,
    SbOverUnderMarketItemComponent,
    SbSingleDropDoubleOddItemComponent,
    StreamBetTemplateDropDownComponent,
    SbSingleDropDownSingleOddComponent,
    SbMultipleOddsMarketItemComponent,
    SbRacingMarketItemComponent,
    SbPriceOddsButtonComponent,
    SBPriceOddsClassDirective,
    SBPriceOddsDisabledDirective,
    SbGroupedMarketTemplatesComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyEventVideoStreamModule {
  static entry = EventVideoStreamComponent;
}