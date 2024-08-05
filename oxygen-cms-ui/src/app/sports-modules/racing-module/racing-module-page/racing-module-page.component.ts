import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AppConstants } from '@app/app.constants';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { racingModuleTypes } from '@app/sports-modules/constant/module-types.constant';

@Component({
  selector: 'racing-module-page',
  templateUrl: 'racing-module-page.component.html'
})
export class RacingModulePageComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  form: FormGroup;
  module: SportsModule;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;
  isVirtualRacingModule: boolean;
  isIntToteModule: boolean;

  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
    private snackBar: MatSnackBar
  ) {
    this.isValidModule = this.isValidModule.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  loadInitialData(params): void {
    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
      this.module = moduleData[0];
      this.module.racingConfig = moduleData[0].racingConfig || {} as any;

      this.isVirtualRacingModule = this.module.racingConfig['type'] === racingModuleTypes.VIRTUAL_RACE_CAROUSEL;
      this.isIntToteModule = this.module.racingConfig['type'] === racingModuleTypes.INTERNATIONAL_TOTE_CAROUSEL;

      this.setUpForm();
        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

  setUpForm(): void {
    let formControls = {
      title: new FormControl(this.module.title, [Validators.required])
    };

    let moduleSpecificControls = {};
    if (this.isVirtualRacingModule) {
      moduleSpecificControls = {
        limit: new FormControl(this.module.racingConfig.limit, [Validators.required, Validators.min(1), Validators.max(12)]),
        excludeTypeIds: new FormControl(this.module.racingConfig.excludeTypeIds, [Validators.required, Validators.pattern('[1-9]\\d*(,?\\s?[1-9]\\d*)*')]),
        classId: new FormControl(this.module.racingConfig.classId, [Validators.required, Validators.min(1)])
      };
    } else if (this.isIntToteModule) {
      moduleSpecificControls = {
        classId: new FormControl(this.module.racingConfig.classId, [Validators.required, Validators.min(1)])
      };
    }

    formControls = Object.assign(formControls, moduleSpecificControls);
    this.form = new FormGroup(formControls);
  }

  get limit() {return this.form.get('limit'); }

  get classId() { return this.form.get('classId'); }

  get excludeTypeIds() { return this.form.get('excludeTypeIds'); }

  isValidModule(): boolean {
    return this.form.valid;
  }

  actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.sportsModulesService.updateModule(this.module)
          .subscribe((module: SportsModule) => {
            this.module = module;
            this.actionButtons.extendCollection(this.module);
            this.snackBar.open(`Sports module saved!`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          });
        break;
      case 'revert':
        this.loadInitialData(this.routeParams);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
