import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute, Params} from '@angular/router';

import {HttpResponse} from '@angular/common/http';
import {BigCompetitionAPIService} from '../../../service/big-competition.api.service';
import {BigCompetitionService} from '../../../service/big-competition.service';
import * as _ from 'lodash';
import {CompetitionModule, StatsCenterGroups, StatsCenterSeason} from '../../../../../client/private/models';

@Component({
  selector: 'app-results-module',
  templateUrl: './results-module.component.html',
  styleUrls: ['./results-module.component.scss']
})
export class ResultsModuleComponent implements OnInit {
  private allSeasons: StatsCenterSeason[];
  private currentSeasonName: string;
  public seasonsNames: Array<string>;
  public seasonsNotFound: boolean = false;

  @Input() module: CompetitionModule;

  constructor(private bigCompetitionApiService: BigCompetitionAPIService,
              private activatedRoute: ActivatedRoute,
              private bigCompetitionService: BigCompetitionService) { }

  ngOnInit() {
    this.loadInitData();
  }

  private loadInitData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      // Get available competition seasons from statsCenter
      this.bigCompetitionApiService.getCompetitionGroups(params.competitionId)
        .map((response: HttpResponse<StatsCenterGroups>) => {
          return response.body;
        })
        .subscribe((data: StatsCenterGroups) => {
          this.allSeasons = _.isObject(data) && data.allSeasons;

          const currentSeason = _.find(this.allSeasons, ['id', this.module.resultModuleSeasonId]),
            parsedData = this.bigCompetitionService.parseCompetitionSeasonsData(this.allSeasons);

          this.seasonsNames = parsedData.seasonsNames;
          this.seasonsNotFound = parsedData.seasonsNotFound;
          this.currentSeasonName = currentSeason ? currentSeason.name : '';
        }, () => {
          this.seasonsNotFound = true;
        });
    });
  }

  /**
   * Set season id into module model
   * @param {string} seasonName
   */
  public onSelectSeasonChanged(seasonName: string): void {
    const selectedSeason = _.find(this.allSeasons, { name: seasonName });
    this.module.resultModuleSeasonId = selectedSeason.id;
  }

  /**
   * Check if field maxDisplay is valid(not empty)
   * @returns {boolean}
   */
  public isValidForm(): boolean {
    return !!(this.module.maxDisplay && this.currentSeasonName);
  }
}
