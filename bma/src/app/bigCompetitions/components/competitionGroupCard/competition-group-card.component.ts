import { Component, Input, OnInit } from '@angular/core';
import { IGroupModuleData, IGroupTeam } from '@app/bigCompetitions/models/big-competitions.model';

@Component({
  selector: 'competition-group-card',
  templateUrl: './competition-group-card.component.html'
})
export class CompetitionGroupCardComponent implements OnInit {
  @Input() groupData: IGroupModuleData;
  @Input() redirectLink: string;
  @Input() numberQualifiers: number;

  ngOnInit(): void {
    if (this.redirectLink) {
      this.redirectLink = `/big-competition${this.redirectLink}`;
    }
    this.groupData.tableName = this.groupData.tableName[this.groupData.tableName.length - 1];
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

  trackByTeam(i: number, element: IGroupTeam): string {
    return `${i}_${element.name}`;
  }
}
