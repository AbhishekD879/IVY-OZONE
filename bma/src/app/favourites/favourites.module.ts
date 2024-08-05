import { APP_INITIALIZER, NgModule } from '@angular/core';

import { FavouritesService } from '@app/favourites/services/favourites.service';
import { FavouritesMatchesService } from '@app/favourites/services/favourites-matches.service';
import { FavouritesStorageService } from '@app/favourites/services/favourites-storage.service';
import { run } from '@app/favourites/services/favouritesRunService/favourites-run-function';
import { SharedModule } from '@sharedModule/shared.module';
import { FavouritesMatchesComponent } from '@app/favourites/components/matchList/favourites-matches.component';

import { FavouritesRunService } from '@app/favourites/services/favouritesRunService/favourites-run.service';

@NgModule({
  imports: [
    SharedModule
  ],
  exports: [ FavouritesMatchesComponent ],
  declarations: [ FavouritesMatchesComponent ],
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
})
export class FavouritesModule {}
