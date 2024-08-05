import {AbstractControl, ValidationErrors, ValidatorFn} from '@angular/forms';

export function splitTagsEntitiesAndCheckLength(charLimit:number): ValidatorFn {
    return (control:AbstractControl) : ValidationErrors | null => {

        const value = control.value;

        if (!value) {
            return null;
        }

        const valid = value.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '').length < charLimit;
        return !valid ? {splitTagsAndCheckLength:true}: null;
    }
}