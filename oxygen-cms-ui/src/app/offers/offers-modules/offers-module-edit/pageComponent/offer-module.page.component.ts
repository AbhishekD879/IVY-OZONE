import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { OfferModule } from '../../../../client/private/models/offermodule.model';
import { OfferModuleAPIService } from '../../../service/offer-module.api.service';
import { DialogService } from '../../../../shared/dialog/dialog.service';
import { HttpResponse } from '@angular/common/http';
import { Breadcrumb } from '../../../../client/private/models/breadcrumb.model';

@Component({
  selector: 'offer-module-page',
  templateUrl: './offer-module.page.component.html',
  styleUrls: ['./offer-module.page.component.scss']
})
export class OfferModulePageComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;

  getDataError: string;
  offerModule: OfferModule;
  id: string;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private offerModuleAPIService: OfferModuleAPIService
  ) {}

  /**
   * Checks whether offer data are provided correctly
   */
  isValidModel(offerModule: OfferModule) {
    return offerModule.name.length > 0;
  }

  /**
   * Reset changes appplied to offer
   */
  revertOfferModuleChanges() {
    this.loadInitialData();
  }

    /**
   * Send DELETE API request
   * @param {Offer} offer
   */
  removeOfferModule() {
    this.offerModuleAPIService.deleteOfferModule(this.offerModule.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Offer Module is Removed.'
        });
        this.router.navigate(['/offers/offer-modules/']);
      });
  }

  /**
   * Make PUT request to server to update
   */
  saveOfferModuleChanges() {
    this.offerModuleAPIService.putOfferModulesChanges(this.offerModule)
      .map((response: HttpResponse<OfferModule>) => {
        return response.body;
      })
      .subscribe((data: OfferModule) => {
        this.offerModule = data;
        this.actionButtons.extendCollection(this.offerModule);
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'Offer Module Changes are Saved.'
        });
      });
  }

  /**
   * Load initial data to initialize component
   */
  loadInitialData() {
    this.offerModuleAPIService.getSingleOfferModulesData(this.id)
      .subscribe((data: any) => {
        this.offerModule = data.body;
        this.breadcrumbsData = [{
          label: `Offer modules`,
          url: `/offers/offer-modules`
        }, {
          label: this.offerModule.name,
          url: `/offers/offer-modules/${this.offerModule.id}`
        }];
      }, error => {
        this.getDataError = error.message;
      });
  }

  onShowModuleOnChange(value: string): void  {
    this.offerModule.showModuleOn = value;
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeOfferModule();
        break;
      case 'save':
        this.saveOfferModuleChanges();
        break;
      case 'revert':
        this.revertOfferModuleChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
