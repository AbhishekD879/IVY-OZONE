import { Component, OnChanges, SimpleChanges } from '@angular/core';
import { CompetitionsCategoryComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-categories.component';

@Component({
  selector: 'competitions-category-list',
  templateUrl: './competitions-category-list.component.html'
})
export class CompetitionsCategoryListComponent extends CompetitionsCategoryComponent implements OnChanges {

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes.categories.firstChange) {
      this.isExpanded = [false];
      this.goToTypes(0);
    }
  }
}

