import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { sportFanzoneRoutingModule } from './sport-fanzone-routing.module';
import { SharedModule } from '@root/app/shared/shared.module';
import { BetsbasedonmoduleComponent } from './bets-based-on-your-module/bets-based-on-module.component';

@NgModule({
  declarations: [
    BetsbasedonmoduleComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    sportFanzoneRoutingModule
  ]
})
export class SportFanzoneModule { }
