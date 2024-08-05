import { IFeaturedModel } from '@app/featured/models/featured.model';
import { IOutputModule } from '@app/featured/models/output-module.model';

export const channelName = 'fanzoneModule';
export const initStateOfFanzone: IFeaturedModel = {
    directiveName: null,
    modules: [],
    showTabOn: null,
    title: null,
    visible: null
};
export const fanzoneCleanModule: IOutputModule= {
    _id: null,
    title: null,
    displayOrder: null,
    showExpanded: null,
    maxRows: null,
    maxSelections: null,
    totalEvents: null,
    publishedDevices: [],
    data: [],
    dataSelection: null,
    footerLink: {
    },
    cashoutAvail: null,
    hasNoLiveEvents: null,
    outcomeColumnsTitles: [],
    errorMessage: null,
    special: null,
    enhanced: null,
    yourCallAvailable: null
  };