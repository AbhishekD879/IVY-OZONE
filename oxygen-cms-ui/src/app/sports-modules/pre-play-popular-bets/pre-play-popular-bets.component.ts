import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import {ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { SportsModulesService } from '../../sports-modules/sports-modules.service';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';


@Component({
  selector: 'pre-play-popular-bets',
  templateUrl: './pre-play-popular-bets.component.html'
})
export class PreplayPopularbetsComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  module: SportsModule;
  popularBetsFormGroup: FormGroup;
  HourMin: any = [{ time: 'Hour', short: true }, { time: 'Minute', short: false }];
  isBetReceiptRoute: boolean;
  title: string;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;
  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  /**
    * To Load initial data
  */
  private loadInitialData(params): void {
    this.globalLoaderService.showLoader();

    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
        this.module = moduleData[0];
        this.module.popularBetConfig = moduleData[0].popularBetConfig || {} as any;
        this.createFormGroup();
        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

    /**
    * To create form group data for fields
  */
  public createFormGroup(): void {
    this.popularBetsFormGroup = new FormGroup({
      displayName: new FormControl(this.module.popularBetConfig?.displayName || '', [Validators.required]),
      redirectionUrl: new FormControl(this.module.popularBetConfig?.redirectionUrl || '', [Validators.required]),
      mostBackedIn: new FormControl(this.module.popularBetConfig?.mostBackedIn || '', [Validators.required]),
      eventStartsIn: new FormControl(this.module.popularBetConfig?.eventStartsIn || '', [Validators.required]),
      maxSelections: new FormControl(this.module.popularBetConfig?.maxSelections || '', [Validators.min(1), Validators.max(5)]),
      priceRange: new FormControl(this.module.popularBetConfig?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      enableBackedInTimes: new FormControl(this.module.popularBetConfig.enableBackedInTimes || false,[]),
    });
  }


  /**
  * To Handle actions
  * @param {string} event
  */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.loadInitialData(this.routeParams);
        break;
      default:
        break;
    }
  }


  private saveChanges(): void {
    this.sportsModulesService.updateModule(this.module)
    .subscribe((module: SportsModule) => {
      this.module = module;
      this.actionButtons.extendCollection(this.module);
      this.snackBar.open(`Sports module saved!`, 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });

  }

     // form validation and default field validation must be considered here 
     public validationHandler(): boolean {
      return this.popularBetsFormGroup && this.popularBetsFormGroup.valid;
    }
}
