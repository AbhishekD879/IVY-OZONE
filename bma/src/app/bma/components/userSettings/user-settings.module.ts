import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { UserSettingsComponent } from '@bma/components/userSettings/user-settings.component';
import { UserSettingsRoutingModule } from '@bma/components/userSettings/user-settings-routing.module';
import { UserPreferenceProvider } from './user-settings.service';

@NgModule({
  imports: [
    UserSettingsRoutingModule,
    SharedModule
  ],
  declarations: [
    UserSettingsComponent,
  ],
  providers: [UserPreferenceProvider]
})

export class UserSettingsModule {
}
