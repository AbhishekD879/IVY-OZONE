interface MyBadge {
    label: string;
    rulesDisplay: string;
    lastUpdateFlag: Boolean;
    gamificationActiveMessage: string;
}
export class MyBadges implements MyBadge {
    label: string;
    rulesDisplay: string;
    lastUpdateFlag: Boolean;
    gamificationActiveMessage: string;
}







/* 
********************************** mock Data ***************************************** */

export const mybadgesMock: MyBadges = {
    label: "zzzz",
    rulesDisplay: "cccccccccc",
    lastUpdateFlag: true,
    gamificationActiveMessage: 'test'
}