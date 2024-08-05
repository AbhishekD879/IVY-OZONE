export class IBetpackLivServeResponse {
    freebetOfferId: string;
    freebetOfferName: string;
    startTime: string;
    endTime: string;
    description: string;
    freebetOfferCcyCodes: string;
    freebetTrigger: IfreebetTrigger[];
    freebetToken: IfreebetToken[];
    freebetOfferLimits: IfreebetOfferLimits;
    offerGroup:IofferGroup
}
export class IofferGroup{
    offerGroupId:string;
    offerGroupName:string;
}
export class IfreebetTrigger {
    freebetTriggerId: string;
    freebetTriggerType: string;
    freebetTriggerRank: string;
    freebetTriggerQualification: string;
    freebetTriggerAmount: IfreebetTriggerAmount;
    freebetTriggerBetType: string;
    freebetTriggerMinPriceNum: string;
    freebetTriggerMinPriceDen: string;
    freebetTriggerMinLegPriceNum: string;
    freebetTriggerMinLegPriceDen: string;
    freebetTriggerMinLoseLegs: string;
    freebetTriggerMaxLoseLegs: string;
    freebetTriggerPrecentageBonus: null;
    freebetTriggerBonus: string;
    freebetTriggerMaxBonus: string;
    freebetTriggerCalcMethod: string;
}
export class IfreebetTriggerAmount {
    currency: string;
    value: string
}
export class IfreebetToken {
    freebetTokenId: string;
    freebetTokenDisplayText: string;
    freebetTokenValue: IfreebetTokenValue[];
}
export class IfreebetTokenValue {
    currency: string;
    value: string;
}
export interface IfreebetOfferLimits {
    limitEntry: ILimitEntry[]; /// new Data ty
}
export interface ILimitEntry {
    limitId: number;
    limitSort: string;
    limitRemaining: number;
     limitDefinition: ILimitDefinition;
}
export interface ILimitDefinition {
    limitComponent: ILimitComponent;
}
export interface ILimitComponent {
    limitParam: IlimitParam[];
}
export interface IlimitParam {
    name: string;
    value: number
}
export interface IBetpackLivServe {
    response: IBetpackLivServeResponse
}
