import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {TopGame} from '../../../client/private/models/topgame.model';
import {TopGamesCreateComponent} from '../top-games-create/top-games-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './top-games-list.component.html',
  styleUrls: ['./top-games-list.component.scss']
})
export class TopGamesListComponent implements OnInit {

  public topGames: Array<TopGame>;
  public error: string;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Image Title',
      'property': 'imageTitle',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    },
    {
      'name': 'Alt',
      'property': 'alt',
    },
    {
      'name': 'Target Uri',
      'property': 'targetUri',
    }
  ];
  public searchableProperties: Array<string> = [
    'imageTitle'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: TopGame[]) => {
        this.topGames = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createTopGame(): void {
    this.dialogService.showCustomDialog(TopGamesCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Top Game',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (topGame: TopGame) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.topGame()
          .save(topGame)
          .map(response => {
            return response.body;
          })
          .subscribe((data: TopGame) => {
            this.topGames.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/menus/top-games/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(topGame: TopGame): void {
    this.dialogService.showConfirmDialog({
      title: 'Top Game',
      message: 'Are You Sure You Want to Remove Top Game?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.topGame()
          .delete(topGame.id)
          .subscribe(() => {
            _.remove(this.topGames, {id: topGame.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .topGame()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Top game order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
