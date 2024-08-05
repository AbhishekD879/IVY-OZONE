import {Component, Input, OnInit} from '@angular/core';
import {
  CompetitionModule,
  StatsCenterCompetition,
  StatsCenterGroups,
  StatsCenterSeason
} from '../../../../../client/private/models';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import {BigCompetitionService} from '../../../service/big-competition.service';
import {ActivatedRoute, Params} from '@angular/router';
import * as _ from 'lodash';
import {HttpResponse} from '@angular/common/http';

@Component({
  selector: 'app-group-individual',
  templateUrl: './group-individual.component.html',
  styleUrls: ['./group-individual.component.scss']
})
export class GroupIndividualComponent implements OnInit {
  private statsCenterGroups: StatsCenterGroups;
  private selectedCompetition: StatsCenterCompetition;
  private selectedSeason: StatsCenterSeason;
  public currentGroupName: string;
  public currentSeasonName: string;
  public groupsNames: Array<string>;
  public seasonsNames: Array<string>;
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
          this.seasonsNames = parsedData.seasonsNames;
          this.groupsNotFound = parsedData.groupsNotFound;
          this.groupsNames =  this.filterGroupsBasedOnSeasons(this.module.groupModuleData.seasonId);
          this.currentGroupName = this.bigCompetitionService.setGroupCurrentValue(
            this.statsCenterGroups, this.module.groupModuleData.competitionId);
          this.currentSeasonName = this.bigCompetitionService.setSeasonCurrentValue(
            this.statsCenterGroups, this.module.groupModuleData.seasonId);
        }, () => {
          this.groupsNotFound = true;
        });
    });
  }

 private filterGroupsBasedOnSeasons(selectedSeasonId){
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
  
  public onSelectGroupChanged(value): void {
    this.selectedCompetition = _.find(this.groupsNames, { name: value }) as any;
    this.module.groupModuleData.sportId = this.selectedCompetition.sportId;
    this.module.groupModuleData.areaId = this.selectedCompetition.areaId;
    this.module.groupModuleData.competitionId = this.selectedCompetition.id;
  }

  public onSelectSeasonChanged(value: string): void {
    this.selectedSeason = _.find(this.statsCenterGroups.allSeasons, { name: value });
    this.module.groupModuleData.seasonId = this.selectedSeason.id;
    this.groupsNames = this.filterGroupsBasedOnSeasons(this.selectedSeason.id);
    if(this.currentGroupName){
      this.onSelectGroupChanged(this.currentGroupName);
    }
  }


  /**
   * Checks if season ID and group ID is selected.
   * @returns {boolean}
   */
  public isValidForm(): boolean {
    return !!(this.module.groupModuleData && this.module.groupModuleData.seasonId &&
       this.module.groupModuleData.competitionId);
  }
}
