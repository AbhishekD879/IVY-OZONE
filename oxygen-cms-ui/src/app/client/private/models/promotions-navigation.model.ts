import { Base } from '@app/client/private/models/base.model';

export interface NavigationGroup extends Base {
    brand: string;
    title: string;
    status: boolean;
}

export interface PromotionNavigation extends Base {
    title: string;
    status: boolean;
}

export interface PromotionsNavigationGroup {
    id?: string;
    title?: string;
    status?: boolean;
    updatedAt?: string;
    brand?:string;
    promotionIds?: string[];
    navItems?: PromoNavItemsClass[];
    createdAt?:string;
    createdByUserName?:string;
    updatedByUserName?:string;
    sortOrder?: number;
    leaderboardStatus?: boolean;
}

export interface PromoNavItems extends Base {
    name: string;
    type: string;
    navigationGroupId: string;
}

export class PromoNavItemsClass {
    name: string;
    navType: string;
    navigationGroupId: string;
    id: string;
    brand: string;
    createdBy: string;
    createdAt: string;
    updatedBy: string;
    updatedAt: string;
    updatedByUserName: string;
    createdByUserName: string;
    url?: string;
    leaderboardId?: string;
    leaderboardStatus?: boolean;
    descriptionTxt?: string;
    sortOrder?: number;
}

export class PromotionsNavigationGroupClass implements PromotionsNavigationGroup {
    id: string;
    brand: string;
    updatedAt: string;
    title: string;
    status: boolean;
    promotionIds: string[];
    navItems: PromoNavItemsClass[];
}
export class NavigationParentGroup implements NavigationGroup {
    title: string;
    status: boolean;
    id: string;
    brand: string;
    createdBy: string;
    createdAt: string;
    updatedBy: string;
    updatedAt: string;
    updatedByUserName: string;
    createdByUserName: string;
}
export interface PromotionsNavigationContent {
    id: string;
    title: string;
    status: boolean;
    updatedAt: string;
    navItems: NavTypeContent[];
}

export interface NavTypeContent {
    brand?: string;
    name: string;
    navType?: string;
    url?: string;
    leaderboardId?: string;
    descriptionTxt?: string;
    navigationGroupId?: string;
}

export interface PromoNavContent extends NavTypeContent {
    id: string;
    createdBy: string;
    createdByUserName: string;
    updatedByUserName: string;
    updatedBy: string;
    createdAt: string;
    updatedAt: string;
    sortOrder?: number;
}

export interface LeaderboardGroup {
    id: string;
    name: string;
    brand?: string,
    navGIds?: string,
    status?: boolean,
    updatedAt?: string
}

export interface PromoNavList {
    id: string;
    title: string;
    status: boolean;
    createdByUserName: string;
    updatedByUserName: string;
    createdAt: string;
    updatedAt: string;
    navItems: PromoNavContent[];
    promotionIds: string[];
}
