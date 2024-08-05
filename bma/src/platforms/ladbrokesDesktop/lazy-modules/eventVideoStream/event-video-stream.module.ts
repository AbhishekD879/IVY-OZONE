import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';


import {
  LadbrokesEventVideoStreamComponent
} from '@ladbrokesMobile/lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream.component';
import { IGameMediaComponent } from '@lazy-modules/eventVideoStream/components/iGameMedia/i-game-media.component';
import {
  VideoStreamProvidersComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamProviders/video-stream-providers.component';
import {
  VideoStreamErrorDialogComponent
} from '@eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';
import { CSBPlayerComponent } from '@lazy-modules/eventVideoStream/components/csb-player/csb-player.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    LadbrokesEventVideoStreamComponent,
    IGameMediaComponent,
    VideoStreamProvidersComponent,
    VideoStreamErrorDialogComponent,
    CSBPlayerComponent
  ],
  providers: [],
  exports: [
    LadbrokesEventVideoStreamComponent,
    IGameMediaComponent,
    VideoStreamProvidersComponent,
    VideoStreamErrorDialogComponent,
    CSBPlayerComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyEventVideoStreamModule {
  static entry = LadbrokesEventVideoStreamComponent;
}
