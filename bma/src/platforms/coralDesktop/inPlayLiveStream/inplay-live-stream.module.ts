import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { InPlayLiveStreamService } from '@inPlayLiveStream/services/inPlayLiveStream/in-play-live-stream.service';
import { InPlayLiveStreamComponent } from '@inPlayLiveStream/components/inPlayLiveStream/inplay-live-stream.component';
import { SportCarouselComponent } from '@inPlayLiveStream/components/sportCarousel/sport-carousel.component';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktopModule/desktop.module';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule
  ],
  declarations: [
    InPlayLiveStreamComponent,
    SportCarouselComponent,
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
}
