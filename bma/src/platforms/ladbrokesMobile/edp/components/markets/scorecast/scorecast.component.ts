import { Component, ComponentFactoryResolver, Input, OnInit } from '@angular/core';
import { ScorecastComponent as AppScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { ScorecastService } from '@ladbrokesMobile/edp/components/markets/scorecast/scorecast.service';
import { IScorecastLookupTable, IScorecastMarket, IScoreCastMarkets, ITeam } from '@app/edp/components/markets/scorecast/scorecast.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { DialogService } from '@app/core/services/dialogService/dialog.service';

import { BetslipSelectionsDataService } from '@app/core/services/betslipSelectionsData/betslip-selections-data';
import { PriceOddsButtonAnimationService } from '@app/shared/components/priceOddsButton/price-odds-button.animation.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';

@Component({
  selector: 'scorecast',
  templateUrl: 'scorecast.component.html'
})
export class ScorecastComponent extends AppScorecastComponent implements OnInit {

  @Input() eventEntity: ISportEvent;
  @Input() markets: IMarket[];
  @Input() memoryId: number | string;
  @Input() memoryLocation: string;
  @Input() isExpanded: boolean;

  scorecastMarkets: IScoreCastMarkets | any = {};
  selectedScorecastMarket: IScorecastMarket | any = {};
  cashoutAvail: boolean;
  teamsArray: ITeam[] = [];
  correctScore: IMarket;
  selectedGoalscorerTeamScorers: IOutcome[];
  cumulativeOddPriceToShow = {};
  scorecastScoresTeamH: any;
  scorecastScoresTeamA: any;
  scorecastKeys: string[];
  data = [];
  combinedData: any;
  goalscorerOutcome: IOutcome;
  correctScoreOutcome: IOutcome;
  team: ITeam;
  groupedOutcometest: any;
  showFG: boolean;
  showLG: boolean;
  lookupTableData:IScorecastLookupTable
  goalscorer: any[];
  loaded: boolean;


  constructor(
    protected fracToDecFactory: FracToDecService,
    protected scorecastService: ScorecastService,
    protected betSlipSelectionsData: BetslipSelectionsDataService,
    protected priceOddsButtonService: PriceOddsButtonAnimationService,
    protected pubsubService: PubSubService,
    protected localeService: LocaleService,
    protected filterService: FiltersService,
    protected componentFactoryResolver: ComponentFactoryResolver,
    protected dialogService: DialogService,
    protected scorecastDataService: ScorecastDataService
    ) {
    super(fracToDecFactory, scorecastService, betSlipSelectionsData, priceOddsButtonService, pubsubService, localeService, filterService, scorecastDataService);
  }
  }
