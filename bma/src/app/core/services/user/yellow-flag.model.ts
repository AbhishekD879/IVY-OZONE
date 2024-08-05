export interface YellowFlagInfo {
  brand: string;
  moduleName: string;
  aliasModuleNames: string;
  bonusSuppression?: boolean;
  subModuleEnabled?: boolean;
  subModules?: YellowFlagInfo[];
  sportsActions?: SportsAction[];
}

export interface RGYConfig {
  brand: string;
  reasonCode: number;
  riskLevelCode: number;
  riskLevelDesc: string;
  reasonDesc: string;
  modules: YellowFlagInfo[];
}

export interface SportsAction {
  action: string;
  externalLink: string;
  enabled: boolean;
}

export const YellowFlagData = [{
  "brand": "bma",
  "moduleName": "Promotions",
  "aliasModuleNames": "Promotions",
  "subModuleEnabled": true,
  "subModules": [
    {
      "brand": "bma",
      "moduleName": "Promotion Sub 1",
      "aliasModuleNames": "Promotion Sub 1",
      "bonusSuppression": false,
    },
    {
      "brand": "bma",
      "moduleName": "Promotion Sub 2",
      "aliasModuleNames": "Promotion Sub 2",
      "bonusSuppression": false,
    }
  ]
},
{
  "brand": "bma",
  "moduleName": "Football Super Series",
  "aliasModuleNames": "Promotion Sub 1",
  "bonusSuppression": true,
},
{
  "brand": "ladbrokes",
  "moduleName": "freeRide",
  "aliasModuleNames": "Promotion Sub 1",
  "bonusSuppression": true,
}]