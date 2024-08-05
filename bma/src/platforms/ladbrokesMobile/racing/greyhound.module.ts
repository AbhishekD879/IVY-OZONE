import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { RacingModule } from './racing.module';
import { GreyhoundRacingRoutingModule } from './greyhound-routing.module';

@NgModule({
  declarations: [],
  imports: [
    RacingModule,
    GreyhoundRacingRoutingModule
  ],
  exports: [],
  providers: [],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class GreyhoundModule {}
