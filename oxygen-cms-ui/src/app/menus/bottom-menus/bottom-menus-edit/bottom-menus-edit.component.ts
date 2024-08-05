import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';

import { DialogService } from '../../../shared/dialog/dialog.service';
import { BottomMenu } from '../../../client/private/models/bottommenu.model';
import { ApiClientService } from '../../../client/private/services/http';
import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';

@Component({
  templateUrl: './bottom-menus-edit.component.html',
  styleUrls: ['./bottom-menus-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class BottomMenusEditComponent implements OnInit {

  public bottomMenu: BottomMenu;
  public form: FormGroup;
  public sections: Array<string> = ['help', 'quick links'];
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
      this.apiClientService.bottomMenu()
        .findOne(params['id'])
        .map((data: HttpResponse<BottomMenu>) => {
          return data.body;
        })
        .subscribe((bottomMenu: BottomMenu) => {
          this.bottomMenu = bottomMenu;
          this.form = new FormGroup({
            linkTitle: new FormControl(this.bottomMenu.linkTitle, [Validators.required]),
            targetUri: new FormControl(this.bottomMenu.targetUri, [Validators.required]),
            section: new FormControl(this.bottomMenu.section, [Validators.required]),
            disabled: new FormControl(!this.bottomMenu.disabled, []),
            inApp: new FormControl(this.bottomMenu.inApp, []),
            authRequired: new FormControl(this.bottomMenu.authRequired, []),
            systemID: new FormControl(this.bottomMenu.systemID, []),
            startUrl: new FormControl(this.bottomMenu.startUrl, [])
          });
          this.breadcrumbsData = [{
            label: `Bottom Menus`,
            url: `/menus/bottom-menus`
          }, {
            label: this.bottomMenu.linkTitle,
            url: `/menus/bottom-menus/${this.bottomMenu.id}`
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
    this.apiClientService.bottomMenu()
      .update(this.bottomMenu)
      .map((data: HttpResponse<BottomMenu>) => {
        return data.body;
      })
      .subscribe((data: BottomMenu) => {
        this.bottomMenu = data;
        this.actionButtons.extendCollection(this.bottomMenu);
        this.dialogService.showNotificationDialog({
          title: 'Bottom Menu',
          message: 'Bottom Menu is Saved.'
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
    this.apiClientService.bottomMenu()
      .delete(this.bottomMenu.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/menus/bottom-menus/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  onSectionChanged(value: string): void {
    this.bottomMenu.section = this.form.value.section;
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
