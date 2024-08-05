import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { FavouritesService } from '@app/favourites/services/favourites.service';

export const FavouritesRouteGuard:CanActivateFn = () => {
  return inject(FavouritesService).showFavourites();
}
