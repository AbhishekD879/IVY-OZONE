import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';

import {
  SportsHighlightCarouselsRoutingModule
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels-routing.module';
import {
  HighlightCarouselsModuleComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels-module/highlight-carousels-module.component';
import {
  SportsHighlightCarouselListComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousel-list/highlight-carousel-list.component';
import {
  SportsHighlightCarouselComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousel/highlight-carousel.component';
import {
  SportsHighlightCarouselsService
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousels.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportsHighlightCarouselsRoutingModule
  ],
  declarations: [
    HighlightCarouselsModuleComponent,
    SportsHighlightCarouselListComponent,
    SportsHighlightCarouselComponent
  ],
  entryComponents: [
    HighlightCarouselsModuleComponent,
    SportsHighlightCarouselListComponent
  ],
  providers: [SportsHighlightCarouselsService],
  exports: []
})
export class SportsHighlightCarouselsModule {
}
