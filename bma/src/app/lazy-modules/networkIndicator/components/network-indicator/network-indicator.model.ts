export class NIConfig {
    networkSpeed: string;
    timeout?: number;
    displayText: string;
    indicatorColor?: string;
    displayIcon?: string;
    infoMsg?: string;
}

export class NIConfigMessage {
    displayText: string;
    networkSpeed: string;
    infoMsg?: string;
}

export class NICMSConfig {
    id: string;
    networkIndicatorEnabled: boolean;
    pollingInterval: number;
    networkSpeed: { slow: NIConfig, online: NIConfig, offline: NIConfig };
    thresholdTime: number;
    slowTimeout: number;
    imageURL: string;
    brand: string;
}