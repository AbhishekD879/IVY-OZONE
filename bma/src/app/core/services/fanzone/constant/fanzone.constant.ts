import { FanzoneDetails } from "@app/core/services/fanzone/models/fanzone.model";

export const FANZONEDETAILS: FanzoneDetails[] = [{ "id": "61a5b39461a27a14501511a6", "createdBy": "5645b8a220bd9e0800afdc57", "createdByUserName": "ozoneqa@ivycomptech.com", "updatedBy": "5645b8a220bd9e0800afdc57", "updatedByUserName": "ozoneqa@ivycomptech.com", "createdAt": "2021-11-30T05:16:04.832Z", "updatedAt": "2021-12-01T13:12:00.971Z", "pageName": "Fanzone", "brand": "ladbrokes", "name": "Everton", "teamId": "123", "openBetID": "223344", "assetManagementLink": "everton", "launchBannerUrl": "{143F3F36-FFDF-43CC-A489-DF85311A7ECD}", "fanzoneBanner": "{143F3F36-FFDF-43CC-A489-DF85311A7ECD}", "ctaBtnText": "Let me see!", "description": "Welcome to Fanzone, a dedicated place where you can find all bets for your club!", "primaryCompetitionId": "442", "secondaryCompetitionId": '434, 436', "clubIds": "23456, 34567", "location": "Goodison Park, Liverpool", "nextGamesLbl": "Everton's Next Games", "outRightsLbl": "Everton Outrights", "premierLeagueLbl": "PREMIER LEAGUE TABLE", "active": true, "fanzoneConfiguration": { "showCompetitionTable": true, "showNowNext": true, "showStats": true, "showClubs": true, "showGames": true, "showSlotRivals": true, "showScratchCards": true, "sportsRibbon": true, "homePage": true, "footballHome": true, "atozMenu": true } }];
export const FANZONE_POS_GET = {
  "preferences": [
    {
      "category": "football",
      "commLastUpdatedAt": "2022-04-01T11:10:42Z",
      "subscriptionDate": "2022-04-01T11:10:42Z",
      "preferenceMap": [
        {
          "key": "TEAM_ID",
          "value": "ehd2iemqmschhj2ec0vayztzz"
        },
        {
          "key": "TEAM_NAME",
          "value": "Everton FC"
        },
        {
          "key": "COMM_PREFERENCES",
          "value": "[\"TEAM_NEWS\",\"PRE_MATCH\"]"
        }
      ]
    }
  ]
}
export const noTeamSelected = {teamId:'FZ001', teamName:'Arsenal FC', subscriptionDate:'', showSYCPopupOn: ''}
export const selectedTeam = {teamId:'123', teamName:'Arsenal FC', subscriptionDate: '', showSYCPopupOn: ''};
export const alreadySelectedTeam = {teamId:'123', teamName:'Arsenal FC', subscriptionDate: '', showSYCPopupOn: '', isFanzoneExists: true, isResignedUser: false}
export const alreadyResignedTeam = {teamId:'123', teamName:'Arsenal FC', subscriptionDate: '', showSYCPopupOn: '', isResignedUser: true}
export const communication = ['test1','test2']
