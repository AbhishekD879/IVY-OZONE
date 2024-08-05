import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { IGroupModule, IGroupModuleData } from '@app/bigCompetitions/models/big-competitions.model';

@Component({
  selector: 'competition-groups-individual',
  templateUrl: './competition-groups-individual.component.html'
})
export class CompetitionGroupIndividualComponent implements OnInit {
  @Input() moduleConfig: IGroupModule;

  numberQualifiers: number;
  individualModuleData: IGroupModuleData;

  ngOnInit(): void {
    this.numberQualifiers = this.moduleConfig.groupModuleData.numberQualifiers;
    if (_.isArray(this.moduleConfig.groupModuleData.data)) {
      this.individualModuleData = this.moduleConfig.groupModuleData.data[0];
    }
  }

  /**
   * Get qualified class if needed for single team
   * @param {number} index
   * @returns {string}
   */
  getQualifiedClass(index: number): string {
    if (index + 1 <= this.numberQualifiers) {
      return 'team-qualified';
    }
    return '';
  }

  trackByTeams(i: number, element: IGroupModuleData): string {
    return `${i}_${element.competitionId}`;
  }
}
