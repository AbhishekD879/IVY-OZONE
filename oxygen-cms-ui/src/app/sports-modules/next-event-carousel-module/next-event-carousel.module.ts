import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { NextEventCarouselComponent } from './next-event-carousel/next-event-carousel.component';
import { NextEventCarouselRoutingModule } from './next-event-carousel-routing.module';
import { NextEventCarouselListComponent } from './next-event-carousel-list/next-event-carousel-list.component';
import { SportsNextEventCarouselsService } from '@root/app/client/private/services/http/sportsNextEventCarousels.service';
import { NextEventCarouselFormComponent } from './next-event-carousel-form/next-event-carousel-form.component';

@NgModule({
  declarations: [NextEventCarouselComponent, NextEventCarouselListComponent, NextEventCarouselFormComponent],
  imports: [
    CommonModule,
    SharedModule,
    NextEventCarouselRoutingModule
  ],
  entryComponents: [
    NextEventCarouselComponent
  ],
  providers: [SportsNextEventCarouselsService],
})
export class NextEventCarouselModule { }
