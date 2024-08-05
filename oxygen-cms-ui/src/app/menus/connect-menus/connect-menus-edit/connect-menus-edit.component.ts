import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

import { DialogService} from '../../../shared/dialog/dialog.service';
import { ConnectMenu} from '../../../client/private/models/connectmenu.model';
import { ApiClientService } from '../../../client/private/services/http';
import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';
import { AppConstants } from '../../../app.constants';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  templateUrl: './connect-menus-edit.component.html',
  styleUrls: ['./connect-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class ConnectMenusEditComponent implements OnInit {

  public connectMenu: ConnectMenu;
  public connectMenus: ConnectMenu[];
  public form: FormGroup;
  public menuLevels: Array<string> = ['1', '2'];
  public showModes: Array<string> = ['Both', 'Logged In', 'Logged Out'];
  public breadcrumbsData: Breadcrumb[];
  public isIMActive: boolean;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private brandService: BrandService
  ) {
    this.isIMActive = this.brandService.isIMActive();
  }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.connectMenu()
        .findAllByBrand()
        .map((data: HttpResponse<ConnectMenu[]>) => {
          return data.body;
        })
        .subscribe((connectMenues: ConnectMenu[]) => {
          this.connectMenus = connectMenues;
          this.connectMenu = _.find(connectMenues, (menu: ConnectMenu) => menu.id === params['id']);
          this.form = new FormGroup({
            disabled: new FormControl(!this.connectMenu.disabled, []),
            inApp: new FormControl(this.connectMenu.inApp, []),
            upgradePopup: new FormControl(this.connectMenu.upgradePopup, []),
            linkTitle: new FormControl(this.connectMenu.linkTitle, [Validators.required]),
            linkSubtitle: new FormControl(this.connectMenu.targetUri, []),
            targetUri: new FormControl(this.connectMenu.targetUri, [Validators.required]),
            level: new FormControl(this.connectMenu.level, [Validators.required]),
            showItemFor: new FormControl(this.connectMenu.showItemFor, []),
            parent: new FormControl(this.connectMenu.parent, [])
          });
          this.breadcrumbsData = [{
            label: `Connect Menus`,
            url: `/menus/connect-menus`
          }, {
            label: this.connectMenu.linkTitle,
            url: `/menus/connect-menus/${this.connectMenu.id}`
          }];
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  onParentChanged(): void {
    this.connectMenu.parent = this.form.value.parent;
  }

  public getParentLink(): string {
    return `/menus/connect-menus/${this.connectMenu.parent}`;
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.connectMenu()
      .update(this.connectMenu)
      .map((data: HttpResponse<ConnectMenu>) => {
        return data.body;
      })
      .subscribe((data: ConnectMenu) => {
        this.connectMenu = data;
        this.actionButtons.extendCollection(this.connectMenu);
        this.dialogService.showNotificationDialog({
          title: 'Connect Menu',
          message: 'Connect Menu is Saved.'
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
    this.apiClientService.connectMenu()
      .delete(this.connectMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/connect-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onLevelChanged(): void {
    this.connectMenu.level = this.form.value.level;
  }

  onShowModeChanged(): void {
    this.connectMenu.showItemFor = this.form.value.showItemFor;
  }

  uploadSvgHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.connectMenu()
      .uploadSvg(this.connectMenu.id, file)
      .map((data: HttpResponse<ConnectMenu>) => {
        return data.body;
      })
      .subscribe((data: ConnectMenu) => {
        this.connectMenu = _.extend(data, _.pick(this.connectMenu, 'level', 'linkTitle', 'showItemFor', 'targetUri'));
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeSvgHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.connectMenu()
      .removeSvg(this.connectMenu.id)
      .map((data: HttpResponse<ConnectMenu>) => {
        return data.body;
      })
      .subscribe((data: ConnectMenu) => {
        this.connectMenu = _.extend(data, _.pick(this.connectMenu, 'level', 'linkTitle', 'showItemFor', 'targetUri'));
        this.snackBar.open(`Image Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {

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
