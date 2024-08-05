import { Injectable, Injector } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';

@Injectable()
export class FavouritesRunService {

 constructor(
   private commandService: CommandService,
   private injector: Injector
 ) {}

 run() {
   this.commandService.register(
     this.commandService.API.SYNC_FAVOURITES_FROM_NATIVE,
       favourites => this.favouritesService.syncFromNative(favourites));
 }

 private get favouritesService(): FavouritesService {
   return this.injector.get(FavouritesService);
 }
 private set favouritesService(value:FavouritesService){}
}
