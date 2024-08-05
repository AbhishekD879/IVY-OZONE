import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {StaticTextOtfRoutingModule} from './static-text-routing.module';
import {StaticTextOtfCreateComponent} from './static-text-create/static-text.create.component';
import {StaticTextOtfListComponent} from './static-text-list/static-text-list.page.component';
import {StaticTextOtfComponent} from './static-text-edit/pageComponent/static-text-edit.component';
import {StaticTextOtfAPIService} from '../service/staticTextOtf.api.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    StaticTextOtfRoutingModule
  ],
  declarations: [
    StaticTextOtfListComponent,
    StaticTextOtfComponent,
    StaticTextOtfCreateComponent
  ],
  providers: [
    StaticTextOtfAPIService
  ],
  entryComponents: [
    StaticTextOtfCreateComponent
  ]
})
export class StaticTextOtfModule { }
