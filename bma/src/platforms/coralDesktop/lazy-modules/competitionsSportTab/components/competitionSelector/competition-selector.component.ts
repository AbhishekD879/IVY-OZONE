import { Component, OnInit, Input } from '@angular/core';
import { CmsService } from '@core/services/cms/cms.service';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';

import * as _ from 'underscore';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import { ActivatedRoute, Router } from '@angular/router';
import { ICompetitionCategory } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { IClassModel } from '@core/models/class.model';
import { from as fromPromise, Observable, Observer, ObservableInput } from 'rxjs';
import { concatMap } from 'rxjs/operators';

interface IOpenCompetition {
  child?: string;
  parent?: string;
}

@Component({
  selector: 'competition-selector',
  templateUrl: 'competition-selector.component.html',
  styleUrls: ['competition-selector.component.scss']
})
export class CompetitionSelectorComponent implements OnInit {
  @Input() sportId: string;

  sportName: string;
  selectedItem = 'Change Competition';
  competitions: ICompetitionCategory[];
  list: IClassModel[] = [];

  constructor(
    private activatedRoute: ActivatedRoute,
    private cmsService: CmsService,
    private currentMatchesService: CurrentMatchesService,
    private routingHelperService: RoutingHelperService,
    private router: Router
  ) {
    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
  }

  ngOnInit() {
    this.getCompetitionList();
  }

  /**
   * Get Competitions List
   * @returns {Array}
   */
  getCompetitionList(): void {
    this.cmsService.getCompetitions(this.sportName)
      .subscribe((cmsData: ICompetitionsConfig) => {
        const idsArray: string[] = cmsData.InitialClassIDs.split(',');
        if (this.sportName === 'football') {
          this.currentMatchesService.getFootballClasses(idsArray)
            .then((competitions: ICompetitionCategory[]) => this.prepeareCompetionsList(competitions));
        } else {
          this.currentMatchesService.getOtherClasses(idsArray, this.sportId)
            .then((competitions: ICompetitionCategory[]) => this.prepeareCompetionsList(competitions));
        }
      });
  }

  /**
   * Go To Selected Competition
   * @param {String} typeName
   * @param {String} className
   */
  goToCompetition(typeName: string, className: string): void {
    const competitionPageUrl = this.routingHelperService.formCompetitionUrl({
      sport: this.sportName,
      typeName,
      className
    });

    this.router.navigateByUrl(competitionPageUrl);
  }

  /**
   * Open Selected Competition
   * @param {String|Object} name
   */
  openCompetition(name: IOpenCompetition): void {
    if (this.sportName === 'tennis') {
      const className: string = _.find(this.list, { name }).typeClassName;
      this.goToCompetition(name as string, className);
    }
    const menuList = _.findWhere(this.list, { originalName: name });
    if (menuList && !menuList.list) {
      this.currentMatchesService.getTypesForClasses(name as string, this.sportId).then(types => {
        _.extend(menuList, { list: _.pluck(types, 'type') });
      });
    }
    if (name && name.child) {
      this.goToCompetition(name.child, name.parent);
    }
  }

  private prepeareCompetionsList(competitions: ICompetitionCategory[]): void {
    if (this.sportName === 'tennis') {
      this.competitions = competitions;
      let sourceObservable;
      Observable.create((observer: Observer<IClassModel[]>) => sourceObservable = observer).pipe(
        concatMap((observer: ObservableInput<{}>) => observer)
      ).subscribe((types: IClassModel[]) => {
        _.each(types, (type: IClassModel) => {
          type.type.typeClassName = _.findWhere(_.pluck(this.competitions, 'class'), { id: type.type.classId })
            && _.findWhere(_.pluck(this.competitions, 'class'), { id: type.type.classId }).originalName;
          this.list.push(type.type);
        });
      }, err => {
        console.warn(err);
      });
      _.each(competitions, (competition: ICompetitionCategory) => {
        sourceObservable.next(fromPromise(this.currentMatchesService.getTypesForClasses(competition.class.name, this.sportId)));
      });
    } else {
      this.list = _.each(_.pluck(competitions, 'class'), item => (item.hasChild = true)) as IClassModel[];
    }
  }
}
