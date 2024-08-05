import { Component, OnInit, ViewChild } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActivatedRoute, Params } from '@angular/router';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';

@Component({
  selector: 'app-surface-bet-module',
  templateUrl: './surface-bet-module.component.html'
})

export class SurfaceBetModuleComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  public module: SportsModule;
  public breadcrumbsData: Breadcrumb[];
  public routeParams: Params;

  constructor(
    private activatedRoute: ActivatedRoute,
    private sportsModulesService: SportsModulesService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService
  ) {

  }

  public ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.routeParams = params;
      this.loadInitialData(params);
    });
  }

  public loadInitialData(params: Params): void {
    this.sportsModulesService.getSingleModuleData(params['moduleId'], params['id'])
      .subscribe((moduleData: [SportsModule, SportCategory]) => {
        this.module = moduleData[0];

        this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
          module: this.module
        }).subscribe((breadcrubs: Breadcrumb[]) => {
          this.breadcrumbsData = breadcrubs;
        });
      });
  }
}
