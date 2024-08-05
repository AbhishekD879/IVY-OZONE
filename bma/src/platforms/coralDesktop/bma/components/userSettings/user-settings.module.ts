import { NgModule } from '@angular/core';
import { CoralDesktopUserSettingsComponent } from '@coralDesktop/bma/components/userSettings/user-settings.component';
import { UserSettingsRoutingModule } from '@coralDesktop/bma/components/userSettings/user-settings-routing.module';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [
    UserSettingsRoutingModule,
    SharedModule
  ],
  declarations: [
    CoralDesktopUserSettingsComponent
  ]
})

export class UserSettingsModule {}
