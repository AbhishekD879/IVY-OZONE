import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SportMainModule } from '@sbModule/components/sportMain/sport-main.module';
import { LazyEventRoutingModule } from './event-routing.module';
import { SportEventComponent } from '@sb/components/sportEvent/sport-event.component';

@NgModule({
  imports: [
    SportMainModule,

    LazyEventRoutingModule
  ],
  declarations: [
    SportEventComponent
  ],
  providers: [],
  exports: [
    SportEventComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyEventModule { }
