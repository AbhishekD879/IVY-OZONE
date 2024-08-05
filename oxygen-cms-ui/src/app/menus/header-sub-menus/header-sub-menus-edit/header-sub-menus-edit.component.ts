import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import * as _ from 'lodash';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { HeaderSubMenu } from '@app/client/private/models/headersubmenu.model';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  templateUrl: './header-sub-menus-edit.component.html',
  styleUrls: ['./header-sub-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class HeaderSubMenusEditComponent implements OnInit {

  public headerSubMenu: HeaderSubMenu;
  public headerSubMenues: HeaderSubMenu[];
  public form: FormGroup;
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
      this.apiClientService.headerSubMenu()
        .findAllByBrand()
        .map((data: HttpResponse<HeaderSubMenu[]>) => {
          return data.body;
        })
        .subscribe((headerSubMenues: HeaderSubMenu[]) => {
          this.headerSubMenu = _.find(headerSubMenues, (menu: HeaderSubMenu) => menu.id === params['id']);
          this.form = new FormGroup({
            disabled: new FormControl(!this.headerSubMenu.disabled, []),
            inApp: new FormControl(this.headerSubMenu.inApp, []),
            linkTitle: new FormControl(this.headerSubMenu.linkTitle, [Validators.required]),
            targetUri: new FormControl(this.headerSubMenu.targetUri, [Validators.required])
          });

          this.breadcrumbsData = [{
            label: `Header Menus`,
            url: `/menus/header-submenus`
          }, {
            label: this.headerSubMenu.linkTitle,
            url: `/menus/header-submenus/${this.headerSubMenu.id}`
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
    this.apiClientService.headerSubMenu()
      .update(this.headerSubMenu)
      .map((data: HttpResponse<HeaderSubMenu>) => {
        return data.body;
      })
      .subscribe((data: HeaderSubMenu) => {
        this.headerSubMenu = data;
        this.actionButtons.extendCollection(this.headerSubMenu);
        this.dialogService.showNotificationDialog({
          title: 'Header  Submenu',
          message: 'Header Submenu is Saved.'
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
    this.apiClientService.headerSubMenu()
      .delete(this.headerSubMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/header-submenus/']);
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
}
