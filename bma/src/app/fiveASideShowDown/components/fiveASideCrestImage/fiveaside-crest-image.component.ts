import { Component, OnInit, Input } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { DEFAULT_TEAM_COLOURS } from '@app/fiveASideShowDown/constants/constants';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';

@Component({
  selector: 'fiveaside-crest-image',
  template: ``
})
export class FiveasideCrestImageComponent implements OnInit {
  @Input() hasTeamImage: boolean;
  @Input() team: ITeamColor;
  @Input() widthHeight: number;
  @Input() hasBorder: boolean;
  @Input() hasBorderDetails: boolean = false;
  @Input() hasOverflow: boolean = false;
  backgroundColor: string;
  readonly TEAMSIMAGEPATH: string = `${environment.CMS_ROOT_URI}${environment.FIVEASIDE.svgImagePath}`;
  constructor(private leaderboardService: FiveasideLeaderBoardService) { }

  ngOnInit(): void {
    this.backgroundColor = this.getCountryBackground();
  }

  /**
   * To Get country background
   * @returns {string}
   */
  private getCountryBackground(): string {
    const primaryColor: string = this.leaderboardService.checkHexColor(this.team.primaryColour, DEFAULT_TEAM_COLOURS.primary);
    const secondaryColour: string = this.leaderboardService.checkHexColor(this.team.secondaryColour, DEFAULT_TEAM_COLOURS.secondary);
    return `linear-gradient(to right, ${primaryColor} 50%, ${secondaryColour} 50%)`;
  }

}
