import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {FooterMenu} from '../../../client/private/models/footermenu.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants, CSPSegmentLSConstants} from '@app/app.constants';
import * as _ from 'lodash';
import { BrandService } from '@app/client/private/services/brand.service';
import { ISegmentModel } from '@app/client/private/models/segment.model';
import { SegmentStoreService } from '@app/client/private/services/segment-store.service';

@Component({
  templateUrl: './footer-menus-edit.component.html',
  styleUrls: ['./footer-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class FooterMenusEditComponent implements OnInit {

  public footerMenu: FooterMenu;
  public form: FormGroup;
  public showModes: Array<string> = ['both', 'logged in', 'logged out'];
  public breadcrumbsData: Breadcrumb[];
  public isIMActive: boolean;
  public isRevert = false;
  segmentsList: ISegmentModel = {
    exclusionList: [],
    inclusionList: [],
    universalSegment: true
  };
  isSegmentValid: boolean = false;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private brandService: BrandService,
    private segmentStoreService: SegmentStoreService
  ) {
    this.isIMActive = this.brandService.isIMActive();
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.footerMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<FooterMenu>) => {
          return data.body
        })
        .subscribe((footerMenu: FooterMenu) => {
          if (footerMenu) {
            this.footerMenu = footerMenu;
            this.form = new FormGroup({
              linkTitle: new FormControl(this.footerMenu.linkTitle, [Validators.required]),
              targetUri: new FormControl(this.footerMenu.targetUri, []),
              disabled: new FormControl(!this.footerMenu.disabled, []),
              inApp: new FormControl(this.footerMenu.inApp, []),
              mobile: new FormControl(this.footerMenu.mobile, []),
              tablet: new FormControl(this.footerMenu.tablet, []),
              desktop: new FormControl(this.footerMenu.desktop, []),
              authRequired: new FormControl(this.footerMenu.authRequired, []),
              showItemFor: new FormControl(this.footerMenu.showItemFor, []),
              systemID: new FormControl(this.footerMenu.systemID, [])
            });
            this.segmentsList = {
              exclusionList: this.footerMenu.exclusionList,
              inclusionList: this.footerMenu.inclusionList,
              universalSegment: this.footerMenu.universalSegment
            };

            this.breadcrumbsData = [{
              label: `Footer Menus`,
              url: `/menus/footer-menus`
            }, {
              label: this.footerMenu.linkTitle,
              url: `/menus/footer-menus/${this.footerMenu.id}`
            }];
            this.globalLoaderService.hideLoader();
          }
        }, error => {
          this.globalLoaderService.hideLoader();
        });
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerMenu()
      .update(this.footerMenu)
      .map((data: HttpResponse<FooterMenu>) => {
        return data.body;
      })
      .subscribe((data: FooterMenu) => {
        const self = this;
        this.footerMenu = data;
        this.actionButtons.extendCollection(this.footerMenu);
        this.segmentStoreService.setSegmentValue(this.footerMenu ,CSPSegmentLSConstants.FOOTER_MENU_RIBBON);
        this.dialogService.showNotificationDialog({
          title: AppConstants.FOOTER_MENU,
          message: AppConstants.FOOTER_MENU_SAVED,
          closeCallback() {
            self.router.navigate([`/menus/footer-menus`]);
          }
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
    this.isRevert = true;
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerMenu()
      .delete(this.footerMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/footer-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onShowModeChanged(option: string): void {
    this.footerMenu.showItemFor = option;
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
    this.apiClientService.footerMenu()
      .uploadImage(this.footerMenu.id, file)
      .map((data: HttpResponse<FooterMenu>) => {
        return data.body;
      })
      .subscribe((data: FooterMenu) => {
        this.footerMenu = _.extend(data, _.pick(this.footerMenu, Object.keys(this.form.controls)));
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
    this.apiClientService.footerMenu()
      .removeImage(this.footerMenu.id)
      .map((data: HttpResponse<FooterMenu>) => data.body)
      .subscribe((data: FooterMenu) => {
        this.footerMenu = _.extend(data, _.pick(this.footerMenu, Object.keys(this.form.controls)));
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
    this.apiClientService.footerMenu()
      .uploadSvg(this.footerMenu.id, file)
      .map((data: HttpResponse<FooterMenu>) => {
        return data.body;
      })
      .subscribe((data: FooterMenu) => {
        this.footerMenu = _.extend(data, _.pick(this.footerMenu, Object.keys(this.form.controls)));
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
    this.apiClientService.footerMenu()
      .removeSvg(this.footerMenu.id)
      .map((data: HttpResponse<FooterMenu>) => data.body)
      .subscribe((data: FooterMenu) => {
        this.footerMenu = _.extend(data, _.pick(this.footerMenu, Object.keys(this.form.controls)));
        this.snackBar.open(`Svg Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  /*
  *Disables save button based upon the return type
   */
  public validationHandler(): boolean {
    return this.form.valid && this.isSegmentValid;
  }

  /**
   * updates issegmentvalid true/false on child form changes
  */
  isSegmentFormValid(isValid: boolean): void {
    this.isSegmentValid = isValid;
  }

  /*
   * Handles logic for child emitted data. 
  */
  modifiedSegmentsHandler(segmentConfigData: ISegmentModel): void {
    this.isRevert = false;
    this.footerMenu = { ...this.footerMenu, ...segmentConfigData };
  }
}
