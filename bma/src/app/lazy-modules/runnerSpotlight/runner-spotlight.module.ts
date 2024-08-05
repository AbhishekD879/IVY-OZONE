import { RunnerSpotlightComponent } from '@lazy-modules/runnerSpotlight/runner-spotlight.component';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { RunnerSpotlightTableComponent } from './runner-spotlight-table.component';

@NgModule({
  imports: [
    SharedModule
  ],
  declarations: [
    RunnerSpotlightComponent,
    RunnerSpotlightTableComponent
  ],
  providers: [],
  exports: [
    RunnerSpotlightComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RunnerSpotlightModule {
  static entry = RunnerSpotlightComponent;
}
