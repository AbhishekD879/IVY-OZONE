import { Base } from "@root/app/client/private/models/base.model";

interface MyBadge extends Base {
    label: string;
    rulesDisplay: string;
    lastUpdatedFlag: Boolean;
    viewButtonLabel: string;
}

export class MyBadges implements MyBadge {
    lbrRedirectionUrl: string;
    lbrRedirectionLabel: string;
    label: string;
    viewBadges: boolean;
    viewLbrUrl: boolean;
    rulesDisplay: string;
    lastUpdatedFlag: Boolean;
    viewButton: Boolean;
    viewButtonLabel: string;
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    id: string;
    brand: string;
}

export class SeasonData implements Seasons {
    seasonName: string;
    seasonInfo: string;
    displayFrom: string;
    displayTo: string;
    teams: Array<Teams>;
    badgeTypes: Array<Badges>;
    isActive: boolean;
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    id: string;
    brand: string;
    gamificationLinked?:boolean;
    gameLinked?:boolean;
    highlighted: boolean;
}

interface Seasons extends Base {
    seasonName: string;
    seasonInfo: string;
    displayFrom: string;
    displayTo: string;
    teams: Array<Teams>;
    badgeTypes: Array<Badges>;
    isActive: boolean;
}

interface Badges {
    name: string;
    numberOfBadges: number;
    congratsMsg: string;
    prizeType: string;
    amount: number;
}

interface Teams {
    displayName: string;
    assetManagementObjectId?: string;
    svgId: string;
    svg: string;
}

interface GamificationList {
    seasonId: string;
    seasonName: string;
}

export class GamificationListClass implements GamificationList {
    seasonId: string;
    seasonName: string;
}

export class Team implements Teams {
    displayName: string;
    svgId: string;
    svg: string;
    assetManagementObjectId?: string;
}

interface Gamification extends Base {
    seasonId: string;
    seasonName: string;
    teams: Array<Teams>;
    badgeTypes: Array<Badges>;
}

export class GamificationData implements Gamification {
    seasonId: string;
    seasonName: string;
    teams = new Array<Teams>();
    badgeTypes: Array<Badges>;
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    id: string;
    brand: string;
}

interface TabNameConfiguration extends Base {
    currentTabLabel: string;
    previousTabLabel: string;
}

export class TabNameConfigurationData implements TabNameConfiguration {
    currentTabLabel: string;
    previousTabLabel: string;
    createdAt: string;
    createdBy: string;
    createdByUserName: string;
    updatedAt: string;
    updatedBy: string;
    updatedByUserName: string;
    id: string;
    brand: string;
}




/* 
***
******************************* mock Data **************************************
*** 
*/

export const mybadgesMock: MyBadges = {
    "lbrRedirectionUrl": "sample",
    "lbrRedirectionLabel":"sample",
    "id": "61f26fbeb77f212d2de45b8a",
    "viewButtonLabel": "sample",
    "createdBy": "54905d04a49acf605d645271",
    "createdByUserName": "test.admin@coral.co.uk",
    "updatedBy": "54905d04a49acf605d645271",
    "updatedByUserName": "test.admin@coral.co.uk",
    "createdAt": "2022-01-27T10:11:10.469Z",
    "updatedAt": "2022-01-27T10:31:59.086Z",
    "brand": "bma",
    "label": "test me updated",
    "rulesDisplay": "rule info",
    "lastUpdatedFlag": true,
    "viewButton": true,
    "viewLbrUrl": true,
    "viewBadges": true
}

