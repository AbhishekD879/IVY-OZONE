import {Component, OnInit} from '@angular/core';
import {SportsModulesService} from '../../sports-modules.service';
import {SportsModule} from '@app/client/private/models/homepage.model';
import {ActivatedRoute, Params} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AppConstants} from '@app/app.constants';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {SportCategory} from '@app/client/private/models/sportcategory.model';
import {SportsModulesBreadcrumbsService} from '@app/sports-modules/sports-modules-breadcrumbs.service';
import {IAemBannersConfig} from '@app/client/private/models/sport-modules/aem-banners-config.modul';
import {DateRange} from '@app/client/private/models/dateRange.model';

@Component({
  selector: 'aem-banner-module',
  templateUrl: './aem-banner.component.html',
  styleUrls: ['./aem-banner.component.scss']
})

export class AemBannerComponent implements OnInit {
  module: SportsModule;
  breadcrumbsData: Breadcrumb[];
  routeParams: Params;
  aemBannersConfig: IAemBannersConfig;

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
        this.module = moduleData[0] as SportsModule;
        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }

  isValidModule(): boolean {
    return true;
  }

  public handleDateUpdate(data: DateRange): void {
    this.module.moduleConfig.displayFrom = new Date(data.startDate).toISOString();
    this.module.moduleConfig.displayTo = new Date(data.endDate).toISOString();
  }

  actionsHandler(event) {
    switch (event) {
      case 'save':
        this.sportsModulesService.updateModule(this.module)
          .subscribe((module: SportsModule) => {
            this.module = module;
            // this.actionButtons.extendCollection(this.module);
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
