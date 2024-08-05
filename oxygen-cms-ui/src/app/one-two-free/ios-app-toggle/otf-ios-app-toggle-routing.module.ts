import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {OtfIosAppTogglePageComponent} from '@app/one-two-free/ios-app-toggle/page/otf-ios-app-toggle-page.component';

const otfIosAppToggleRoutes: Routes = [
  {
    path: '',
    component: OtfIosAppTogglePageComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(otfIosAppToggleRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OtfIosAppToggleRoutingModule {

}