export const seasonMockData: SeasonData[] = [{
    id: 'dkjgqewydgediuye',
    highlighted: false,
    brand: "ladbrokes",
    seasonName: "Season1",
    seasonInfo: "nnnnnnnnnnnnnnnnnnnnnnnnnn",
    displayFrom: "2021-12-27T08:37:11.639Z",
    displayTo: "2021-12-31T08:37:11Z",

    teams: [
        {
            "displayName": "Arsenal1",
            "svgId": "tlt_arr",
            "svg": "<symbol id=\"tlt_arr\" viewBox=\"0 0 34 56\"><defs xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M0 .41h28.456v56.678H0z\" id=\"0f05f8d7__prefix__a\"/></defs><g fill=\"none\" fill-rule=\"evenodd\" transform=\"rotate(-6 5.96 9.419)\" xmlns=\"http://www.w3.org/2000/svg\"><mask fill=\"#fff\" id=\"0f05f8d7__prefix__b\"><use xmlns:xlink=\"http://www.w3.org/1999/xlink\" xlink:href=\"#0f05f8d7__prefix__a\"/></mask><path d=\"M18.216 54.304c-1.131-.615-2.142 1.11-1.01 1.727 3 1.63 7.04.98 10.269.627.88-.097 1.295-1.014.707-1.708-2.501-2.951-4.424-6.27-5.97-9.805-.514-1.177-2.237-.16-1.726 1.009a42.975 42.975 0 003.83 6.94C6.586 44.612-1.63 18.947 3.667.866 3.89.103 1.845.376 1.633 1.1c-5.608 19.14 3.508 46.013 23.11 53.877-2.262.239-4.702.318-6.527-.674\" fill=\"#FEFEFE\" mask=\"url(#0f05f8d7__prefix__b)\"/></g></symbol>"
        }, {
            "displayName": "Arsenal2",
            "svgId": "tlt_arr",
            "svg": ""
        }, {
            "displayName": "sssss",
            "svgId": "tlt_arr",
            "svg": ""
        }
    ],

    badgeTypes: [
        {
            name: "Primary",
            numberOfBadges: 3,
            congratsMsg: 'kkkkk',
            prizeType: 'cc',
            amount: 3
        },
        {
            name: 'Secondary',
            numberOfBadges: 5,
            congratsMsg: 'eeeeeeeeeeee',
            prizeType: 'cc',
            amount: 3
        },

    ],
    isActive: true,
    createdByUserName: 'qa@coral',
    createdBy: 'qa@coral',
    createdAt: '',
    updatedByUserName: '',
    updatedBy: '',
    updatedAt: ''
}]

export const MockTeams = [
    {
        id: '4dsgumo7d4zupm2ugsvm4zm4d', name: 'Arsenal FC'
    },
    { id: 'b496gs285it6bheuikox6z9mj', name: 'Aston Villa' },
    { id: '7yx5dqhhphyvfisohikodajhv', name: 'Brentford FC' },
    { id: 'e5p0ehyguld7egzhiedpdnc3w ', name: 'Brighton & Hove Albion' },
    { id: '64bxxwu2mv2qqlv0monbkj1om ', name: 'Burnley FC' },
    { id: '9q0arba2kbnywth8bkxlhgmdr ', name: 'Chelsea FC' },
    { id: '1c8m2ko0wxq1asfkuykurdr0y ', name: 'Crystal Palace' },
    { id: 'ehd2iemqmschhj2ec0vayztzz ', name: 'Everton FC' },
    { id: '48gk2hpqtsl6p9sx9kjhaydq4 ', name: 'Leeds United' },
    { id: 'avxknfz4f6ob0rv9dbnxdzde0 ', name: 'Leicester City' },
    { id: 'c8h9bw1l82s06h77xxrelzhur ', name: 'Liverpool FC' },
    { id: 'a3nyxabgsqlnqfkeg41m6tnpp', name: 'Manchester City' },
    { id: '6eqit8ye8aomdsrrq0hk3v7gh ', name: 'Manchester United' },
    { id: '7vn2i2kd35zuetw6b38gw9jsz ', name: 'Newcastle United' },
    { id: 'suz80crpy3anixyzccmu6jzp ', name: 'Norwich City' },
    { id: 'd5ydtvt96bv7fq04yqm2w2632', name: 'Southampton FC' },
    { id: '22doj4sgsocqpxw45h607udje ', name: 'Tottenham Hotspur 01' },
    { id: '4t83rqbdbekinxl5fz2ygsyta', name: 'Watford FC' },
    { id: '4txjdaqveermfryvbfrr4taf7', name: 'West Ham United' },
    {
        id: 'b9si1jn1lfxfund69e9ogcu2n', name: 'Wolverhampton Wanderers'
    }
]


export const MockgamificationList = [
    { seasonId: '1233r4rf', seasonName: 'test1' },
    { seasonId: '1233r4rf', seasonName: 'test3' },
    { seasonId: '1233r4rf', seasonName: 'test2' }
]

export const MockTabNameConfigurationList = [
    {
        "previousTabLabel": "Previous",
        "currentTabLabel": "Current"
    }
]
