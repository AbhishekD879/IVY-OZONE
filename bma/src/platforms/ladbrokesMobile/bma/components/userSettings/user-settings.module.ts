  import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesUserSettingsComponent } from '@ladbrokesMobile/bma/components/userSettings/user-settings.component';
import { UserSettingsRoutingModule } from '@ladbrokesMobile/bma/components/userSettings/user-settings-routing.module';
@NgModule({
  imports: [
    UserSettingsRoutingModule,
    SharedModule
  ],
  declarations: [
    LadbrokesUserSettingsComponent,
  ],
  providers: []
})

export class LadbrokesUserSettingsModule {
}
