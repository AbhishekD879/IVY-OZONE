
import { of as observableOf } from 'rxjs';
import { Injectable, Injector } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { YourcallService } from '@yourCallModule/services/yourcallService/yourcall.service';
import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { YOURCALL_DATA_PROVIDER } from '@yourcall/constants/yourcall-data-provider';
import { ISportEvent } from '@core/models/sport-event.model';

@Injectable({ providedIn: 'root' })
export class YourcallRunService {

 constructor(
   private commandService: CommandService,
   private injector: Injector
 ) {}

 run() {
   this.commandService.register(
     this.commandService.API.DS_WHEN_YC_READY,
     (ruleToCheck: string, useCache: boolean) => this.yourCallService.whenYCReady(ruleToCheck, useCache).toPromise()
   );

   this.commandService.register(
     this.commandService.API.DS_WHEN_YC_STATIC_BLOCKS_READY,
     () => this.yourCallService.getStaticBlocks()
   );
   this.commandService.register(
     this.commandService.API.DS_GET_GAME,
     (obGameId: string, catId: string) => this.yourCallMarketsService.getGame(obGameId, catId)
   );
   this.commandService.register(
     this.commandService.API.GET_YC_TAB,
     (event: ISportEvent) => this.yourCallService.getYCTab(event)
   );
   this.commandService.register(
     this.commandService.API.GET_5ASIDE_TAB,
     (event: ISportEvent) => this.yourCallService.get5ASideTab(event)
   );
   this.commandService.register(
     this.commandService.API.GET_YC_BETS,
     (betId: number) => this.yourCallProvider.useOnce(YOURCALL_DATA_PROVIDER.BYB).getBets(betId)
   );
   this.commandService.register(
     this.commandService.API.DS_IS_AVAILABLE_FOR_COMPETITION,
     (competitionId: number) => observableOf(this.yourCallService.isBYBIconAvailable(competitionId)).toPromise()
   );
   this.commandService.register(
    this.commandService.API.DS_IS_AVAILABLE_FOR_EVENTS,
    (eventId: number) => observableOf(this.yourCallService.isBYBIconAvailableForEvents(eventId)).toPromise()
  );
 }

 private get yourCallService(): YourcallService {
   return this.injector.get(YourcallService);
 }
 private set yourCallService(value:YourcallService){}

 private get yourCallMarketsService(): YourcallMarketsService {
   return this.injector.get(YourcallMarketsService);
 }
 private set yourCallMarketsService(value:YourcallMarketsService){}

 private get yourCallProvider(): YourcallProviderService {
   return this.injector.get(YourcallProviderService);
 }
 private set yourCallProvider(value:YourcallProviderService){}
}
