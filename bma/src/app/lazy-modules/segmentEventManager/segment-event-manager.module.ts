import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CoralSportsSegmentModule } from '@lazy-modules/coralSportsSegmentProvider/coralsports-segment.module';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { SegmentLogService } from './service/segmented-logs.service';

@NgModule({
  providers: [SegmentLogService],
  schemas: [NO_ERRORS_SCHEMA],
  imports: [CoralSportsSegmentModule]
})
export class SegmentEventManagerModule {
  // eslint-disable-next-line
  constructor(private segmentEventManagerService: SegmentEventManagerService,
    private segmentLogService: SegmentLogService) {
  }
}
