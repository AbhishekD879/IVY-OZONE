import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LiveStreamWrapperComponent } from '@bma/components/liveStream/live-stream-wrapper.component';
import { LiveStreamWrapperRoutingModule } from '@bma/components/liveStream/live-stream-wrapper-routing.module';

@NgModule({
  imports: [
    LiveStreamWrapperRoutingModule,
    SharedModule
  ],
  declarations: [
    LiveStreamWrapperComponent,
  ]
})

export class LiveStreamWrapperModule {
  static entry = LiveStreamWrapperComponent;
}
