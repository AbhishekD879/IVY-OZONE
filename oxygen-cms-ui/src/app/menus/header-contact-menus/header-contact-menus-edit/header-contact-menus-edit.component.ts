import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';

import { DialogService } from '../../../shared/dialog/dialog.service';
import { HeaderContactMenu } from '../../../client/private/models/headercontactmenu.model';
import { ApiClientService } from '../../../client/private/services/http';
import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';


@Component({
  templateUrl: './header-contact-menus-edit.component.html',
  styleUrls: ['./header-contact-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class HeaderContactMenusEditComponent implements OnInit {

  public headerContactMenu: HeaderContactMenu;
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
      this.apiClientService.headerContactMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<HeaderContactMenu>) => {
          return data.body;
        })
        .subscribe((headerContactMenu: HeaderContactMenu) => {
          this.headerContactMenu = headerContactMenu;
          this.form = new FormGroup({
            linkTitle: new FormControl(this.headerContactMenu.linkTitle, [Validators.required]),
            targetUri: new FormControl(this.headerContactMenu.targetUri, [Validators.required]),
            label: new FormControl(this.headerContactMenu.label, []),
            disabled: new FormControl(!this.headerContactMenu.disabled, []),
            inApp: new FormControl(this.headerContactMenu.inApp, []),
            authRequired: new FormControl(this.headerContactMenu.authRequired, []),
            systemID: new FormControl(this.headerContactMenu.systemID, []),
            startUrl: new FormControl(this.headerContactMenu.startUrl, [])
          });
          this.breadcrumbsData = [{
            label: `Header Contact menus`,
            url: `/menus/header-contact-menus`
          }, {
            label: this.headerContactMenu.linkTitle,
            url: `/menus/header-contact-menus/${this.headerContactMenu.id}`
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
    this.apiClientService.headerContactMenu()
      .update(this.headerContactMenu)
      .map((data: HttpResponse<HeaderContactMenu>) => {
        return data.body;
      })
      .subscribe((data: HeaderContactMenu) => {
        this.headerContactMenu = data;
        this.actionButtons.extendCollection(this.headerContactMenu);
        this.dialogService.showNotificationDialog({
          title: 'Header Contact Menu',
          message: 'Header Contact Menu is Saved.'
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
    this.apiClientService.headerContactMenu()
      .delete(this.headerContactMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/header-contact-menus/']);
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

}
