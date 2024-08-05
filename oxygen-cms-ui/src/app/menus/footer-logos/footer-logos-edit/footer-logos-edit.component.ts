import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {FooterLogo} from '../../../client/private/models/footerlogo.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './footer-logos-edit.component.html',
  styleUrls: ['./footer-logos-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class FooterLogosEditComponent implements OnInit {

  public footerLogo: FooterLogo;
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
      this.apiClientService.footerLogo()
        .findOne(params['id'])
        .map((data: HttpResponse<FooterLogo>) => {
          return data.body;
        })
        .subscribe((footerLogo: FooterLogo) => {
          this.footerLogo = footerLogo;
          this.form = new FormGroup({
            title: new FormControl(this.footerLogo.title, [Validators.required]),
            target: new FormControl(this.footerLogo.target, [Validators.required]),
            disabled: new FormControl(!this.footerLogo.disabled, [])
          });
          this.breadcrumbsData = [{
            label: `Footer Logos`,
            url: `/menus/footer-logos`
          }, {
            label: this.footerLogo.title,
            url: `/menus/footer-logos/${this.footerLogo.id}`
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
    this.apiClientService.footerLogo()
      .update(this.footerLogo)
      .map((data: HttpResponse<FooterLogo>) => {
        return data.body;
      })
      .subscribe((data: FooterLogo) => {
        this.footerLogo = data;
        this.actionButtons.extendCollection(this.footerLogo);
        this.dialogService.showNotificationDialog({
          title: 'Footer Logo',
          message: 'Footer Logo is Saved.'
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
    this.apiClientService.footerLogo()
      .delete(this.footerLogo.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/footer-logos/']);
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

  uploadPngHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerLogo()
      .uploadPng(this.footerLogo.id, file)
      .map((data: HttpResponse<FooterLogo>) => {
        return data.body;
      })
      .subscribe((data: FooterLogo) => {
        this.footerLogo = _.extend(data, _.pick(this.footerLogo, 'title', 'target'));
        this.snackBar.open(`Png Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removePngHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerLogo()
      .removePng(this.footerLogo.id)
      .map((data: HttpResponse<FooterLogo>) => {
        return data.body;
      })
      .subscribe((data: FooterLogo) => {
        this.footerLogo = _.extend(data, _.pick(this.footerLogo, 'title', 'target'));
        this.snackBar.open(`Png Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  uploadSvgHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.footerLogo()
      .uploadSvg(this.footerLogo.id, file)
      .map((data: HttpResponse<FooterLogo>) => {
        return data.body;
      })
      .subscribe((data: FooterLogo) => {
        this.footerLogo = _.extend(data, _.pick(this.footerLogo, 'title', 'target'));
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
    this.apiClientService.footerLogo()
      .removeSvg(this.footerLogo.id)
      .map((data: HttpResponse<FooterLogo>) => {
        return data.body;
      })
      .subscribe((data: FooterLogo) => {
        this.footerLogo = _.extend(data, _.pick(this.footerLogo, 'title', 'target'));
        this.snackBar.open(`Svg Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
}
