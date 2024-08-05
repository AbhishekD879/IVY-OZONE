import {Injectable} from '@angular/core';
import Sortable from 'sortablejs';

interface SortableOptions {
  mainSelector: string;
  handlerSelector: string;
  onReorderEnd: Function;
  dataToReorder: Array<any>;
}

/**
 * could be used as a factory in Component providers
 */
@Injectable()
export class SortableTableService {
  constructor() {}

  addSorting(options: SortableOptions) {
    const self = this;

    Sortable.create(
      document.querySelector(options.mainSelector),
      {
        animation: 150,
        scroll: true,
        handle: options.handlerSelector,
        onEnd(data) {
          const newIndex = data.newIndex;
          const oldIndex = data.oldIndex;

          self.reorderArray((options.dataToReorder || []), oldIndex, newIndex);
          /* tslint:disable */
          // Maksym Shturmin
          options.onReorderEnd && options.onReorderEnd(data, newIndex);
          /* tslint:enable */
        }
      }
    );
  }

  reorderArray(array: Array<any>, oldIndex: number, newIndex: number) {
    while (oldIndex < 0) {
      oldIndex += array.length;
    }
    while (newIndex < 0) {
      newIndex += array.length;
    }
    if (newIndex >= array.length) {
      let k = newIndex - array.length;
      while ((k--) + 1) {
        array.push(undefined);
      }
    }
    array.splice(newIndex, 0, array.splice(oldIndex, 1)[0]);
    return array;
  }
}
