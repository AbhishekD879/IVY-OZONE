import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { FavouritesService } from '@app/favourites/services/favourites.service';
import { FavouritesMatchesService } from '@app/favourites/services/favourites-matches.service';
import { FavouritesStorageService } from '@app/favourites/services/favourites-storage.service';
import { run } from '@app/favourites/services/favouritesRunService/favourites-run-function';
import { SharedModule } from '@sharedModule/shared.module';

import { FavouritesRunService } from '@app/favourites/services/favouritesRunService/favourites-run.service';

// Overridden
import { DesktopFavouritesMatchesComponent } from '@coralDesktop/favourites/components/matchList/favourites-matches.component';

@NgModule({
  imports: [
    SharedModule
  ],
  exports: [
    DesktopFavouritesMatchesComponent
  ],
  declarations: [
    DesktopFavouritesMatchesComponent
  ],
  providers: [
    FavouritesRunService,
    FavouritesService,
    FavouritesMatchesService,
    FavouritesStorageService,
    {
      provide: APP_INITIALIZER,
      useFactory: run,
      deps: [FavouritesRunService],
      multi: true
    }
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class FavouritesModule {}
