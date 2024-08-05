import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {
  HighlightCarouselsModuleComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels-module/highlight-carousels-module.component';
import {
  SportsHighlightCarouselComponent
} from '@app/sports-modules/highlight-carousels-module/highlight-carousels/highlight-carousel/highlight-carousel.component';

const routes: Routes = [
  {
    path: ':moduleId',
    component: HighlightCarouselsModuleComponent,
    children: []
  },
  {
    path: ':moduleId/carousel/edit/:carouselId',
    component: SportsHighlightCarouselComponent,
    children: []
  },
  {
    path: ':moduleId/carousel/create',
    component: SportsHighlightCarouselComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class SportsHighlightCarouselsRoutingModule {
}
