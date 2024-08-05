import { Injectable } from '@angular/core';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';
import { IEntrySummaryInfo, IOutCome } from '../models/entry-information';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { FIVEASIDE_STATS_CATEGORIES, FIVEASIDE_STATS_CATEGORIES_SINGULAR } from '@app/fiveASideShowDown/constants/enums';

@Injectable({
    providedIn: FiveASideShowDownApiModule
})
export class FiveASideEntryInfoService {

    constructor(public fracToDecService: FracToDecService) { }

    /**
     * entriesCreation sort based on odds
     * @param  {Array<IEntrySummaryInfo>} myEntriesList
     * @returns Array
     */
    public entriesCreation(myEntriesList: Array<IEntrySummaryInfo>): Array<IEntrySummaryInfo> {
            return myEntriesList.map((x: IEntrySummaryInfo) => {
                x.oddsDecimal = this.fracToDecService.getDecimal(Number(x.priceNum), Number(x.priceDen));
                return x;
            }).sort((x, y) => Number(x.oddsDecimal) - Number(y.oddsDecimal)).reverse();
    }

    /**
     * outComesFormation
     * ex: Out ComeProgress like 2 of 3 goals score
     * @param entry
     * @returns Array
     */
    public outComesFormation(entry: Array<IOutCome>): Array<IOutCome> {
            entry = entry.map((x: IOutCome) => {
                return this.outComeProgress(x);
            });
            return entry;
    }
    /**
     * isOpened to enable only one details on the page
     * @param  {number} index
     * @param  {Array<IEntrySummaryInfo>} entries
     * @returns Array
     */
    public isOpened(index: number, entries: Array<IEntrySummaryInfo>): Array<IEntrySummaryInfo> {
            entries.forEach((x, i) => {
                if (index !== i) {
                    entries[i].isOpened = false;
                } else {
                    entries[i].isOpened = !entries[i].isOpened;
                }
            });
            return entries;
    }

    /**
     * Name Format adding *** after lenght 5
     * @param entry
     * @returns string
     */
    private nameFormat(entry: string): string {
       return entry ? `${entry.slice(0, 5)}***` : '';
    }

    /**
     * outComeProgress e.g:2 of 3 goals scored
     * @param OutCome
     * @returns
     */
    private outComeProgress(OutCome: IOutCome): IOutCome {
        OutCome = this.isCleanSheetMarketUpdate(OutCome);
        OutCome.title = this.createSelection(OutCome);
        const target = this.parseStatValue(OutCome.statValue);
        OutCome.statValue = target.toString();
        OutCome.optaStatValue = !OutCome.optaStatValue ? 0 : OutCome.optaStatValue;
        OutCome.progressPct = OutCome.progressPct >= 100 ? 100 : OutCome.progressPct;
        const isSettled = OutCome.progressPct === 100;
        OutCome.isSetteled = isSettled;
        const statsCaterories = this.statsCategorySingularOrNot(isSettled, OutCome, target);
        OutCome.legprogressdetails = isSettled ? ` ${statsCaterories[OutCome.statCategory]}` :
            ` of ${target} ${statsCaterories[OutCome.statCategory]}`;
        return OutCome;
    }

    /**
     * @param  {IOutCome} OutCome
     * @returns IOutCome
     * isCleanSheetMarketUpdate
     */
    private isCleanSheetMarketUpdate(OutCome: IOutCome): IOutCome {
        // DUE TO CHANGES REMOVED FROM BE WE HAVE ADDED
        // WHEN GOAL KEEPER CONCEDED A GOAL progressPct will be -1 then changes the status to 'LOST'
        // ONE MORE HERE THE ACTUAL statValue will be 1 (0 of 1 goalconceded) TO SHOW IN UI like (0 of 0 goalconceded)
        // CHANGING the target to 0
        if (/To Keep A Clean Sheet$/i.test(OutCome.marketName)) {
            OutCome.statValue = '0';
            if (OutCome.progressPct === -1) {
                OutCome.progressPct = 0;
                OutCome.status = 'LOST';
            }
        }
        return OutCome;
    }

