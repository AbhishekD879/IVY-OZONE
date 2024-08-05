import { Pipe, PipeTransform } from '@angular/core';

/**
 * Transform numeric value from bytes to kilobyte ("kB" not kibibyte "KiB"/"KB"!)
 *  optionally adds "kB" prefix.
 */
@Pipe({name: 'byteToKb'})
export class ByteToKbPipe implements PipeTransform {
  transform(value: number | string, fraction: number = 1, units: string = 'kB'): string {
    let transformedNumber: number = typeof value === 'number' ? value : +value;

    transformedNumber = +(transformedNumber / 1000).toFixed(fraction);

    return `${transformedNumber} ${units}`;
  }
}
