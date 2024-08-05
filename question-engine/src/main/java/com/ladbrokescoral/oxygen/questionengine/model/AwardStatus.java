package com.ladbrokescoral.oxygen.questionengine.model;

import com.amazonaws.services.dynamodbv2.datamodeling.*;
import lombok.*;
import lombok.experimental.Accessors;


@Data
@DynamoDBTable(tableName = "question-engine-award-status")
@Accessors(chain = true)
public class AwardStatus {

    @org.springframework.data.annotation.Id
    @Getter(value = AccessLevel.NONE)
    @Setter(value = AccessLevel.NONE)
    private Id id;

    @DynamoDBHashKey
    private final String rewardType;

    @DynamoDBRangeKey
    private final String rewardValue;

    @DynamoDBAttribute
    private final String requestReferenceId;

    @DynamoDBAttribute
    private final String dateSubmitted;

    @DynamoDBAttribute
    private final String accountName;

    @DynamoDBAttribute
    private final String reasonOfFailure;

    @DynamoDBAttribute
    private final String type;

    @Getter
    @ToString
    @RequiredArgsConstructor
    public static class Id {

        @DynamoDBHashKey
        private final String rewardType;

        @DynamoDBRangeKey
        private final String rewardValue;
    }
}
