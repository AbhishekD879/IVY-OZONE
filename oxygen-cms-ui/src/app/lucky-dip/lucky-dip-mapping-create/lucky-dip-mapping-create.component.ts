import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { LUCKYDIP_MAPPING, LUCKYDIP_MAPPING_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsSurfaceBetsService } from '@root/app/sports-modules/surface-bets/surface-bets.service';
import { ILuckyDipMapping } from '../lucky-dip-v2.model';

@Component({
  selector: 'app-lucky-dip-mapping-create',
  templateUrl: './lucky-dip-mapping-create.component.html'
})

export class LuckyDipMappingCreateComponent implements OnInit {
  public form: FormGroup;

  isReady: boolean;
  public sportCategories: SportCategory[] = [];
  public readonly LUCKYDIP_MAPPING = LUCKYDIP_MAPPING;
  public readonly LUCKYDIP_MAPPING_CONST = LUCKYDIP_MAPPING_CONST;
  luckyDipMapping: ILuckyDipMapping;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  breadcrumbsData = [{
    label: `Lucky Dip Mapping`,
    url: `/lucky-dip/mapping`
  }, {
    label: 'CREATE LUCKY DIP MAPPING',
    url: `/lucky-dip/mapping-create`
  }];
  constructor(
    private apiClientService: ApiClientService,
    private brandService: BrandService,
    private dialogService: DialogService,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
    private router: Router,
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.isReady = true;
    this.luckyDipMapping = {
      ...LUCKYDIP_MAPPING,
      brand: this.brandService.brand
    };
    this.sportsSurfaceBetsService.getSportCategories().subscribe((response) => {
      this.sportCategories = response;
    });
    this.generateForm();
  }

  saveluckyDipMapping() {
    const method = this.luckyDipMapping.id ? 'put' : 'post';
    this.apiClientService.luckyDipService().saveluckyDipMapping(method, this.luckyDipMapping, this.luckyDipMapping.id || '')
      .subscribe(data => {
        this.luckyDipMapping = data.body;
        this.actionButtons.extendCollection(this.luckyDipMapping);
        this.dialogService.showNotificationDialog({
          title: 'Save Completed',
          message: 'Lucky Dip Mapping is Stored',
          closeCallback: () => {
            this.router.navigate(['lucky-dip/mapping']);
          }
        });
      },
        error => {
          this.dialogService.showNotificationDialog({
            title: 'Error',
            message: error
          });
        });
  }

  generateForm(): void {
    this.form = new FormGroup({
      categoryId: new FormControl(this.luckyDipMapping?.categoryId, [Validators.required]),
      typeIds: new FormControl(this.luckyDipMapping?.typeIds, [Validators.required]),
      active: new FormControl(this.luckyDipMapping?.active, [Validators.required]),
    });
  }

  public validationHandler(): boolean {
    return this.form && this.form.valid
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.saveluckyDipMapping();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
