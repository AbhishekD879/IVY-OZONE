import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DesktopRacingEventModelComponent } from '@lazy-modules/racingEventModel/racing-event-model.component';
import { SharedModule } from '@sharedModule/shared.module';


@NgModule({
  declarations: [
    DesktopRacingEventModelComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports: [DesktopRacingEventModelComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingEventModelModule {
  static entry = DesktopRacingEventModelComponent;
}
