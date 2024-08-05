import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Game } from '@app/client/private/models/game.model';
import { GameAPIService } from '@root/app/one-two-free/service/game.api.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { HttpResponse } from '@angular/common/http';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { GamesEvent } from '@app/client/private/models';
import { AppConstants } from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SeasonsApiService } from '@root/app/one-two-free/service/seasons.api.service';

@Component({
  selector: 'game-page',
  templateUrl: './game.page.component.html',
  styleUrls: ['./game.page.component.scss']
})
export class GamePageComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;

  getDataError: string;
  errorMessage: string;
  game: Game;
  id: string;
  events: GamesEvent[] = [];
  eventsNotEditable: boolean = false;
  selectedSeason: string;
  isActive: boolean = false;
  seasons = [];
  isValidSeason = true;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private gameAPIService: GameAPIService,
    private seasonsApiService: SeasonsApiService,
    private snackBar: MatSnackBar,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }

  isValidModel(game): boolean {
    console.log(game);
    return game.id.length > 0 && !this.checkIfGameisActive(game) ;
  }

  gameNotValid(game) {
    return (game.events.length === 0 && game.enabled);
  }

  checkIfEventsEditable(game) {
    return new Date().getTime() >= new Date(game.displayFrom).getTime() && game.enabled;
  }

  /**
   * check if game is active
   * @param game 
   * @returns boolean
   */
  checkIfGameisActive(game: Game ) {
    return ((new Date(game.displayFrom).getTime() <= new Date().getTime())
      && (new Date(game.displayTo).getTime() > new Date().getTime()))
      && game.enabled;
  }

  showNotification(message) {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  revertGameChanges() {
    this.loadInitialData();
  }

  removeGame() {
    this.gameAPIService.deleteGame(this.game.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Game is Removed.'
        });
        this.router.navigate(['/one-two-free/games/']);
      });
  }

  /**
   * Make PUT request to server to update
   */
  saveGameChanges() {
    const doSaveChanges = () => this.gameAPIService.putGamesChanges(this.game)
      .map((response: HttpResponse<Game>) => {
        return response.body;
      })
      .subscribe((data: Game) => {
        this.game = data;
        this.eventsNotEditable = this.checkIfEventsEditable(data);
        this.actionButtons.extendCollection(this.game);
        this.showNotification('Game Changes are Saved.');
      }
      );

    if (this.gameNotValid(this.game)) {
      this.dialogService.showNotificationDialog({
        title: 'Error on saving',
        message: 'You can`t activate game without any event'
      });
      this.revertGameChanges();
    } else {
      if (this.isEndDatePrecedsLatestMatch()) {
        this.dialogService.showConfirmDialog({
          title: 'WARNING!',
          message: `Warning! The Game 'Display To' date precedes the latest match final whistle\
           [est. to finish\ ${new Date(this.getLatestMatchApxEndDateMillis())}]. Saving these changes\
           might negatively affect the end users. Are you sure you want to save anyway?`,
          yesCallback: doSaveChanges,
        });
      } else {
        doSaveChanges();
      }
    }
  }

  private isEndDatePrecedsLatestMatch() {
    return this.game.enabled && new Date(this.game.displayTo).getTime() < this.getLatestMatchApxEndDateMillis();
  }

  private getLatestMatchApxEndDateMillis() {
    return new Date(this.game.events[this.game.events.length - 1].startTime).getTime() + this.estimatedFootballMatchTimeMillis();
  }

  /**
   * 2 halves + break + est. first half extra time + est. second time extra time.
   */
  private estimatedFootballMatchTimeMillis() {
    return (90 + 15 + 1 + 3) * 60 * 1000;
  }

  /**
   * Load initial data to initialize component
   */
  loadInitialData() {
    this.gameAPIService.getSingleGamesData(this.id)
      .subscribe((data: any) => {
        this.game = data.body;
        this.game.seasonId != null ? this.selectedSeason = this.game.seasonId : this.selectedSeason = '';
        this.isActive = this.checkIfGameisActive(data.body);
        this.eventsNotEditable = this.checkIfEventsEditable(data.body);
        this.breadcrumbsData = [{
          label: `Games`,
          url: `/one-two-free/games`
        }, {
          label: this.game.title,
          url: `/one-two-free/games/${this.game.id}`
        }];
      }, error => {
        this.getDataError = error.message;
      });
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadSeasons();
    this.loadInitialData();
  }

  onGamesEvents(events) {
    this.events = events;
  }

  updateGame() {
    if (this.gameNotValid(this.game)) {
      this.dialogService.showNotificationDialog({
        title: 'Error on saving',
        message: 'You can`t activate game without any event'
      });
      this.revertGameChanges();
    } else {
      this.gameAPIService.getSingleGamesData(this.id)
        .subscribe((data: any) => {
          this.game = data.body;
        });
    }
  }

  handleVisibilityDateUpdate(data: DateRange): void {
    this.game.displayFrom = new Date(data.startDate).toISOString();
    this.game.displayTo = new Date(data.endDate).toISOString();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'updateGameState':
        if (this.actionButtons) {
          this.actionButtons.extendCollection(this.game);
        }
        break;
      case 'remove':
        this.removeGame();
        break;
      case 'save':
        this.saveGameChanges();
        break;
      case 'game update':
        this.updateGame();
        break;
      case 'revert':
        this.revertGameChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * Method to fetch All Seasons
   * @param null
   * @return seasons 
   */
  loadSeasons() {
    this.seasonsApiService.getAllSeasons().subscribe(data => {
      this.seasons = data.body;
      this.seasons.push({ id: '', seasonName: 'No PL Teams' })
    });
  }

  /**
   * Method to fetch All Seasons
   * @param value, game
   */
  onSelectSeason(value, game : Game) {
    const seasonSel = this.seasons.find(season => season.id == value.value);
    if (value.value != '' && (new Date(seasonSel.displayTo) < new Date())) {
      this.dialogService.showNotificationDialog({
        title: 'Game Error',
        message: 'Please note, not allowed to link expired season'
      })
      this.isValidSeason = false;
    } else {
      this.isValidSeason = true;
      this.selectedSeason = value.value;
      this.selectedSeason == '' ? game.seasonId = null : game.seasonId = this.selectedSeason;
    }
  }
}
