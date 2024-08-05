import { Injectable, Injector } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { RacingEnhancedMultiplesService } from '@racing/components/racingEnhancedMultiples/racing-enhanced-multiples.service';
import { RacingGaService } from '@racing/services/racing-ga.service';

@Injectable()
export class RacingRunService {

 constructor(
   private commandService: CommandService,
   private injector: Injector,
   // eslint-disable-next-line
   private updateEventService: UpdateEventService // for events subscription (done in service init)
 ) { }

 run() {
   this.commandService.register(this.commandService.API.HR_ENHANCED_MULTIPLES_EVENTS, () => {
     return this.racingEnhancedMultiplesService.getEnhancedMultiplesEvents('horseracing').toPromise();
   });

   this.commandService.register(this.commandService.API.RACING_GA_SERVICE, () => {
     return Promise.resolve(this.racingGaService);
   });
 }

 private get racingEnhancedMultiplesService(): RacingEnhancedMultiplesService {
   return this.injector.get(RacingEnhancedMultiplesService);
 }
 private set racingEnhancedMultiplesService(value:RacingEnhancedMultiplesService){}
 private get racingGaService(): RacingGaService {
   return this.injector.get(RacingGaService);
 }
 private set racingGaService(value:RacingGaService){}
}
