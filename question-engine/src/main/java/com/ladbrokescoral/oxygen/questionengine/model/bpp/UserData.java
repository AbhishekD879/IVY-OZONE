package com.ladbrokescoral.oxygen.questionengine.model.bpp;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class UserData {
    private String oxiApiToken;

    @JsonProperty("sportBookUserName")
    private String username;
}
