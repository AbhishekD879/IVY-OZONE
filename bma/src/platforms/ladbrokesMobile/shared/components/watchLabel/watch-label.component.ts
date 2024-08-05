import { ChangeDetectionStrategy, Component, ViewEncapsulation } from '@angular/core';

import { WatchLabelComponent } from '@shared/components/watchLabel/watch-label.component';

@Component({
  selector: 'watch-label',
  template: `<span [i18n]="'app.watch'" data-crlat="watchLive"></span>`,
  styleUrls: ['./watch-label.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesWatchLabelComponent extends WatchLabelComponent {}
