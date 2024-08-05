import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LadbrokesNextRacesModuleComponent as NextRacesModuleComponent} from '@ladbrokesDesktop/lazy-modules/nextRaces/component/next-races.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [NextRacesModuleComponent],
  exports: [NextRacesModuleComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class NextRacesModule {
  static entry = NextRacesModuleComponent;
}