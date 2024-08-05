import {
  Component,
  OnInit,
  Input,
  ViewEncapsulation,
  ChangeDetectorRef,
  EventEmitter,
  Output
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import * as _ from 'underscore';

import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import {
  ICompetitionCategory,
  ICompetitionType } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { ISportConfig } from '@app/core/services/cms/models';

@Component({
  selector: 'competitions-categories',
  templateUrl: 'competitions-categories.component.html',
  styleUrls: ['./competitions-categories.component.scss'],
  // eslint-disable-next-line
  encapsulation: ViewEncapsulation.None
})
export class CompetitionsCategoryComponent implements OnInit {
  @Input() categories: ICompetitionCategory[];
  @Input() isAzCategories: boolean;
  @Input() categoryId: string | number;
  @Input() competitionsClasses: string;
  @Input() showLoader: boolean = true;
  @Input() allAccorditions? : ICompetitionCategory[];
  @Input() targetTab?:ISportConfig;
  @Input() sportName?:string;
  @Output() readonly pageLoaded: EventEmitter<boolean> = new EventEmitter<boolean>();

  isExpanded: boolean | boolean[] = [];
  initiallyExpanded: boolean | boolean[] = [];
  isShowAz: boolean;
  loading: boolean = true;

  constructor(
    private activatedRoute: ActivatedRoute,
    private currentMatchesService: CurrentMatchesService,
    private routingHelperService: RoutingHelperService,
    private pubsubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    if (this.categories[0] && !this.isAzCategories && !this.isTennis()) {
      this.goToTypes(0, true);
    }
    if (this.categories[0] && this.isTennis()) {
      _.each(this.categories, (category: ICompetitionCategory, index: number) => {
        category.class && this.goToTypes(index, true);
      });
    }
    this.isShowAz = Boolean(this.isAzCategories && this.categories.length && this.categories[0].class);
    this.updateLoadingState();
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  // go to types
  goToTypes(index: number, initial: boolean = false): void {
    this.isExpanded[index] = !this.isExpanded[index];
    this.categories[index].loading = true;
    this.changeDetectorRef.detectChanges();
    this.initiallyExpanded[index] = initial && this.isExpanded[index];

    if (this.isExpanded[index] && !this.categories[index].types) {
      this.currentMatchesService.getClassToSubTypeForClass(this.categories[index].class.id).subscribe((types: ICompetitionType[]) => {
        this.categories[index].loading = false;
        this.categories[index].types = this.extendTypes(this.categories[index], types);
        this.changeDetectorRef.detectChanges();
      }, (error) => {
        console.warn(error);
        this.categories[index].loading = false;
      }, () => {
        initial && this.updateLoadingState();
        this.changeDetectorRef.detectChanges();
      });
    } else {
      this.categories[index].loading = false;
      initial && this.updateLoadingState();
      this.changeDetectorRef.detectChanges();
    }
  }

  closeChangeCompetition(): void {
    this.pubsubService.publishSync(this.pubsubService.API.CHANGE_STATE_CHANGE_COMPETITIONS, false);
  }

  // Should be hidden only if tennis
  isTennis(): boolean {
    return this.categoryId === '34';
  }

  /**
   * Go to competition page
   * @params {object} typeItem
   */
  competitionsLink(typeItem: ICompetitionType, className: string): string {
    return this.routingHelperService.formCompetitionUrl({
      sport: this.activatedRoute.snapshot.paramMap.get('sport'),
      typeName: typeItem.type.name,
      className
    });
  }

  private extendTypes(category: ICompetitionCategory, types: ICompetitionType[]): ICompetitionType[] {
    return _.sortBy(_.filter(types, (typeItem: ICompetitionType) => {
      if (typeItem.type) {
        typeItem.name = typeItem.type.name;
        typeItem.link = category.class.originalName ?
          this.competitionsLink(typeItem, category.class.originalName) : '';
        return true;
      } else {
        return false;
      }
    }), (item: ICompetitionType) => item.type.displayOrder);
  }

  /**
   * Updates content ready state when child component data loaded
   */
  private updateLoadingState(): void {
    this.loading = this.categories && this.categories.some((category, i) => this.initiallyExpanded[i] ? category.loading : false);
    if (!this.loading) {
      this.pageLoaded.emit(true);
    }
  }
}
