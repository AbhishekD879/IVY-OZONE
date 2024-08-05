import {Component, OnInit} from '@angular/core';
import {DialogService} from '../../shared/dialog/dialog.service';
import {ApiClientService} from '../../client/private/services/http';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {HttpResponse} from '@angular/common/http';
import {League} from '../../client/private/models/league.model';
import {CreateLeagueDialogComponent} from '../create-league-dialog/create-league-dialog.component';
import {ActiveInactiveExpired} from '../../client/private/models/activeInactiveExpired.model';
import {Router} from '@angular/router';
import {AppConstants} from '../../app.constants';

@Component({
  selector: 'app-leagues-list',
  templateUrl: './leagues-list.component.html',
  styleUrls: ['./leagues-list.component.scss'],
  providers: [
    DialogService
  ]
})
export class LeaguesListComponent implements OnInit {

  public isLoading: boolean = false;
  public searchField: string = '';
  public leagues: League[] = [];
  dataTableColumns: any[] = [
    {
      name: 'Title',
      property: 'name',
      link: {
        hrefProperty: 'id',
      },
      type: 'link'
    },
    {
      name: 'Type Id',
      property: 'typeId'
    },
    {
      name: 'Cat. Id',
      property: 'categoryId'
    },
    {
      name: 'Cat. Code',
      property: 'ssCategoryCode'
    },
    {
      name: 'Bet Builder Url',
      property: 'betBuilderUrl'
    },
    {
      name: 'League Url',
      property: 'leagueUrl'
    },
    {
      name: 'Redirect Url',
      property: 'redirectionUrl'
    },
    {
      name: 'Mob. Banner',
      property: 'banner'
    },
    {
      name: 'Tabl. Banner',
      property: 'tabletBanner'
    }
  ];

  filterProperties: string[] = [
    'name'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.showHideSpinner();
    this.apiClientService.league()
        .findAllByBrand()
        .map((leaguesResponse: HttpResponse<League[]>) => {
          return leaguesResponse.body;
        })
        .subscribe((leaguesList: League[]) => {
          this.leagues = leaguesList;
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  public removeLeague(league: League): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove League',
      message: 'Are You Sure You Want to Remove League?',
      yesCallback: () => {
        this.leagues = this.leagues.filter((l) => {
          return l.id !== league.id;
        });
        this.apiClientService.league().remove(league.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'League is Removed.'
          });
        });
      }
    });
  }

  public createLeague(): void {
    this.dialogService.showCustomDialog(CreateLeagueDialogComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New League',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (leagueItem: League) => {
        this.apiClientService.league()
          .add(leagueItem)
          .map((res: HttpResponse<League>) => res.body)
          .subscribe((league: League) => {
            this.leagues.unshift(league);
            this.router.navigate([`/leagues/${league.id}`]);
        }, () => {
          console.error('Can not create league');
        });
      }
    });
  }

  get leaguesAmount(): ActiveInactiveExpired {
    return {
      active: this.leagues.length,
      showOnlyTotal: true
    };
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

}
