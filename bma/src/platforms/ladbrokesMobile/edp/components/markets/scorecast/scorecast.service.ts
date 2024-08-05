import { Injectable } from '@angular/core';
import { ScorecastService as AppScorecastService } from '@edp/components/markets/scorecast/scorecast.service';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { HttpClient } from '@angular/common/http';
import { IScorecastLookupTable } from '@edp/components/markets/scorecast/scorecast.model';
import { GtmService } from '@core/services/gtm/gtm.service';

@Injectable()
export class ScorecastService extends AppScorecastService {
  private lookupTableData: IScorecastLookupTable;

  constructor(
    scoreMarketService: ScoreMarketService,
    isPropertyAvailableService: IsPropertyAvailableService,
    cashOutLabelService: CashOutLabelService,
    gtmService:GtmService,
    private http: HttpClient) {
    super(scoreMarketService, isPropertyAvailableService, cashOutLabelService, gtmService);
  }
}
