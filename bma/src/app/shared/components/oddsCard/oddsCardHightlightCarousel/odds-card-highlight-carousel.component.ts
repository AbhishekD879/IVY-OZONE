import { Component, Input, OnInit } from '@angular/core';
import { OddsCardSportComponent } from '@sharedModule/components/oddsCard/oddsCardSport/odds-card-sport.component';
import { IOutcome } from '@core/models/outcome.model';
import { ISportTeamColors } from '@app/sb/models/sport-configuration.model';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'odds-card-highlight-carousel',
  templateUrl: 'odds-card-highlight-carousel.component.html',
  styleUrls: ['odds-card-highlight-carousel.component.scss']
})

export class OddsCardHighlightCarouselComponent extends OddsCardSportComponent implements OnInit {
  @Input() outcomeColumnsTitles: string[];
  @Input() carouselByTypeId: boolean = false;
  @Input() carouselByEventIds: boolean = false;
  @Input() changeStrategy: string;
  @Input() participants: any[];
  @Input() isDesktop: boolean;
  @Input() index: number;
  @Input() eagerLoadCount: number;

  readonly CMS_UPLOADS_PATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  isBadminton: boolean = false;
  showScoreData: boolean;
  isKitsAvailable: boolean = false;
  outcomeColumnsHeaders: string[] = [];
  homeTeamData:ISportTeamColors = {};
  awayTeamData:ISportTeamColors = {};

  ngOnInit(): void {
    super.ngOnInit();
    this.isKitsAvailable = this.isPremChampLeagueCheck();

    if (this.event.categoryName === 'Badminton') {
      this.isBadminton = true;
      this.initBadmintonScores();
    }
    this.checkScores();
    this.setOutcomeColumnsHeaders();
    this.getSportTeamImage();
  }

  teamKit(teamName: string): string {
    return teamName.replace(/[ ,.:;]+/g, '-').toLowerCase().trim();
  }

  hasEventScores(): boolean {
    return !!this.eventComments && !!this.eventComments.teams && !this.event.outcomeStatus && this.event.isStarted === true;
  }

  /**
   * Checks if player is active (green ball icon for tennis)
   * @param 1 or 2 as number of player,
   * the function created for two team players only
   * The reason: at paired tennis both players got isActive from BE.
   */
  isPlayerActive(player: number): boolean {
    return this.eventComments ?
      this.eventComments.teams[`player_${player}`].isActive &&
      !this.eventComments.teams[`player_${3 - player}`].isActive : false;
  }

  /**
   * if at least one image is unavailable - HIDE KITS
   * @param {boolean} kitStatus
   */
  checkKits(kitStatus: boolean): void {
    this.isKitsAvailable = kitStatus;
  }

  checkScores(): boolean {
    if ((this.event.categoryId === '13' && this.eventComments && this.eventComments.teams &&
      this.eventComments.teams.home && this.eventComments.teams.home.score) ||
      (this.event.categoryId !== '13' && this.eventComments && this.eventComments.teams &&
        this.eventComments.teams.home && !this.boxScore)) {
      this.showScoreData = true;
    } else {
      this.showScoreData = false;
    }
    return this.showScoreData;
  }

  /**
   * Check if both teams have the images
   * @returns { boolean }
   */
  checkForTeamsImageData(): boolean {
    return (this.homeTeamData.hasOwnProperty('teamsImage') && this.homeTeamData.teamsImage.filename && this.awayTeamData.hasOwnProperty('teamsImage') && this.awayTeamData.teamsImage.filename) ? true : false;
  }

  /**
   * Check if both teams exist
   * @returns { boolean }
   */
  checkForTeamsExist(): boolean {
    return this.participants ? false :
    Object.keys(this.homeTeamData).length > 0 && Object.keys(this.awayTeamData).length > 0;
  }

  /**
   * Get the team images for the teams
   * @returns { void }
   */
  public getSportTeamImage(): void {
    if (this.event.hasOwnProperty('assetManagements') && this.event.assetManagements.length === 2 && !this.participants) {
      this.homeTeamData = this.event.assetManagements[0];
      this.awayTeamData = this.event.assetManagements[1];
    }
  }
  /**
   * Badminton scores gets from
   * G - games - eventComments.setsScores[eventComments.teams.player_1.id] = comments.teams.home/away.score
   * P - points - eventComments.teams.player_1.score = comments.teams.home/away.currentPoints
   */
  private initBadmintonScores(): void {
    const eventComments = this.event.comments;
    if (!!eventComments && eventComments.teams) {
      eventComments.teams.home = {};
      eventComments.teams.away = {};
      eventComments.teams.home.score = eventComments.setsScores[eventComments.runningSetIndex || 1][eventComments.teams.player_1.id];
      eventComments.teams.away.score = eventComments.setsScores[eventComments.runningSetIndex || 1][eventComments.teams.player_2.id];
      eventComments.teams.home.currentPoints = eventComments.teams.player_1.score;
      eventComments.teams.away.currentPoints = eventComments.teams.player_2.score;
      this.isEventHasCurrentPoints = true;
    }
  }

  private setOutcomeColumnsHeaders(): void {
    const homeDrawAwayMap = {
      'football': {
        'H': 'Home',
        'D': 'Draw',
        'A': 'Away'
      },
      'other': {
        'H': '1',
        'D': 'x',
        'A': '2'
      }
    };
    const outcomesNames = this.correctedOutcomes;
    const sport = this.event.categoryCode.toLowerCase();
    this.outcomeColumnsHeaders = outcomesNames
      .map((outcome: IOutcome) => outcome ?
        homeDrawAwayMap[sport === 'football' ? sport : 'other'][outcome.outcomeMeaningMinorCode as string] : null);

  }

  /**
   * Team-kits are for football only
   */
  private isPremChampLeagueCheck(): boolean {
    if ((this.carouselByTypeId || this.carouselByEventIds) && this.event.categoryCode.toLowerCase() === 'football') {
      const typeName = this.event.typeName.toLowerCase();
      return typeName.indexOf('championship') >= 0 || (typeName.indexOf('league') >= 0 &&
        (typeName.indexOf('premier') >= 0 || typeName.indexOf('champions') >= 0));
    } else {
      return false;
    }
  }

  appendDrillDownTagNames (market) {
    return market.drilldownTagNames ? market.drilldownTagNames + `${market.name},` : `${market.name},`;
  }
}
