import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {OnBoardingGuide} from '@app/client/private/models/onBoardingGuide';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';
import {AppConstants} from '@app/app.constants';

@Component({
  selector: 'app-on-boarding-guide-edit',
  templateUrl: './on-boarding-guide-edit.component.html',
  providers: [
    DialogService
  ]
})
export class OnBoardingGuideEditComponent implements OnInit {

  public onBoardingGuide: OnBoardingGuide;
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

  ngOnInit(): void {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.onBoardingGuide()
        .getSingleOnBoardingGuide(params['id'])
        .map((data: HttpResponse<OnBoardingGuide>) => {
          return data.body;
        })
        .subscribe((onBoardingGuide: OnBoardingGuide) => {
          this.onBoardingGuide = onBoardingGuide;
          this.form = new FormGroup({
            enabled: new FormControl(!this.onBoardingGuide.enabled, []),
            name: new FormControl(this.onBoardingGuide.guideName, [Validators.required]),
          });
          this.breadcrumbsData = [{
            label: `On Boarding Guide`,
            url: `/on-boarding-guide/`
          }, {
            label: this.onBoardingGuide.guideName,
            url: `/on-boarding-guide/${this.onBoardingGuide.id}`
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
    this.apiClientService.onBoardingGuide()
      .putOnBoardingGuideChanges(this.onBoardingGuide.id, this.onBoardingGuide)
      .map((data: HttpResponse<OnBoardingGuide>) => {
        return data.body;
      })
      .subscribe((data: OnBoardingGuide) => {
        this.onBoardingGuide = data;
        this.actionButtons.extendCollection(this.onBoardingGuide);
        this.dialogService.showNotificationDialog({
          title: 'On Boarding Guide',
          message: 'On Boarding Guide is Saved.'
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
    this.apiClientService.onBoardingGuide()
      .deleteOnBoardingGuide(this.onBoardingGuide.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/on-boarding-guide/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  uploadSVGHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.onBoardingGuide()
      .postOnBoardingGuideImage(this.onBoardingGuide.id, file)
      .map((data: HttpResponse<OnBoardingGuide>) => {
        return data.body;
      })
      .subscribe((data: OnBoardingGuide) => {
        this.onBoardingGuide = _.extend(data, _.pick(this.onBoardingGuide, 'name'));
        this.snackBar.open(`SVG image is uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeSVGHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.onBoardingGuide()
      .removeOnBoardingGuideImage(this.onBoardingGuide.id)
      .map((data: HttpResponse<OnBoardingGuide>) => {
        return data.body;
      })
      .subscribe((data: OnBoardingGuide) => {
        this.onBoardingGuide = _.extend(data, _.pick(this.onBoardingGuide, 'name'));
        this.snackBar.open(`SVG image is deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
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
