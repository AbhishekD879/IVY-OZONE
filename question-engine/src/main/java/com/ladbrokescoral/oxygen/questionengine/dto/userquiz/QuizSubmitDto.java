package com.ladbrokescoral.oxygen.questionengine.dto.userquiz;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username;
import com.ladbrokescoral.oxygen.questionengine.configuration.LinkedHashMapConverter;
import lombok.Data;
import lombok.experimental.Accessors;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import java.util.List;
import java.util.Map;

@Data
@Accessors(chain = true)
public class QuizSubmitDto {

    @NotEmpty
    private String sourceId;

    @NotEmpty
    @Username
    private String username;

    @NotEmpty
    private String customerId;

    @NotEmpty
    private String quizId;

    @Valid
    @NotEmpty
    @JsonDeserialize(converter = LinkedHashMapConverter.class)
    private Map<@NotEmpty String, @Valid @NotEmpty List<@NotEmpty String>> questionIdToAnswerId;

    private String channel;
}
