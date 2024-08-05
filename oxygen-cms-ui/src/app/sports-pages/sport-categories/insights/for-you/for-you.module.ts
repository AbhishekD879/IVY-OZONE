import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { foryoumainComponent } from './for-you-main/for-you-main.component';
import { ForyoupersonalizedComponent } from './for-you-personalized/for-you-personalized.component';
import { ForYouRoutingModule } from './for-you-routing.module';
import { ForYouService } from './for-you-personalized/for-you.service';


@NgModule({
  declarations: [
    foryoumainComponent,
    ForyoupersonalizedComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    ForYouRoutingModule
  ],
  providers: [
    ForYouService
  ]
})
export class ForYouModule { }
