import { Component, OnInit, ViewChild } from '@angular/core';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { LUCKYDIP_MAPPING, LUCKYDIP_MAPPING_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { ApiClientService } from '@root/app/client/private/services/http';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ErrorService } from '@root/app/client/private/services/error.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsSurfaceBetsService } from '@root/app/sports-modules/surface-bets/surface-bets.service';
import { ILuckyDipMapping } from '../lucky-dip-v2.model';

@Component({
  selector: 'app-lucky-dip-mapping-edit',
  templateUrl: './lucky-dip-mapping-edit.component.html'
})

export class LuckyDipMappingEditComponent implements OnInit {
  public form: FormGroup;
  id: string;
  isReady: boolean;
  public sportCategories: SportCategory[] = [];
  public readonly LUCKYDIP_MAPPING = LUCKYDIP_MAPPING;
  public readonly LUCKYDIP_MAPPING_CONST = LUCKYDIP_MAPPING_CONST;
  luckyDipMapping: ILuckyDipMapping;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private errorService: ErrorService,
    private route: ActivatedRoute,
    private router: Router,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.sportsSurfaceBetsService.getSportCategories().subscribe((response) => {
      this.sportCategories = response;
    });
    this.id = this.route.snapshot.paramMap.get('id');
    this.getLuckyDipMappingDetails(this.id);
  }

  getLuckyDipMappingDetails(id: string) {
    this.apiClientService.luckyDipService().getLuckyDipMappingData(id).subscribe((luckyDipMapping: ILuckyDipMapping) => {
      this.luckyDipMapping = luckyDipMapping;
      this.breadcrumbsData = [{
        label: `Lucky Dip Mapping`,
        url: `/lucky-dip/mapping`
      }, {
        label: this.luckyDipMapping.categoryId,
        url: `/lucky-dip/mapping/edit/${this.luckyDipMapping.id}`
      }];
      this.isReady = true;
      this.generateForm();
    }, error => {
      console.error(error.message);
    });
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
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
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

  deleteLuckyDipMapping(id: string) {
    this.apiClientService.luckyDipService().deleteLuckyDipMapping(id).subscribe(() => {
      this.router.navigate(['lucky-dip/mapping']);
    }, error => {
      console.error(error.message);
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.deleteLuckyDipMapping(this.id);
        break;
      case 'save':
        this.saveluckyDipMapping();
        break;
      case 'revert':
        this.getLuckyDipMappingDetails(this.id);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
