import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { PopularBetsRoutingModule } from './popular-bets.routing.module';
import { PopularbetsComponent } from './popular-bets.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PopularAccasWidgetComponent } from './popular-accas-widget/popular-accas-widget.component';
import { PopularAccasWidgetCardComponent } from './popular-accas-widget-card/popular-accas-widget-card.component';


@NgModule({
  imports: [
    SharedModule,
    PopularBetsRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    PopularbetsComponent,
    PopularAccasWidgetComponent,
    PopularAccasWidgetCardComponent
  ],
  providers: [],
  entryComponents: [
    PopularbetsComponent,
    PopularAccasWidgetComponent,
    PopularAccasWidgetCardComponent
  ]
})
export class PopularbetsModule { }