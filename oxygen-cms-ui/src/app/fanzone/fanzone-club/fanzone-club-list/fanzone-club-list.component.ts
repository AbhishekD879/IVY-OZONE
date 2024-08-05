import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActiveInactiveExpired } from '@root/app/client/private/models/activeInactiveExpired.model';
import { DataTableColumn } from '@root/app/client/private/models/dataTableColumn';
import { ClubPromo } from '@root/app/client/private/models/fanzone.model';
import { ErrorService } from '@root/app/client/private/services/error.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { FANZONE_CLUB } from '../../constants/fanzone.constants';
import { FanzonesAPIService } from '../../services/fanzones.api.service';

@Component({
  selector: 'app-fanzone-club-list',
  templateUrl: './fanzone-club-list.component.html'
})
export class FanzoneClubListComponent implements OnInit {
  public readonly FANZONE_CLUB = FANZONE_CLUB;
  clubData: ClubPromo[];
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Fanzone Name',
      property: 'title',
      link: {
        hrefProperty: 'id',
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Validity Start',
      property: 'validityPeriodStart',
      type: 'date',
      width: 2
    },
    {
      name: 'Validity End',
      property: 'validityPeriodEnd',
      type: 'date',
      width: 2
    },
    {
      name: 'Enabled',
      property: 'active',
      type: 'boolean'
    },
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(public router: Router,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService) { }

  ngOnInit(): void {
    this.getFanzonesClubs();
  }

  getFanzonesClubs() {
    this.fanzonesAPIService.getAllFanzoneClubs()
      .subscribe(data => {
        this.clubData = data.body;
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  createClub() {
    this.router.navigate(['fanzones/club-create']);
  }

  get clubsAmount(): ActiveInactiveExpired {
    const activeClubs = this.getFilteredClubs();
    const activeClubsAmount = activeClubs && activeClubs.length;
    const inactiveClubsAmount = this.clubData.length - activeClubsAmount;

    return {
      active: activeClubsAmount,
      inactive: inactiveClubsAmount
    };
  }

  /**
   * Method to get active clubs data
   * @returns active clubs
   */
  private getFilteredClubs() {
    return this.clubData && this.clubData.filter((club) => club.active === true);
  }

  /**
   * handles deleting fanzone club
   * @param {club} club
   */
  removeFanzoneClub(club: ClubPromo) {
    this.dialogService.showConfirmDialog({
      title: 'Club Removal',
      message: 'Are You Sure You Want to Remove Club?',
      yesCallback: () => {
        this.sendRemoveRequest(club);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Fanzone} fanzone
   */
  sendRemoveRequest(club: ClubPromo): void {
    this.fanzonesAPIService.deleteFanzoneClub(club.id)
      .subscribe(() => {
        this.clubData.splice(this.clubData.indexOf(club), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Club is Removed.'
        });
      }, error => {
        console.error(error.message);
      });
  }

  /**
   * Removes multiple fanzone Clubs
   * @param clubIds string[]
   */
  removeHandlerMulty(clubIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Fanzones (${clubIds.length})`,
      message: 'Are You Sure You Want to Remove Fanzones?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.fanzonesAPIService.deleteFanzoneClub(clubIds)
          .subscribe(() => {
            clubIds.forEach((id) => {
              const index = this.clubData.findIndex(clubs => clubs.id === id);
              this.clubData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

}
