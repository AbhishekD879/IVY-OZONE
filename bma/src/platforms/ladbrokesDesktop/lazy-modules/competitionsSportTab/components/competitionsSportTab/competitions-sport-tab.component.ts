import { Component, OnInit, Input } from '@angular/core';
import * as _ from 'underscore';
import { CompetitionsService } from '../../services/competitons/competitons.service';
import { ICompetitionCategory } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { FiltersService } from '@app/core/services/filters/filters.service';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import { map, switchMap } from 'rxjs/operators';
import { GamingService } from '@core/services/sport/gaming.service';
import { ISportConfigTab } from '@app/core/services/cms/models';

@Component({
  selector: 'competitions-sport-tab',
  templateUrl: './competitions-sport-tab.component.html'
})
export class DesktopCompetitionsSportTabComponent implements OnInit {
  @Input() sport: GamingService;
  @Input() sportTabs: ISportConfigTab[];
  competitions: ICompetitionsConfig;
  position: number;
  loader: boolean;
  categories: {
    AZCategories: ICompetitionCategory[];
    Popular: ICompetitionCategory[];
  };
  currentTabCategories: ICompetitionCategory[];
  switchers: {
    label: string;
    onClick: Function;
  }[];
  categoryName: string;
  isResponseError: boolean = false;
  categoryId: string;
  isTierOne: boolean;
  targetTab: ISportConfigTab;

  constructor(
    private competitionsService: CompetitionsService,
    private cmsService: CmsService,
    private filtersService: FiltersService
  ) {
    this.position = 0;
    this.loader = true;
    this.categories = {
      Popular: undefined,
      AZCategories: undefined
    };
  }
  /**
   * OnInit controller function
   */
  ngOnInit(): void {
    this.isTierOne = this.sport.config.tier === 1;
    this.categoryName = this.sport.config.name;
    this.categoryId = this.sport.config.request.categoryId;
    if (this.isTierOne) {
      // load data for tabs
      this.loadCompetitionsData(this.categoryName);
      // switchers behaviour, onClick should be moved to switchers component
      this.switchers = [
        {
          label: 'Popular',
          onClick: () => {
            this.position = 0;
            this.currentTabCategories = this.categories.Popular;
          }
        }, {
          label: 'A - Z',
          onClick: () => {
            this.position = 1;
            this.currentTabCategories = this.categories.AZCategories;
          }
        }
      ];

      this.isTennis() && this.switchers.splice(1);
    }
    if(this.sportTabs){
      this.targetTab = this.sportTabs.find((tab: ISportConfigTab) => tab.id.includes('competitions'));
    }
  }

  isFootball(): boolean {
    return this.categoryName === 'football';
  }

  isTennis(): boolean {
    return this.categoryName === 'tennis';
  }

  /**
   * Load Sport Competitions Data
   */
  loadCompetitionsData(categoryName: string): void {
    this.loader = true;
    this.isResponseError = false;

    this.cmsService.getCompetitions(categoryName)
      .pipe(
        map((cmsData: ICompetitionsConfig) => {
          this.competitions = cmsData;
        }),
        switchMap(() => {
          return this.competitionsService.getClassesWithTypes({
            popular: this.competitions.InitialClassIDs.split(','),
            all: this.isTennis() ? [] : this.competitions['A-ZClassIDs'].split(',')
          }, this.categoryId);
        })
      )
      .subscribe((result: any[] ) => {
        this.categories.Popular = result[0];
        this.categories.AZCategories = _.filter(
          this.filtersService.orderBy(result[1],
            ['class.name']),
          (category: ICompetitionCategory) => {
            return !!category;
          });
        this.currentTabCategories = result[0];
        this.isResponseError = false;
        this.loader = false;
      }, error => {
        console.warn('CMS Competitions Data:', error);
        this.loader = false;
        this.isResponseError = true;
      });
  }
}
