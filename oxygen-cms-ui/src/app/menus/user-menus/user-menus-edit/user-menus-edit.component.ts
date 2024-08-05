import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {UserMenu} from '../../../client/private/models/usermenu.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './user-menus-edit.component.html',
  styleUrls: ['./user-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class UserMenusEditComponent implements OnInit {

  public userMenu: UserMenu;
  public form: FormGroup;
  public showModes: Array<string> = ['both', 'mobile', 'desktop'];
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
      this.apiClientService.userMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<UserMenu>) => {
          return data.body;
        })
        .subscribe((userMenu: UserMenu) => {
          this.userMenu = userMenu;
          this.form = new FormGroup({
            linkTitle: new FormControl(this.userMenu.linkTitle, [Validators.required]),
            targetUri: new FormControl(this.userMenu.targetUri, [Validators.required]),
            disabled: new FormControl(!this.userMenu.disabled, []),
            activeIfLogout: new FormControl(this.userMenu.activeIfLogout, []),
            qa: new FormControl(this.userMenu.qa, []),
            showUserMenu: new FormControl(this.userMenu.showUserMenu, [])
          });
          this.breadcrumbsData = [{
            label: `User Menus`,
            url: `/menus/user-menus`
          }, {
            label: this.userMenu.linkTitle,
            url: `/menus/user-menus/${this.userMenu.id}`
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
    this.apiClientService.userMenu()
      .update(this.userMenu)
      .map((data: HttpResponse<UserMenu>) => {
        return data.body;
      })
      .subscribe((data: UserMenu) => {
        this.userMenu = data;
        this.actionButtons.extendCollection(this.userMenu);
        this.dialogService.showNotificationDialog({
          title: 'User Menu',
          message: 'User Menu is Saved.'
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
    this.apiClientService.userMenu()
      .delete(this.userMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/user-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onShowModeChanged(): void {
    this.userMenu.showUserMenu = this.form.value.showUserMenu;
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
    this.apiClientService.userMenu()
      .uploadImage(this.userMenu.id, file)
      .map((data: HttpResponse<UserMenu>) => {
        return data.body;
      })
      .subscribe((data: UserMenu) => {
        this.userMenu = _.extend(data, _.pick(this.userMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'showUserMenu'));
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
    this.apiClientService.userMenu()
      .removeImage(this.userMenu.id)
      .map((data: HttpResponse<UserMenu>) => {
        return data.body;
      })
      .subscribe((data: UserMenu) => {
        this.userMenu = _.extend(data, _.pick(this.userMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'showUserMenu'));
        this.snackBar.open(`Image Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  uploadSvgHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.userMenu()
      .uploadSvg(this.userMenu.id, file)
      .map((data: HttpResponse<UserMenu>) => {
        return data.body;
      })
      .subscribe((data: UserMenu) => {
        this.userMenu = _.extend(data, _.pick(this.userMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'showUserMenu'));
        this.snackBar.open(`Svg Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeSvgHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.userMenu()
      .removeSvg(this.userMenu.id)
      .map((data: HttpResponse<UserMenu>) => {
        return data.body;
      })
      .subscribe((data: UserMenu) => {
        this.userMenu = _.extend(data, _.pick(this.userMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'showUserMenu'));
        this.snackBar.open(`Svg Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
}
