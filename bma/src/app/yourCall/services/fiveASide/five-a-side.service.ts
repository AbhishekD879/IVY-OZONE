import { Injectable } from '@angular/core';
import { catchError, map, shareReplay, finalize } from 'rxjs/operators';
import { Observable, from as fromPromise, of, forkJoin, from } from 'rxjs';
import { DomSanitizer } from '@angular/platform-browser';

import { CmsService } from '@app/core/services/cms/cms.service';
import { IFormation } from '@app/core/services/cms/models';
import { YourcallProviderService } from '../yourcallProvider/yourcall-provider.service';
import { IPlayerBets, IPlayerBet } from '../../models/yourcall-api-response.model';
import { IFiveASidePlayers, IFiveASidePlayer, ITeamColors, ITeamColorsData, ITeamsExist } from './five-a-side.model';
import environment from '@environment/oxygenEnvConfig';
import { IConstant } from '@app/core/services/models/constant.model';
import { YourcallMarketsService } from '../yourCallMarketsService/yourcall-markets.service';
import { YourCallEvent } from '../../models/yourcall-event';
import { POSITIONS, MARKETS, PLAYER_STATS_NAMES, PLAYER_STATS_EXCLUDE } from '../../constants/five-a-side.constant';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { IMatrixFormation, IShowView } from '@yourcall/models/five-a-side.model';
import { DEFAULT_TEAM_COLOURS, LINE_UPS } from '@yourcall/constants/five-a-side.constant';
import { IYourcallStatisticResponse, IYourcallStatisticItem } from '@yourcall/models/yourcall-api-response.model';
import { IJourneyItems, IJourneyStaticBlock } from '@core/services/cms/models/five-a-side-journey.model';
import { IPitchDetails, IPlayer } from '@yourcall/models/pitch-details';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { FiveASideBetService } from '@yourcall/services/fiveASideBet/five-a-side-bet.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Injectable({ providedIn: 'root' })
export class FiveASideService {
  formations: IFormation[];
  players: IPlayerBets;
  playerList: IFiveASidePlayers;
  game: YourCallEvent;
  teamsColors = {} as ITeamColors;
  activeObEventId: number;
  isEditMode: boolean = false;
  optaStatisticsAvailable: boolean = false;
  imagesExistOnHomeAway: ITeamsExist | Object = {};
  eventId: number;

  private readonly positionsMap: IConstant = POSITIONS;
  private readonly marketsMap: IConstant = MARKETS;
  private readonly OPTA_ENV: string = environment.OPTA_SCOREBOARD.ENV;
  private view: string;
  private item: IMatrixFormation;
  private player: IFiveASidePlayer;
  private teamsColorObservable: Observable<ITeamColors>;
  private formation: string;
  private matrixFormation: IMatrixFormation[];
  private _localStorage: Storage;
  private journeyItems: IJourneyItems = {};
  private scrollPosition: number;

  private playerStats: {[key: string]: IYourcallStatisticItem[]} = {};

  constructor(
    private cmsService: CmsService,
    private yourcallProviderService: YourcallProviderService,
    private yourcallMarketsService: YourcallMarketsService,
    private coreToolsService: CoreToolsService,
    private domSanitizer: DomSanitizer,
    private fiveASideBetService: FiveASideBetService,
    private windowRefService: WindowRefService
  ) {
    this._localStorage = localStorage;
  }

  get activeView(): string {
    return this.view;
  }
  set activeView(value:string){}

  get activeFormation(): string {
    return this.formation;
  }

  set activeFormation(value: string) {
    this.formation = value;
  }

  set playerListScrollPosition(value: number) {
    this.scrollPosition = value;
  }

  get playerListScrollPosition(): number {
    return this.scrollPosition;
  }

  get activeItem(): IMatrixFormation {
    return this.item;
  }
  set activeItem(value:IMatrixFormation){}

  get activePlayer(): IFiveASidePlayer {
    return this.player;
  }
  set activePlayer(value:IFiveASidePlayer){}

  set activeMatrixFormation(value: IMatrixFormation[]) {
    this.matrixFormation = value;
  }

  get activeMatrixFormation(): IMatrixFormation[] {
    return this.matrixFormation;
  }

