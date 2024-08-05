import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MarketLinksEditComponent } from './market-links-edit/market-links-edit.component';
import { MarketLinksListComponent } from './market-links-list/market-links-list.component';

const MarketLinksRoutes: Routes = [
  {
    path: '',
    component: MarketLinksListComponent,
    children: []
  },
  { path: ':id',  component: MarketLinksEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(MarketLinksRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class MarketLinksRoutingModule { }
