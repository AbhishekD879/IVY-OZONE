import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateFreebetSignpostingComponent } from './freebet/freebet-signposting/create-freebet-signposting/create-freebet-signposting.component';
import { FreebetSignpostingListComponent } from './freebet/freebet-signposting/freebet-signposting-list.component';

const route: Routes = [
  {
    path: '',
    component: FreebetSignpostingListComponent,
    children: []
  },
  { path: 'freebet-signposting', component: FreebetSignpostingListComponent },
  { path: 'freebet-signposting/create-signpost', component: CreateFreebetSignpostingComponent },
  { path: 'freebet-signposting/:id', component: CreateFreebetSignpostingComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(route)
  ],
  exports: [
    RouterModule
  ]
})
export class SignpostingRoutingModule { }
