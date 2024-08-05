import { Injectable } from '@angular/core';
import { ITierInfo } from '@app/client/private/models/euroLoyalty.model';

@Injectable({ providedIn: 'root' })
export class SpecialPagesValidationService {

    /**
     * Checks if the provided key value is unique
     * @param - {string | number} property
     * @param - {string} key
     * @returns - {boolean}
     */
    isUnique(property: number | string, objectItems: ITierInfo[], key: string, index?: number): boolean {
        const valueArr = objectItems.map(function(item) {
            return Number(item[key]);
        });
        if (index || index === 0) {
            valueArr.splice(index, 1);
        }

        const propertyValue: number = (typeof(property) === 'number') ? property : Number(property);

        return (valueArr.includes(propertyValue)) ? false : true;
    }

    /**
     * Check if integer or not
     * @param - {Array<Number | string> | string} text
     * @returns - {boolean}
     */
    checkIfInteger(text: Array<Number | string> | string | number): boolean {
        if (text) {
            if (typeof(text) === 'number') {
                return Number.isInteger(text);
            } else {
                const numArray = Array.isArray(text) ? text : text.split(',');
                return !numArray.some((num) => !Number.isInteger(Number(num)));
            }
        }
    }
}
