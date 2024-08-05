import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { TimelineComponent } from '@lazy-modules/timeline/components/timeline/timeline.component';
import { SliderPanelComponent } from '@lazy-modules/timeline/components/sliderPanel/slider-panel.component';
import { TimelinePostComponent } from '@lazy-modules/timeline/components/timelinePost/timeline-post.component';
import { TimelineService } from '@lazy-modules/timeline/services/timeline.service';
import { LocaleService } from '@core/services/locale/locale.service';
import {
  TimelineTutorialOverlayComponent
} from '@lazy-modules/timeline/components/timelineTutorialOverlay/timeline-tutorial-overlay.component';

import * as timeline from '@localeModule/translations/en-US';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [
    TimelineComponent,
    SliderPanelComponent,
    TimelinePostComponent,
    TimelineTutorialOverlayComponent
  ],
  exports: [
    TimelineComponent,
    SliderPanelComponent,
    TimelineTutorialOverlayComponent
  ],
  providers: [
    TimelineService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class TimelineModule {
  static entry = TimelineComponent;

  constructor(private localeService: LocaleService) {
    this.localeService.setLangData(timeline);
  }
}
