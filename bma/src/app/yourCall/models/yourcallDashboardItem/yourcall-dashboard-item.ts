import { IYourcallSelection } from '@yourcall/models/selection.model';
import { IYourCallMarket } from '@app/core/services/cms/models';
import { YourCallMarketPlayer } from '@yourcall/models/markets/yourcall-market-player';

export class YourCallDashboardItem {
  market: IYourCallMarket | YourCallMarketPlayer;
  selection: IYourcallSelection;

  constructor(data: {market: IYourCallMarket | YourCallMarketPlayer; selection: IYourcallSelection}) {
    this.market = data.market;
    this.selection = data.selection;
  }

  /**
   * Get selections market title
   * @returns {string|*|{value}}
   */
  getMarketTitle(): string {
    return this.market.getTitle();
  }

  /**
   * Get selection value title
   * @returns {*|string}
   */
  getSelectionTitle(): string {
    return (this.market as IYourCallMarket).getSelectionTitle(this.selection);
  }

  /**
   * Get item title
   * @returns {string}
   */
  getTitle(): string {
    return (`${this.getMarketTitle()} ${this.getSelectionTitle()}`).trim();
  }

  /**
   * Get betslip item title
   * @returns {*|string}
   */
  getBetslipTitle(): string {
    const formattedTitle = this.getBetslipFormattedTitle()?.toLowerCase();
    if (formattedTitle) {
      return `<strong class="value">${formattedTitle}</strong>`;
    }

    return (this.market as IYourCallMarket).getBetslipTitle(this.selection);
  }

  private getBetslipFormattedTitle(): string {
    const mktTitle = this.market.title.toUpperCase();

    // To score N or more goals
    const match = mktTitle.match(/^TO SCORE (\d+) OR MORE GOALS$/i);
    if (match) {
      return `${this.selection.title} To Score ${match[1]}+ Goals`;
    }

    // Anytime goalscorer
    if (mktTitle === 'ANYTIME GOALSCORER') {
      return `${this.selection.title} Anytime Goalscorer`;
    }

    // To be shown a card
    if (mktTitle === 'TO BE SHOWN A CARD') {
      return `${this.selection.title} To Be Carded`;
    }

    return '';
  }
}
