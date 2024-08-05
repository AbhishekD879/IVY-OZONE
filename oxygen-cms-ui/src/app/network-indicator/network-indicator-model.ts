import { Base } from "../client/private/models/base.model";

export const NETWORK_INDICATOR_DEFAULT_VALUS: INetworkWIndicator = {
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    networkIndicatorEnabled: true,
    debugLogEnabled: false,
    pollingInterval: 0,
    thresholdTime: 0,
    slowTimeout: 0,
    imageURL: '',
    brand: 'ladbrokes',
    networkSpeed: {
        slow: {
        displayText: "",
        infoMsg: ""
        },
        online: {
            displayText: "",
            timeout: 0
        },
        offline: {
            displayText: ''
        }
    }
}

export interface InetworkSpeed {
    slow: {
        displayText: string;
        infoMsg: string;
    },
    online: {
        displayText: string;
        timeout: number;
    },
    offline: {
        displayText: string
    }
}


export interface INetworkWIndicator extends Base{
    networkIndicatorEnabled: boolean;
    pollingInterval: number;
    networkSpeed: InetworkSpeed;
    thresholdTime: number;
    slowTimeout: number;
    imageURL: string;
    brand: string;
    debugLogEnabled: boolean;
}




