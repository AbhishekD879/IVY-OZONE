import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'numberNormalizer'
})
export class NumberNormalizerPipe implements PipeTransform {

  transform(value: string | number): string {
    if (typeof value !== 'number') {
      value = parseFloat(value);
    }
    return value.toFixed(2);
  }
}
