import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {RightMenu} from '../../../client/private/models/rightmenu.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './right-menus-edit.component.html',
  styleUrls: ['./right-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class RightMenusEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  public rightMenu: RightMenu;
  public form: FormGroup;
  public sections: Array<string> = ['top', 'center', 'bottom'];
  public types: Array<string> = ['link', 'button'];
  public viewModes: Array<string> = ['both', 'icon', 'description'];
  public alignmentModes: Array<string> = ['left', 'right'];
  public breadcrumbsData: Breadcrumb[];

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
      this.apiClientService.rightMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<RightMenu>) => {
          return data.body;
        })
        .subscribe((rightMenu: RightMenu) => {
          this.rightMenu = rightMenu;
          this.form = new FormGroup({
            linkTitle: new FormControl(this.rightMenu.linkTitle, [Validators.required]),
            subHeader: new FormControl(this.rightMenu.subHeader, []),
            targetUri: new FormControl(this.rightMenu.targetUri, [Validators.required]),
            section: new FormControl(this.rightMenu.section, []),
            type: new FormControl(this.rightMenu.type, []),
            disabled: new FormControl(!this.rightMenu.disabled, []),
            inApp: new FormControl(this.rightMenu.inApp, []),
            qa: new FormControl(this.rightMenu.qa, []),
            showItemFor: new FormControl(this.rightMenu.showItemFor, []),
            showOnlyOnIOS: new FormControl(this.rightMenu.showOnlyOnIOS, []),
            showOnlyOnAndroid: new FormControl(this.rightMenu.showOnlyOnAndroid, []),
            menuItemView: new FormControl(this.rightMenu.menuItemView, []),
            iconAligment: new FormControl(this.rightMenu.iconAligment, []),
            authRequired: new FormControl(this.rightMenu.authRequired, []),
            systemID: new FormControl(this.rightMenu.systemID, []),
            startUrl: new FormControl(this.rightMenu.startUrl, [])
          });
          this.breadcrumbsData = [{
            label: `Right Menus`,
            url: `/menus/right-menus`
          }, {
            label: this.rightMenu.linkTitle,
            url: `/menus/right-menus/${this.rightMenu.id}`
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
    this.apiClientService.rightMenu()
      .update(this.rightMenu)
      .map((data: HttpResponse<RightMenu>) => {
        return data.body;
      })
      .subscribe((data: RightMenu) => {
        this.rightMenu = data;
        this.actionButtons.extendCollection(this.rightMenu);
        this.dialogService.showNotificationDialog({
          title: 'Right Menu',
          message: 'Right Menu is Saved.'
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
    this.apiClientService.rightMenu()
      .delete(this.rightMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/right-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onSectionChanged(): void {
    this.rightMenu.section = this.form.value.section;
  }

  onTypeChanged(): void {
    this.rightMenu.type = this.form.value.type;
  }

  onShowModeChanged(mode: string): void {
    this.rightMenu.showItemFor = mode;
  }

  onViewModeChanged(): void {
    this.rightMenu.menuItemView = this.form.value.menuItemView;
  }

  onAlignmentModeChanged(): void {
    this.rightMenu.iconAligment = this.form.value.iconAligment;
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

  uploadImageHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.rightMenu()
      .uploadImage(this.rightMenu.id, file)
      .map((data: HttpResponse<RightMenu>) => {
        return data.body;
      })
      .subscribe((data: RightMenu) => {
        this.rightMenu = _.extend(data, _.pick(this.rightMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
          'section', 'type', 'showItemFor', 'menuItemView', 'iconAligment', 'startUrl'));
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeImageHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.rightMenu()
      .removeImage(this.rightMenu.id)
      .map((data: HttpResponse<RightMenu>) => {
        return data.body;
      })
      .subscribe((data: RightMenu) => {
        this.rightMenu = _.extend(data, _.pick(this.rightMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
          'section', 'type', 'showItemFor', 'menuItemView', 'iconAligment', 'startUrl'));
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
    this.apiClientService.rightMenu()
      .uploadSvg(this.rightMenu.id, file)
      .map((data: HttpResponse<RightMenu>) => {
        return data.body;
      })
      .subscribe((data: RightMenu) => {
        this.rightMenu = _.extend(data, _.pick(this.rightMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
          'section', 'type', 'showItemFor', 'menuItemView', 'iconAligment', 'startUrl'));
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
    this.apiClientService.rightMenu()
      .removeSvg(this.rightMenu.id)
      .map((data: HttpResponse<RightMenu>) => {
        return data.body;
      })
      .subscribe((data: RightMenu) => {
        this.rightMenu = _.extend(data, _.pick(this.rightMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
          'section', 'type', 'showItemFor', 'menuItemView', 'iconAligment', 'startUrl'));
        this.snackBar.open(`Svg Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
}
