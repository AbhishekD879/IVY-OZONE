import {Component, Input, OnInit} from '@angular/core';
import {
  CompetitionModule,
  GroupAllMarket,
  StatsCenterCompetition,
  StatsCenterGroups,
  StatsCenterSeason
} from '../../../../../client/private/models';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import {BigCompetitionService} from '../../../service/big-competition.service';
import {ActivatedRoute, Params} from '@angular/router';
import * as _ from 'lodash';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AppConstants} from '../../../../../app.constants';

@Component({
  selector: 'app-group-all',
  templateUrl: './group-all.component.html'
})
export class GroupAllComponent implements OnInit {
  private statsCenterGroups: StatsCenterGroups;
  private selectedCompetition: StatsCenterCompetition;
  private selectedSeason: StatsCenterSeason;
  public currentGroupName: string;
  public currentSeasonName: string;
  public groupsNames: Array<string>;
  public seasonsNames: Array<string>;
  public groupsNotFound: boolean = false;
  public marketId: string;
  public marketIdIsValid: boolean = true;
  public marketIdExists: boolean = false;
  public isMarketsMaxLength: boolean = false;
  @Input() module: CompetitionModule;

  constructor(private bigCompetitionApiService: BigCompetitionAPIService,
              private activatedRoute: ActivatedRoute,
              private bigCompetitionService: BigCompetitionService,
              private snackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.loadInitData();
  }

  private loadInitData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      // Get available competition groups from statsCenter
      this.bigCompetitionApiService.getCompetitionGroups(params.competitionId)
        .map((response: HttpResponse<StatsCenterGroups>) => {
          return response.body;
        })
        .subscribe((data: StatsCenterGroups) => {
          this.statsCenterGroups = data;
          const parsedData = this.bigCompetitionService.parseCompetitionGroupsData(this.statsCenterGroups);
          this.groupsNames =  this.filterGroupsBasedOnSeasons(this.module.groupModuleData.seasonId);
          this.seasonsNames = parsedData.seasonsNames;
          this.groupsNotFound = parsedData.groupsNotFound;
          this.currentGroupName = this.bigCompetitionService.setGroupCurrentValue(
            this.statsCenterGroups, this.module.groupModuleData.competitionId);
          this.currentSeasonName = this.bigCompetitionService.setSeasonCurrentValue(
            this.statsCenterGroups, this.module.groupModuleData.seasonId);
        }, () => {
          this.groupsNotFound = true;
        });
    });
  }

  public onSelectGroupChanged(value): void {
    this.selectedCompetition = _.find(this.groupsNames, { name: value  }) as any;
    this.module.groupModuleData.sportId = this.selectedCompetition.sportId;
    this.module.groupModuleData.areaId = this.selectedCompetition.areaId;
    this.module.groupModuleData.competitionId = this.selectedCompetition.id;
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

  public onSelectSeasonChanged(value: string): void {
    this.selectedSeason = _.find(this.statsCenterGroups.allSeasons, { name: value });
    this.module.groupModuleData.seasonId = this.selectedSeason.id;
    this.groupsNames = this.filterGroupsBasedOnSeasons(this.selectedSeason.id)
    if(this.currentGroupName){
      this.onSelectGroupChanged(this.currentGroupName);
    }
  }

  public uploadMarketData(): void {
    this.marketIdExists = !!(_.find(this.module.markets, market => market.marketId === this.marketId));

    // there should be only 2 outright markets via Group All module
    if (this.module.markets.length === 2) {
      this.isMarketsMaxLength = true;
      this.marketIdExists = false;
    }

    if (!this.marketIdExists && !this.isMarketsMaxLength) {
      this.bigCompetitionApiService.getSiteServeMarket(this.marketId)
        .map((response: HttpResponse<GroupAllMarket>) => {
          return response.body;
        })
        .subscribe((market: GroupAllMarket) => {
          this.marketIdIsValid = true;
          _.extend(market, {marketId: market.id, defaultName: market.name, enabled: true});
          this.module.markets.push(market);
          this.showMessage();
          this.marketId = null;
        }, () => {
          this.marketIdIsValid = this.marketIdExists = false;
        });
    }
  }

  /**
   * Show message banner according to response
   */
  private showMessage(): void {
    this.snackBar.open('OPENBET OUTRIGHT MARKET ID LOADED!!', 'OK!', {
      duration: AppConstants.HIDE_DURATION
    });
  }

  /**
   * Remove all markets
   */
  public removeModuleMarkets(): void {
    this.module.markets = [];
    this.marketId = null;
    this.isMarketsMaxLength = false;
    this.marketIdIsValid = true;
  }

  /**
   * Remove only one outright market ID
   * @param {Object} market
   */
  public removeMarketId(market: GroupAllMarket): void {
    const marketName = market.name || market.defaultName;
    this.module.markets.splice(this.module.markets.indexOf(market), 1);

    if (!this.module.markets.length || this.module.markets.length < 2) {
      this.marketId = null;
      this.isMarketsMaxLength = false;
      this.marketIdIsValid = true;
    }

    this.snackBar.open(`OUTRIGHT MARKET ${marketName} HAS BEEN REMOVED!!`, 'OK!', {
      duration: AppConstants.HIDE_DURATION
    });
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
