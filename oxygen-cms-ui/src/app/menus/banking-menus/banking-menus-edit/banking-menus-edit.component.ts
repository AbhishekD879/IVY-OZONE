import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import { BrandService } from '@app/client/private/services/brand.service';
import {BankingMenu} from '../../../client/private/models/bankingmenu.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './banking-menus-edit.component.html',
  styleUrls: ['./banking-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class BankingMenusEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  public bankingMenu: BankingMenu;
  public form: FormGroup;
  public sections: Array<string> = ['top', 'center', 'bottom'];
  public types: Array<string> = ['link', 'button'];
  public viewModes: Array<string> = ['both', 'icon', 'description'];
  public alignmentModes: Array<string> = ['left', 'right'];
  public breadcrumbsData: Breadcrumb[];
  public isIMActive: boolean;

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
      this.apiClientService.bankingMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<BankingMenu>) => {
          return data.body;
        })
        .subscribe((bankingMenu: BankingMenu) => {
          this.bankingMenu = bankingMenu;
          this.form = new FormGroup({
            linkTitle: new FormControl(this.bankingMenu.linkTitle, [Validators.required]),
            subHeader: new FormControl(this.bankingMenu.subHeader, []),
            targetUri: new FormControl(this.bankingMenu.targetUri, [Validators.required]),
            section: new FormControl(this.bankingMenu.section, []),
            type: new FormControl(this.bankingMenu.type, []),
            disabled: new FormControl(!this.bankingMenu.disabled, []),
            inApp: new FormControl(this.bankingMenu.inApp, []),
            qa: new FormControl(this.bankingMenu.qa, []),
            showItemFor: new FormControl(this.bankingMenu.showItemFor, []),
            showOnlyOnIOS: new FormControl(this.bankingMenu.showOnlyOnIOS, []),
            showOnlyOnAndroid: new FormControl(this.bankingMenu.showOnlyOnAndroid, []),
            menuItemView: new FormControl(this.bankingMenu.menuItemView, []),
            iconAligment: new FormControl(this.bankingMenu.iconAligment, []),
            authRequired: new FormControl(this.bankingMenu.authRequired, []),
            systemID: new FormControl(this.bankingMenu.systemID, []),
            startUrl: new FormControl(this.bankingMenu.startUrl, [])
          });
          this.breadcrumbsData = [{
            label: `Banking Menus`,
            url: `/menus/banking-menus`
          }, {
            label: this.bankingMenu.linkTitle,
            url: `/menus/banking-menus/${this.bankingMenu.id}`
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
    this.apiClientService.bankingMenu()
      .update(this.bankingMenu)
      .map((data: HttpResponse<BankingMenu>) => {
        return data.body;
      })
      .subscribe((data: BankingMenu) => {
        this.bankingMenu = data;
        this.actionButtons.extendCollection(this.bankingMenu);
        this.dialogService.showNotificationDialog({
          title: 'Banking Menu',
          message: 'Banking Menu is Saved.'
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
    this.apiClientService.bankingMenu()
      .delete(this.bankingMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/banking-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onSectionChanged(): void {
    this.bankingMenu.section = this.form.value.section;
  }

  onTypeChanged(): void {
    this.bankingMenu.type = this.form.value.type;
  }

  onShowModeChanged(mode: string): void {
    this.bankingMenu.showItemFor = mode;
  }

  onViewModeChanged(): void {
    this.bankingMenu.menuItemView = this.form.value.menuItemView;
  }

  onAlignmentModeChanged(): void {
    this.bankingMenu.iconAligment = this.form.value.iconAligment;
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
    this.apiClientService.bankingMenu()
      .uploadImage(this.bankingMenu.id, file)
      .map((data: HttpResponse<BankingMenu>) => {
        return data.body;
      })
      .subscribe((data: BankingMenu) => {
        this.bankingMenu = _.extend(data, _.pick(this.bankingMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
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
    this.apiClientService.bankingMenu()
      .removeImage(this.bankingMenu.id)
      .map((data: HttpResponse<BankingMenu>) => {
        return data.body;
      })
      .subscribe((data: BankingMenu) => {
        this.bankingMenu = _.extend(data, _.pick(this.bankingMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
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
    this.apiClientService.bankingMenu()
      .uploadSvg(this.bankingMenu.id, file)
      .map((data: HttpResponse<BankingMenu>) => {
        return data.body;
      })
      .subscribe((data: BankingMenu) => {
        this.bankingMenu = _.extend(data, _.pick(this.bankingMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
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
    this.apiClientService.bankingMenu()
      .removeSvg(this.bankingMenu.id)
      .map((data: HttpResponse<BankingMenu>) => {
        return data.body;
      })
      .subscribe((data: BankingMenu) => {
        this.bankingMenu = _.extend(data, _.pick(this.bankingMenu, 'linkTitle', 'targetUri', 'alt', 'qa', 'systemID',
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
