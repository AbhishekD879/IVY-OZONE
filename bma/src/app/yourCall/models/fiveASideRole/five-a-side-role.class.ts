import { IFiveASidePlayer } from '@yourcall/services/fiveASide/five-a-side.model';
import { IMatrixFormation } from '@yourcall/models/five-a-side.model';
import { FiveASideBetService } from '@yourcall/services/fiveASideBet/five-a-side-bet.service';
import { PLAYER_MARKETS } from '@yourcall/constants/five-a-side.constant';
import environment from '@environment/oxygenEnvConfig';

export class FiveASideRole {
  player: IFiveASidePlayer;
  role: IMatrixFormation;
  statValue: number = 0;
  statId: number;
  playerName: string;
  playerId: number;
  hasConflict: boolean = false;
  playerIconBackground: string;
  marketTitle: string;
  shortHandMarketTitle?: string;
  teamsImage: string;
  fiveASideToggle: boolean;
  readonly TEAMSIMAGEPATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  private primaryTeamColour: string;
  private secondaryTeamColour: string;
  private bet: FiveASideBetService;
  constructor(selection: IFiveASidePlayer, matrixItem: IMatrixFormation, betInstance: FiveASideBetService,
              defaultStatValue: number) {
    this.player = selection;
    this.role = matrixItem;
    this.playerId = this.player.id;
    this.statId = this.role.statId;
    this.playerName = this.player.name;
    this.primaryTeamColour = this.player.teamColors.primaryColour;
    this.secondaryTeamColour = this.player.teamColors.secondaryColour;
    this.teamsImage = this.player.teamColors.teamsImage && this.player.teamColors.teamsImage.filename ?
    `${this.TEAMSIMAGEPATH}${this.player.teamColors.teamsImage.filename}`: '';
    this.fiveASideToggle = this.player.teamColors.fiveASideToggle;
    this.bet = betInstance;
    this.playerIconBackground = this.getPlayerIconBackground();
    this.changeStatValue(defaultStatValue, false);
  }

  /**
   * Set conflict identifier for player
   */
  setConflict() {
    this.hasConflict = true;
  }

  /**
   * Reset conflict identifier for player
   */
  resetConflict() {
    this.hasConflict = false;
  }

  /**
   * Change value of player selection
   * @param statValue - new value of statistic for chosen player
   * @param updatePrices - defines whether need to update prices
   */
  changeStatValue(statValue: number, updatePrices: boolean = true): void {
    this.statValue = statValue;
    this.marketTitle = this.getMarketName();
    this.shortHandMarketTitle = this.getShortHandMarketTitle();
    updatePrices && this.bet.updateBet();
  }

  private getPlayerIconBackground(): string {
    return `linear-gradient(to right, ${this.primaryTeamColour} 50%, ${this.secondaryTeamColour} 50%)`;
  }

  private getMarketName(): string {
    const selection = this.role.stat;
    const value = this.statValue ? `${this.statValue}+` : this.statValue;
    const isExist = (text) => selection && selection.toLowerCase().includes(text);
    switch (true) {
      case isExist('to be carded'):
      case isExist('to keep a clean sheet'):
        return selection;
      case isExist('to concede') && !!value:
        return `${selection} ${value} Goals`;
      case isExist('to concede') && !value:
        return `To Keep A Clean Sheet`;
      default:
        return `${value} ${selection}`;
    }
  }

  /**
   * To get short hand for below listed markets
   */
  private getShortHandMarketTitle(): string {
    const selection: string = this.role.stat;
    const isExist = (text: string) => selection && selection.toLowerCase().includes(text);
    switch (true) {
      case isExist(PLAYER_MARKETS.shotsOutside.longTerm):
        return `${this.statValue}+ ${PLAYER_MARKETS.shotsOutside.shortTerm}`;
      case isExist(PLAYER_MARKETS.goalsOutside.longTerm):
        return `${this.statValue}+ ${PLAYER_MARKETS.goalsOutside.shortTerm}`;
      case isExist(PLAYER_MARKETS.goalsInside.longTerm):
          return `${this.statValue}+ ${PLAYER_MARKETS.goalsInside.shortTerm}`;
      default:
        return this.marketTitle;
    }
  }
}
