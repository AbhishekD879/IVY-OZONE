import { from as observableFrom, Observable, Subscription } from 'rxjs';
import { Injectable } from '@angular/core';
import { CurrentMatchesService } from '@app/sb/services/currentMatches/current-matches.service';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { GridHelperService } from '@ladbrokesDesktop/shared/services/gridHelperService/grid-helper.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { ActivatedRoute } from '@angular/router';
import { IClassModel, IClassResultModel } from '@app/core/models/class.model';
import { ICompetitionType } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';

@Injectable()
export class CompetitionsService {

  constructor(
    private сurrentMatchesService: CurrentMatchesService,
    private gridHelperService: GridHelperService,
    private routingHelperService: RoutingHelperService,
    private routingState: RoutingState,
    private route: ActivatedRoute,
  ) { }

  /**
   * Return classes with types
   * @params{object} Class Ids from CMS
   * return {Promise} Filtered sub-categories with types
   */
  getClassesWithTypes(ids: { popular: string[], all: string[] }, categoryId: string): Observable<any[] | IClassModel[] | Subscription> {
    return observableFrom(this.сurrentMatchesService.getAllClasses(categoryId)
      .then((result: IClassModel[]) => ({ allClasses: true, result }))
      .then((classes: IClassResultModel) => {
        return [this.сurrentMatchesService.filterInitialClasses(classes, ids.popular),
          this.сurrentMatchesService.filterInitialClasses(classes, ids.all)];
      }));
  }

  /**
   * Returns url for competition page
   * @params{object} item
   * @params{string} className
   */
  goToCompetitionPage(item: ICompetitionType, className: string): string | boolean {
    if (!item.type.name) {
      return false;
    }

    return this.routingHelperService.formCompetitionUrl({
      sport: this.routingState.getRouteParam('sport', this.route.snapshot),
      typeName: item.type.name,
      className
    });
  }

  /**
   * returns types for classes
   * @params{string} name
   */
  getTypesForClasses(name: string, categoryId: string): Observable<IClassModel[]> {
    return observableFrom(this.сurrentMatchesService.getTypesForClasses(name, categoryId));
  }

  /**
   * Add empty cells for grid layout 3 and 4 columns
   * @params{array} types
   */
  applyGrid(types): void {
    const rowForFour = this.gridHelperService.addCells(4, types.length);
    const rowForThree = this.gridHelperService.addCells(3, types.length);
    const rowLimit = rowForFour + rowForThree;
    for (let i = 0; rowLimit > i; i++) {
      types.push({
        type: {
          grid: rowForFour > i ? '4' : '3'
        }
      });
    }
  }
}
