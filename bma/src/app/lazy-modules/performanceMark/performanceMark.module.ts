import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { PerformanceMarkService } from './service/performance-mark.service';
@NgModule({
  providers: [PerformanceMarkService],
  schemas: [NO_ERRORS_SCHEMA]
})
export class PerformanceMarkModule {
   // eslint-disable-next-line
  constructor(private performanceMarkService: PerformanceMarkService) {
  }
}
