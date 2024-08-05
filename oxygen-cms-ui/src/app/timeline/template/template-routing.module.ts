import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {TemplateListComponent} from '@app/timeline/template/template-list/template-list.component';
import {TemplateEditComponent} from '@app/timeline/template/template-edit/template-edit.component';

const routes: Routes = [
  {
    path: '',
    component: TemplateListComponent
  },
  {
    path: ':id',
    component: TemplateEditComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TemplateRoutingModule { }
