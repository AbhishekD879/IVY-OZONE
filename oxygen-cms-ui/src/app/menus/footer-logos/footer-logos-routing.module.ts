import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { FooterLogosListComponent } from './footer-logos-list/footer-logos-list.component';
import { FooterLogosEditComponent } from './footer-logos-edit/footer-logos-edit.component';

const routes: Routes = [
  {
    path: 'footer-logos',
    component: FooterLogosListComponent,
    children: []
  },
  {
    path: 'footer-logos/:id', component: FooterLogosEditComponent
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
export class FooterLogosRoutingModule { }
