import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesDesktopUserSettingsComponent } from '@ladbrokesDesktop/bma/components/userSettings/user-settings.component';
import { UserSettingsRoutingModule } from '@ladbrokesDesktop/bma/components/userSettings/user-settings-routing.module';

@NgModule({
  imports: [
    SharedModule,
    UserSettingsRoutingModule
  ],
  declarations: [
    LadbrokesDesktopUserSettingsComponent
  ],
})

export class UserSettingsModule {
}
