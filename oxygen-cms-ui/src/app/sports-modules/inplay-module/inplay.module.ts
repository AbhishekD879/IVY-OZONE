import {NgModule} from '@angular/core';
import {InplayModuleComponent} from './module-page/inplay-module.component';
import {InplayRoutingModule} from './inplay-routing.module';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import { InplaySportCreateComponent } from './inplay-sport-create/inplay-sport-create.component';
import { InplaySportEditComponent } from './inplay-sport-edit/inplay-sport-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    InplayRoutingModule
  ],
  declarations: [
    InplayModuleComponent,
    InplaySportCreateComponent,
    InplaySportEditComponent
  ],
  entryComponents: [
    InplayModuleComponent,
    InplaySportCreateComponent
  ],
  providers: [],
  exports: []
})
export class InplayModule { }
