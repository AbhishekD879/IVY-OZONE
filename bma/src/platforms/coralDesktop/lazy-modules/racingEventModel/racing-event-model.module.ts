import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CoralDesktopRacingEventModelComponent } from './racing-event-model.component';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@coralDesktop/desktop/desktop.module';


@NgModule({
  declarations: [
    CoralDesktopRacingEventModelComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    DesktopModule
  ],
  exports: [CoralDesktopRacingEventModelComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingEventModelModule {
  static entry = CoralDesktopRacingEventModelComponent;
}
