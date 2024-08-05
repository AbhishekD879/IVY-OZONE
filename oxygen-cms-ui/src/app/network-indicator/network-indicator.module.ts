import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';
import {ManagementModule} from '../management/management.module';
import { NetworkIndicatorComponent } from './network-indicator.component';
import { NetworkIndicatorRoutingModule } from './network-indicator-routing.module';

@NgModule({
  imports: [
    SharedModule,
    ManagementModule,
    NetworkIndicatorRoutingModule
  ],
  declarations: [
    NetworkIndicatorComponent
  ],
  providers: [
  ]
})

export class NetworkIndicatorModule { }
