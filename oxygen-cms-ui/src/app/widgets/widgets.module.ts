import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {WidgetsPageComponent} from './all-widgets-page/pageComponent/widgets.page.component';
import {SharedModule} from '../shared/shared.module';
import {WidgetPageComponent} from './single-widget-page/pageComponent/widget.page.component';
import {WidgetsRoutingModule} from './widgets-routing.module';
import {WidgetsAPIService} from './service/widgets.api.service';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    WidgetsRoutingModule
  ],
  declarations: [
    WidgetsPageComponent,
    WidgetPageComponent
  ],
  providers: [
    WidgetsAPIService
  ]
})
export class WidgetsModule { }
