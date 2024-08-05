import { Injectable, Injector } from '@angular/core';

import { CommandService } from '@core/services/communication/command/command.service';
import { InplayDataService } from '@app/inPlay/services/inplayData/inplay-data.service';
import { InplaySubscriptionManagerService } from '@app/inPlay/services/InplaySubscriptionManager/inplay-subscription-manager.service';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { InplayApiModule } from '@app/inPlay/inplay-api.module';

@Injectable({
  providedIn: InplayApiModule
})
export class InplayRunService {

 constructor(
   private commandService: CommandService,
   private injector: Injector
 ) {}

 run() {
   this.commandService.register(this.commandService.API.LOAD_COMPETITION_EVENTS,
     (dataType: string, loadParams: IRequestParams = {}) => {
       return this.inPlayDataService.loadData(dataType, loadParams).toPromise();
     });
   this.commandService.register(this.commandService.API.SUBSCRIBE_FOR_LIVE_UPDATES,
     eventIds => {
       this.inPlaySubscriptionManager.subscribeForLiveUpdates(eventIds);
       return Promise.resolve(null);
     });
   this.commandService.register(this.commandService.API.UNSUBSCRIBE_FOR_LIVE_UPDATES,
     eventIds => {
       this.inPlaySubscriptionManager.unsubscribeForLiveUpdates(eventIds);
       return Promise.resolve(null);
     });
 }

 private get inPlayDataService(): InplayDataService {
   return this.injector.get(InplayDataService);
 }
 private set inPlayDataService(value:InplayDataService){}
 private get inPlaySubscriptionManager(): InplaySubscriptionManagerService {
   return this.injector.get(InplaySubscriptionManagerService);
 }
 private set inPlaySubscriptionManager(value:InplaySubscriptionManagerService){}
}
