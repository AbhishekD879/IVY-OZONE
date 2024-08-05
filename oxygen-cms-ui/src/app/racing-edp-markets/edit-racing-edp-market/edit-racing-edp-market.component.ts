import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { RacingEdpMarket } from '../../client/private/models/racing.edpmarket.model';
import { Breadcrumb } from '../../client/private/models';
import { DialogService } from '../../shared/dialog/dialog.service';
import { ACTION_TYPE, RACING_EDP_ERRORS, SAVE_NOTIFICATION_DIALOG, RACING_EDP_ROUTES, BREADCRUMBS_LABEL } from '../constants/racing-edp.constants';
import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-racing-edp-market',
  templateUrl: './edit-racing-edp-market.component.html'
})
export class EditRacingEdpMarketComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  racingEDPMarket: RacingEdpMarket;
  breadCrumbs: Breadcrumb[];
  racingEdpForm: FormGroup;
  isLoading: boolean = false;
  private birEnabledMarkets: string[];
  isBirMarketFlag: boolean;

  constructor(private activatedRoute: ActivatedRoute,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private router: Router,
    private dialogService: DialogService) { }

  ngOnInit(): void {
    this.racingEdpForm = new FormGroup({
      name: new FormControl('', [Validators.required]),
      description: new FormControl('', [Validators.maxLength(200)]),
      birDescription: new FormControl('', [Validators.maxLength(200)])
    });
    this.loadInitData();
    this.getBirEnabledMarkets();
  }

  /**
   * Verify the validity of form
   * @param {RacingEdpMarket} edpMarket
   * @returns {boolean}
   */
  isValidForm(edpMarket: RacingEdpMarket): boolean {
    return !!(edpMarket.name && edpMarket.name.length > 0);
  }

  /**
   * Handler for each action of action-button
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case ACTION_TYPE.remove:
        this.removeRacingEdpMarket();
        break;
      case ACTION_TYPE.save:
        this.saveChanges();
        break;
      case ACTION_TYPE.revert:
        this.revertChanges();
        break;
      default:
        console.error(RACING_EDP_ERRORS.unhandledAction);
        break;
    }
  }

  /**
   * Revert the changes to initial data
   */
  revertChanges(): void {
    this.loadInitData();
  }

  /**
   * Save the market details
   */
  saveChanges(): void {
    this.apiClientService.racingEdp()
        .edit(this.racingEDPMarket)
        .map((response: HttpResponse<RacingEdpMarket>) => {
          return response.body;
        })
        .subscribe((market: RacingEdpMarket) => {
          this.racingEDPMarket = market;
          this.actionButtons.extendCollection(this.racingEDPMarket);
          this.dialogService.showNotificationDialog({
            title: SAVE_NOTIFICATION_DIALOG.title,
            message: SAVE_NOTIFICATION_DIALOG.message
          });
    });
  }

  /**
   * Remove the racing edp market
   */
  removeRacingEdpMarket(): void {
    this.apiClientService.racingEdp().remove(this.racingEDPMarket.id).subscribe(() => {
      this.router.navigate([RACING_EDP_ROUTES.base]);
    });
  }

  /**
   * Loads initial data based on id
   * @param {boolean} isLoading
   */
  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.racingEdp().getById(params['id'])
        .map((response: HttpResponse<RacingEdpMarket>) => response.body)
        .subscribe((racingEDPMarket: RacingEdpMarket) => {
          this.racingEDPMarket = racingEDPMarket;
          this.breadCrumbs = [
            {
              label: BREADCRUMBS_LABEL,
              url: RACING_EDP_ROUTES.base
            },
            {
              label: this.racingEDPMarket.name,
              url: `${RACING_EDP_ROUTES.base}/${this.racingEDPMarket.id}`
            }
          ];
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  /**
  * Loads all the data from system-config
  */
  private getBirEnabledMarkets(): void {
    this.apiClientService.publicApi().getSystemConfigByBrand().subscribe((systemConfigData: HttpResponse<any>) => {
      this.birEnabledMarkets = systemConfigData.body['HorseRacingBIR'].marketsEnabled;
      this.isBirMarketFlag = this.birEnabledMarkets && this.racingEDPMarket?.name && this.isBirEnabledMarket(this.racingEDPMarket.name);
    });
  }
  /**
   * returns a boolean value by checking if the marketName is in birEnabledMarkets array or not
   * @param marketName
   * @returns boolean
   */
  private isBirEnabledMarket(marketName: string): boolean {
    return this.birEnabledMarkets.includes(marketName);
  }
}
