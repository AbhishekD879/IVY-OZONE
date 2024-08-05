import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import * as _ from 'lodash';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { HeaderMenu } from '@app/client/private/models/headermenu.model';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  templateUrl: './header-menus-edit.component.html',
  styleUrls: ['./header-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class HeaderMenusEditComponent implements OnInit {

  public headerMenu: HeaderMenu;
  public headerMenues: HeaderMenu[];
  public form: FormGroup;
  public menuLevels: Array<string> = ['1', '2'];
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.headerMenu()
        .findAllByBrand()
        .map((data: HttpResponse<HeaderMenu[]>) => {
          return data.body;
        })
        .subscribe((headerMenues: HeaderMenu[]) => {
          this.headerMenues = _.filter(headerMenues, (menu: HeaderMenu) => menu.id !== params['id'] && menu.level === '1');
          this.headerMenu = _.find(headerMenues, (menu: HeaderMenu) => menu.id === params['id']);
          this.form = new FormGroup({
            disabled: new FormControl(!this.headerMenu.disabled, []),
            inApp: new FormControl(this.headerMenu.inApp, []),
            linkTitle: new FormControl(this.headerMenu.linkTitle, [Validators.required]),
            targetUri: new FormControl(this.headerMenu.targetUri, [Validators.required]),
            level: new FormControl(this.headerMenu.level, []),
            parent: new FormControl(this.headerMenu.parent, [])
          });

          this.breadcrumbsData = [{
            label: `Header Menus`,
            url: `/menus/header-menus`
          }, {
            label: this.headerMenu.linkTitle,
            url: `/menus/header-menus/${this.headerMenu.id}`
          }];
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  public getParentLink(): string {
    return `/menus/header-menus/${this.headerMenu.parent}`;
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.headerMenu()
      .update(this.headerMenu)
      .map((data: HttpResponse<HeaderMenu>) => {
        return data.body;
      })
      .subscribe((data: HeaderMenu) => {
        this.headerMenu = data;
        this.actionButtons.extendCollection(this.headerMenu);
        this.dialogService.showNotificationDialog({
          title: 'Header Menu',
          message: 'Header Menu is Saved.'
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
    this.apiClientService.headerMenu()
      .delete(this.headerMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/header-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onLevelChanged(): void {
    this.headerMenu.level = this.form.value.level;
    if (this.headerMenu.level === '1') {
      this.headerMenu.parent = null;
    }
  }

  onParentChanged(): void {
    this.headerMenu.parent = this.form.value.parent;
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
}
