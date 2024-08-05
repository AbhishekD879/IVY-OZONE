import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { BrandService } from '../../../client/private/services/brand.service';
import { DialogService } from '../../../shared/dialog/dialog.service';
import { BybAPIService } from '../../service/byb.api.service';
import { BYBSwitcher } from '../../../client/private/models';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';

@Component({
  selector: 'byb-switchers-edit',
  templateUrl: './byb-switchers-edit.component.html',
  styleUrls: ['./byb-switchers-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class BYBSwitchersEditComponent implements OnInit {

  getDataError: string;
  public bybSwitcher: BYBSwitcher;
  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];
  public form: FormGroup;

  constructor(
    private bybSwitchersService: BybAPIService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router,
    private brandService: BrandService,
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  public saveChanges(): void {
    this.globalLoaderService.showLoader();
    const updatedSwitcher = this.getBYBSwitcher();
    this.bybSwitcher.name = updatedSwitcher.name;
    this.bybSwitcher.provider = updatedSwitcher.provider;
    this.bybSwitcher.enabled = updatedSwitcher.enabled;
    this.bybSwitcher.default = updatedSwitcher.default;

    this.bybSwitchersService
      .putSwitcherChanges(this.bybSwitcher)
      .map((bybSwitcher: HttpResponse<BYBSwitcher>) => {
        return bybSwitcher.body;
      })
      .subscribe((data: BYBSwitcher) => {
        this.bybSwitcher = data;
        this.actionButtons.extendCollection(this.bybSwitcher);
        this.dialogService.showNotificationDialog({
          title: `BYB Switcher`,
          message: `BYB Switcher is Saved`
        });
      });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public getBYBSwitcher(): BYBSwitcher {
    return this.form.value;
  }

  public removeBYBSwitcher(): void {
    this.bybSwitchersService.deleteSwitcher(this.bybSwitcher.id)
      .subscribe(() => {
        this.router.navigate(['/byb/byb-switchers']);
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeBYBSwitcher();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private loadInitData(): void {
    this.getDataError = '';

    this.activatedRoute.params.subscribe((params: Params) => {
      this.bybSwitchersService.getSingleSwitcher(params['id'])
        .map((bybSwitcher: HttpResponse<BYBSwitcher>) => {
          return bybSwitcher.body;
        })
        .subscribe((bybSwitcher: BYBSwitcher) => {
          this.bybSwitcher = bybSwitcher;
          this.breadcrumbsData = [{
            label: `BYB Switchers`,
            url: `/byb/byb-switchers`
          }, {
            label: this.bybSwitcher.name,
            url: `/byb/byb-switchers/${this.bybSwitcher.id}`
          }];

          this.form = new FormGroup({
            name: new FormControl(this.bybSwitcher.name, [Validators.required]),
            provider: new FormControl(this.bybSwitcher.provider, [Validators.required]),
            default: new FormControl(this.bybSwitcher.default, []),
            enabled: new FormControl(this.bybSwitcher.enabled, []),
            brand: new FormControl(this.brandService.brand, [Validators.required])
          });

        }, error => {
          this.getDataError = error.message;
        });
    });
  }
}

