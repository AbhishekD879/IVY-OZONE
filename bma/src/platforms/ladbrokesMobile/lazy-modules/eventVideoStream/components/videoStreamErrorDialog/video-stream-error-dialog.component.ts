import { Component } from '@angular/core';

import {
  VideoStreamErrorDialogComponent as VideoStreamErrorDialogBaseComponent
} from '@lazy-modules/eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component';

@Component({
  selector: 'video-stream-error-dialog',
  styleUrls: ['./video-stream-error-dialog.component.scss'],
  // eslint-disable-next-line
  templateUrl: '../../../../../../app/lazy-modules/eventVideoStream/components/videoStreamErrorDialog/video-stream-error-dialog.component.html'
})
export class VideoStreamErrorDialogComponent extends VideoStreamErrorDialogBaseComponent {
}
