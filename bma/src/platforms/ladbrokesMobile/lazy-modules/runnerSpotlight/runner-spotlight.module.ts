import { LadbrokesRunnerSpotlightComponent } from '@ladbrokesMobile/lazy-modules/runnerSpotlight/runner-spotlight.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { MobileRunnerSpotlightTableComponent } from './runner-spotlight-table.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    LadbrokesRunnerSpotlightComponent,
    MobileRunnerSpotlightTableComponent
  ],
  providers: [],
  exports: [
    LadbrokesRunnerSpotlightComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RunnerSpotlightModule {
  static entry = LadbrokesRunnerSpotlightComponent;
}
