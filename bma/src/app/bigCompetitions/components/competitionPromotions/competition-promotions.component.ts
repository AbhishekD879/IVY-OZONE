import { Component, Input, OnInit } from '@angular/core';

import { ICompetitionModules } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'competition-promotions',
  templateUrl: './competition-promotions.html'
})
export class CompetitionPromotionsComponent implements OnInit {

  @Input() moduleConfig: ICompetitionModules;
  private readonly moduleName = rgyellow.PROMOTIONS;
  promotions: IPromotion[];
  constructor(protected bonusSuppressionService: BonusSuppressionService) {}
  ngOnInit(): void {
    if(!this.bonusSuppressionService.checkIfYellowFlagDisabled(this.moduleName)) {
      this.bonusSuppressionService.navigateAwayForRGYellowCustomer();
    }
    this.promotions = (this.moduleConfig.promotionsData && this.moduleConfig.promotionsData.promotions) || [];
  }
}
