import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models';
import { DateRange } from '@root/app/client/private/models/dateRange.model';
import { ClubPromo } from '@root/app/client/private/models/fanzone.model';
import { ErrorService } from '@root/app/client/private/services/error.service';
import { ActionButtonsComponent } from '@root/app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { FANZONE_CLUB } from '../../constants/fanzone.constants';
import { FanzonesAPIService } from '../../services/fanzones.api.service';

@Component({
  selector: 'app-fanzone-club-edit',
  templateUrl: './fanzone-club-edit.component.html'
})
export class FanzoneClubEditComponent implements OnInit {
  public readonly FANZONE_CLUB = FANZONE_CLUB;
  isReady: boolean;
  id: string;
  club: ClubPromo;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private dialogService: DialogService,
    private fanzonesAPIService: FanzonesAPIService,
    private errorService: ErrorService) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getFanzoneClub(this.id);
  }

  getFanzoneClub(id: string) {
    this.fanzonesAPIService.getFanzoneClub(id).subscribe(data => {
      this.breadcrumbsData = [
        { label: 'Fanzone Clubs', url: '/fanzones/club' },
        { label: data.body.title, url: `/fanzones/club/${this.id}` }
      ];
      this.club = data.body;
      this.isReady = true;
    }, error => {
      console.error(error.message);
    });
  }

  updatePromotion(data) {
    this.club.description = data;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.deleteFanzoneClub(this.id);
        break;
      case 'save':
        this.updateFanzoneClub();
        break;
      case 'revert':
        this.getFanzoneClub(this.id);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  handleDateUpdate(data: DateRange) {
    this.club.validityPeriodStart = data.startDate;
    this.club.validityPeriodEnd = data.endDate;
  }

  updateFanzoneClub() {
    this.fanzonesAPIService.updateFanzoneClub(this.id, this.club).subscribe((data: any) => {
      this.club = data.body;
      this.actionButtons.extendCollection(this.club);
      this.dialogService.showNotificationDialog({
        title: 'Club Saved'
      });
    }, error => {
      this.errorService.emitError(error.error.message || 'Something went wrong');
    });
  }

  deleteFanzoneClub(id: string) {
    this.fanzonesAPIService.deleteFanzoneClub(id).subscribe(() => {
      this.router.navigate(['fanzones/club']);
    }, error => {
      console.error(error.message);
    });
  }

  public validationHandler(): boolean {
    return this.club.title && this.club.bannerLink && this.club.description && true;
  }

}
