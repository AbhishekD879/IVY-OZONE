import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Injectable({ providedIn: BetslipApiModule })
export class BetSelections {

  selectionsData: any[] = []; // IBetSelection[] | BetSelection[]

  constructor(
    public pubSubService: PubSubService
  ) {}

  get data(): any[] {
    return this.selectionsData;
  }

  set data(data: any[]) {
    this.selectionsData = data;
    this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_SELECTIONS_UPDATE, this.selectionsData);
  }
}
