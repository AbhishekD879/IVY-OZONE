import { Component, EventEmitter, Input, OnInit, Output, QueryList, ViewChildren } from '@angular/core';
import * as _ from 'lodash';
import { GamesEvent } from '@app/client/private/models';
import { Game } from '@app/client/private/models/game.model';
import { DialogService } from 'app/shared/dialog/dialog.service';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TeamKitAPIService } from '@app/one-two-free/teamKit.api.service';
import { SvgOptionModel } from '@app/client/private/models/svgOption.model';
import { CmsUploadDropdownComponent } from '@app/shared/cms-upload-dropdown/cms-upload-dropdown.component';
import { GameAPIService } from '../../../service/game.api.service';
import { Prize } from '@app/client/private/models/prize.model';
import { EventScore } from '@app/client/private/models/eventScore.model';
import { ABANDONED_SCORE, EventScoreDto, SUSPENDED_SCORE } from '@app/client/private/models/eventScoreDto.model';

@Component({
  selector: 'event-create-table',
  templateUrl: './event.create.component.html',
  styleUrls: ['./event.create.component.scss'],
})

export class EventCreateComponent implements OnInit {
  private _game: Game;

  @Input() set game(value: Game) {
    this._game = value;
    if (this._game.events && this._game.events.length) {
      this._game.events.forEach(event => event.initialEventId = event.eventId);
      this.actionsEmitter.emit('updateGameState');
    }
  }

  get game() {
    return this._game;
  }


  @Input() eventsNotEditable: boolean;

  @Output() actionsEmitter = new EventEmitter<string>();

  @ViewChildren('home')
  homeComponents: QueryList<CmsUploadDropdownComponent>;

  @ViewChildren('away')
  awayComponents: QueryList<CmsUploadDropdownComponent>;

  private getEventThrottleDelay: Number = 600;
  private getEventThrottled: Function;
  public eventId: string;
  public prize: Prize;
  public selectTVIconsOptions = [
    {id: null, name: 'No TV icon'},
    {id: 'BBC', name: 'BBC'},
    {id: 'ITV', name: 'ITV'},
    {id: 'Sky_Sports', name: 'Sky Sports'},
    {id: 'BT_Sports', name: 'BT Sport'},
    {id: 'Channel_1', name: 'Channel 1'},
    {id: 'Channel_2', name: 'Channel 2'},
    {id: 'Channel_3', name: 'Channel 3'},
    {id: 'Channel_4', name: 'Channel 4'}
  ];
  public prizeTypes = new Map<string, string>();
  public namePathsOptions = new Map<string, SvgOptionModel[]>();
  public scoreSection: boolean[] = [];

  public scores: EventScoreDto[] = [];
  public scoreMapping = {
    MATCH_ARRANGED: {
      getScores: index => [this.scores[index].home, this.scores[index].away],
      setScores: (index, home, away) => {
        this.scores[index].home = home;
        this.scores[index].away = away;
      }
    },
    MATCH_SUSPENDED: {
      getScores: () => [SUSPENDED_SCORE, SUSPENDED_SCORE],
      setScores: () => {}
    },
    MATCH_ABANDONED: {
      getScores: () => [ABANDONED_SCORE, ABANDONED_SCORE],
      setScores: () => {}
    }
  };
  public selectedScoresOption = [];

  constructor(
    private gameAPIService: GameAPIService,
    private teamKitAPIService: TeamKitAPIService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar
   ) {}

  ngOnInit() {
    this.prize = {
      correctSelections: 0,
      prizeType: '',
      amount: 0.0,
      currency: '',
      promotionId: ''
    };
    this.prizeTypes.set('CREDIT', 'Credit');
    this.prizeTypes.set('FREE_BETS', 'Free bets');
    if (_.isNil(this.game.prizes)) {
      this.game.prizes = [];
    }
    if (_.isEmpty(this.game.prizes)) {
      const size = this.game.events.length;
      let i;
      for (i = 0; i < size; i++) {
        this.game.prizes.push(new Prize(size - i, 'CREDIT', 0.0));
      }
    }
    if (!_.isEmpty(this.game.events)) {
      this.game.events.forEach(event => {
             if(event.home.isNonPLTeam == null){
                  event.home.isNonPLTeam = false;
                }
                if(event.away.isNonPLTeam == null){
                  event.away.isNonPLTeam = false;
                }
              });
      const size = this.game.events.length;
      let i;
      for (i = 0; i < size; i++) {
        this.scoreSection[i] = false;
        this.scores.push(new EventScoreDto());
      }
    }
    this.uploadTeamKits();
    this.getEventThrottled = index => this.throttle(this.getEventHandler.bind(this, index), this.getEventThrottleDelay)();

    this.scoreMapping[SUSPENDED_SCORE] = 'MATCH_SUSPENDED';
    this.scoreMapping[ABANDONED_SCORE] = 'MATCH_ABANDONED';
  }

