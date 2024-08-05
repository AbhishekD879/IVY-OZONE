import { Component, OnInit } from '@angular/core';
import { FanzoneSelectYourTeamAppComponent } from '@app/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';

@Component({
  selector: 'fanzone-select-your-team',
  templateUrl: '../../../../../app/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component.html',
  styleUrls: ['./fanzone-select-your-team.component.scss'],
})
export class FanzoneSelectYourTeamDesktopComponent extends FanzoneSelectYourTeamAppComponent implements OnInit {

  ngOnInit() {
    super.ngOnInit()
  }

}
