import { Injectable } from '@angular/core';
import * as _ from 'underscore';

// Models
import { IMarket } from '@core/models/market.model';
import { IGroupedMarket, IMarketsGroup } from '@edp/services/marketsGroup/markets-group.model';

// Constants
import { MARKETS_GROUP } from '@sharedModule/constants/markets-group.constant';

// Services
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TemplateService } from '@app/shared/services/template/template.service';

@Injectable()
export class FootballExtensionService {
  constructor(
    private marketsGroupFactory: MarketsGroupService,
    private pubsub: PubSubService,
    private templateService: TemplateService
  ) {}

  public eventMarkets(parentScope): void {
    // sets tabs where scorecast Market should be shown
    parentScope.scorecastInTabs = ['main', 'all-markets'];

    // check if event has scoreCastMarkets
    const scorecastPattern = new RegExp('^(first|last)\\sgoal\\s?scorecast$', 'i');
    const scorerPattern = new RegExp('^(first|last)\\sgoal\\s?scorer$', 'i');
    const isScorecastMatched = parentScope.sport.isAnyMarketByPattern(parentScope.eventEntity.markets, scorecastPattern);
    parentScope.isScorecastMarketsAvailable = isScorecastMatched &&
      parentScope.sport.isAnyMarketByPattern(parentScope.eventEntity.markets, scorerPattern);
    if (isScorecastMatched) {
      _.each(parentScope.eventEntity.markets, (market: IMarket) => {
        if (market.name.toString().match(scorecastPattern) !== null) {
          market.hidden = true;
        }
      });
    }

    if (!parentScope.isSpecialEvent) {
      this.generateMarketsGroups(parentScope);
      this.pubsub.subscribe('marketsGroup', 'UPDATE_OUTCOMES_FOR_MARKET', updatedMarket => {
        const marketEntity: IMarket = _.find(parentScope.eventEntity.markets, (market: IMarket) => market.id === updatedMarket.id);
        if (marketEntity) {
          this.marketsGroupFactory.updateMarketsGroup(marketEntity, parentScope.marketConfig);
        }
      });
    }
  }

  /**
   * Generate Grouped Market with column and switchers
   * @param parentScope
   */
  private generateMarketsGroups(parentScope): void {
    parentScope.marketConfig = MARKETS_GROUP;
    parentScope.marketConfig = MARKETS_GROUP.filter(market => {
      return !((market.name === 'Popular Goalscorer Markets' && !this.templateService.getPopularScorer())
      || (market.name === 'Other Goalscorer Markets' && !this.templateService.getOtherScorer() ));
      });
    // Live Market available and grouped market should be renewed in case
    // this market with (templateMarketName) belongs to grouped market
    if (parentScope.liveMaketTemplateMarketName) {
      const groups: IMarketsGroup[] = this.marketsGroupFactory
        .templateMarketInMarketsGroups(parentScope.marketConfig, parentScope.liveMaketTemplateMarketName);
      groups.forEach(group => {
        const mGIndex = _.findIndex(parentScope.marketGroup, (mG: IMarketsGroup) => mG.localeName === group.localeName);
        if (mGIndex !== -1) {
          parentScope.marketGroup.splice(mGIndex, 1);
        }
      });
    }
    parentScope.marketAvailable = {};
    _.each(parentScope.marketConfig, (marketConfig: IGroupedMarket) => {
      const isMarketAvailable = this.marketsGroupFactory
        .isMarketAvailable(parentScope.eventEntity.markets, parentScope.marketGroup, marketConfig);
      parentScope.marketAvailable[marketConfig.localeName] = isMarketAvailable;
      if (isMarketAvailable) {
        const isGroupExist: boolean = !!_.find(parentScope.marketGroup, { localeName: marketConfig.localeName });
        if (isGroupExist) {
          this.marketsGroupFactory.groupMarkets(parentScope.eventEntity.markets, marketConfig);
        } else {
          const marketsGroup = this.marketsGroupFactory.generateMarketsGroup(parentScope.eventEntity.markets, marketConfig);
          parentScope.marketGroup.push(marketsGroup);
        }
      }
    });
  }
}
