import { Injectable } from '@angular/core';
import { ITierInfo } from '@app/client/private/models/euroLoyalty.model';
import { SpecialPagesValidationService } from '@app/special-pages/validators/special-pages.validation.service';

@Injectable({ providedIn: 'root' })
export class EuroLoyaltyValidationService {

    constructor (
        private specialPagesValidationService: SpecialPagesValidationService
    ) {}

    /**
     *  Validate property before adding.
     * @param - {ITierInfo} property
     * @param - {boolean} uniqueFlag
     * @returns - {boolean}
     */
    isValidConfigProperty(property: ITierInfo, uniqueFlag: boolean): boolean {
        return this.isNewPropertyNameValid(property, uniqueFlag) &&
        this.isTierNumberValid(property.tierName) &&
        this.isFreeBetLocationValid(property.freeBetPositionSequence) &&
        this.isOfferIdValid(property);
    }

    /**
     * Validate property name
     * @param - {ITierInfo} property
     * @returns - {boolean}
     */
    isNewPropertyNameValid(property: ITierInfo, uniqueFlag: boolean): boolean {
        return property.tierName
            && uniqueFlag
            && property.offerIdSeq
            && property.offerIdSeq.length > 0
            && property.freeBetPositionSequence
            && property.freeBetPositionSequence.length > 0;
    }

    /**
     * Validate if entered tiernumber is integer or not
     * @param - {string | number} property
     * @returns - {boolean}
     */
    isTierNumberValid(property: string | number): boolean {
        return (property > 0 && this.specialPagesValidationService.checkIfInteger(property)) ? true : false;
    }

    /**
     * Validate if entered freebet location is integer or not
     * @param - {string | number[]} property
     * @returns - {boolean}
     */
    isFreeBetLocationValid(property: string | number[]): boolean {
        return (this.specialPagesValidationService.checkIfInteger(property)) ? true : false;
    }

    /**
     * Validate if entered freebet position sequence is correct
     * @param - {ITierInfo} property
     * @returns - {boolean}
     */
    isOfferIdValid(property: ITierInfo): boolean {
        return (this.specialPagesValidationService.checkIfInteger(property.offerIdSeq)
                && this.checkLocationAndSequenceCount(property)) ? true : false;
    }

    /**
     * Validate if count of freebet position sequence is one greater than count of freebet locations
     * @param - {ITierInfo} property
     * @returns - {boolean}
     */
    checkLocationAndSequenceCount(property: ITierInfo): boolean {
        const locationLen = (Array.isArray(property.freeBetPositionSequence)) ?
        property.freeBetPositionSequence.length :
        property.freeBetPositionSequence.split(',').length;
        const sequenceLen = (Array.isArray(property.offerIdSeq)) ?
        property.offerIdSeq.length :
        property.offerIdSeq.split(',').length;

        return (sequenceLen !== locationLen + 1) ? false : true;
    }
}
