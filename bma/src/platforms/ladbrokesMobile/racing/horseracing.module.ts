import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingModule } from './racing.module';
import { HorseracingRoutingModule } from './horseracing-routing.module';

@NgModule({
  declarations: [],
  imports: [
    RacingModule,
    HorseracingRoutingModule
  ],
  exports: [],
  providers: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class HorseracingModule {}
