import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {OlympicsPagesListPageComponent} from './olympic-sports-page/pageComponent/olympics.page.component';
import {SharedModule} from '../../shared/shared.module';
import {SingleOlympicsPageComponent} from './single-olympics-page/pageComponent/olympics.page.component';
import {WidgetsRoutingModule} from './olympics-routing.module';
import {DialogService} from '../../shared/dialog/dialog.service';
import {OlympicsAPIService} from './service/olympics.api.service';
import {AddOlympicsPageComponent} from './olympic-sports-page/add-olympics-page-dialog/add-olympics-page.component';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    WidgetsRoutingModule
  ],
  declarations: [
    OlympicsPagesListPageComponent,
    SingleOlympicsPageComponent,
    AddOlympicsPageComponent
  ],
  providers: [
    DialogService,
    OlympicsAPIService
  ],
  entryComponents: [AddOlympicsPageComponent]
})
export class OlympicsModule { }
