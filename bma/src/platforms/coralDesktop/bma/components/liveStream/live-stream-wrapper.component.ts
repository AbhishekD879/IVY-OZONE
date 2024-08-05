import { Component } from '@angular/core';
import { LiveStreamWrapperComponent } from '@app/bma/components/liveStream/live-stream-wrapper.component';

@Component({
  selector: 'live-stream-wrapper',
  templateUrl: 'live-stream-wrapper.component.html'
})
export class DesktopLiveStreamWrapperComponent extends LiveStreamWrapperComponent {}
