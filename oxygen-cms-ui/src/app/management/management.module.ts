import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { SharedModule } from '../shared/shared.module';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { LeftMenuComponent } from './left-menu/left-menu.component';

@NgModule({
  imports: [
    RouterModule,
    SharedModule
  ],
  declarations: [HeaderMenuComponent, LeftMenuComponent],
  exports: [HeaderMenuComponent, LeftMenuComponent]
})
export class ManagementModule { }