  initTeamsColors(sportId: string, obEventId: number): Observable<ITeamColors> {
    if (this.activeObEventId === obEventId && Object.keys(this.teamsColors).length) {
      return of(this.teamsColors);
    }

    this.activeObEventId = obEventId;
    this.teamsColors = {} as ITeamColors;

    const teamNames = [this.game.homeTeam.title, this.game.visitingTeam.title];
    if (!this.teamsColorObservable) {
      this.teamsColorObservable = this.cmsService.getTeamsColors(teamNames, sportId).pipe(
        shareReplay(1),
        map((cmsTeams: ITeamColorsData[]) => {
          teamNames.forEach((teamName: string) => {
            const team = cmsTeams.find(el => el.teamName.toUpperCase() === teamName.toUpperCase() || el.secondaryNames && el.secondaryNames.includes(teamName.toUpperCase()));

            const primaryColour = team && team.primaryColour;
            const secondaryColour = team && team.secondaryColour;
            const teamsImage  =  team && team.teamsImage;
            const fiveASideToggle= team && team.fiveASideToggle;
            const highlightCarouselToggle = team && team.highlightCarouselToggle;
            if(teamsImage) {
              this.imagesExistOnHomeAway[teamName] = {
                filename: teamsImage.originalname,
                fiveASideToggle: fiveASideToggle
              };
            }
            this.teamsColors[teamName] = {
              primaryColour: this.checkHexColor(primaryColour, DEFAULT_TEAM_COLOURS.primary),
              secondaryColour: this.checkHexColor(secondaryColour, DEFAULT_TEAM_COLOURS.secondary),
              teamsImage : teamsImage,
              fiveASideToggle : fiveASideToggle,
              highlightCarouselToggle  : highlightCarouselToggle
            };
          });
          return this.teamsColors;
        }),
        catchError((err) => {
          console.warn('Error', err);
          return of(this.teamsColors);
        }),
        finalize(() => {
          this.teamsColorObservable = null;
        })
      );
    }
    return this.teamsColorObservable;
  }

  getFormations(): Observable<IFormation[]> {
    this.game = this.yourcallMarketsService.game;
    return this.cmsService.getFiveASideFormations();
  }

  getPlayerList(obEventId: number, sportId: string): Observable<IFiveASidePlayers> {
    return forkJoin(this.getPlayers(obEventId), this.initTeamsColors(sportId, obEventId))
      .pipe(
        map((data: [IPlayerBets, ITeamColors]) => this.preapereOPTAInfo(data[0], obEventId)),
      );
  }

  /**
   * To sort players
   * @param {IMatrixFormation} formation
   * @param {string} teamColors
   * @returns {IFiveASidePlayer[]}
   */
  sortPlayers(formation: IMatrixFormation, team: string = 'allPlayers'): IFiveASidePlayer[] {
    this.item = formation;
    return this.sortByProperties(this.playerList[team], [this.marketsMap[formation.stat], 'name']);
  }

  showView(showView: IShowView, isEditMode: boolean = false): void {
    this.view = showView.view;
    this.isEditMode = isEditMode;

    if (showView.item) {
      this.item = showView.item;
    }

    if (showView.player) {
      this.player = showView.player;
    }
  }

  hideView(): void {
    this.view = '';
    this.player = undefined;
    this.item = undefined;
    this.isEditMode = false;
  }

  applyStatEdit(item: IMatrixFormation): void {
    if (this.item !== item) {
      this.item.stat = item.stat;
      this.item.statId = item.statId;
    }
  }

  saveDefaultStat(): void {
    if (!this.item.defaultStat) {
      this.item.defaultStat = { stat: this.item.stat, statId: this.item.statId };
    }
  }

  restoreDefaultStat(): void {
    const defaultStat = this.item.defaultStat;
    if (defaultStat) {
      this.item.stat = defaultStat.stat;
      this.item.statId = defaultStat.statId;
      this.item.defaultStat = null;
    }
  }

  loadPlayerStats(obEventId: number, playerId: number): Observable<IYourcallStatisticItem[]> {
    const key = `${obEventId}-${playerId}`;

    if (this.playerStats[key]) {
      return of(this.playerStats[key]);
    }

    return from(this.yourcallMarketsService.getStatisticsForPlayer({ obEventId: `${obEventId}`, playerId })).pipe(
      map((res: IYourcallStatisticResponse) => {
        const allData = res && res.allData;

        if (!allData) {
          throw new Error('No data');
        }

        const stats = allData
          .filter((item: IYourcallStatisticItem) => {
            return !PLAYER_STATS_EXCLUDE.includes(item.id);
          })
          .map((item: IYourcallStatisticItem) => {
            return { ...item, title: PLAYER_STATS_NAMES[item.id] || item.title };
          });

        stats.sort((a: IYourcallStatisticItem, b: IYourcallStatisticItem) => {
          if (a.title < b.title) { return -1; }
          if (a.title > b.title) { return 1; }
          return 0;
        });

        this.playerStats[key] = stats;

        return stats;
      })
    );
  }

