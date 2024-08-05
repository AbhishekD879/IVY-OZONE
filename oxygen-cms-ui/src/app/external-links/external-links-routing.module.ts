import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ExternalLinksPageComponent} from './external-links-page/external-links-page.component';
import {EditExternalLinkComponent} from './edit-external-link/edit-external-link.component';

const routes: Routes = [
  {
    path: '',
    component: ExternalLinksPageComponent
  }, {
    path: ':id',
    component: EditExternalLinkComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExternalLinksRoutingModule { }
