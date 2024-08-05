import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TopSportsListComponent } from '@app/virtual-sports/top-sports/top-sports-list/top-sports-list.component';
import { TopSportsCreateAndUpdateComponent } from '@app/virtual-sports/top-sports/top-sports-create-and-update/top-sports-create-and-update.component';


const routes: Routes = [
  { path: '', component: TopSportsListComponent },
  { path: 'top-sports', component: TopSportsListComponent },
  { path: 'create-top-sport', component: TopSportsCreateAndUpdateComponent },
  { path: ':id', component: TopSportsCreateAndUpdateComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})

export class TopSportsRoutingModule { }