  getPlayerStats(obEventId: number, playerId: number): IYourcallStatisticItem[] {
    return this.playerStats[`${obEventId}-${playerId}`];
  }

  /**
   * Return Observable of cached static blocks if or requests for journey static blocks
   */
  getJourneyStaticBlocks(): Observable<IJourneyItems> {
    return Object.keys(this.journeyItems).length ? of(this.journeyItems) : this.getFiveASideStaticBlocks();
  }

  /**
   * To fetch route formation from formations list
   * @param {IFormation[]} formations
   * @param  {string} pitchFormation
   * @returns {IFormtion}
   */
  getFormation(formations: IFormation[], pitchFormation: string): IFormation {
    return formations.find((formation: IFormation) => formation.actualFormation === pitchFormation);
  }

  /**
   * To build players data
   * @param {string[]} players
   * @returns {IPlayer[]}
   */
  buildPitchPlayers(players: string[]): IPlayer[] {
    const pitchPlayers: IPlayer[] = [];
    let count = 0;
    players.forEach((player) => {
      count = count + 1;
      const playerData = player.split('-');
      if (playerData.length === 5) {
        pitchPlayers.push({
          index: +playerData[1] - 1,
          player: playerData[2],
          statId: +playerData[3],
          line: +playerData[4],
          count: count
        });
      }
    });
    return pitchPlayers;
  }

  /**
   * To set selected players from route
   * @param {} pitch
   * @param {} players
   * @param {} eventEntity
   */
  setPlayerDetails(pitch: IPitchDetails, players: IFiveASidePlayers,
    eventEntity: ISportEvent): void {
    const observables: Observable<void>[] = [];

    if (pitch && pitch.players && pitch.players.length) {
      pitch.players.forEach((player: IPlayer) => {
        const playerData = players.allPlayers.find((data: IFiveASidePlayer) => +data.id === +player.player);
        if (playerData) {
          const playerStat$: Observable<void> = this.addRole(playerData, this.matrixFormation[player.index], eventEntity, player);
          observables.push(playerStat$);
        }
      });
    }

    if (observables.length) {
      forkJoin(observables)
      .subscribe(() => {
        this.fiveASideBetService.updateBet();
      });
    }
  }

  /**
   * To validate lineup availability
   * @param {string} eventId
   * @returns {boolean}
   */
  isLineupAvailable(eventId: number): boolean {
    const optaInfo = JSON.parse(this._localStorage.getItem(`scoreBoards_${this.OPTA_ENV}_prematch_${eventId}`));
    const optaParticipants = optaInfo && optaInfo.data && optaInfo.data.participants;
    const homeLineUps = optaParticipants && optaParticipants.home && optaParticipants.home.lineup;
    const awayLineUps = optaParticipants && optaParticipants.away && optaParticipants.away.lineup;
    return !!(homeLineUps || awayLineUps);
  }

  /**
   * To open lineup
   * @param {number} eventId
   * @param {string} eventCategory
   */
  setLineUps(eventId: number, eventCategory: string): void {
    let scoreboardOverlayWrapper: HTMLElement = this.windowRefService.document.querySelector(LINE_UPS.overlayWrapper);
    if (scoreboardOverlayWrapper) {
      const scoreboardOverlay: HTMLElement = this.windowRefService.document.querySelector(LINE_UPS.overlay);
      this.setParameters(scoreboardOverlay, eventCategory, {matchId: eventId,
         env: environment.OPTA_SCOREBOARD.ENV, overlayKey: LINE_UPS.overlayKey});
    } else {
      scoreboardOverlayWrapper = this.createOverlayWrapper(eventId, eventCategory, environment.OPTA_SCOREBOARD.ENV);
    }
    scoreboardOverlayWrapper.classList.add(LINE_UPS.styles.visible);
    this.windowRefService.document.body.classList.add(LINE_UPS.styles.overlayShown);
  }