  private addPrize() {
    const size = this.game.events.length;
    if (size > 0) {
      this.game.prizes.unshift(new Prize(size, 'CREDIT', 0.0));
    }
  }

  private uploadTeamKits() {
    this.namePathsOptions.clear();
    _.forEach(this.game.events, (event: GamesEvent) => {
      this.fillTeamKits(event.home.name);
      this.fillTeamKits(event.away.name);
    });
  }

  public fillTeamKits(name: string) {
    this.teamKitAPIService.getTeamKitsByTeamName(name).subscribe((values) => {
        _.forEach(values.body, value => {
          const {path, svg, svgId, teamName} = value;
          const existedPaths: SvgOptionModel[] = this.namePathsOptions.get(teamName);
          const svgOptionModel = new SvgOptionModel(path, this.parseSvgName(path), svg, svgId, this.parseSvgName(path));
          let paths = [];
          paths = (_.isNil(existedPaths)) ? [...paths, svgOptionModel] : [...existedPaths, svgOptionModel];
          this.namePathsOptions.set(teamName, paths);
        });

        this.updateSelection();
      }
    );
  }

  parseSvgName(fullPath): string {
    const arr = fullPath ? fullPath.split('/') : [];
    return arr && arr.length > 0 ? arr[arr.length - 1] : '';
  }

  public setSelectionToComponent = (component, event, teamType) => {
    const existedTeamType = event ? event[teamType] : false;
    if (existedTeamType && event.eventId === component.id) {
      component.selected = this.getSelected(existedTeamType.name, this.parseSvgName(existedTeamType.teamKitIcon));
    }
  }

  public updateSelection() {
    _.forEach(this.game.events, event => {

      this.homeComponents.forEach((homeComponent: CmsUploadDropdownComponent) => (
        this.setSelectionToComponent(homeComponent, event, 'home'))
      );

      this.awayComponents.forEach((awayComponent: CmsUploadDropdownComponent) => (
        this.setSelectionToComponent(awayComponent, event, 'away'))
      );
    });
  }

  private throttle(func, ms) {
    let isThrottled = false;

    return function() {
      if (isThrottled) {
        return;
      }

      func();
      isThrottled = true;
      setTimeout(function() { isThrottled = false; }, ms);
    };
  }

  getEvent(index?) {
    this.getEventThrottled(index);
  }

  isAddingAlreadyPresentEvent(index?): boolean {
    if (!index && this.eventId) {
      for (const event of this.game.events) {
        if (String(event.eventId) === String(this.eventId)) {
          this.dialogService.showNotificationDialog({
            title: 'Event Fetching Error',
            message: 'Event with such ID already added'
          });
          return true;
        }
      }
    }

    return false;
  }

  getEventHandler(index?) {
    const requestedEventId = (this.game.events[index] && this.game.events[index].eventId) || this.eventId;
    if (this.isAddingAlreadyPresentEvent(index)) {
      return;
    }
    if (!index) {
      this.eventId = '';
    }

    if (requestedEventId) {
      this.gameAPIService.getEventById(requestedEventId)
        .subscribe(event => {
          if (event.body) {
            const { eventId, homeTeamName, awayTeamName, startTime, tvIcon } = event.body;
            const { brand, id: gameId } = this.game;
            const home = {
              name: homeTeamName,
              displayName: homeTeamName,
              teamKitIcon: null
            };
            const away = {
              name: awayTeamName,
              displayName: awayTeamName,
              teamKitIcon: null
            };
            if(this.game.seasonId){
                          Object.assign(home,{isNonPLTeam:false});
                            Object.assign(away,{isNonPLTeam:false});
                          }
            const fullEvent = { brand, gameId, tvIcon, eventId, startTime, home, away, sortOrder: 0 };

            if (this.game.events[index]) {
              this.game.events[index] = fullEvent;
            } else {
              this.scores.push(new EventScoreDto());
              this.game.events.push(fullEvent);
              this.addPrize();
            }
            this.gameAPIService.putGamesChanges(this.game).subscribe(response => this.game.events = response.body.events);

          } else {
            this.dialogService.showNotificationDialog({
              title: 'Save Error',
              message: 'Event not found'
            });
            if (this.game.events[index]) {
              this.game.events[index].eventId = this.game.events[index].initialEventId;
            }
          }
        });
    }
  }

