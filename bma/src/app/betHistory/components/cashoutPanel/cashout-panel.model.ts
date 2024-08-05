export interface ILSUpdate {
    updatePayload: IPayload;
    type: string;
    id: string;
}

export interface IPayload {
    displayed: string;
    is_off: string;
    status: string;
    names: {
        en: string;
    };
    ev_id: string;
}

export interface ICashoutFlags {
    isDisplayed: boolean;
    isActive: boolean;
    rawIsOffCode: string;
    cashoutAvail: string;
    name: string;
}
export interface ICashout {
    isDisplayed: boolean;
    isActive: boolean;
    rawIsOffCode: string;
    cashoutAvail: string;
    isCashoutMessagingEnabled: boolean;
}

export interface ICashoutMarketEvent {
    name: string;
    event_name: string;
    event_id: string;
    type: string;
    cashoutMessagingFlags: ICashout;
}
