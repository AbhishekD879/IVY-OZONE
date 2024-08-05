import { Component } from '@angular/core';
import { TimelineComponent } from '@lazy-modules/timeline/components/timeline/timeline.component';

@Component({
  selector: 'timeline',
  templateUrl: '../../../../../../app/lazy-modules/timeline/components/timeline/timeline.component.html',
  styleUrls: ['../../../../../../app/lazy-modules/timeline/components/timeline/timeline.component.scss'],
})
export class LadsTimelineComponent extends TimelineComponent {}