  removeEvent(index: number) {
    this.game.events.splice(index, 1);
    this.game.prizes.shift();
  }

  isValidEventId(): boolean {
    return parseInt(this.eventId, 10) > 0;
  }

  uploadSvgHandler(file, eventId, fileName, teamType): void {
    this.gameAPIService.uploadImage(this.game.id, eventId, teamType, fileName, file)
      .subscribe((data) => {
        this.updateGameEventOnUploadSvg(eventId, data.body);
        this.uploadTeamKits();
        this.showNotification('Svg Uploaded.');
        this.gameAPIService.hideLoader();
      });
  }

  removeSvgHandler(eventId, teamType): void {
    this.gameAPIService.deleteImage(this.game.id, eventId, teamType)
      .subscribe((result) => {
        this.updateGameEventOnRemoveSvg(eventId, result.body, teamType);
        this.showNotification('Svg Deleted.');
      });
  }

  updateGameEventOnUploadSvg(eventId, result): void {
    const customizer = (objValue, srcValue) => {
      if (_.isNull(srcValue)) {
        return objValue;
      }
    };
    this.game.events.forEach((event, i) => {
      if (event.eventId === eventId) {
        this.game.events[i] = _.mergeWith(this.game.events[i], result, customizer);
      }
    });
  }

  updateGameEventOnRemoveSvg(eventId, result, teamType): void {
    this.game.events.forEach((event, i) => {
      if (event.eventId === eventId) {
        const toUpdateEvent = this.game.events[i];
        if (teamType === 'home') {
          toUpdateEvent.home.teamKitIcon = undefined;
        } else {
          toUpdateEvent.away.teamKitIcon = undefined;
        }
      }
    });
  }

  showNotification(message) {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  getAvailableOptions(teamName): SvgOptionModel[] {
    const options = this.namePathsOptions.get(teamName);
    return !!options ? options : [];
  }

  getSelected(teamName, teamPath): SvgOptionModel {
    const options: SvgOptionModel[] = this.namePathsOptions.get(teamName);
    const option = !!options ? options.filter((item) => item.name === teamPath)[0] : new SvgOptionModel('', '', '', '', '');
    return !!option ? option : new SvgOptionModel('', '', '', '', '');
  }

  onChange(value, eventId, teamType) {
    const event: GamesEvent = _.filter(this.game.events, (item: GamesEvent) => item.eventId === eventId)[0];
    const isHomeTeam = teamType === 'home';
    const existedTeamType = event ? event[teamType] : false;
    const components = isHomeTeam ? this.homeComponents : this.awayComponents;

    components.forEach((component: CmsUploadDropdownComponent) => {
      if (existedTeamType && event.eventId === component.id) {
        component.selected = this.getSelected(existedTeamType.name, value);
        component.svgList.reinitSvgElement(component.selected.svg);
        existedTeamType.teamKitIcon = component.selected.fullPath;
      }
    });
  }

  getLabel(prizeTypeKey: string): string {
    return this.prizeTypes.get(prizeTypeKey);
  }

  getKeys(): string[] {
    return Array.from(this.prizeTypes.keys());
  }

  toggleScorePanel(index, eventId): void {
    if (this.scoreSection[index]) {
      this.scoreSection[index] = !this.scoreSection[index];
    } else {
      this.gameAPIService.getScore(eventId)
        .map(response => response.body)
        .subscribe(score => {
          if (score.length) {
            const home = score[0];
            const away = score[1];

            this.selectedScoresOption[index] = this.scoreMapping[home] || 'MATCH_ARRANGED';
            this.scoreMapping[this.selectedScoresOption[index]].setScores(index, home, away);
          }
        });
      this.scoreSection[index] = true;
    }
  }

  isScorePanelExpanded(index): boolean {
    if (this.scoreSection[index]) {
      return this.scoreSection[index];
    } else {
      return false;
    }
  }

  handleDateUpdate(data, index): void {
    this.game.events[index].startTime = new Date(data).toISOString();
  }

  saveScore(position) {
    const actualScores: number[] = this.scoreMapping[this.selectedScoresOption[position]].getScores(position);
    const score = new EventScore({eventId: this.game.events[position].eventId, eventPosition: position, actualScores});

    this.gameAPIService.saveScore(this.game.id, score)
      .subscribe((result) => {
        if (result.body.isSuccessfull) {
          this.showNotification('Score saved.');
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Send score updates error',
            message: 'Error: ' + result.body.message
          });
        }
      });
  }
}
