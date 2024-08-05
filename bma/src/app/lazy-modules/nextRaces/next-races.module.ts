import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NextRacesModuleComponent } from '@app/lazy-modules/nextRaces/component/next-races.component';
import { SharedModule } from '@sharedModule/shared.module';
import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [NextRacesModuleComponent],
  exports: [NextRacesModuleComponent],
  providers: [
    HorseracingService,
    GreyhoundService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class NextRacesModule {
  static entry = NextRacesModuleComponent;
}