    /**
     * Check if stats category are singular or not
     * @param  {boolean} isSettled
     * @param  {IOutCome} Outcome
     * @param  {number} target
     */
    private statsCategorySingularOrNot(isSettled: boolean, Outcome: IOutCome, target: number) {
        if (isSettled) {
            if (Number(Outcome.optaStatValue) === 1) {
                return FIVEASIDE_STATS_CATEGORIES_SINGULAR;
            } else {
                return FIVEASIDE_STATS_CATEGORIES;
            }
        } else {
            if (Number(target) === 1) {
                return FIVEASIDE_STATS_CATEGORIES_SINGULAR;
            } else {
                return FIVEASIDE_STATS_CATEGORIES;
            }
        }
    }

    /**
     * parseStatValue
     * ex:if staValue is >0.5 then return value 1;
     * @param statValue
     * @returns
     */
    private parseStatValue(statValue: string): number {
            const pattern = new RegExp(/[\=\>\<]+/, 'g');
            if (statValue.includes('=') || statValue.includes('<')) {
                return Math.floor(Number(statValue.replace(pattern, '')));
            } else {
                return Math.ceil(Number(statValue.replace(pattern, '')));
            }
    }
    /**
     * progressPercentage
     * @param min
     * @param max
     * @param value
     * @returns
     */
    private progressPercentage(min: number = 0, max: number = 100, value: number = 0): number {
            if (min >= max) {
                return 0;
            }
            if (value < min) {
                return 0;
            }
            if (value > max) {
                return 100;
            }
            return 100 / (max - min) * (value - min);
    }
    /**
     * @param  {IOutCome} part
     * @returns string
     */
    private createSelection(part: IOutCome): string {
        const description = this.capitalize(part.outcomeName);
        const eventMarketDesc = this.capitalize(part.marketName);
        // Anytime Goalscorer
        if (/Anytime Goalscorer$/i.test(eventMarketDesc)) {
            return `${description} Anytime Goalscorer`;
        }
        // To Keep A Clean Sheet (remove yes/no)
        if (/To Keep A Clean Sheet$/i.test(eventMarketDesc)) {
            return description.replace(/ - (Yes|No)/i, '');
        }
        // To Be Shown A Card
        if (eventMarketDesc.includes('To Be Shown A Card')) {
            return this.formCardedTitle(description);
        }
        // To Score 2 Or More Goals
        if (eventMarketDesc.match(/Build Your Bet TO SCORE \d Or More Goals/i)) {
            return this.formGoalsTitle(description, eventMarketDesc);
        }
        // Replace to have -> to make for passes, assists, tackles
        if (/(Passes|Assists|Tackles)/i.test(eventMarketDesc)) {
            return this.formPlayerMakeTitle(description);
        }
        // Other player bets
        if (this.checkForCommonPlayerBetTitle(eventMarketDesc)) {
            return this.formCommonPlayerBetTitle(description);
        }
        // Default title and description
        return description;
    }
    /**
     * @param  {string} description
     * @returns string
     */
    private formCardedTitle(description: string): string {
        return `${description} To Be Carded`;
    }

    /**
     * @param  {string} description
     * @returns string
     */
    private formPlayerMakeTitle(description: string): string {
        return description
            .replace(/ or more/gi, '+')
            .replace(/to have/gi, 'To Make');
    }

    /**
     * @param  {string} description
     * @param  {string} eventMarketDesc
     * @returns string
     */
    private formGoalsTitle(description: string, eventMarketDesc: string): string {
        const title = eventMarketDesc.replace(/Build Your Bet /ig, '');
        return `${description} ${title}`
            .replace(/ or more/gi, '+');
    }

    /**
     * @param  {string} description
     * @returns string
     */
    private formCommonPlayerBetTitle(description: string): string {
        return description
            .replace(/ or more/gi, '+')
            .replace(/to be/gi, 'To Have')
            .replace(/SHOTS WOODWORK/gi, 'Shots Hit The Woodwork')
            .replace(/Offside /gi, 'Offsides ');
    }
    /**
     * @param  {string} eventMarketDesc
     * @returns boolean
     */
    private checkForCommonPlayerBetTitle(eventMarketDesc: string): boolean {
        return eventMarketDesc.includes('Build Your Bet Player') &&
            !eventMarketDesc.includes('To Get First Booking') &&
            !eventMarketDesc.includes('To Outscore The Opposition');
    }
    /**
     * @param  {string} text
     * @returns string
     * example: i/p:RáDéBó AáBó o/p :Rádébó Aábó
     */
    private capitalize(text: string): string {
        return text.toLowerCase().replace(/(^.|\s\S)/g, (e) => {
            return e.toUpperCase();
        });
    }

}
