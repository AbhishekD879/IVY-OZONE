import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { InplayHomeTabComponent } from '@bma/components/inlayHomeTab/inplay-home-tab.component';
import { InplayHomeTabRoutingModule } from '@bma/components/inlayHomeTab/inplay-home-tab.routing.module';

@NgModule({
  imports: [
    InplayHomeTabRoutingModule,
    SharedModule
  ],
  declarations: [
    InplayHomeTabComponent,
  ]
})

export class InplayHomeTabModule {
  static entry = InplayHomeTabComponent;
}
