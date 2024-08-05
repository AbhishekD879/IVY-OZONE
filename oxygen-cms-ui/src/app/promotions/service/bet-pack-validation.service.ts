import { Injectable } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Promotion } from '@app/client/private/models';

@Injectable({ providedIn: 'root' })
export class BetPackValidationService {
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
    betPackBtnCount(text: string) {
        const htmlBody = this.convertToHTML(text);
        return htmlBody.querySelectorAll('.bet-pack-btn').length;
    }

    /**
     * Checking the betpack validation
     * @param promo the betpack object in the promotion
     * @returns boolean if all the betpack information is provided or not
     */
    isBetPackInfoValid(promo: Promotion) {
        return promo.betPack?.isBetPack &&
            promo.betPack.bodyText &&
            promo.betPack.congratsMsg &&
            promo.betPack.offerId &&
            promo.betPack.triggerIds &&
            promo.betPack.betValue &&
            promo.betPack.lowFundMessage &&
            promo.betPack.notLoggedinMessage &&
            promo.betPack.errorMessage;
    }

    /**
     * isBetPackDetailsValid to see the betpack classes in the description
     * @param promo accept the promotion with betpack information
     * @returns boolean with appropriate dialogue message
     */
    isBetPackDetailsValid(promo: Promotion): Boolean {
        let valid = true;
        const totalBetPackBtn = this.betPackBtnCount(promo.description);
        if (totalBetPackBtn === 1) {
            if (!promo.betPack.isBetPack) {
                valid = false;
                this.dialogService.showNotificationDialog({
                    title: 'Error in saving',
                    message: 'Bet pack details are required'
                });
            } else {
                if (!this.isBetPackInfoValid(promo) || !this.checkIfDecimal(promo?.betPack?.betValue)
                    || !this.checkIfInteger(promo?.betPack?.triggerIds) || !this.checkIfInteger(promo?.betPack?.offerId)) {
                    valid = false;
                    this.dialogService.showNotificationDialog({
                        title: 'Error in saving',
                        message: 'Bet pack details are incorrect'
                    });
                }
            }
        } else if (totalBetPackBtn > 1) {
            valid = false;
            this.dialogService.showNotificationDialog({
                title: 'Error in saving',
                message: 'Multiple bet pack buttons in description.'
            });
        } else {
            if (promo?.betPack?.isBetPack) {
                this.dialogService.showNotificationDialog({
                    title: 'Error in saving',
                    message: 'Marked as BetPack Enabler. Please add Bet pack button'
                });
                valid = false;
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

    checkIfDecimalOrNot(val: string): boolean {
        const strRegex = /^-?(0|[1-9]\d*)(\.\d+)?$/;
        const urlRegex = new RegExp(strRegex);
        return urlRegex.test(val);
    }
}
