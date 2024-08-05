import { Injectable } from '@angular/core';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { Promotion } from '@app/client/private/models';

@Injectable({
    providedIn: 'root'
})
export class FreeRideValidationServiceService {

    constructor(private dialogService: DialogService) { }

    /**
       * method to convert the text to html
       * @param text will accept the text
       * @returns parsed html
       */
    convertToHTML(text: string) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        return doc.body;
    }

    /**
     * Verifying if the description contains betpack button
     * @param text description text
     * @returns number of betpack classes in the description
     */
    freeRideBtnCount(text: string) {
        const htmlBody = this.convertToHTML(text);
        return htmlBody.querySelectorAll('.btn').length;
    }

    /**
     * Checking the betpack validation
     * @param promo the betpack object in the promotion
     * @returns boolean if all the betpack information is provided or not
     */
    isFreeRideInfoValid(promo: Promotion) {
        return promo.freeRideConfig?.isFreeRidePromo &&
            promo.freeRideConfig.errorMessage &&
            promo.freeRideConfig.ctaPreLoginTitle &&
            promo.freeRideConfig.ctaPostLoginTitle;
    }

    /**
     * isFreeRideDetailsValid to see the freeride classes in the description
     * @param promo accept the promotion with freeride information
     * @returns boolean with appropriate dialogue message
     */
    isFreeRideDetailsValid(promo: Promotion): Boolean {
        let valid = true;
        if (promo?.freeRideConfig?.isFreeRidePromo) {
            const totalBetPackBtn = this.freeRideBtnCount(promo.description);
            if (totalBetPackBtn === 0) {
                if (!promo.freeRideConfig.isFreeRidePromo) {
                    valid = false;
                    this.dialogService.showNotificationDialog({
                        title: 'Error in saving',
                        message: 'Free Ride details are required'
                    });
                } else {
                    if (!this.isFreeRideInfoValid(promo)) {
                        valid = false;
                        this.dialogService.showNotificationDialog({
                            title: 'Error in saving',
                            message: 'Free Ride details are incorrect'
                        });
                    }
                }
            } else if (totalBetPackBtn > 0) {
                valid = false;
                this.dialogService.showNotificationDialog({
                    title: 'Error in saving',
                    message: 'Cannot create button for Free Ride.'
                });
            }
        }
        return valid;
    }

    /**
     * To check the url validation for url format
     * @param url accept the url string
     * @returns boolean if the string satisfies the url regExp
     */
    checkValidUrl(url: string): boolean {
        const strRegex = '^s?https?:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+$';
        const urlRegex = new RegExp(strRegex);
        return urlRegex.test(url);
    }

    /**
     * to check the input if it's number
     * @param val string or number
     * @returns boolean if the param is a number or not
     */
    checkIfInteger(val: string): boolean {
        const strRegex = /^[0-9]*$/;
        const urlRegex = new RegExp(strRegex);
        return urlRegex.test(val);
    }

    /**
     * to check the input if it's a decimal number
     * @param val string
     * @returns boolean if the param is a Decimal number or not
     */
    checkIfDecimal(val: string): boolean {
        const strRegex = /^[0-9]+(\.[0-9]*)?$/;
        const urlRegex = new RegExp(strRegex);
        return urlRegex.test(val);
    }
}
