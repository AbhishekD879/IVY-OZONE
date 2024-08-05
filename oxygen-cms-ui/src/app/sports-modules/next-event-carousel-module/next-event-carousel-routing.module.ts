import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NextEventCarouselComponent } from './next-event-carousel/next-event-carousel.component';
import { NextEventCarouselFormComponent } from './next-event-carousel-form/next-event-carousel-form.component';


const routes: Routes = [
  {
    path: ':moduleId',
    component: NextEventCarouselComponent,
    children: []
  },
  {
    path: ':moduleId/carousel/edit/:nextEventId',
    component: NextEventCarouselFormComponent,
    children: []
  },
  {
    path: ':moduleId/carousel/create',
    component: NextEventCarouselFormComponent,
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
export class NextEventCarouselRoutingModule { }
