export class YourCallBet {
  public freebet: any;
  public token: string;
  public currency: string;
  public currencyName: string;
  public stake: any = null;
  public stakeAmount: number = 0;
  public potentialPayout: string = '0.00';
  public hasLP: boolean = true;
  public typeId: any;
  public eventId: any;
  public oldOddsValue: any;
  public newOddsValue: any = null;
  public betOdds: any;
  public betOddsFract: any;
  public selections: any;
  public game: any;
  public isYourCallBet: boolean = true;
  public channel: string;
  public price: any = {
    isPriceChanged: false,
    isPriceUp: false,
    isPriceDown: false
  };
  public disabled: boolean;
  freebetValue: number;
  public classId: string;
  public categoryId: string;
  private _oddsFormat: any;
  typeName: string;
  categoryName: string;

  constructor({ dashboardData, odds, oddsFract, currencySymbol, currency, token, oddsFormat, channel }) {
    this._oddsFormat = oddsFormat;
    this.selections = dashboardData.selections;
    this.classId = dashboardData.classId;
    this.categoryId = dashboardData.categoryId;
    this.token = token;
    this.currency = currencySymbol;
    this.currencyName = currency;
    this.typeId = dashboardData.game.obTypeId;
    this.eventId = dashboardData.game.obEventId;
    this.oldOddsValue = this._oddsFormat === 'dec' ? parseFloat(odds).toFixed(2) : oddsFract;
    this.betOdds = odds;
    this.betOddsFract = oddsFract;
    this.selections = dashboardData.selections;
    this.game = dashboardData.game;
    this.channel = channel;
  }

  /**
   * Calculate Estimated Returns for single selection
   * @return {string}
   */
  getPotentialPayout() {
    const stake = (Number(this.stake) || 0) + (this.freebetValue || 0);
    return (stake * parseFloat(this.betOdds)).toFixed(2);
  }

  /**
   * Handler for selection's stake change.
   */
  onStakeChange() {
    this.stakeAmount = parseFloat(this.stake) || 0;
    this.potentialPayout = this.getPotentialPayout();
  }

  /**
   * Handler for selection's odds change.
   */
  onOddsChange(odds, betOddsFract) {
    this.betOdds = odds;
    this.betOddsFract = betOddsFract;
    this.onStakeChange();
  }
}
