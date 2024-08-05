import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DeleteSegmentsComponent } from './delete-segments.component';

const DeleteSegmentsRoutes: Routes = [
  {
    path: '',
    component: DeleteSegmentsComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(DeleteSegmentsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class DeleteSegmentsRoutingModule { }
