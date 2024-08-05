import { Component, Input, OnInit } from '@angular/core';
import { IGroupData, IGroupModule, IGroupModuleData } from '@app/bigCompetitions/models/big-competitions.model';


@Component({
  selector: 'competition-groups-widget',
  templateUrl: './competition-groups-widget.component.html'
})
export class CompetitionGroupsWidgetComponent implements OnInit {
  @Input() moduleConfig: IGroupModule;

  groupsData: IGroupData;

  ngOnInit(): void {
    this.groupsData = this.moduleConfig.groupModuleData;
  }

  trackByTeams(i: number, element: IGroupModuleData): string {
    return `${i}_${element.competitionId}`;
  }
}
