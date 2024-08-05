import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { FavouritesMatchesComponent } from './components/matchList/favourites-matches.component';
import { FavouritesRouteGuard } from '@app/favourites/favourites-route.guard';

export const routes: Routes = [
  {
    path: 'favourites',
    component: FavouritesMatchesComponent,
    data: {
      segment: 'favourites'
    },
    canActivate: [FavouritesRouteGuard]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class FavouritesRoutingModule {
}
