export interface IModuleData {
    modules?: IModuleData[];
    id: string,
    brand: string,
    moduleName: string,
    aliasModuleNames: string,
    aliasModules: IAliasModulesTagsData[],
    subModuleEnabled: boolean,
    subModules: []
}
export interface IBonusSuppressionModule {
    brand: string;
    id: string;
    moduleName: string;
    bonusSuppression: boolean;
    riskLevelCode: string;
    reasonCode: string;
    riskLevelDesc?: string;
    reasonDesc?: string;
    modules: IModuleData[];
    enabled?: boolean
}

export interface BonusSupData {
    globalBonusSuppresion: boolean;
    data: IBonusSuppressionModule[];
}

 export interface BonusSupDialogData {
    data: {
        dialogType: string;
        dialogData: IBonusSuppressionModule;
    }
 }

 export interface ModulesDialogData {
    data: {
        dialogType: string;
        dialogData: IModuleData;
    }
 }

export interface IAliasModulesTagsData{
            id : string; 
            title: string; 
            addTag: boolean; 
}

 export interface IAliasModuleNamesData {
    SB: IAliasModulesTagsData[],
    QL: IAliasModulesTagsData[]
 }


 export const SAVE_MODULE_DIALOG = {
    title: 'Add Bonus Suppression Module',
    updateTitle: 'Update Bonus Suppression Module',
    yesOption: 'Save',
    noOption: 'Cancel',
    moduleName: 'Module Name',
    bonusSuppression: 'Enable Bonus Suppression',
    isSubModuleRequired: 'Configure Sub Modules',
    subModuleName: 'Sub-Module Name',
    isSubModuleEnabled: 'Enable Sub Modules',
    add: 'Add',
    update: 'Update',
    add_module: 'Add Module',
    modConfSuccess: 'Module Configured Successfully',
    modConfUpdSuccess: 'Module Configured Successfully',
    subModulesEnabled: 'Sub Modules Enabled'
  };
