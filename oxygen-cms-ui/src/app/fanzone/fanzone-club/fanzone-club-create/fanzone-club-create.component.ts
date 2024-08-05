import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ClubPromo } from '@root/app/client/private/models/fanzone.model';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ErrorService } from '@root/app/client/private/services/error.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { FanzonesAPIService } from '../../services/fanzones.api.service';
import { CLUB, FANZONE_CLUB } from '../../constants/fanzone.constants';
import { DateRange } from '@root/app/client/private/models/dateRange.model';

@Component({
  selector: 'app-fanzone-club-create',
  templateUrl: './fanzone-club-create.component.html'
})
export class FanzoneClubCreateComponent implements OnInit {
  public readonly FANZONE_CLUB = FANZONE_CLUB;
  club: ClubPromo;

  breadcrumbsData = [{
    label: 'Fanzone Clubs',
    url: '/fanzones/club'
  }, {
    label: 'Create Club',
    url: `/fanzones/club-create`
  }];

  constructor(
    private router: Router,
    private dialogService: DialogService,
    private brandService: BrandService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService) { }

  ngOnInit(): void {
    this.club = {
      ...CLUB,
      brand: this.brandService.brand
    };
  }

  updatePromotion(data) {
    this.club.description = data;
  }

  handleDateUpdate(data: DateRange) {
    this.club.validityPeriodStart = data.startDate;
    this.club.validityPeriodEnd = data.endDate;
  }

  saveClub() {
    this.fanzonesAPIService.saveFanzoneClub(this.club)
      .subscribe(data => {
        this.finishClubCreation(data.body.id);
      }, error => {
        this.errorService.emitError(error.error.message || 'Something went wrong');
      });
  }

  /**
   * Redirect to fanzone-edit page
   * @param id  { id }
   * @returns void
   */
  finishClubCreation(id: string): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Club Saved',
      message: 'You can edit or remove this Club',
      closeCallback() {
        self.router.navigate([`fanzones/club/${id}`]);
      }
    });
  }

  isValidModel() {
    return this.club.title && this.club.bannerLink && this.club.description;
  }
}
