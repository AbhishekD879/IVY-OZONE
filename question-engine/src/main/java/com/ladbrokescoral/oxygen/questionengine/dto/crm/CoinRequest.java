package com.ladbrokescoral.oxygen.questionengine.dto.crm;

import lombok.Data;

import java.util.HashMap;
import java.util.List;

@Data
public class CoinRequest {
    private String accountId;
    private String accountName;
    private String requestReferenceId;
    private RewardAttributes rewardDetails;
    private List<ChannelInfo> rewardCommunication;
    private HashMap<String,String> additionalParam;
    private PlayerSourceInfo playerSourceInfo;
    private CampaignSourceDetails campaignSorceDetails;
}
