import { Injectable, Injector } from '@angular/core';

import * as bethistoryLangData from '@localeModule/translations/en-US/bethistory.lang';

import { BetHistoryApiModule } from '@app/betHistory/bet-history-api.module';

import { CommandService } from '@core/services/communication/command/command.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { BetsIntegrationService } from '@betHistoryModule/services/betsIntegration/bets-integration.service';
import { CashoutBetsStreamService } from '@betHistoryModule/services/cashoutBetsStream/cashout-bets-stream.service';
import { OpenBetsCounterService } from '@app/betHistory/services/openBetsCounter/open-bets-counter.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class BetHistoryRunService {
 constructor(
   private commandService: CommandService,
   private localeService: LocaleService,
   protected injector: Injector
 ) {}

 run() {
   this.localeService.setLangData(bethistoryLangData);
   this.commandService.register(this.commandService.API.GET_CASH_OUT_BETS_ASYNC,
     () => {
       return this.betsIntegrationService.getCashOutBets().toPromise();
     });
   this.commandService.register(this.commandService.API.GET_PLACED_BETS_ASYNC,
     (eventId) => {
       return this.betsIntegrationService.getPlacedBets(eventId).toPromise();
     });
   this.commandService.register(this.commandService.API.GET_BETS_FOR_EVENT_ASYNC,
     (eventId, cashoutBetsArray, placedBetsArray) => {
       return this.betsIntegrationService.getBetsForEvent(eventId, cashoutBetsArray, placedBetsArray).toPromise();
     });
   this.commandService.register(this.commandService.API.OPEN_CASHOUT_STREAM, () => {
     return this.cashoutBetsStreamService.openBetsStream().toPromise();
   });
   this.commandService.register(this.commandService.API.CLOSE_CASHOUT_STREAM, () => {
     this.cashoutBetsStreamService.closeBetsStream();
     return Promise.resolve();
   });
   this.commandService.register(this.commandService.API.GET_OPEN_BETS_COUNT, () => {
     return Promise.resolve(this.openBetsCounterService.init());
   });
   this.commandService.register(this.commandService.API.UNSUBSCRIBE_OPEN_BETS_COUNT, () => {
    this.openBetsCounterService.unsubscribeBetsCounter();
    return Promise.resolve();
  });
 }

 protected get openBetsCounterService(): OpenBetsCounterService {
   return this.injector.get(OpenBetsCounterService);
 }
 protected set openBetsCounterService(value: OpenBetsCounterService){}
 private get betsIntegrationService(): BetsIntegrationService {
   return this.injector.get(BetsIntegrationService);
 }
 private set betsIntegrationService(value: BetsIntegrationService){}
 private get cashoutBetsStreamService(): CashoutBetsStreamService {
   return this.injector.get(CashoutBetsStreamService);
 }
 private set cashoutBetsStreamService(value: CashoutBetsStreamService){}
}
