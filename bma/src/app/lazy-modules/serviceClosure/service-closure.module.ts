import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { ServiceClosureService } from '@lazy-modules/serviceClosure/service-closure.service';

@NgModule({
  providers: [ServiceClosureService],
  schemas: [NO_ERRORS_SCHEMA]
})

export class ServiceClosureModule {
  constructor(private serviceClosureService: ServiceClosureService) {
  }
}
