package com.egalacoral.spark.timeform.entity;

import com.amazonaws.services.dynamodbv2.datamodeling.*;
import java.io.Serializable;
import org.hibernate.validator.constraints.NotBlank;

@DynamoDBDocument
public class PositionEntity implements Serializable {
  @DynamoDBHashKey @DynamoDBAutoGeneratedKey private String id;
  @NotBlank @DynamoDBAttribute private String meetingDate;
  @NotBlank @DynamoDBAttribute private String positionStatus;

  public String getMeetingDate() {
    return meetingDate;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public String getPositionStatus() {
    return positionStatus;
  }

  public void setPositionStatus(String positionStatus) {
    this.positionStatus = positionStatus;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    PositionEntity that = (PositionEntity) o;

    if (!meetingDate.equals(that.meetingDate)) return false;
    return positionStatus.equals(that.positionStatus);
  }

  @Override
  public int hashCode() {
    int result = meetingDate.hashCode();
    result = 31 * result + positionStatus.hashCode();
    return result;
  }

  public static final class PositionEntityBuilder {
    private String meetingDate;
    private String positionStatus;

    private PositionEntityBuilder() {}

    public static PositionEntityBuilder aPositionEntity() {
      return new PositionEntityBuilder();
    }

    public PositionEntityBuilder meetingDate(String meetingDate) {
      this.meetingDate = meetingDate;
      return this;
    }

    public PositionEntityBuilder positionStatus(String positionStatus) {
      this.positionStatus = positionStatus;
      return this;
    }

    public PositionEntity build() {
      PositionEntity positionEntity = new PositionEntity();
      positionEntity.setMeetingDate(meetingDate);
      positionEntity.setPositionStatus(positionStatus);
      return positionEntity;
    }
  }
}
