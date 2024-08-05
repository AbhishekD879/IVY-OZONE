import { Injectable } from '@angular/core';
import { IIteratorItem } from './iterator-item.model';
import { Iterator } from './iterator.class';

@Injectable()
export class IteratorService {
  create(items?: IIteratorItem[]) {
    return new Iterator(items);
  }
}
