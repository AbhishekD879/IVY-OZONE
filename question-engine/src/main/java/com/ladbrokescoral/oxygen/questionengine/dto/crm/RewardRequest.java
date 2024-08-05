package com.ladbrokescoral.oxygen.questionengine.dto.crm;

import lombok.Data;

@Data
public class RewardRequest {

    private String accountName;
    private String actionType;
    private String externalRequestRefID;
    private String externalCampaignType;
    private String externalCampaignID;
    private RewardAttributes rewardDetails;
}
