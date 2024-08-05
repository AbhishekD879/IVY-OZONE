import { IARC } from "@app/client/private/models/arcConfig.model"

export const Arc_Mock: IARC = {
    items: [{
        profile: "2.1",
        sportsActions: [
            {
                action: "Home Page",
                messagingContent: "Display of component on first session and if closed then next display is based on frequency. Last action is kept i.e. if minimised then it should remain as in on next session and if the component is closed then it's applied everywhere else in the journey",
                gcLink: "https://qa3.sports.ladbrokes.com/",
                enabled: true
            }
        ],
        frequency: "15",
        enabled: true,
        brand: "coral",
        modelRiskLevel: '2 - Problem Gambler Low',
        reasonCode: '1 - Difference in spend from norm'
    }
    ]
}

export const CONFIGGROUP_MOCK: IARC = {
    items: [
        {
            profile: "2.1",
            sportsActions: [
                {
                    action: "Home Page",
                    messagingContent: "Display of component on first session and if closed then next display is based on frequency. Last action is kept i.e. if minimised then it should remain as in on next session and if the component is closed then it's applied everywhere else in the journey",
                    gcLink: "https://qa3.sports.ladbrokes.com/",
                    enabled: true
                }
            ],
            frequency: "15",
            enabled: true,
            brand: "coral",
            modelRiskLevel: '2 - Problem Gambler Low',
            reasonCode: '1 - Difference in spend from norm'
        },
        {
            profile: "7.6",
            sportsActions: [
                {
                    action: "Display on Homepage",
                    messagingContent: "home",
                    gcLink: "https://qa3.sports.ladbrokes.com/",
                    enabled: true
                },
                {
                    action: "Removal of RPG",
                    messagingContent: "rpg2",
                    gcLink: "https://qa3.sports.ladbrokes.com/",
                    enabled: true
                }
            ],
            frequency: "7",
            enabled: true,
            brand: "bma",
            modelRiskLevel: '7 - At Risk Medium',
            reasonCode: '6 - Multiple payment methods'
        }
    ]
}