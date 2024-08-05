import { FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { BackToTopComponent } from '@desktopModule/components/backToTop/back-to-top.component';
import {
  EnhancedMultiplesCarouselComponent
} from '@desktopModule/components/enchancedMultiplesCarousel/enhancedMultiplesCarousel.component';
import { FilterButtonsComponent } from '@desktopModule/components/filterButtons/filter-buttons.component';
import { StreamButtonComponent } from '@desktopModule/components/streamButton/stream-button.component';
import { FreeBetIconComponent } from '@desktopModule/components/freeBetIcon/free-bet-icon.component';
import { TimeFormWidgetComponent } from '@desktopModule/components/timeformWidget/timeform-widget.component';
import { ActionArrowsComponent } from '@desktopModule/components/actionArrows/action-arrows.component';
import { InplayWidgetComponent } from '@desktopModule/components/widgets/inplayWidget/inplay-widget.component';
import { InplaySportCardComponent } from '@desktopModule/components/widgets/inplayWidget/inplaySportCard/inplay-sport-card.component';
import {
  InplayOutrightCardComponent
} from '@desktopModule/components/widgets/inplayWidget/inplayOutrightCard/inplay-outright-card.component';
import { WidgetsComponent } from '@desktopModule/components/widgets/widgets.component';
import { WidgetsService } from '@desktopModule/components/widgets/widgets.service';
import { LiveStreamWidgetComponent } from '@desktopModule/components/widgets/liveStreamWidget/live-stream-widget.component';
import {
  LiveStreamWidgetService
} from '@desktopModule/components/widgets/liveStreamWidget/liveStreamWidgetService/live-stream-widget.service';
import { PrivateMarketsComponent } from '@desktopModule/components/privateMarkets/private-markets.component';
import { ResultsWidgetComponent } from '@desktopModule/components/widgets/resultsWidget/results-widget.component';
import { TableWidgetComponent } from '@desktopModule/components/widgets/tableWidget/table-widget.component';
import { LeftMenuComponent } from '@desktopModule/components/leftMenu/left-menu.component';
import { HeaderSectionComponent } from '@desktopModule/components/headerSection/header-section.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule
  ],
  exports: [
    LeftMenuComponent,
    BackToTopComponent,
    EnhancedMultiplesCarouselComponent,
    FilterButtonsComponent,
    StreamButtonComponent,
    FreeBetIconComponent,
    TimeFormWidgetComponent,
    ActionArrowsComponent,
    PrivateMarketsComponent,
    ActionArrowsComponent,
    InplayWidgetComponent,
    InplaySportCardComponent,
    InplayOutrightCardComponent,
    WidgetsComponent,
    ResultsWidgetComponent,
    TableWidgetComponent,
    HeaderSectionComponent
  ],
  declarations: [
    LeftMenuComponent,
    BackToTopComponent,
    EnhancedMultiplesCarouselComponent,
    FilterButtonsComponent,
    StreamButtonComponent,
    FreeBetIconComponent,
    TimeFormWidgetComponent,
    ActionArrowsComponent,
    PrivateMarketsComponent,
    ActionArrowsComponent,
    InplayWidgetComponent,
    InplaySportCardComponent,
    InplayOutrightCardComponent,
    WidgetsComponent,
    LiveStreamWidgetComponent,
    ResultsWidgetComponent,
    TableWidgetComponent,
    HeaderSectionComponent
  ],
  providers: [
    WidgetsService,
    LiveStreamWidgetService

  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class DesktopModule { }

