import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';

import {ManagementModule} from '../management/management.module';

import {HomeComponent} from './home.component';

import {HomeRoutingModule} from './home-routing.module';
import {GlobalLoaderComponent} from '../shared/globalLoader/loaderView/global-loader.component';
import {GlobalLoaderService} from '../shared/globalLoader/loader.service';

@NgModule({
  imports: [
    SharedModule,
    HomeRoutingModule,
    ManagementModule
  ],
  declarations: [
    HomeComponent,
    GlobalLoaderComponent
  ],
  providers: [
    GlobalLoaderService
  ]
})

export class HomeModule { }
