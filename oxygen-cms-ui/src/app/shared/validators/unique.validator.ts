import {AbstractControl, ValidatorFn} from '@angular/forms';

/*
 * Checks if element exists in array of objects (by key => value)
 */
export function uniqueValidator(collection: any[], field: string, ignore?: any): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any } => {
    const index = collection.findIndex(obj => obj[field] === control.value);
    let ignoreElementIndex;

    if (ignore) {
      ignoreElementIndex = collection.findIndex(obj => obj[field] === ignore[field]);
    }

    return (index >= 0 && ignoreElementIndex !== index) ? {'unique': {value: control.value}} : null;
  };
}
