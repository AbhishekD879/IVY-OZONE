import { Price } from "@app/client/private/models/price.model";

export interface SignpostingInfo {
    id: string;
    createdBy: string;
    createdByUserName: string;
    updatedBy: string;
    updatedByUserName: string;
    createdAt: string;
    updatedAt: string;
    sortOrder: number;
    brand: string;
    freeBetType: string;
    fromOffer: string;
    betConditions: string;
    sport: string;
    event: string;
    market: string;
    price: Price;
    signPost: string;
    disabled: boolean;
    isActive: boolean;
    title: string;
}