  /**
   * If OPTA type, creates players data with stats, else creates data without stats
   *
   * @param {IPlayerBets} players
   * @param {number} obEventId
   * @return {*}  {IFiveASidePlayers}
   * @memberof FiveASideService
   */
  preapereOPTAInfo(players: IPlayerBets, obEventId: number): IFiveASidePlayers {
    this.players = players;
    this.eventId = obEventId;
    const banachPlayers: IPlayerBet[] = players.data;
    const opta = JSON.parse(this._localStorage.getItem(`scoreBoards_${this.OPTA_ENV}_prematch_${obEventId}`));

    const optaPlayers = opta && opta.data && opta.data.players;
    this.playerList = {
      home: [],
      away: [],
      allPlayers: []
    };

    banachPlayers.forEach((banachplayer: IPlayerBet) => {
      optaPlayers && ['home', 'away'].some((team: string): boolean => {
        let optaPlayer = (optaPlayers[team] || []).find((player: IConstant) => player.name.matchName === banachplayer.name);
        if (optaPlayer) {
          optaPlayer = this.parsePlayer(optaPlayer, banachplayer);
          this.playerList[team].push(optaPlayer);
          this.playerList.allPlayers.push(optaPlayer);
        }
        return !!optaPlayer;
      }) || this.parsePlayerWithoutStats(banachplayer);
    });

    return this.playerList;
  }

  /**
   * To add role for the selected player and add to playerobject
   * @param {IFiveASidePlayer} player
   * @param {IMatrixFormation} item
   * @param {ISportEvent} evententity
   * @param {pitchPlayer} pitchPlayer
   */
  private addRole(player: IFiveASidePlayer, item: IMatrixFormation,
    eventEntity: ISportEvent, pitchPlayer: IPlayer): Observable<void> {
    const playerId = player.id;
    const obEventId = eventEntity.id.toString();
    return Observable.create(observer => {
      this.loadPlayerStats(+obEventId, playerId)
      .subscribe((response: IYourcallStatisticItem[]) => {
        if (!response || !response.length) {
          return;
        }
        this.setPlayerStats(item, response, player, pitchPlayer);
        observer.next();
        observer.complete();
      });
    });
  }

  /**
   * To map playerstats if available or take default value
   * @param {IMatrixFormation} item
   * @param {IYourcallStatisticItem[]} response
   * @param {IFiveASidePlayer} player
   * @param {IPlayer} pitchPlayer
   */
  private setPlayerStats(item: IMatrixFormation, response: IYourcallStatisticItem[],
    player: IFiveASidePlayer, pitchPlayer: IPlayer): void {
    const statId = pitchPlayer.statId;
    const playerStats = response.find((playerStat: IYourcallStatisticItem) => +playerStat.id === statId);
    if (playerStats) {
      item.stat = playerStats.title;
      item.statId = statId;
      this.fiveASideBetService.addRole(player, item, pitchPlayer.line, false);
    }
  }

  /**
   * Tp create overlay wrapper, if it doesnot exist
   * @param {number} eventId
   * @param {string} eventCategory
   * @param {string} env
   * @returns {HTMLElement}
   */
  private createOverlayWrapper(eventId: number, eventCategory: string, env: string): HTMLElement {
    const scoreboardOverlay = this.windowRefService.document.createElement(LINE_UPS.overlay);
    const scoreboardOverlayWrapper = this.windowRefService.document.createElement(LINE_UPS.wrapper.parent);

    this.setParameters(scoreboardOverlay, eventCategory,
      {matchId: eventId, env: env, overlayKey: LINE_UPS.overlayKey});
    scoreboardOverlayWrapper.setAttribute(LINE_UPS.wrapper.parentAttributeId,
       LINE_UPS.wrapper.parentAttributeValue);
    scoreboardOverlayWrapper.appendChild(scoreboardOverlay);
    this.windowRefService.document.body.appendChild(scoreboardOverlayWrapper);

    return scoreboardOverlayWrapper;
  }

  /**
   * To set scoreboard overlay attribute
   * @param {HTMLElement} scoreboardElement
   * @param {string} eventCategory
   * @param {[key: string]: string} options
   */
  private setParameters(scoreboardElement: HTMLElement, eventCategory: string,
    options: {[key: string]: string|number}): void {
    const sbData = {
      sport: eventCategory,
      provider: LINE_UPS.scoreboardData.provider,
      ...options
    };
    scoreboardElement.setAttribute(LINE_UPS.scoreboardData.key, JSON.stringify(sbData));
  }

  /**
   * Requests journey static blocks and prepares
   */
  private getFiveASideStaticBlocks(): Observable<IJourneyItems> {
    return this.cmsService.getFiveASideStaticBlocks()
      .pipe(
        map((data: IJourneyStaticBlock[] | any) => {
          data.forEach((item: IJourneyStaticBlock) => {
            this.journeyItems[item.title] = {
              title: item.title,
              htmlMarkup: this.domSanitizer.bypassSecurityTrustHtml(item.htmlMarkup)
            };
          });
          return this.journeyItems;
        })
      );
  }

