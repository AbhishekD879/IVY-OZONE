import * as _ from 'underscore';
import { Injectable } from '@angular/core';

import { cashoutConstants } from '../../constants/cashout.constant';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { LocaleService } from '@core/services/locale/locale.service';
import { CashOutMapService } from '../cashOutMap/cash-out-map.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { CashoutErrorMessageService } from '../cashoutErrorMessageService/cashout-error-message.service';
import { CashoutDataProvider } from '../cashoutDataProvider/cashout-data.provider';

import { PartialCashOut } from '../../betModels/partialCashOut/partial-cash-out.class';
import { FullCashOut } from '../../betModels/fullCashOut/full-cash-out.class';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { CashoutBetsStreamService } from '@app/betHistory/services/cashoutBetsStream/cashout-bets-stream.service';
import { LiveServConnectionService } from '@core/services/liveServ/live-serv-connection.service';
import { DeviceService } from '@core/services/device/device.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable({ providedIn: BetHistoryApiModule })
export class CashOutService {

  readonly cashoutConstants = cashoutConstants;

  constructor(
   private localeService: LocaleService,
   private cashOutMapService: CashOutMapService,
   private gtm: GtmService,
   private toolsService: CoreToolsService,
   private filtersService: FiltersService,
   private cashOutErrorMessage: CashoutErrorMessageService,
   private cashoutDataProvider: CashoutDataProvider,
   private pubsub: PubSubService,
   private awsService: AWSFirehoseService,
   private liveServConnectionService: LiveServConnectionService,
   private clientUserAgentService: ClientUserAgentService,
   private cashoutBetsStreamService: CashoutBetsStreamService,
   private deviceService: DeviceService
   ) {}

  /**
   * Get new instance of partial cash out model
   * @return {PartialCashOut}
   */
  createPartialCashOut(): PartialCashOut {
    return new PartialCashOut(this.filtersService, this.localeService, this.cashOutMapService,
      this.gtm, this.cashoutDataProvider, this.toolsService, this.cashOutErrorMessage, this.pubsub,
      this.awsService, this.liveServConnectionService, this.clientUserAgentService, this.deviceService);
  }

  /**
   * Get new instance of full cash out instance
   * @return {FullCashOut}
   */
  createFullCashOut(): FullCashOut {
    return new FullCashOut(this.filtersService, this.localeService, this.cashOutMapService,
      this.gtm, this.cashoutDataProvider, this.toolsService, this.cashOutErrorMessage, this.pubsub,
      this.awsService, this.liveServConnectionService, this.clientUserAgentService, this.deviceService, this.cashoutBetsStreamService);
  }

  /**
   * Generates terms string
   * @param {object} part
   * @param {string} type
   * @returns {string|undefined}
   * @private
   */
  getEachWayTerms(part, type: string): string {
    if (!part) {
      return '';
    }
    let terms = part.eventMarketDesc || '',
      places;
    if (type && type.toUpperCase() === 'E' && part.eachWayPlaces) {
      places = _.map(Array(+part.eachWayPlaces), (val, index) => index + 1);
      terms += `, ${part.eachWayNum}/${part.eachWayDen} odds - places ${places.join(',')}`;
    }
    return terms;
  }
}
