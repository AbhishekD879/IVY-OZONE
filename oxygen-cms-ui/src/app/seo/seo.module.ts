import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {SeoPagesListPageComponent} from './seo-list-page/pageComponent/seo.page.component';
import {SharedModule} from '../shared/shared.module';
import {SingleSeoPageComponent} from './single-seo-page/pageComponent/seo.page.component';
import {WidgetsRoutingModule} from './seo-routing.module';
import {SeoAPIService} from './service/seo.api.service';
import {AddSeoPageComponent} from './seo-list-page/add-seo-page-dialog/add-seo-page.component';
import { AutoSeolistComponent} from './auto-seo-list/auto-seo-list.component';
import { AutoseoPageDialogComponent } from './auto-seo-list/auto-seo-dialog/auto-seo-dialog.component';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    WidgetsRoutingModule
  ],
  declarations: [
    SeoPagesListPageComponent,
    SingleSeoPageComponent,
    AddSeoPageComponent,
    AutoSeolistComponent,
    AutoseoPageDialogComponent
  ],
  providers: [
    SeoAPIService
  ],
  entryComponents: [AddSeoPageComponent]
})
export class SeoModule { }
