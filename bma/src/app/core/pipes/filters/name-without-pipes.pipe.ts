import { Pipe, PipeTransform } from '@angular/core';
import { FiltersService } from '../../services/filters/filters.service';

@Pipe({
  name: 'nameWithoutPipes'
})
export class NameWithoutPipesPipe implements PipeTransform {
  constructor(private filtersService: FiltersService) {
  }

  /**
   * Removes pipes from name. E.g. |Event name| => Event name
   *
   * @param name
   * @param args
   */
  transform(name: string): string {
    return this.filtersService.removeLineSymbol(name);
  }
}
