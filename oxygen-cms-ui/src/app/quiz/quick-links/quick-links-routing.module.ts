import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {QuickLinksListComponent} from '@app/quiz/quick-links/quick-links-list/quick-links-list.component';
import {QuickLinksAddComponent} from '@app/quiz/quick-links/quick-links-add/quick-links-add.component';
import {QuickLinksEditComponent} from '@app/quiz/quick-links/quick-links-edit/quick-links-edit.component';

const routes: Routes = [{
  path: '',
  component: QuickLinksListComponent
},
  {
    path: 'quick-link/:id',
    component: QuickLinksEditComponent
  },
  {
    path: 'create',
    component: QuickLinksAddComponent
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class QuickLinksRoutingModule { }
