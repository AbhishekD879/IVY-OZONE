import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { HttpResponse } from '@angular/common/http';

import { DialogService } from '../../shared/dialog/dialog.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';

import { League } from '../../client/private/models/league.model';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';

@Component({
  selector: 'app-edit-league',
  templateUrl: './edit-league.component.html',
  styleUrls: ['./edit-league.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditLeagueComponent implements OnInit {

  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  public league: League;

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) {
  }

  ngOnInit(): void {
    this.loadInitData();
  }

  public isValidForm(league: League): boolean {
    return !!(league.name && league.name.trim().length > 0);
  }

  public saveChanges(): void {
    this.apiClientService.league()
        .edit(this.league)
        .map((league: HttpResponse<League>) => {
          return league.body;
        })
        .subscribe((league: League) => {
          this.league = league;
          this.actionButtons.extendCollection(this.league);
          this.dialogService.showNotificationDialog({
            title: `League Saving`,
            message: `League is Saved.`
          });
    });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public removeLeague(): void {
    this.apiClientService.league().remove(this.league.id).subscribe(() => {
      this.router.navigate(['/leagues']);
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeLeague();
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

  public getLink(type): string {
    return `/banners/receipt/${type}/${type === 'mobile' ? this.league.banner : this.league.tabletBanner}`;
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.league().getById(params['id']).map((league: HttpResponse<League>) => {
        return league.body;
      }).subscribe((league: League) => {
        this.league = league;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: 'Leagues',
          url: '/leagues'
        }, {
          label: this.league.name,
          url: `/leagues/${this.league.id}`
        }];
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

}
