import { IMarket } from '@core/models/market.model';
import { IDividend } from '@core/models/dividend.model';
import { IRuleDeduction } from '@core/models/rule-deduction.model';
import { IOutcome } from '@core/models/outcome.model';

export interface IRacingMarket extends IMarket {
  hasResults?: boolean;               // has at least one outcome with SP prices
  hasPositions?: boolean;             // has at least one resulted outcomes with position
  nonRunners?: IOutcome[];
  dividends?: IDividend[];
  unPlaced?: IOutcome[];
  outcomesWithoutPrices?: IOutcome[];
  rulesFourDeduction?: IRuleDeduction[];
  ncastTypeCodes?: string;
  lang?: string;
  description?: string;
  isHR?: boolean;
  isGH?: boolean;
  isNew?: boolean;
}

