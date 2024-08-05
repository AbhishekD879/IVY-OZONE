import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { InPlayLiveStreamService } from '@ladbrokesDesktop/inPlayLiveStream/services/inPlayLiveStream/in-play-live-stream.service';
import { InPlayLiveStreamComponent } from '@ladbrokesDesktop/inPlayLiveStream/components/inPlayLiveStream/inplay-live-stream.component';
import { SportCarouselComponent } from '@ladbrokesDesktop/inPlayLiveStream/components/sportCarousel/sport-carousel.component';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktop/desktop.module';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule
  ],
  declarations: [
    InPlayLiveStreamComponent,
    SportCarouselComponent
  ],
  exports: [
    SportCarouselComponent,
    InPlayLiveStreamComponent,
  ],
  providers: [
    InPlayLiveStreamService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class InplayLiveStreamModule {
  static entry = InPlayLiveStreamComponent;
}