  private getPlayers(obEventId: number): Observable<IPlayerBets> {
    return fromPromise(this.yourcallProviderService.getPlayers(obEventId));
  }

  private parsePlayerWithoutStats(banachplayer: IPlayerBet): void {
    const playerWithoutStats = this.parsePlayer({}, banachplayer);
    if (banachplayer.team.title === this.game.homeTeam.title) {
      this.playerList.home.push(playerWithoutStats);
    } else {
      this.playerList.away.push(playerWithoutStats);
    }
    this.playerList.allPlayers.push(playerWithoutStats);
  }

  private parsePlayer(optaPlayer: IConstant, banachplayer: IPlayerBet): IFiveASidePlayer {
    const goalKeeper = optaPlayer.goalKeeper;
    const passes = optaPlayer.passes;
    const attendance = optaPlayer.attendance;
    const isAppeared = attendance && attendance.appearances === 0;

    if (!this.optaStatisticsAvailable) {
      this.optaStatisticsAvailable = !!(attendance && attendance.appearances);
    }

    return {
      id: banachplayer.id,
      name: banachplayer.name,
      teamName: banachplayer.team.title,
      teamColors: this.teamsColors && this.teamsColors[banachplayer.team.title],
      appearances: attendance && attendance.appearances,
      cleanSheets: attendance && attendance.cleanSheets,
      tackles: optaPlayer.tackles && optaPlayer.tackles.avg,
      passes: passes && passes.avg,
      crosses: passes && passes.avg,
      assists: optaPlayer.assists && optaPlayer.assists.goal,
      ...this.getPlayerShots(optaPlayer) as IFiveASidePlayer,
      goals: optaPlayer.goals && optaPlayer.goals.scored,
      goalsInsideTheBox: optaPlayer.goals && optaPlayer.goals.scored,
      goalsOutsideTheBox: optaPlayer.goals && optaPlayer.goals.scored,
      ...this.getPlayerCards(optaPlayer) as IFiveASidePlayer,
      position: {
        long: optaPlayer.position,
        short: this.positionsMap[optaPlayer.position]
      },
      penaltySaves: goalKeeper && goalKeeper.penaltySaves,
      conceeded: goalKeeper && (isAppeared ? 0 : Math.round(goalKeeper.conceeded / attendance.appearances * 10) / 10),
      saves: goalKeeper && (isAppeared ? 0 : Math.round(goalKeeper.totalSaves / attendance.appearances * 10) / 10),
      isGK: this.isGK(banachplayer, optaPlayer)
    };
  }

  private getPlayerShots(optaPlayer: IConstant): IConstant {
    const shots = optaPlayer.shots;
    return {
      shots: shots && shots.avg,
      shotsOnTarget: shots && shots.avgOnTarget,
      shotsOutsideTheBox: shots && shots.avg,
    };
  }

  private getPlayerCards(optaPlayer: IConstant): IConstant {
    const cards = optaPlayer.cards;
    return {
      cards: cards && cards.red + cards.yellow,
      cardsRed: cards && cards.red,
      cardsYellow: cards && cards.yellow,
    };
  }

  /**
   * Sorts array of objects sequentially comparing object properties
   * Sorting works: first iteration descending, second: ascending, next: descending
   * @param items      {array}  array to sort
   * @param properties {array}  properties to compare
   * @return {array}
   */
  private sortByProperties(items: IFiveASidePlayer[], properties: string[]): IFiveASidePlayer[] {
    items.sort((a, b) => {
      for (let i = 0; i < properties.length; ++i) {
        const prop = properties[i];
        let aVal = this.coreToolsService.getOwnDeepProperty(a, prop);
        let bVal = this.coreToolsService.getOwnDeepProperty(b, prop);

        if (aVal === undefined) {
          aVal = -1;
        }

        if (bVal === undefined) {
          bVal = -1;
        }

        if (i === 0) {
          if (aVal < bVal) { return 1; }
          if (aVal > bVal) { return -1; }
        } else {
          if (aVal > bVal) { return 1; }
          if (aVal < bVal) { return -1; }
        }
      }
      return -1;
    });
    return items;
  }

  private checkHexColor(color: string, defaultColor: string): string {
    const pattern = new RegExp('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$');
    return pattern.test(color) ? color : defaultColor;
  }

  private isGK(banachPlayer: IPlayerBet, optaPlayer: IConstant): boolean {
    return Boolean(
      (banachPlayer.position && banachPlayer.position.title === 'Goalkeeper') ||
      (optaPlayer.position === 'Goalkeeper')
    );
  }
}
