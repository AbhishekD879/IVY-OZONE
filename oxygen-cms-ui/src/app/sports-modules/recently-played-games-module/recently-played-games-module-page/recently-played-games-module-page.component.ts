import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { AppConstants } from '@app/app.constants';

@Component({
  selector: 'recently-played-games-module-page',
  templateUrl: 'recently-played-games-module-page.component.html'
})

export class RecentlyPlayedGamesModulePageComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  form: FormGroup;
  module: SportsModule;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;

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
        this.module.rpgConfig = moduleData[0].rpgConfig || {} as any;
        this.setUpForm();
        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

  setUpForm(): void {
    this.form = new FormGroup({
      title: new FormControl(this.module.rpgConfig.title, [Validators.required]),
      seeMoreLink: new FormControl(this.module.rpgConfig.seeMoreLink, [Validators.required]),
      gamesAmount: new FormControl(this.module.rpgConfig.gamesAmount, [Validators.required]),
      bundleUrl: new FormControl(this.module.rpgConfig.bundleUrl, [Validators.required]),
      loaderUrl: new FormControl(this.module.rpgConfig.loaderUrl, [Validators.required]),
    });
  }

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
