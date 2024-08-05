import { AppRunnerSpotlightComponent } from '@coralDesktop/lazy-modules/runnerSpotlight/runner-spotlight.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopRunnerSpotlightTableComponent } from './runner-spotlight-table.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    AppRunnerSpotlightComponent,
    DesktopRunnerSpotlightTableComponent
  ],
  providers: [],
  exports: [
    AppRunnerSpotlightComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RunnerSpotlightModule {
  static entry = AppRunnerSpotlightComponent;
}
