import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { NetworkIndicatorComponent } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [
    NetworkIndicatorComponent,
  ],
  exports: [
    NetworkIndicatorComponent,
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class NetworkIndicatorModule {
  static entry = NetworkIndicatorComponent;
}
