import * as _ from 'lodash';

import { Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GamingSubMenu } from '@root/app/client/private/models/gaming-submenu.model';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Breadcrumb } from '@root/app/client/private/models';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '../../../app.constants';

@Component({
    templateUrl: './gaming-menus-edit.component.html',
    providers: [
        DialogService
    ]
})
export class GamingMenusEditComponent implements OnInit {

  public gamingSubMenu: GamingSubMenu;
  public gamingSubMenus: GamingSubMenu[];
  public form: FormGroup;
  public breadcrumbs: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons;
  public targetWindow: Array<string> = ['NEW', 'CURRENT'];

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.gamaingSubMenuService()
        .findAllByBrand()
        .map(response => response.body)
        .subscribe((gamingSubMenus: GamingSubMenu[]) => {
          this.gamingSubMenu = _.find(gamingSubMenus, (menu: GamingSubMenu) => menu.id === params['id']);
          this.form = new FormGroup({
            isNative: new FormControl(this.gamingSubMenu.isNative, [Validators.required]),
            title: new FormControl(this.gamingSubMenu.title, [Validators.required]),
            url: new FormControl(this.gamingSubMenu.url, [Validators.required]),
            target: new FormControl(this.gamingSubMenu.target, []),
            externalImageId: new FormControl(this.gamingSubMenu.externalImageId, []),
            pngFilename: new FormControl(this.gamingSubMenu.pngFilename, [])
          });

          this.breadcrumbs = [{
            label: `Gaming SubMenus`,
            url: `/menus/gaming-submenus`
          }, {
            label: this.gamingSubMenu.title,
            url: `/menus/gaming-submenus/${this.gamingSubMenu.id}`
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
    this.apiClientService.gamaingSubMenuService()
      .update(this.gamingSubMenu)
      .map(response => response.body)
      .subscribe((data: GamingSubMenu) => {
        this.gamingSubMenu = data;
        this.actionButtons.extendCollection(this.gamingSubMenu);
        this.dialogService.showNotificationDialog({
          title: 'Gaming  Submenu',
          message: 'Gaming Submenu is Saved.'
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
    this.apiClientService.gamaingSubMenuService()
      .delete(this.gamingSubMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/gaming-submenus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event: string): void {
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

  onTargetWindowChanged(): void {
    this.gamingSubMenu.target = this.form.value.target;
  }

  uploadPngHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.gamaingSubMenuService()
      .uploadPng(this.gamingSubMenu.id, file)
      .map(response => response.body)
      .subscribe((data: GamingSubMenu) => {
        this.gamingSubMenu = _.extend(data, _.pick(this.gamingSubMenu,
          'url', 'title', 'target', 'sortOrder', 'isNative', 'externalImageId'));
        this.snackBar.open(`PNG Image has been uploaded.`, 'OK', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removePngHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.gamaingSubMenuService()
      .removePng(this.gamingSubMenu.id)
      .map(response => response.body)
      .subscribe((data: GamingSubMenu) => {
        this.gamingSubMenu = _.extend(data, _.pick(this.gamingSubMenu,
          'url', 'title', 'target', 'sortOrder', 'isNative', 'externalImageId'));
        this.snackBar.open(`PNG Image has been deleted.`, 'OK', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
}
