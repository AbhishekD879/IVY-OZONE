import {ApiClientService} from './../../../client/private/services/http/index';
import {GlobalLoaderService} from './../../../shared/globalLoader/loader.service';
import {Component, OnInit} from '@angular/core';
import {GameAPIService} from '../../service/game.api.service';
import {Game} from '../../../client/private/models/game.model';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {GameCreateComponent} from '../game-create/game.create.component';
import {AppConstants} from '../../../app.constants';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {forkJoin} from 'rxjs/observable/forkJoin';
import {Router} from '@angular/router';
import * as _ from 'lodash';

@Component({
  selector: 'games-page',
  templateUrl: './games.page.component.html',
  styleUrls: ['./games.page.component.scss']
})
export class GamesPageComponent implements OnInit {
  gamesData: Array<Game>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Status',
      property: 'status'
    },
    {
      name: 'Game Name',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Display From',
      property: 'displayFrom'
    },
    {
      name: 'Active?',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Display To',
      property: 'displayTo'
    }
  ];

  filterProperties: Array<string> = [
    'displayFrom',
    'title',
    'displayTo',
    'status'
  ];
  constructor(
    public snackBar: MatSnackBar,
    private gameAPIService: GameAPIService,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private router: Router
  ) {}

  removeGame(game: Game) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Game',
      message: 'Are You Sure You Want to Remove Game?',
      yesCallback: () => {
        this.sendRemoveRequest(game);
      }
    });
  }

  removeHandlerMulty(gamesIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Game (${gamesIds.length})`,
      message: 'Are You Sure You Want to Remove Games?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(gamesIds.map(id => this.apiClientService.gamesService().deleteGame(id)))
          .subscribe(() => {
            gamesIds.forEach((id) => {
              const index = _.findIndex(this.gamesData, { id: id });
              this.gamesData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  sendRemoveRequest(game: Game) {
    this.gameAPIService.deleteGame(game.id)
      .subscribe((data: any) => {
        this.gamesData.splice(this.gamesData.indexOf(game), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Game is Removed.'
        });
      });
  }

  reloadGames() {
    this.gameAPIService.getGamesData()
    .subscribe((data: any) => {
        this.gamesData = data.body;
        const dateNow = new Date();
        this.gamesData.forEach(game => this.setGameStatus(game, dateNow));
    }, error => {
        this.getDataError = error.message;
    });
  }

  private setGameStatus(game: Game, dateNow: Date) {
    const displayFromDate = new Date(game.displayFrom);
    const displayToDate = new Date(game.displayTo);
    if (displayToDate < dateNow) {
      game.status = 'Past';
    } else if (displayFromDate > dateNow) {
      game.status = 'Future';
    } else if (displayFromDate < dateNow && displayToDate > dateNow) {
      game.highlighted = true;
      game.status = 'Current';
    }
  }

  createGame() {
    const dialogRef = this.dialog.open(GameCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newGame => {
      if (newGame) {
        this.gameAPIService.postNewGame(newGame)
          .subscribe(response => {
            if (response) {
              this.gamesData.push(newGame);
              this.router.navigate([`/one-two-free/games/${response.body.id}`]);
            }
          });
      }
    });
  }

  ngOnInit() {
    this.reloadGames();
  }
}
