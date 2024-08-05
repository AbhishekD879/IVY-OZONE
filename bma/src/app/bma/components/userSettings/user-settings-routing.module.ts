import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { UserSettingsComponent } from '@bma/components/userSettings/user-settings.component';

const routes: Routes = [
  {
    path: '',
    component: UserSettingsComponent,
    data: {
      segment: 'settings'
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class UserSettingsRoutingModule {}

