import {Component, Input, OnInit} from '@angular/core';
import {
  CompetitionModule,
  StatsCenterGroups,
  StatsCenterSeason
} from '@app/client/private/models/competitionmodule.model';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import {ActivatedRoute, Params} from '@angular/router';
import * as _ from 'lodash';
import {HttpResponse} from '@angular/common/http';
import {BigCompetitionService} from '../../../service/big-competition.service';

@Component({
  selector: 'app-group-widget',
  templateUrl: './group-widget.component.html',
  styleUrls: ['./group-widget.component.scss']
})
export class GroupWidgetComponent implements OnInit {
  private statsCenterGroups: StatsCenterGroups;
  private selectedSeason: StatsCenterSeason;
  public currentSeasonName: string;
  public groupsNames: {
    groupId: number,
    groupName: string
  }[];
  public seasonsNames: Array<string>;
  public redirectLinkPaths: Array<string>;
  public groupsNotFound: boolean = false;
  @Input() module: CompetitionModule;

  constructor(private bigCompetitionApiService: BigCompetitionAPIService,
              private activatedRoute: ActivatedRoute,
              private bigCompetitionService: BigCompetitionService) { }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData() {
    this.activatedRoute.params.subscribe((params: Params) => {
      // Get available competition groups from statsCenter
      this.bigCompetitionApiService.getCompetitionGroups(params.competitionId)
        .map((response: HttpResponse<StatsCenterGroups>) => {
          return response.body;
        })
        .subscribe((data: StatsCenterGroups) => {
          this.statsCenterGroups = data;
          const parsedData = this.bigCompetitionService.parseCompetitionGroupsData(this.statsCenterGroups);
          this.groupsNames = this.getAllGroupsName(this.module.groupModuleData.seasonId);
          this.seasonsNames = parsedData.seasonsNames;
          this.groupsNotFound = parsedData.groupsNotFound;
          this.currentSeasonName = this.bigCompetitionService.setSeasonCurrentValue( this.statsCenterGroups,
            this.module.groupModuleData.seasonId);
        }, () => {
          this.groupsNotFound = true;
        });
      this.bigCompetitionApiService.getSingleCompetition(params.competitionId)
        .map((response: HttpResponse<StatsCenterGroups>) => {
          return response.body;
        }).subscribe((data: any) => {
          this.redirectLinkPaths = this.bigCompetitionService.getAllPaths(data.competitionTabs);
        });
    });
  }
  /**
   * Transforms
   * @param {statsCenterGroups} data
   * @returns {Array}
   */
  private getAllGroupsName(selectedSeasonId): {groupId: number, groupName: string}[] {
    let filteredGroups = [];
    this.statsCenterGroups.allSeasons.forEach((season:StatsCenterSeason)=>{
        if(selectedSeasonId === season.id){
           season.competitionIds.forEach(seasonId => {
            const matchingCompetition = _.find(this.statsCenterGroups.allCompetitions, {
              id: +seasonId
            });
            filteredGroups.push(matchingCompetition);
           });
        }
    });
    if(filteredGroups.length > 1 ) {
      filteredGroups.shift(); // removing the parent group record from the filtered Groups
    }
    filteredGroups = _.sortBy(filteredGroups, ['name']);
    return filteredGroups;
  }
  /**
   * Season changed handler
   * @param {string} value
   */
  public onSelectSeasonChanged(value: string): void {
    this.selectedSeason = _.find(this.statsCenterGroups.allSeasons, { name: value });
    this.module.groupModuleData.sportId = this.selectedSeason.sportId;
    this.module.groupModuleData.areaId = this.selectedSeason.areaId;
    this.module.groupModuleData.seasonId = this.selectedSeason.id;
    this.groupsNames = this.getAllGroupsName(this.selectedSeason.id);
  }

  /**
   * Check if "seasonId" is selected and links for all grooups are selected
   * @returns {boolean}
   */
  public isValidForm(): boolean {
    const allGroupsMapped = this.module.groupModuleData &&
      this.module.groupModuleData.details && this.groupsNames;

    return !!(allGroupsMapped && this.module.groupModuleData.seasonId);
  }
}
