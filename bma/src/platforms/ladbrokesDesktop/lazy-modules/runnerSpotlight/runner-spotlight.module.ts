import { DesktopRunnerSpotlightComponent } from '@ladbrokesDesktop/lazy-modules/runnerSpotlight/runner-spotlight.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesRunnerSpotlightTableComponent } from './runner-spotlight-table.component';
@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    DesktopRunnerSpotlightComponent,
    LadbrokesRunnerSpotlightTableComponent
  ],
  providers: [],
  exports: [
    DesktopRunnerSpotlightComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RunnerSpotlightModule {
  static entry = DesktopRunnerSpotlightComponent;
}
