import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LadbrokesDesktopRacingEventModelComponent } from './racing-event-model.component';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@ladbrokesDesktop/desktop/desktop.module';


@NgModule({
  declarations: [
    LadbrokesDesktopRacingEventModelComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    DesktopModule
  ],
  exports: [LadbrokesDesktopRacingEventModelComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingEventModelModule {
  static entry = LadbrokesDesktopRacingEventModelComponent;
}
