import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [SharedModule],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class InPlaySportTabModule {
}