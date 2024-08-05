import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {EndPageListComponent} from '@app/quiz/end-page/end-page-list/end-page-list.component';
import {EndPageEditComponent} from '@app/quiz/end-page/end-page-edit/end-page-edit.component';
import {EndPageCreateComponent} from '@app/quiz/end-page/end-page-create/end-page-create.component';

const routes: Routes = [
  {
    path: '',
    component: EndPageListComponent
  },
  {
    path: 'edit/:id',
    component: EndPageEditComponent
  },
  {
    path: 'create',
    component: EndPageCreateComponent
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EndPageRoutingModule {
}
