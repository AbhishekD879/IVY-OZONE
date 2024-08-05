package com.ladbrokescoral.oxygen.questionengine.dto.crm;

import lombok.Data;

import java.util.HashMap;
import java.util.Map;

@Data
public class ChannelInfo {

    private String type;
    private String sitecoreTemplateId;
    private Map<String, String> customCommunicationMap;
    private HashMap<String, String> additionalInfo;

    public Map<String, String> asCommunicationMap(
            String quizName, String userName,
            String rewardValue, String rewardType) {
        Map<String, String> hashMap = new HashMap<>();
        hashMap.put("#quizname#", quizName);
        hashMap.put("#username#", userName);
        hashMap.put("#reward_value#", rewardValue);
        hashMap.put("#reward_type#", rewardType);
        return hashMap;
    }
}
