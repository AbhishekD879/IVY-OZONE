import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CoralSportsSegmentProviderService } from './service/coralsports-segment-provider.service';
import { SegmentCacheManagerService } from './service/segment-cache-manager.service';

@NgModule({
  providers: [CoralSportsSegmentProviderService, SegmentCacheManagerService],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CoralSportsSegmentModule {
  // eslint-disable-next-line
  constructor() {
  }
}
