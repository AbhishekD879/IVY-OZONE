import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { DevLogRoutingModule } from '@lazy-modules/devLog/dev-log-routing.module';
import { DevLogComponent } from '@lazy-modules/devLog/components/devLog/dev-log.component';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [
    SharedModule,
    DevLogRoutingModule
  ],
  declarations: [
    DevLogComponent
  ],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class DevLogModule {
  static entry = DevLogComponent;
}
