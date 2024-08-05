import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SortByOptionsComponent } from '@lazy-modules/sortByOptions/components/sort-by-options.component';

@NgModule({
  imports: [CommonModule],
  declarations: [SortByOptionsComponent],
  exports: [SortByOptionsComponent],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SortByOptionsModule {
  static entry = SortByOptionsComponent;
}
