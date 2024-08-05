import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {TopGame} from '../../../client/private/models/topgame.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './top-games-edit.component.html',
  styleUrls: ['./top-games-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class TopGamesEditComponent implements OnInit {

  public topGame: TopGame;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.topGame()
        .findOne(params['id'])
        .map((data: HttpResponse<TopGame>) => {
          return data.body;
        })
        .subscribe((topGame: TopGame) => {
          this.topGame = topGame;
          this.form = new FormGroup({
            imageTitle: new FormControl(this.topGame.imageTitle, [Validators.required]),
            targetUri: new FormControl(this.topGame.targetUri, [Validators.required]),
            disabled: new FormControl(!this.topGame.disabled, []),
            alt: new FormControl(this.topGame.alt, [])
          });
          this.breadcrumbsData = [{
            label: `Top Games`,
            url: `/menus/top-games`
          }, {
            label: this.topGame.imageTitle,
            url: `/menus/top-games/${this.topGame.id}`
          }];
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .update(this.topGame)
      .map((data: HttpResponse<TopGame>) => {
        return data.body;
      })
      .subscribe((data: TopGame) => {
        this.topGame = data;
        this.actionButtons.extendCollection(this.topGame);
        this.dialogService.showNotificationDialog({
          title: 'Top Game',
          message: 'Top Game is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .delete(this.topGame.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/top-games/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  uploadFileHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .uploadImage(this.topGame.id, file)
      .map((data: HttpResponse<TopGame>) => {
        return data.body;
      })
      .subscribe((data: TopGame) => {
        this.topGame = _.extend(data, _.pick(this.topGame, 'imageTitle', 'targetUri', 'alt'));
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeFileHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .removeImage(this.topGame.id)
      .map((data: HttpResponse<TopGame>) => {
        return data.body;
      })
      .subscribe((data: TopGame) => {
        this.topGame = _.extend(data, _.pick(this.topGame, 'imageTitle', 'targetUri', 'alt'));
        this.snackBar.open(`Image Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  uploadIconHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .uploadIcon(this.topGame.id, file)
      .map((data: HttpResponse<TopGame>) => {
        return data.body;
      })
      .subscribe((data: TopGame) => {
        this.topGame = _.extend(data, _.pick(this.topGame, 'imageTitle', 'targetUri', 'alt'));
        this.snackBar.open(`Icon Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeIconHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.topGame()
      .removeIcon(this.topGame.id)
      .map((data: HttpResponse<TopGame>) => {
        return data.body;
      })
      .subscribe((data: TopGame) => {
        this.topGame = _.extend(data, _.pick(this.topGame, 'imageTitle', 'targetUri', 'alt'));
        this.snackBar.open(`Icon Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
}
