import { NgModule } from '@angular/core';
import { FanzoneFeaturedService } from '@app/fanzone/services/fanzone-featured-ms.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';

@NgModule({
  declarations: [],
  providers: [FanzoneAppModuleService, FanzoneFeaturedService,FanzoneSharedService,FanzoneGamesService]
})
export class FanzoneApiModule {}
