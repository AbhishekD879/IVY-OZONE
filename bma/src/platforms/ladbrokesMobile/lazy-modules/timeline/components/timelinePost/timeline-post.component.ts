import { Component } from '@angular/core';
import { TimelinePostComponent } from '@lazy-modules/timeline/components/timelinePost/timeline-post.component';

@Component({
  selector: 'timeline-post',
  templateUrl: '../../../../../../app/lazy-modules/timeline/components/timelinePost/timeline-post.component.html',
  styleUrls: ['../../../../../../app/lazy-modules/timeline/components/timelinePost/timeline-post.component.scss']
})
export class LadsTimelinePostComponent extends TimelinePostComponent {}
