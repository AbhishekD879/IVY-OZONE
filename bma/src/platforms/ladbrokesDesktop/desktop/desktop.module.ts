import { FormsModule } from '@angular/forms';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { BackToTopComponent } from '@desktop/components/backToTop/back-to-top.component';
import { EnhancedMultiplesCarouselComponent } from '@desktop/components/enchancedMultiplesCarousel/enhancedMultiplesCarousel.component';
import { FilterButtonsComponent } from '@desktop/components/filterButtons/filter-buttons.component';
import { StreamButtonComponent } from '@desktop/components/streamButton/stream-button.component';
import { TimeFormWidgetComponent } from '@desktop/components/timeformWidget/timeform-widget.component';
import { ActionArrowsComponent } from '@desktop/components/actionArrows/action-arrows.component';
import { InplayWidgetComponent } from '@desktop/components/widgets/inplayWidget/inplay-widget.component';
import { InplaySportCardComponent } from '@desktop/components/widgets/inplayWidget/inplaySportCard/inplay-sport-card.component';
import { InplayOutrightCardComponent } from '@desktop/components/widgets/inplayWidget/inplayOutrightCard/inplay-outright-card.component';
import { WidgetsComponent } from '@desktop/components/widgets/widgets.component';
import { WidgetsService } from '@desktop/components/widgets/widgets.service';
import { LiveStreamWidgetComponent } from '@desktop/components/widgets/liveStreamWidget/live-stream-widget.component';
import { LiveStreamWidgetService } from '@desktop/components/widgets/liveStreamWidget/liveStreamWidgetService/live-stream-widget.service';
import { PrivateMarketsComponent } from '@desktop/components/privateMarkets/private-markets.component';
import { ResultsWidgetComponent } from './components/widgets/resultsWidget/results-widget.component';
import { TableWidgetComponent } from './components/widgets/tableWidget/table-widget.component';
import { LeftMenuComponent } from '@desktop/components/leftMenu/left-menu.component';
import { HeaderSectionComponent } from '@desktop/components/headerSection/header-section.component';

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
    TimeFormWidgetComponent,
    ActionArrowsComponent,
    PrivateMarketsComponent,
    ActionArrowsComponent,
    InplayWidgetComponent,
    InplaySportCardComponent,
    InplayOutrightCardComponent,
    WidgetsComponent,
    ResultsWidgetComponent,
    HeaderSectionComponent,
    TableWidgetComponent
  ],
  declarations: [
    LeftMenuComponent,
    BackToTopComponent,
    EnhancedMultiplesCarouselComponent,
    FilterButtonsComponent,
    StreamButtonComponent,
    TimeFormWidgetComponent,
    ActionArrowsComponent,
    PrivateMarketsComponent,
    ActionArrowsComponent,
    InplayWidgetComponent,
    InplaySportCardComponent,
    InplayOutrightCardComponent,
    WidgetsComponent,
    HeaderSectionComponent,
    LiveStreamWidgetComponent,
    ResultsWidgetComponent,
    TableWidgetComponent
  ],
  providers: [
    WidgetsService,
    LiveStreamWidgetService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class DesktopModule { }

