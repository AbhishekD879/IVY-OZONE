import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { PrePlayPopularBetsRoutingModule } from './pre-play-popular-bets.routing.module';
import { PreplayPopularbetsComponent } from './pre-play-popular-bets.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  imports: [
    SharedModule,
    PrePlayPopularBetsRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    PreplayPopularbetsComponent
  ],
  entryComponents: [
    PreplayPopularbetsComponent
  ],
  providers: [],
  exports: [],
})
export class PreplayPopularbetsModule { }